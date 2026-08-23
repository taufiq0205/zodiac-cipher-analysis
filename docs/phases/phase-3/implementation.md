# Phase 3 Implementation

## Scope

- Built a character four-gram scorer from Project Gutenberg's public-domain *Pride and Prejudice* corpus.
- Built a seeded homophonic-substitution generator and simulated-annealing search.
- Kept the final 20% of the corpus out of scorer training.
- Loaded the Z408 reference only after search completed.

## Run

```bash
.venv/bin/python -m unittest discover -s tests
.venv/bin/python -m src.classical
```

## Exit check

Three independently seeded, held-out 300-character samples recovered 92.7%, 95.3%, and 92.7% of characters. The baseline passes the useful-plaintext gate.

Source: https://www.gutenberg.org/ebooks/1342
