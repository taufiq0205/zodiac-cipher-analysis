# Phase 4 Findings

## Results

| Check | Result |
|---|---:|
| Fixed-seed reproduction | Pass |
| Distinct source passages | 90 of 90 |
| Cross-split source overlap | 0 |
| Training / validation / test | 60 / 15 / 15 |
| Homophonic / transposition / both | 30 / 30 / 30 |

## Conclusion

The dataset is reproducible and prevents source-passage leakage between splits, so the Phase 4 exit check passed. Copy-error rates are controlled metadata, allowing later robustness comparisons without confusing corrupted and clean samples.
