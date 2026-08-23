import json
from pathlib import Path
import unittest

from src.classical import load_cipher
from src.ml import evaluate, rank_families, train_classifier


class MLFamilyClassifierTest(unittest.TestCase):
    def test_beats_phase_3_homophonic_assumption_without_plaintext(self):
        records = json.loads(Path("data/synthetic/dataset.json").read_text())["records"]
        ciphertext_only = [
            {key: record[key] for key in ("split", "family", "ciphertext")}
            for record in records
        ]
        results = evaluate(ciphertext_only)
        for split in ("validation", "test"):
            self.assertGreater(results[split]["ml_accuracy"], results[split]["phase_3_assumption_accuracy"])

    def test_ranks_known_cipher_families(self):
        records = json.loads(Path("data/synthetic/dataset.json").read_text())["records"]
        model = train_classifier(records)
        self.assertEqual(rank_families(model, load_cipher(Path("data/raw/z408.json")))[0]["family"], "homophonic")
        self.assertEqual(rank_families(model, load_cipher(Path("data/raw/z340.json")))[0]["family"], "both")
