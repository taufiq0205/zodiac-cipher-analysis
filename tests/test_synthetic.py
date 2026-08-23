from pathlib import Path
import unittest

from src.synthetic import FAMILIES, SPLIT_COUNTS, build_dataset


class SyntheticDatasetTest(unittest.TestCase):
    def test_reproducible_without_split_leakage(self):
        corpus = Path("data/corpus-english.txt").read_text()
        first = build_dataset(corpus)
        self.assertEqual(first, build_dataset(corpus))
        records = first["records"]
        self.assertEqual(len(records), sum(SPLIT_COUNTS.values()))
        self.assertEqual({record["family"] for record in records}, set(FAMILIES))
        sources = {
            split: {record["source_passage_id"] for record in records if record["split"] == split}
            for split in SPLIT_COUNTS
        }
        self.assertTrue(sources["train"].isdisjoint(sources["validation"] | sources["test"]))
        self.assertTrue(sources["validation"].isdisjoint(sources["test"]))
        self.assertTrue(any(record["copy_error_positions"] for record in records))
