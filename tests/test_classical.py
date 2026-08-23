import random
from pathlib import Path
import unittest

from src.classical import NGramScorer, accuracy, corpus_body, encrypt_homophonic, search


class ClassicalBaselineTest(unittest.TestCase):
    def test_recovers_useful_plaintext_from_held_out_samples(self):
        corpus = corpus_body(Path("data/corpus-english.txt").read_text())
        scorer = NGramScorer(corpus[: int(len(corpus) * 0.8)])
        for index, plaintext in enumerate((corpus[-900:-600], corpus[-600:-300], corpus[-300:])):
            ciphertext, _ = encrypt_homophonic(plaintext, 40, random.Random(index))
            candidate = search(ciphertext, scorer, seed=100 + index, restarts=4, steps=10_000)[0][1]
            self.assertGreaterEqual(accuracy(candidate, plaintext), 0.5)
