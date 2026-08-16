from __future__ import annotations

import math
import random

import torch

from .model import TinyDecoder


def make_windows(token_ids: list[int], context_length: int) -> list[tuple[list[int], list[int]]]:
    if len(token_ids) < 3:
        raise ValueError("Training text is too short.")
    window = min(context_length, len(token_ids) - 1)
    stride = max(1, window // 2)
    examples = []
    for start in range(0, len(token_ids) - 1, stride):
        chunk = token_ids[start : start + window + 1]
        if len(chunk) >= 3:
            examples.append((chunk[:-1], chunk[1:]))
    return examples


def train_model(
    model: TinyDecoder,
    examples: list[tuple[list[int], list[int]]],
    *,
    steps: int,
    learning_rate: float = 3e-3,
    seed: int = 42,
) -> tuple[float, float]:
    random.seed(seed)
    torch.manual_seed(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
    model.train()
    losses: list[float] = []
    for step in range(steps):
        inputs, targets = examples[step % len(examples)]
        input_tensor = torch.tensor([inputs], dtype=torch.long)
        target_tensor = torch.tensor([targets], dtype=torch.long)
        optimizer.zero_grad(set_to_none=True)
        _, loss = model(input_tensor, target_tensor)
        assert loss is not None
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        losses.append(float(loss.detach()))
    edge = max(1, min(5, len(losses) // 2))
    return sum(losses[:edge]) / edge, sum(losses[-edge:]) / edge


@torch.no_grad()
def evaluate(model: TinyDecoder, examples: list[tuple[list[int], list[int]]]) -> dict[str, float]:
    model.eval()
    losses = []
    for inputs, targets in examples:
        _, loss = model(
            torch.tensor([inputs], dtype=torch.long),
            torch.tensor([targets], dtype=torch.long),
        )
        assert loss is not None
        losses.append(float(loss))
    mean_loss = sum(losses) / len(losses)
    return {"loss": mean_loss, "perplexity": math.exp(min(mean_loss, 20.0))}
