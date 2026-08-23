# Zodiac Cipher ML Project Plan

## Goal

Build a reproducible pipeline that ranks cipher hypotheses and communicates uncertainty. It must not claim to identify a suspect or uniquely solve Z13/Z32.

## Phase 0 — Setup (completed)

### Tasks

- Create `data/raw/`, `data/synthetic/`, `notebooks/`, `src/`, and `tests/`.
- Install `numpy`, `scikit-learn`, and `matplotlib` in `.venv`.
- Record dependencies in `requirements.txt`.
- Confirm a notebook runs with the `.venv` kernel.

### Exit check

Run a notebook cell that imports all three packages and prints the Python version.

## Phase 1 — Acquire and verify data (completed)

### Tasks

- Obtain authoritative transcriptions for Z408, Z340, Z13, and Z32.
- Preserve symbol identity, position, dimensions, and source URL.
- Store known plaintexts for Z408 and Z340 separately from evaluation inputs.
- Manually compare every transcription against its source image.

### Exit check

Assert the expected lengths: 408, 340, 13, and 32 symbols. Document any ambiguity rather than silently correcting it.

## Phase 2 — Explore the ciphers (completed)

### Tasks

- Create `notebooks/01-explore.ipynb`.
- Calculate symbol counts, repeated n-grams, entropy, and index of coincidence.
- Plot symbol-frequency distributions.
- Compare solved and unsolved ciphers without attempting decryption.

### Exit check

The notebook runs top-to-bottom and produces a short observations section supported by calculated results.

## Phase 3 — Build the classical baseline (completed)

### Tasks

- Implement character n-gram scoring from an English corpus.
- Implement one search method: hill climbing or simulated annealing.
- Test first on generated homophonic substitution ciphers.
- Evaluate on Z408 without exposing its plaintext to the search process.

### Metrics

- Character recovery accuracy
- Plaintext n-gram score
- Correct candidate rank
- Runtime

### Exit check

The baseline consistently recovers useful plaintext from held-out synthetic samples. Record failures honestly.

## Phase 4 — Generate synthetic data

### Tasks

- Sample plaintext passages from an English corpus.
- Apply homophonic substitution, transposition, or both.
- Add controlled symbol-copy errors.
- Split by source passage into training, validation, and test sets to prevent leakage.

### Exit check

A fixed random seed reproduces the dataset, and no source passage crosses dataset splits.

## Phase 5 — Add ML only if justified

### Decision gate

Continue only if a specific baseline weakness can be measured. Otherwise, keep the classical system as the final model.

### Tasks

- Train a scikit-learn model to classify cipher families or rank baseline candidates.
- Use only features calculated without knowing the plaintext.
- Compare against the Phase 3 baseline on the untouched test set.

### Exit check

Keep the ML component only if it improves a predefined metric and remains understandable. Report negative results if it does not.

## Phase 6 — Validate and report

### Tasks

- Run the frozen pipeline against Z408 and Z340.
- Test robustness by introducing transcription errors.
- Apply it to Z13 and Z32 only after validation.
- Report several ranked hypotheses, assumptions, and sensitivity—not a declared solution.
- Write the final methodology, results, limitations, and reproduction steps.

### Exit check

Another person can recreate the environment, rerun the notebooks, and obtain the reported results.

## Suggested execution order

```text
Setup → verified data → exploration → classical baseline
      → synthetic evaluation → optional ML → final report
```

Stop after each exit check. Fix that phase before starting the next one.
