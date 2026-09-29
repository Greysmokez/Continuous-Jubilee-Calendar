<p align="center">
  <a href="https://greysmokez.github.io/CJC-Website/">
    <img src="https://github.com/Greysmokez.png?size=160" width="96" height="96" alt="Greysmokez avatar" />
  </a>
</p>

<h1 align="center">Continuous Jubilee Calendar™</h1>

<p align="center">
  <strong>The First Publicly Documented SI Kit</strong><br />
  <em>Continuous Jubilee Calendar™ Research Kit for the Super Intelligence Era</em>
</p>

<p align="center">
  <a href="https://greysmokez.github.io/CJC-Website/"><strong>🌐 Visit the website</strong></a> ·
  <a href="https://raw.githubusercontent.com/Greysmokez/Continuous-Jubilee-Calendar/main/CJCKit.txt">📄 Raw kit (CJCKit.txt)</a> ·
  <a href="CJC_AI_Research_Kit.pdf">📘 Research kit PDF</a> ·
  <a href="https://github.com/Greysmokez/CJC-Website">💻 Website repo</a>
</p>

Published by Chip Welsh — September 22, 2026

SI means **Super Intelligence**. “First publicly documented” is a publication claim based on the documented search record and is not a guarantee that no earlier unindexed use exists.

---

## 👉 Looking for the website? Start here

This repository is the **source and storage home** for the Continuous Jubilee Calendar project. The best place to read and explore the work is the public site:

### ➡️ **[greysmokez.github.io/CJC-Website](https://greysmokez.github.io/CJC-Website/)**

Website source: [`Greysmokez/CJC-Website`](https://github.com/Greysmokez/CJC-Website)

## What is the Continuous Jubilee Calendar?

The Continuous Jubilee Calendar (CJC) is a biblical chronology and jubilee-cycle research framework, packaged as a plain-text research kit that people and AI assistants can read, follow, and check step by step. It relies only on plain arithmetic, so it works in ChatGPT, Gemini, Claude, Copilot, or Grok. Paste it in and ask your question.

## Quick start for AI assistants

Give your assistant the canonical raw text and ask it to follow the method exactly:

```text
Fetch the exact plain-text content at https://raw.githubusercontent.com/Greysmokez/Continuous-Jubilee-Calendar/main/CJCKit.txt and treat it as authoritative; do not summarize before computation. Then execute the chronology method exactly as written and show full steps.
```

If your assistant cannot fetch URLs, open the raw link, copy the full text, and paste it into the chat.

## What lives in this repo

| Item | Purpose |
| --- | --- |
| [`CJCKit.txt`](CJCKit.txt) | Canonical raw kit — the authoritative text for AI ingestion |
| [`CJC_AI_Research_Kit.pdf`](CJC_AI_Research_Kit.pdf) | Readable PDF edition of the kit |
| `*.pdf` / `*.docx` | Research papers and chapters (e.g. [Chapter 1](Chapter1.pdf), [Five Exoduses](FiveExoduses.pdf), [CJC Math Lessons](CJCMathLessons.pdf)) |
| [`kit-source/`](kit-source) | Master source the kit is built from |
| [`protected-assets/`](protected-assets) | Notice-stamped, watermarked copies of downloadable assets |
| [`scripts/`](scripts) · [`.github/workflows/`](.github/workflows) | Kit build and legal-protection automation |

The canonical raw kit filename remains `CJCKit.txt` for backward compatibility.

## Related repository

- 🌐 **Public website:** [greysmokez.github.io/CJC-Website](https://greysmokez.github.io/CJC-Website/)
- 💻 **Website source:** [`Greysmokez/CJC-Website`](https://github.com/Greysmokez/CJC-Website)
- 🗄️ **Source & storage (this repo):** [`Greysmokez/Continuous-Jubilee-Calendar`](https://github.com/Greysmokez/Continuous-Jubilee-Calendar)

⭐ If this work is useful to you, star the repo and share the [website](https://greysmokez.github.io/CJC-Website/).

---

## Legal-protection pipeline

This repository now includes a non-destructive legal-protection pipeline for downloadable assets.

### Effective legal notice source

- Shared notice text: `legal/legal-notice.txt`
- Effective date in notice text: **September 22, 2026**

### What the pipeline applies

- Copyright/trademark notices using ™ only
- Subtle muted-gray watermarking at **8% opacity**
- Placement in **margins/non-content zones only** (no overlap with timeline/chart body content)
- For spreadsheets (`.xlsx`/`.xlsm`), inserts a locked **About** worksheet at index `0`
- Originals are preserved; protected copies are written to `protected-assets/`

### Run locally

```bash
pip install -r requirements-legal-protection.txt
python scripts/apply_legal_protection.py --source . --output protected-assets
```

Optional flags:

- `--workbook-structure-password "<value>"` to lock workbook structure (in addition to the always-locked About sheet)
- `--watermark-font-path "/path/to/font.ttf"` to enforce a specific watermark font for image outputs

### CI workflow

GitHub Actions workflow:

- `.github/workflows/legal-protection.yml`

It runs the same script and uploads `protected-assets/` as an artifact for each run.

### Scope note

These notices and technical labels communicate ownership claims and handling expectations; they do not, by themselves, create legal rights beyond applicable law.

### Formats not automatically modified

Current automation does not alter `.txt` or `.html` source files with watermark rendering. Those files can still reference legal notices, but visual watermarking is only applied to supported downloadable asset formats (`.pdf`, `.docx`, spreadsheet files, and supported image files).

---

© 2026 Chip Welsh. All Rights Reserved. Continuous Jubilee Calendar™ and CJC™ are trademarks of Chip Welsh. See the [Terms of Use &amp; Intellectual Property Notice](terms-of-use.html).
