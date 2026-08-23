"""Generate the deterministic Phase 4 synthetic cipher dataset."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import random

from src.classical import ALPHABET, corpus_body, encrypt_homophonic

SEED = 20260824
SPLIT_COUNTS = {"train": 60, "validation": 15, "test": 15}
FAMILIES = ("homophonic", "transposition", "both")
ERROR_RATES = (0.0, 0.01, 0.03)


def transpose(values: list[int], width: int = 17) -> list[int]:
    return [values[index] for column in range(width) for index in range(column, len(values), width)]


def add_copy_errors(values: list[int], rate: float, rng: random.Random) -> tuple[list[int], list[int]]:
    changed = values.copy()
    candidates = [index for index in range(1, len(values)) if values[index] != values[index - 1]]
    positions = sorted(rng.sample(candidates, min(round(len(values) * rate), len(candidates))))
    for index in positions:
        changed[index] = changed[index - 1]
    return changed, positions


def build_dataset(corpus: str, seed: int = SEED, passage_length: int = 300) -> dict:
    rng = random.Random(seed)
    cleaned = corpus_body(corpus)
    total = sum(SPLIT_COUNTS.values())
    passages = [cleaned[index * passage_length : (index + 1) * passage_length] for index in range(total)]
    if len(passages) < total or any(len(passage) != passage_length for passage in passages):
        raise ValueError(f"corpus must contain at least {total * passage_length} letters")

    source_ids = list(range(total))
    rng.shuffle(source_ids)
    records = []
    offset = 0
    for split, count in SPLIT_COUNTS.items():
        for source_id in source_ids[offset : offset + count]:
            family = FAMILIES[len(records) % len(FAMILIES)]
            plaintext = passages[source_id]
            if family == "transposition":
                ciphertext = transpose([ALPHABET.index(letter) for letter in plaintext])
            else:
                ciphertext, _ = encrypt_homophonic(plaintext, 45, rng)
                if family == "both":
                    ciphertext = transpose(ciphertext)
            error_rate = ERROR_RATES[(len(records) // len(FAMILIES)) % len(ERROR_RATES)]
            ciphertext, error_positions = add_copy_errors(ciphertext, error_rate, rng)
            records.append({
                "id": f"{split}-{source_id:03d}",
                "source_passage_id": source_id,
                "split": split,
                "family": family,
                "plaintext": plaintext,
                "ciphertext": ciphertext,
                "copy_error_rate": error_rate,
                "copy_error_positions": error_positions,
            })
        offset += count
    return {"seed": seed, "passage_length": passage_length, "records": records}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, default=Path("data/corpus-english.txt"))
    parser.add_argument("--output", type=Path, default=Path("data/synthetic/dataset.json"))
    args = parser.parse_args()
    dataset = build_dataset(args.corpus.read_text())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(dataset, separators=(",", ":")) + "\n")
    print(f"wrote {len(dataset['records'])} records to {args.output}")


if __name__ == "__main__":
    main()
