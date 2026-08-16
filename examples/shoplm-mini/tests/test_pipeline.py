from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import torch

EXAMPLE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXAMPLE_ROOT))

from shoplm import CharTokenizer, ModelConfig, TinyDecoder  # noqa: E402
from shoplm.training import make_windows, train_model  # noqa: E402


class TokenizerTests(unittest.TestCase):
    def test_round_trip_and_unknown_token(self) -> None:
        tokenizer = CharTokenizer.train(["退款到账"])
        encoded = tokenizer.encode("退款到账")
        self.assertEqual(tokenizer.decode(encoded), "退款到账")
        self.assertEqual(
            tokenizer.encode("新", add_special_tokens=False),
            [tokenizer.token_to_id["<unk>"]],
        )


class ModelTests(unittest.TestCase):
    def setUp(self) -> None:
        torch.manual_seed(7)
        self.tokenizer = CharTokenizer.train(["退款到账。退款到账。"])
        self.config = ModelConfig(
            vocab_size=self.tokenizer.vocab_size,
            context_length=12,
            embedding_dim=16,
            num_heads=2,
        )

    def test_forward_shape_and_checkpoint_round_trip(self) -> None:
        model = TinyDecoder(self.config)
        inputs = torch.tensor([[1, 4, 5]], dtype=torch.long)
        logits, _ = model(inputs)
        self.assertEqual(tuple(logits.shape), (1, 3, self.config.vocab_size))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "model.pt"
            model.save(path)
            loaded = TinyDecoder.load(path)
            loaded_logits, _ = loaded(inputs)
        self.assertTrue(torch.equal(logits, loaded_logits))

    def test_training_reduces_loss_and_generation_runs(self) -> None:
        model = TinyDecoder(self.config)
        ids = self.tokenizer.encode("退款到账。退款到账。退款到账。")
        examples = make_windows(ids, self.config.context_length)
        start, end = train_model(model, examples, steps=25, learning_rate=1e-2, seed=7)
        self.assertLess(end, start)
        generated = model.generate(
            torch.tensor([[self.tokenizer.token_to_id["<bos>"]]], dtype=torch.long),
            max_new_tokens=4,
            eos_id=self.tokenizer.token_to_id["<eos>"],
        )
        self.assertGreater(generated.size(1), 1)


if __name__ == "__main__":
    unittest.main()
