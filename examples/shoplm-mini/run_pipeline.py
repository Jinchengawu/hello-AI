from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from shoplm import CharTokenizer, ModelConfig, TinyDecoder  # noqa: E402
from shoplm.training import evaluate, make_windows, train_model  # noqa: E402


def load_sft(path: Path) -> list[dict[str, str]]:
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        row = json.loads(line)
        if set(row) != {"user", "assistant"} or not all(isinstance(value, str) and value for value in row.values()):
            raise ValueError(f"Invalid SFT row at line {line_number}.")
        rows.append(row)
    return rows


def format_dialogue(row: dict[str, str]) -> str:
    return f"用户：{row['user']}\n客服：{row['assistant']}"


def run(steps: int, output: Path, seed: int = 42) -> dict[str, object]:
    random.seed(seed)
    torch.manual_seed(seed)
    output.mkdir(parents=True, exist_ok=True)

    pretrain_text = (ROOT / "data/pretrain.txt").read_text(encoding="utf-8").strip()
    sft_rows = load_sft(ROOT / "data/sft.jsonl")
    sft_texts = [format_dialogue(row) for row in sft_rows]
    validation_text = "用户：退款审核完成了吗？\n客服：审核状态需要通过授权工具查询。"

    tokenizer = CharTokenizer.train([pretrain_text, *sft_texts, validation_text])
    tokenizer.save(output / "tokenizer.json")
    config = ModelConfig(vocab_size=tokenizer.vocab_size)
    model = TinyDecoder(config)

    pretrain_ids = tokenizer.encode(pretrain_text)
    pretrain_examples = make_windows(pretrain_ids, config.context_length)
    pre_start, pre_end = train_model(model, pretrain_examples, steps=steps, seed=seed)
    model.save(output / "base_model.pt")

    joined_sft = "\n".join(sft_texts)
    sft_examples = make_windows(tokenizer.encode(joined_sft), config.context_length)
    sft_start, sft_end = train_model(model, sft_examples, steps=steps, learning_rate=2e-3, seed=seed)
    model.save(output / "sft_model.pt")

    reloaded = TinyDecoder.load(output / "sft_model.pt")
    validation = evaluate(
        reloaded,
        make_windows(tokenizer.encode(validation_text), config.context_length),
    )
    prompt = "用户：退款为什么还没到账？\n客服："
    prompt_ids = tokenizer.encode(prompt, add_special_tokens=False)
    generated = reloaded.generate(
        torch.tensor([prompt_ids], dtype=torch.long),
        max_new_tokens=40,
        temperature=0.7,
        eos_id=tokenizer.token_to_id["<eos>"],
    )[0].tolist()

    report: dict[str, object] = {
        "seed": seed,
        "vocab_size": tokenizer.vocab_size,
        "model_parameters": sum(parameter.numel() for parameter in model.parameters()),
        "pretrain": {"start_loss": pre_start, "end_loss": pre_end},
        "sft": {"start_loss": sft_start, "end_loss": sft_end},
        "validation": validation,
        "prompt": prompt,
        "generation": tokenizer.decode(generated),
        "disclaimer": "Teaching-scale output; not suitable for production customer service.",
    }
    (output / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the ShopLM Mini teaching pipeline.")
    parser.add_argument("--steps", type=int, default=80, help="Training steps for each stage.")
    parser.add_argument("--output", type=Path, default=Path("artifacts/shoplm-mini"))
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    if args.steps < 1:
        parser.error("--steps must be positive")
    report = run(args.steps, args.output, args.seed)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
