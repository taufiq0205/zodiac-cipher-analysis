"""Run the frozen Phase 6 validation and write reproducible evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import random
import time

from src.classical import NGramScorer, accuracy, corpus_body, load_cipher, search
from src.ml import FEATURE_NAMES, rank_families, structural_features, train_classifier
from src.synthetic import add_copy_errors

KNOWN_FAMILIES = {"z408": "homophonic", "z340": "both"}
ERROR_RATES = (0.0, 0.01, 0.03)


def feature_ranges(records: list[dict]) -> list[tuple[float, float]]:
    rows = [structural_features(record["ciphertext"]) for record in records if record["split"] == "train"]
    return [(min(column), max(column)) for column in zip(*rows)]


def assess(model, ciphertext: list[int], ranges: list[tuple[float, float]]) -> dict:
    features = structural_features(ciphertext)
    return {
        "family_ranking": rank_families(model, ciphertext),
        "features_outside_training_range": [
            name for name, value, (low, high) in zip(FEATURE_NAMES, features, ranges) if not low <= value <= high
        ],
    }


def sensitivity(model, ciphertext: list[int], ranges: list[tuple[float, float]], seed: int) -> list[dict]:
    rows = []
    for index, rate in enumerate(ERROR_RATES):
        changed, positions = add_copy_errors(ciphertext, rate, random.Random(seed + index))
        result = assess(model, changed, ranges)
        rows.append({"copy_error_rate": rate, "changed_symbols": len(positions), **result})
    return rows


def run(*, steps: int, restarts: int) -> dict:
    records = json.loads(Path("data/synthetic/dataset.json").read_text())["records"]
    model = train_classifier(records)
    ranges = feature_ranges(records)
    known = {}
    for index, (name, expected_family) in enumerate(KNOWN_FAMILIES.items()):
        ciphertext = load_cipher(Path(f"data/raw/{name}.json"))
        known[name.upper()] = {
            "expected_family": expected_family,
            **assess(model, ciphertext, ranges),
            "error_sensitivity": sensitivity(model, ciphertext, ranges, 600 + index * 10),
        }

    z408 = load_cipher(Path("data/raw/z408.json"))
    corpus = corpus_body(Path("data/corpus-english.txt").read_text())
    scorer = NGramScorer(corpus[: int(len(corpus) * 0.8)])
    reference = Path("data/reference/z408-plaintext.txt").read_text()
    decoder_results = []
    for index, rate in enumerate(ERROR_RATES):
        changed, positions = add_copy_errors(z408, rate, random.Random(700 + index))
        started = time.perf_counter()
        candidates = search(changed, scorer, seed=8, restarts=restarts, steps=steps)
        decoder_results.append({
            "copy_error_rate": rate,
            "changed_symbols": len(positions),
            "character_accuracy": accuracy(candidates[0][1], reference),
            "ngram_score": candidates[0][0],
            "runtime_seconds": time.perf_counter() - started,
            "candidate_preview": candidates[0][1][:100],
        })
    known["Z408"]["classical_decoder"] = decoder_results

    validation_passed = all(row["family_ranking"][0]["family"] == row["expected_family"] for row in known.values())
    unsolved = {}
    if validation_passed:
        for index, name in enumerate(("z13", "z32")):
            ciphertext = load_cipher(Path(f"data/raw/{name}.json"))
            unsolved[name.upper()] = {
                **assess(model, ciphertext, ranges),
                "error_sensitivity": sensitivity(model, ciphertext, ranges, 800 + index * 10),
                "interpretation": "exploratory_only",
                "plaintext_candidates": [],
                "reason": "The frozen pipeline has no combined-cipher decoder, and this input is outside its training range.",
            }

    return {
        "configuration": {"random_seeds_fixed": True, "steps": steps, "restarts": restarts},
        "training_feature_ranges": dict(zip(FEATURE_NAMES, ranges)),
        "known_ciphers": known,
        "known_family_validation_passed": validation_passed,
        "unsolved_ciphers": unsolved,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=30_000)
    parser.add_argument("--restarts", type=int, default=8)
    parser.add_argument("--output", type=Path, default=Path("data/results/phase-6.json"))
    args = parser.parse_args()
    results = run(steps=args.steps, restarts=args.restarts)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, indent=2) + "\n")
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
