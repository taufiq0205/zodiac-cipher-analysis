# Phase 2 Findings

The notebook measures the ciphers' visible structure, not their meaning.

| Cipher | Length | Unique symbols | Entropy | Index of coincidence | Repeated bigrams | Repeated trigrams |
|---|---:|---:|---:|---:|---:|---:|
| Z408 | 408 | 49 | 5.512 | 0.0211 | 59 | 10 |
| Z340 | 340 | 64 | 5.752 | 0.0194 | 20 | 2 |
| Z13 | 13 | 9 | 3.027 | 0.0641 | 0 | 0 |
| Z32 | 32 | 29 | 4.812 | 0.0060 | 0 | 0 |

## Meaning

- **Entropy** measures how evenly symbols are used. Higher values mean less predictable symbol choices, but values depend on alphabet size.
- **Index of coincidence** is the chance that two randomly selected positions contain the same symbol.
- **Bigrams and trigrams** are repeated sequences of two or three adjacent symbols.

Z408 contains the most repeated sequences. Z340 uses more distinct symbols and has fewer repeated sequences. Z13 repeats individual symbols but has no repeated adjacent pairs or triples. Z32 uses 29 unique symbols across only 32 positions, making repetition rare.

## Conclusion

Z408 and Z340 are long enough to provide useful structural evidence. Z13 and Z32 are too short for stable statistics: a few symbols can substantially change their measurements. These results support testing methods on the longer solved ciphers first, but they do not support a decryption claim.
