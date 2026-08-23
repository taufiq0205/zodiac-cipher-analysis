# Phase 1 implementation — verified cipher data

Status: complete, 2026-08-24.

Phase 1 established the format with Z340 first, then repeated it for Z408, Z13, and Z32. Each raw record preserves the declared grid, stable symbol tokens, source URL, and explicit ambiguities.

## Files

| Cipher | Source image | Transcription |
|---|---|---|
| Z340 | [`z340-source.jpg`](../../../data/raw/z340-source.jpg) | [`z340.json`](../../../data/raw/z340.json) |
| Z408 | [`z408-source.jpg`](../../../data/raw/z408-source.jpg) | [`z408.json`](../../../data/raw/z408.json) |
| Z13 | [`z13-source.jpg`](../../../data/raw/z13-source.jpg) | [`z13.json`](../../../data/raw/z13.json) |
| Z32 | [`z32-source.jpg`](../../../data/raw/z32-source.jpg) | [`z32.json`](../../../data/raw/z32.json) |

Source provenance and cross-check limits are recorded in [`data/raw/sources.md`](../../../data/raw/sources.md). Known solutions are isolated in [`data/reference/`](../../../data/reference/).

## Record format

```json
{
  "cipher": "Z340",
  "dimensions": [20, 17],
  "source_url": "https://vault.fbi.gov/The%20Zodiac%20Killer/",
  "rows": [["H", "E", "R"]],
  "ambiguities": []
}
```

Unusual glyphs use descriptive tokens such as `circle_crosshair`, `triangle_filled`, `square_diagonal_reversed`, and `K_reversed`; they are not collapsed into approximate keyboard characters.

## Verification

- Transcribed each source row-by-row, followed by a second visual comparison of the complete grids.
- Recorded unresolved mirrored, dotted, and low-resolution glyphs in `ambiguities`.
- Structural check passed for 340, 408, 13, and 32 positions.
- Plaintext was not placed in `data/raw/`.

Phase 2 has not started.
