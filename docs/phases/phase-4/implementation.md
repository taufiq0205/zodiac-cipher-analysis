# Phase 4 Implementation

## Scope

- Sampled 90 non-overlapping, 300-letter passages from the English corpus.
- Generated 30 homophonic, 30 transposition, and 30 combined ciphers.
- Applied controlled symbol-copy error rates of 0%, 1%, and 3%.
- Assigned each source passage once across 60 training, 15 validation, and 15 test records.

## Run

```bash
.venv/bin/python -m src.synthetic
.venv/bin/python -m unittest discover -s tests -v
```

The fixed seed is `20260824`; output is `data/synthetic/dataset.json`.

## Exit check

Repeated generation produced identical data, and all 90 source passage IDs were unique across splits. Phase 4 passed.
