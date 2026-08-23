# Phase 6 Implementation

## Scope

- Ran the frozen family classifier against Z408 and Z340 before assessing Z13 and Z32.
- Added deterministic 1% and 3% symbol-copy error checks.
- Ran the classical homophonic decoder against Z408 at the frozen search settings.
- Recorded ranked family hypotheses, training-range violations, decoder metrics, and limitations.

## Run

```bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m src.phase6
```

## Exit check

The commands recreate the machine-readable results and professional report evidence. Reproduction passed; decoder performance did not support a decryption claim.
