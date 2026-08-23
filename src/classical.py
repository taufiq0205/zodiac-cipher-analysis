"""Minimal homophonic-substitution baseline for Phase 3."""

from __future__ import annotations

import argparse
from collections import Counter
import json
import math
from pathlib import Path
import random
import string
import time

ALPHABET = string.ascii_uppercase
ENGLISH_FREQUENCY = "ETAOINSHRDLCUMWFGYPBVKJXQZ"


def letters(text: str) -> str:
    return "".join(character for character in text.upper() if character in ALPHABET)


def corpus_body(text: str) -> str:
    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK")
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK")
    return letters(text[text.find("\n", start) + 1 : end]) if start >= 0 and end > start else letters(text)


class NGramScorer:
    def __init__(self, corpus: str, n: int = 4) -> None:
        self.n = n
        cleaned = letters(corpus)
        self.counts = Counter(cleaned[index : index + n] for index in range(len(cleaned) - n + 1))
        total = sum(self.counts.values())
        self.floor = math.log10(0.1 / total)
        self.logs = {gram: math.log10(count / total) for gram, count in self.counts.items()}

    def score(self, text: str) -> float:
        cleaned = letters(text)
        return sum(self.logs.get(cleaned[index : index + self.n], self.floor) for index in range(len(cleaned) - self.n + 1))


def symbol_slots(size: int) -> list[str]:
    weights = dict(zip(ENGLISH_FREQUENCY, range(26, 0, -1)))
    slots = list(ALPHABET)
    while len(slots) < size:
        slots.append(max(ALPHABET, key=lambda letter: weights[letter] / slots.count(letter)))
    return slots[:size]


def encrypt_homophonic(plaintext: str, symbol_count: int, rng: random.Random) -> tuple[list[int], dict[int, str]]:
    slots = symbol_slots(symbol_count)
    rng.shuffle(slots)
    choices = {letter: [symbol for symbol, value in enumerate(slots) if value == letter] for letter in ALPHABET}
    cleaned = letters(plaintext)
    return [rng.choice(choices[letter]) for letter in cleaned], dict(enumerate(slots))


def decrypt(ciphertext: list[int], key: list[str]) -> str:
    return "".join(key[symbol] for symbol in ciphertext)


def search(
    ciphertext: list[int], scorer: NGramScorer, *, seed: int = 0, restarts: int = 8, steps: int = 30_000
) -> list[tuple[float, str]]:
    rng = random.Random(seed)
    slots = symbol_slots(max(ciphertext) + 1)
    candidates: list[tuple[float, str]] = []
    for _ in range(restarts):
        rng.shuffle(slots)
        key = slots.copy()
        plaintext = decrypt(ciphertext, key)
        score = scorer.score(plaintext)
        best = (score, plaintext)
        for step in range(steps):
            left, right = rng.sample(range(len(key)), 2)
            key[left], key[right] = key[right], key[left]
            proposal = decrypt(ciphertext, key)
            proposal_score = scorer.score(proposal)
            temperature = max(0.2, 20 * (1 - step / steps))
            if proposal_score > score or rng.random() < math.exp((proposal_score - score) / temperature):
                score = proposal_score
                if score > best[0]:
                    best = (score, proposal)
            else:
                key[left], key[right] = key[right], key[left]
        candidates.append(best)
    return sorted(candidates, reverse=True)


def load_cipher(path: Path) -> list[int]:
    rows = json.loads(path.read_text())["rows"]
    symbols = [symbol for row in rows for symbol in row]
    ids = {symbol: index for index, symbol in enumerate(sorted(set(symbols)))}
    return [ids[symbol] for symbol in symbols]


def accuracy(candidate: str, expected: str) -> float:
    expected = letters(expected)
    return sum(left == right for left, right in zip(candidate, expected)) / len(expected)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, default=Path("data/corpus-english.txt"))
    parser.add_argument("--steps", type=int, default=30_000)
    parser.add_argument("--restarts", type=int, default=8)
    args = parser.parse_args()
    corpus = corpus_body(args.corpus.read_text())
    split = int(len(corpus) * 0.8)
    training, held_out = corpus[:split], corpus[-500:]
    scorer = NGramScorer(training)
    rng = random.Random(7)
    synthetic, _ = encrypt_homophonic(held_out, 45, rng)
    started = time.perf_counter()
    synthetic_candidates = search(synthetic, scorer, seed=17, restarts=args.restarts, steps=args.steps)
    synthetic_runtime = time.perf_counter() - started

    z408 = load_cipher(Path("data/raw/z408.json"))
    started = time.perf_counter()
    z408_candidates = search(z408, scorer, seed=8, restarts=args.restarts, steps=args.steps)
    z408_runtime = time.perf_counter() - started
    # The reference is loaded only after search; it cannot influence candidate generation.
    z408_plaintext = Path("data/reference/z408-plaintext.txt").read_text()

    print(json.dumps({
        "synthetic": {
            "character_accuracy": accuracy(synthetic_candidates[0][1], held_out),
            "ngram_score": synthetic_candidates[0][0],
            "correct_candidate_rank": 1 + sum(score > scorer.score(held_out) for score, _ in synthetic_candidates),
            "runtime_seconds": synthetic_runtime,
            "candidate": synthetic_candidates[0][1],
        },
        "z408": {
            "character_accuracy": accuracy(z408_candidates[0][1], z408_plaintext),
            "ngram_score": z408_candidates[0][0],
            "correct_candidate_rank": 1 + sum(score > scorer.score(z408_plaintext) for score, _ in z408_candidates),
            "runtime_seconds": z408_runtime,
            "candidate": z408_candidates[0][1],
        },
    }, indent=2))


if __name__ == "__main__":
    main()
