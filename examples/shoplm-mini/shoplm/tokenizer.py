from __future__ import annotations

import json
from pathlib import Path


class CharTokenizer:
    """A deliberately small character tokenizer for the teaching pipeline."""

    SPECIAL_TOKENS = ("<pad>", "<bos>", "<eos>", "<unk>")

    def __init__(self, tokens: list[str]) -> None:
        ordered = list(dict.fromkeys([*self.SPECIAL_TOKENS, *tokens]))
        self.token_to_id = {token: index for index, token in enumerate(ordered)}
        self.id_to_token = ordered

    @classmethod
    def train(cls, texts: list[str]) -> "CharTokenizer":
        if not texts or not any(texts):
            raise ValueError("Tokenizer training requires non-empty text.")
        return cls(sorted(set("".join(texts))))

    @property
    def vocab_size(self) -> int:
        return len(self.id_to_token)

    def encode(self, text: str, *, add_special_tokens: bool = True) -> list[int]:
        ids = [self.token_to_id.get(char, self.token_to_id["<unk>"]) for char in text]
        if add_special_tokens:
            ids = [self.token_to_id["<bos>"], *ids, self.token_to_id["<eos>"]]
        return ids

    def decode(self, ids: list[int], *, skip_special_tokens: bool = True) -> str:
        tokens: list[str] = []
        for index in ids:
            token = self.id_to_token[index]
            if skip_special_tokens and token in self.SPECIAL_TOKENS:
                continue
            tokens.append(token)
        return "".join(tokens)

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(self.id_to_token, ensure_ascii=False, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> "CharTokenizer":
        return cls(json.loads(path.read_text(encoding="utf-8")))
