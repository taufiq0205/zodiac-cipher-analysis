# Phase log

## 2026-08-24 — Phase 1: acquire and verify data

Status: complete.

- Established the transcription schema with Z340 before repeating it for Z408, Z13, and Z32.
- Added four source JPEGs, four grid JSON records, and [`data/raw/sources.md`](../../../data/raw/sources.md).
- Added only the known Z340 and Z408 plaintext references under [`data/reference/`](../../../data/reference/).
- Used the FBI Zodiac records as the authority anchor; community transcriptions were cross-checks only.
- Completed row-by-row transcription and a second-pass position check; uncertainties remain explicitly recorded in each JSON file.
- Exit check: `phase-1 raw/reference check: PASS`; expected dimensions `[20,17]`, `[24,17]`, `[1,13]`, and `[1,32]` all passed.

Phase 2 is pending and has not been started.
