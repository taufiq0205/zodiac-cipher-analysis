# Phase 5 Implementation

## Scope

- Trained a logistic-regression classifier on the 60 Phase 4 training records.
- Used seven ciphertext-only structural features: alphabet size, entropy, index of coincidence, repeated bigrams, repeated trigrams, adjacent matches, and lag-17 matches.
- Used the 15 validation records for the decision gate, then evaluated once on the untouched 15-record test split.
- Compared it with Phase 3's fixed assumption that every input is homophonic.

## Run

```bash
.venv/bin/python -m src.ml
.venv/bin/python -m unittest discover -s tests -v
```

## Exit check

The model improved family-classification accuracy from 33.3% to 100% on both validation and test data. It remains a family router; it does not decrypt ciphertext.
