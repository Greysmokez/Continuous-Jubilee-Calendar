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

## 👉 Read the research on the website

This repository is the **source and storage home** of the Continuous Jubilee Calendar project. To read and explore the work, visit:

### ➡️ **[greysmokez.github.io/CJC-Website](https://greysmokez.github.io/CJC-Website/)**

## What is the Continuous Jubilee Calendar?

The **Continuous Jubilee Calendar (CJC)** is a **biblical chronology** research framework. It counts the Bible's 49-year **Jubilee cycles** (Leviticus 25) without a break, from the Exodus to today, with one plain-arithmetic formula, and tests the results against history, astronomy, and ancient records. Among its results:

- Daniel's **seventy weeks** run from the Jubilee of **457 BC** to the Jubilee of **AD 34**, exactly ten cycles.
- **483 years** after the decree, the count reaches **AD 27**, the start of Jesus' ministry (Daniel 9:25).
- The **crucifixion, Friday, April 7, AD 30,** falls in "the midst of the week" (Daniel 9:27).
- The seven-year **sabbatical** rhythm matches independent records, from the Maccabees and Josephus to today's *shemitah*.

**Start here:** [Could It Have Been Planned?](https://greysmokez.github.io/CJC-Website/could-it-have-been-planned.html) · [God's Clock](https://greysmokez.github.io/CJC-Website/isaiah61-cjc-math.html) · [From Decree to Cross](https://greysmokez.github.io/CJC-Website/decree2cross.html) · **For teachers:** [Math Lessons](https://greysmokez.github.io/CJC-Website/cjc-math-lessons.html)

## Quick start for SI and AI assistants

The kit relies only on plain arithmetic, so any capable assistant can follow it.

- **ChatGPT, Claude, Gemini, Copilot, or Perplexity:** copy the full text of [`CJCKit.txt`](https://raw.githubusercontent.com/Greysmokez/Continuous-Jubilee-Calendar/main/CJCKit.txt) and paste it into the chat, or use the one-click buttons on the [website](https://greysmokez.github.io/CJC-Website/).
- **Grok, or on a phone:** Grok treats very long pastes as file uploads, which require signing in, so send this short request instead:

```text
Read the entire CJC Research Kit at https://greysmokez.github.io/CJC-Website/kit.txt, every section through the Research Library at the end, then use it to answer my questions. Start with a short overview of the Continuous Jubilee Calendar.
```

## What lives in this repo

| Item | Purpose |
| --- | --- |
| [`CJCKit.txt`](CJCKit.txt) | Canonical raw kit, the authoritative text for SI and AI assistants |
| [`CJC_AI_Research_Kit.pdf`](CJC_AI_Research_Kit.pdf) | Readable PDF edition of the kit |
| `*.pdf` / `*.docx` | Research papers (e.g. [Chapter 1](Chapter1.pdf), [The Five Exoduses](FiveExoduses.pdf), [Math Lessons](CJCMathLessons.pdf)) |
| [`kit-source/`](kit-source) | Master source the kit is built from |
| [`protected-assets/`](protected-assets) | Notice-stamped, watermarked copies of downloadable files |
| [`scripts/`](scripts) · [`.github/workflows/`](.github/workflows) | Kit build and legal-protection automation |

The canonical raw kit filename remains `CJCKit.txt` for backward compatibility.

## Related links

- 🌐 **Public website:** [greysmokez.github.io/CJC-Website](https://greysmokez.github.io/CJC-Website/)
- 💻 **Website source:** [`Greysmokez/CJC-Website`](https://github.com/Greysmokez/CJC-Website)
- ✉️ **Questions or corrections:** [feedback page](https://greysmokez.github.io/CJC-Website/feedback/)

⭐ If this work is useful to you, **star the repo** and **share the [website](https://greysmokez.github.io/CJC-Website/)**.

*Keywords: CJC, CJC Website, Continuous Jubilee Calendar, Chip Welsh, Bible chronology, biblical calendar, Jubilee year, sabbatical year, shemitah, Leviticus 25, Daniel 9, seventy weeks prophecy, 457 BC, crucifixion date, AD 30, Exodus date, Bible prophecy timeline.*

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
