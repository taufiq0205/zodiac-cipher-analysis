# Zodiac Cipher Analysis Architecture

```mermaid
flowchart LR
    A[Verified cipher transcriptions<br/>Z408, Z340, Z13, Z32] --> C[Dataset loader]
    B[English text corpus] --> D[Synthetic cipher generator]
    D --> C

    C --> E[Feature extraction<br/>frequency, n-grams, entropy, grid patterns]
    E --> F[Classical baseline<br/>hill climbing / simulated annealing]
    E --> G[ML candidate ranker]

    F --> H[Candidate plaintexts]
    G --> H
    H --> I[Evaluation<br/>recovery accuracy, rank, robustness]

    I -->|validate| J[Known solutions<br/>Z408 and Z340]
    I -->|explore| K[Ranked hypotheses<br/>Z13 and Z32]
```

## Methodology flow

1. Preserve each cipher's symbols and grid layout in a verified transcription.
2. Generate labelled training examples from English text using plausible cipher transformations.
3. Establish a classical cryptanalysis baseline before training an ML model.
4. Train the ML component to rank candidate plaintexts or classify cipher families.
5. Validate against the known Z408 and Z340 solutions using held-out tests.
6. Apply the validated pipeline to Z13 and Z32, reporting alternatives rather than claiming a unique solution.

## Boundaries

- The pipeline supports hypothesis ranking, not suspect identification.
- Z13 and Z32 are too short to establish a unique solution from ciphertext alone.
- OCR is excluded initially; verified manual transcriptions are the source of truth.
