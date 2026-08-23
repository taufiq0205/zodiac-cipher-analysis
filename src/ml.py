"""Phase 5 cipher-family classifier using ciphertext-only features."""

from __future__ import annotations

from collections import Counter
import json
import math
from pathlib import Path

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

FAMILIES = ("homophonic", "transposition", "both")
FEATURE_NAMES = (
    "alphabet_size",
    "entropy",
    "index_of_coincidence",
    "repeated_bigrams",
    "repeated_trigrams",
    "adjacent_match_rate",
    "lag_17_match_rate",
)


def structural_features(ciphertext: list[int]) -> list[float]:
    """Return statistics that do not use the plaintext or family label."""
    size = len(ciphertext)
    if size < 2:
        raise ValueError("ciphertext must contain at least two symbols")
    counts = Counter(ciphertext)
    bigrams = Counter(zip(ciphertext, ciphertext[1:]))
    trigrams = Counter(zip(ciphertext, ciphertext[1:], ciphertext[2:]))
    return [
        len(counts),
        -sum((count / size) * math.log2(count / size) for count in counts.values()),
        sum(count * (count - 1) for count in counts.values()) / (size * (size - 1)),
        sum(count > 1 for count in bigrams.values()),
        sum(count > 1 for count in trigrams.values()),
        sum(left == right for left, right in zip(ciphertext, ciphertext[1:])) / (size - 1),
        sum(left == right for left, right in zip(ciphertext, ciphertext[17:])) / (size - 17) if size > 17 else 0.0,
    ]


def train_classifier(records: list[dict]):
    train = [record for record in records if record["split"] == "train"]
    model = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=1_000, random_state=20260824),
    )
    model.fit([structural_features(record["ciphertext"]) for record in train], [record["family"] for record in train])
    return model


def rank_families(model, ciphertext: list[int]) -> list[dict]:
    probabilities = model.predict_proba([structural_features(ciphertext)])[0]
    return sorted(
        ({"family": family, "probability": float(probability)} for family, probability in zip(model.classes_, probabilities)),
        key=lambda row: row["probability"],
        reverse=True,
    )


def evaluate(records: list[dict]) -> dict:
    model = train_classifier(records)

    results = {}
    for split in ("validation", "test"):
        rows = [record for record in records if record["split"] == split]
        expected = [record["family"] for record in rows]
        predicted = model.predict([structural_features(record["ciphertext"]) for record in rows])
        results[split] = {
            "records": len(rows),
            "phase_3_assumption_accuracy": accuracy_score(expected, ["homophonic"] * len(rows)),
            "ml_accuracy": accuracy_score(expected, predicted),
            "confusion_matrix": confusion_matrix(expected, predicted, labels=FAMILIES).tolist(),
        }
    return results


def main() -> None:
    records = json.loads(Path("data/synthetic/dataset.json").read_text())["records"]
    print(json.dumps(evaluate(records), indent=2))


if __name__ == "__main__":
    main()
