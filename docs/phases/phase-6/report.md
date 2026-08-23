# Final Project Report: Zodiac Cipher Analysis

**Date:** 24 August 2026  
**Scope:** Z408, Z340, Z13, and Z32  
**Status:** Phase 6 complete

## Executive summary

This project tested whether reproducible classical cryptanalysis and a small machine-learning classifier could provide defensible evidence about four Zodiac ciphers.

The classifier ranked the expected cipher family first for both solved validation cases: homophonic substitution for Z408 and combined substitution/transposition for Z340. Those rankings remained unchanged after controlled symbol-copy errors affecting up to 3% of each transcription. However, four of seven measured features for each solved cipher fell outside the synthetic training range, so the reported probabilities must not be interpreted as calibrated confidence.

The classical decoder recovered only 3.2% of Z408 characters at the frozen setting. This is not useful plaintext recovery. The pipeline has no decoder for combined substitution/transposition, so it could not attempt Z340 under its top-ranked family.

Z13 and Z32 were assessed only after the solved-cipher family check passed. Both were ranked as combined ciphers, but both were outside the model's training range and neither received plaintext candidates. The project therefore reports no new solution for Z13 or Z32.

## Research objective

The objective was to rank cipher hypotheses while communicating uncertainty. The project was not designed to identify a suspect or declare a unique solution to Z13 or Z32.

## Methodology

The analysis used manually verified cipher transcriptions and kept the known Z408 and Z340 plaintexts separate from candidate generation. The frozen pipeline contained:

1. Seven ciphertext-only structural features.
2. A standardized multinomial logistic-regression classifier trained on 60 synthetic records.
3. A four-gram English scorer and simulated-annealing homophonic-substitution search.
4. Fixed random seeds, eight search restarts, and 30,000 steps per restart.

The recorded environment used Python 3.14.6, NumPy 2.5.2, scikit-learn 1.9.0, Matplotlib 3.11.1, and ipykernel 7.3.0. These direct dependencies are pinned in `requirements.txt`.

Robustness was tested by copying neighboring symbols into deterministic positions at nominal error rates of 1% and 3%. Family ranking was tested on Z408 and Z340. The classical decoder was tested only on Z408 because it does not implement transposition.

## Validation results

| Cipher | Expected family | Top-ranked family | Model probability | Features outside training range | Decoder result |
|---|---|---|---:|---:|---|
| Z408 | Homophonic | Homophonic | 99.92% | 4 of 7 | 3.2% character recovery |
| Z340 | Combined | Combined | 75.92% | 4 of 7 | Not supported |

Family classification matched both expected labels, but the evidence consists of only two real solved ciphers. The out-of-range features and weak Z408 recovery prevent this result from validating the pipeline as a practical decoder.

### Transcription-error sensitivity

| Cipher | Copied symbols | Top family | Model probability | Decoder accuracy |
|---|---:|---|---:|---:|
| Z408 | 0 (0%) | Homophonic | 99.92% | 3.2% |
| Z408 | 4 (1%) | Homophonic | 99.91% | 3.7% |
| Z408 | 12 (3%) | Homophonic | 99.63% | 10.0% |
| Z340 | 0 (0%) | Combined | 75.92% | Not supported |
| Z340 | 3 (1%) | Combined | 83.20% | Not supported |
| Z340 | 10 (3%) | Combined | 88.88% | Not supported |

The top family was stable under these errors. Increasing probability on damaged Z340 text is not evidence of improvement; it illustrates why probabilities from an out-of-distribution model should not be treated as certainty. The small changes in Z408 accuracy remain within an unusably low range.

## Exploratory results for unsolved ciphers

| Rank | Z13 hypothesis | Probability | Z32 hypothesis | Probability |
|---:|---|---:|---|---:|
| 1 | Combined | 92.00% | Combined | 99.63% |
| 2 | Transposition | 7.99% | Homophonic | 0.36% |
| 3 | Homophonic | 0.01% | Transposition | 0.01% |

These are model rankings, not solution probabilities. Five of seven Z13 features and four of seven Z32 features were outside the training range. Their short lengths also make repeated-pattern statistics sparse. Because the top hypothesis requires a decoder the project does not have, and because the classifier is being extrapolated, producing plaintext candidates would be unsupported.

## Limitations

- The synthetic dataset contains 90 fixed-length records produced by three simplified generators.
- Synthetic test accuracy does not establish generalization to historical ciphers.
- Logistic-regression probabilities are uncalibrated for out-of-range real inputs.
- The classical search supports homophonic substitution only.
- Two solved ciphers are insufficient for broad real-world validation.
- Z13 and Z32 are too short for this evidence to establish a unique reading.

## Conclusion

The project succeeded as a reproducible demonstration of hypothesis ranking and failure reporting. It did not produce a reliable Zodiac cipher decoder. Its strongest defensible result is that the family classifier reproduced the expected broad categories for Z408 and Z340 and remained stable under limited transcription errors. Its most important negative result is that the classical decoder failed on Z408 and the ML model extrapolated beyond its training range.

No solution is claimed for Z13 or Z32.

## Reproduction

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m src.phase6
```

The final command recreates `data/results/phase-6.json`. Expected checks are four passing tests, correct top family rankings for Z408 and Z340, and deterministic results apart from measured runtime.

Open `notebooks/hi.ipynb` and `notebooks/01-explore.ipynb` with the `.venv` kernel and run all cells. Both notebooks were also executed top-to-bottom during final verification.
