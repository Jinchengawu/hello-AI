from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

import torch
from torch import nn
from torch.nn import functional as F


@dataclass(frozen=True)
class ModelConfig:
    vocab_size: int
    context_length: int = 48
    embedding_dim: int = 48
    num_heads: int = 4
    num_layers: int = 1
    dropout: float = 0.0


class DecoderBlock(nn.Module):
    def __init__(self, config: ModelConfig) -> None:
        super().__init__()
        self.norm1 = nn.LayerNorm(config.embedding_dim)
        self.attention = nn.MultiheadAttention(
            config.embedding_dim,
            config.num_heads,
            dropout=config.dropout,
            batch_first=True,
        )
        self.norm2 = nn.LayerNorm(config.embedding_dim)
        self.feed_forward = nn.Sequential(
            nn.Linear(config.embedding_dim, 4 * config.embedding_dim),
            nn.GELU(),
            nn.Linear(4 * config.embedding_dim, config.embedding_dim),
            nn.Dropout(config.dropout),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        length = x.size(1)
        causal_mask = torch.triu(
            torch.ones(length, length, device=x.device, dtype=torch.bool), diagonal=1
        )
        normalized = self.norm1(x)
        attended, _ = self.attention(
            normalized,
            normalized,
            normalized,
            attn_mask=causal_mask,
            need_weights=False,
        )
        x = x + attended
        return x + self.feed_forward(self.norm2(x))


class TinyDecoder(nn.Module):
    """A minimal Decoder-only Transformer for CPU teaching experiments."""

    def __init__(self, config: ModelConfig) -> None:
        super().__init__()
        self.config = config
        self.token_embedding = nn.Embedding(config.vocab_size, config.embedding_dim)
        self.position_embedding = nn.Embedding(config.context_length, config.embedding_dim)
        self.blocks = nn.ModuleList(DecoderBlock(config) for _ in range(config.num_layers))
        self.final_norm = nn.LayerNorm(config.embedding_dim)
        self.lm_head = nn.Linear(config.embedding_dim, config.vocab_size, bias=False)
        self.lm_head.weight = self.token_embedding.weight

    def forward(
        self, token_ids: torch.Tensor, targets: torch.Tensor | None = None
    ) -> tuple[torch.Tensor, torch.Tensor | None]:
        if token_ids.size(1) > self.config.context_length:
            raise ValueError("Input is longer than the configured context length.")
        positions = torch.arange(token_ids.size(1), device=token_ids.device)
        x = self.token_embedding(token_ids) + self.position_embedding(positions)
        for block in self.blocks:
            x = block(x)
        logits = self.lm_head(self.final_norm(x))
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), targets.reshape(-1))
        return logits, loss

    @torch.no_grad()
    def generate(
        self,
        token_ids: torch.Tensor,
        max_new_tokens: int,
        *,
        temperature: float = 0.8,
        eos_id: int | None = None,
    ) -> torch.Tensor:
        self.eval()
        for _ in range(max_new_tokens):
            context = token_ids[:, -self.config.context_length :]
            logits, _ = self(context)
            next_logits = logits[:, -1, :] / max(temperature, 1e-6)
            next_id = torch.multinomial(F.softmax(next_logits, dim=-1), num_samples=1)
            token_ids = torch.cat((token_ids, next_id), dim=1)
            if eos_id is not None and bool(torch.all(next_id == eos_id)):
                break
        return token_ids

    def save(self, path: Path) -> None:
        torch.save({"config": asdict(self.config), "state_dict": self.state_dict()}, path)

    @classmethod
    def load(cls, path: Path) -> "TinyDecoder":
        payload = torch.load(path, map_location="cpu", weights_only=True)
        model = cls(ModelConfig(**payload["config"]))
        model.load_state_dict(payload["state_dict"])
        return model
