# Continuous Jubilee Calendar

This repository now includes a non-destructive legal-protection pipeline for downloadable assets.

## Effective legal notice source

- Shared notice text: `/home/runner/work/Continuous-Jubilee-Calendar/Continuous-Jubilee-Calendar/legal/legal-notice.txt`
- Effective date in notice text: **September 22, 2026**

## What the pipeline applies

- Copyright/trademark notices using ™ only
- Subtle muted-gray watermarking at **8% opacity**
- Placement in **margins/non-content zones only** (no overlap with timeline/chart body content)
- For spreadsheets (`.xlsx`/`.xlsm`), inserts a locked **About** worksheet at index `0`
- Originals are preserved; protected copies are written to `protected-assets/`

## Run locally

```bash
pip install -r requirements-legal-protection.txt
python scripts/apply_legal_protection.py --source . --output protected-assets
```

Optional flags:

- `--workbook-structure-password "<value>"` to lock workbook structure (in addition to the always-locked About sheet)
- `--watermark-font-path "/path/to/font.ttf"` to enforce a specific watermark font for image outputs

## CI workflow

GitHub Actions workflow:

- `/home/runner/work/Continuous-Jubilee-Calendar/Continuous-Jubilee-Calendar/.github/workflows/legal-protection.yml`

It runs the same script and uploads `protected-assets/` as an artifact for each run.

## Scope note

These notices and technical labels communicate ownership claims and handling expectations; they do not, by themselves, create legal rights beyond applicable law.

## Formats not automatically modified

Current automation does not alter `.txt` or `.html` source files with watermark rendering. Those files can still reference legal notices, but visual watermarking is only applied to supported downloadable asset formats (`.pdf`, `.docx`, spreadsheet files, and supported image files).
