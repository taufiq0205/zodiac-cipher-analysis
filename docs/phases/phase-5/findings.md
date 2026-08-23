# Phase 5 Findings

## Results

| Evaluation | Records | Phase 3 homophonic assumption | ML classifier |
|---|---:|---:|---:|
| Validation | 15 | 33.3% | 100% |
| Untouched test | 15 | 33.3% | 100% |

The test confusion matrix was perfect: five correct predictions for each of homophonic, transposition, and combined ciphers.

## Conclusion

The model passed the predefined gate and is retained only for cipher-family classification. It learned from ciphertext structure without using plaintext.

This is a small synthetic benchmark whose generators have distinct structural signatures. The result does not prove that the classifier generalizes to real Zodiac ciphers, and it does not improve the classical decryption search by itself. Phase 6 must test that boundary honestly.
