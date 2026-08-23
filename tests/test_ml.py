import json
from pathlib import Path
import unittest

from src.ml import evaluate


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
