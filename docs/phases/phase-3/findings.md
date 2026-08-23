# Phase 3 Findings

## Results

| Evaluation | Character accuracy | N-gram score | Correct rank | Runtime |
|---|---:|---:|---:|---:|
| Three-sample held-out suite | 0.927–0.953 | -1306.9 to -1227.4 | 1 for all | 4.4 s total |
| Full-run synthetic | 1.000 | -1966.8 | 1 | 14.0 s |
| Z408 | 0.032 | -2230.7 | 1 | 11.6 s |

## Conclusion

Simulated annealing consistently recovered useful plaintext from independently seeded, held-out homophonic ciphers, so the Phase 3 exit check passed.

Z408 recovery remained poor. Its known plaintext scored above every generated candidate, showing that the scoring function recognized it but the search failed to reach it. Phase 4 should preserve this as a measured baseline weakness; it does not support a decryption claim.
