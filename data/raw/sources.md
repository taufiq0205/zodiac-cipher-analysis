# Phase 1 cipher sources

## Authority

The FBI Zodiac Killer records are the authority anchor for this dataset:

- [FBI Zodiac Killer records](https://vault.fbi.gov/The%20Zodiac%20Killer/)
- [FBI Zodiac Killer Part 01](https://vault.fbi.gov/The%20Zodiac%20Killer/The%20Zodiac%20Killer%20Part%2001/view)

The FBI release identifies the original cipher specimens in its laboratory records. The public release includes withheld or blacked-out pages, so the local JPEGs below preserve the publicly available correspondence/evidence scans used for direct glyph inspection. They are not represented as FBI-hosted image URLs; the Z408 scan also contains a small third-party highlight over part of row 20.

## Local source images

| File | Image source | Grid |
|---|---|---|
| `z340-source.jpg` | [Cipher Mysteries Z340 scan](https://ciphermysteries.com/wp-content/uploads/sites/6/2017/02/zodiac-killer-cipher-Z340.jpg) | 20×17 |
| `z408-source.jpg` | [Zodiac Killer Ciphers Z408 scan](https://forum.zodiackillerciphers.com/attachments/wpforo/attachments/55/18883%3D1828-gyke408.jpg) | 24×17 |
| `z13-source.jpg` | [Kryptografie Z13 scan](https://kryptografie.de/kryptografie/chiffre/images/zodiac-killer-z13.jpg) | 1×13 |
| `z32-source.jpg` | [Zodiac Killer Ciphers Z32 evidence photograph](https://zodiackillerciphers.com/wiki/images/thumb/7/7d/Button_Letter_with_32_code_large.jpg/600px-Button_Letter_with_32_code_large.jpg) | 1×32 |

Community transcriptions were used only as cross-checks: [TheDecipherist tables](https://github.com/TheDecipherist/TheDecipherist/blob/main/articles/the_zodiac_solved/THE_ZODIAC_SOLVED_COMPLETE.md) and [Z32 comparison material](https://www.zodiackillerciphers.com/wiki/index.php?title=Unsolved_32-character_%22map_code%22_cipher). They did not override the source images.

## Method

Each grid was transcribed row by row from its source image, then checked again against all positions. The JSON `ambiguities` arrays preserve glyphs whose mirrored, dotted, or low-resolution form could not be resolved with complete confidence. Plaintext references are isolated under `data/reference/`; no plaintext is stored beside raw evaluation inputs.
