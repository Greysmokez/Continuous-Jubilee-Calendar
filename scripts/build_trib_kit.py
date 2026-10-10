#!/usr/bin/env python3
"""
Build the Great Tribulation Q&A kit from its database.

  kit-source/tribulation/header.txt          instructions and paper list
  kit-source/tribulation/positions.md        settled positions (guardrails)
  kit-source/tribulation/timeline.md         day markers
  kit-source/tribulation/cjc-math.md         the CJC formula and anchor dates, with a handoff to the CJC kit
  kit-source/tribulation/question-index.md   the top questions, key verses, papers
  kit-source/tribulation/objections/*.md     common objections, each answered from Scripture
  kit-source/tribulation/entries/*.md        full worked entries (only STATUS: approved are built)

Outputs:
  TribulationKit.txt                   this repo
  Tribulation_AI_Research_Kit.pdf      this repo
  <website-out>/tribulation-kit.txt    pushed to CJC-Website by the workflow

Checks (the build stops and publishes nothing if any fail):
  - every approved entry has a QUICK ANSWER, a FULL STUDY, a quoted verse, and a scripturescjc.com paper link
  - every paper link names a page listed in the header
  - the red-flag phrases never appear in the index or the entries

Run locally:
  python scripts/build_trib_kit.py --website-out build-website
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "kit-source" / "tribulation"
sys.path.insert(0, str(ROOT / "scripts"))

RED_FLAGS = {
    "Matthew 24:15 called future or tied to Daniel 12:11": r"(Matthew 24:15|Mark 13:14)[^.\n]{0,120}(still future|yet future|Daniel 12:11|12:11)",
    "Antiochus as a fulfillment": r"Antiochus[^.\n]{0,60}fulfil",
    "seven-year tribulation asserted": r"(?<![Nn]o )(?<![Nn]o future )seven[- ]year tribulation",
    "beast from the earth called Lucifer": r"beast (from|out of) the earth[^.\n]{0,60}(is|was) (Lucifer|Satan)",
    "Jude 14 or Zechariah 14:4-5 at the last trump": r"(Jude 14|Zechariah 14:[45])[^.\n]{0,120}last trump",
    "Babylon called Jerusalem": r"Babylon[^.\n]{0,40}(is|was) Jerusalem",
    "Revelation 10:6 tied to the censer": r"(10:6|time no longer)[^.\n]{0,120}censer",
    "a future calendar date": r"\b20[3-9]\d\b",
    "'cannot' said of the Holy Spirit": r"(Holy )?Spirit[^.\n]{0,30}cannot",
}


def fail(msg: str) -> None:
    print(f"::error::{msg}")
    sys.exit(1)


def read(name: str) -> str:
    p = SRC / name
    if not p.exists():
        fail(f"Missing {p}")
    return p.read_text(encoding="utf-8").strip()


def check_entry(path: Path, text: str, pages: set[str]) -> None:
    for need in ("## QUICK ANSWER", "## FULL STUDY", "## PAPERS"):
        if need not in text:
            fail(f"{path.name}: missing section {need}")
    if not re.search(r"[“\"][^”\"]{12,}[”\"] \([1-3]? ?[A-Z][a-z]+ \d+:\d+", text):
        fail(f"{path.name}: no quoted verse with a reference found")
    links = re.findall(r"https://scripturescjc\.com/([\w-]+\.(?:html|txt))", text)
    if not links:
        fail(f"{path.name}: no scripturescjc.com paper link")
    for link in links:
        if link not in pages:
            fail(f"{path.name}: link to {link}, which is not in the header's paper list")


def check_objections(path: Path, text: str, pages: set[str]) -> None:
    blocks = re.split(r"^### ", text, flags=re.M)[1:]
    if not blocks:
        fail(f"{path.name}: no objections found (each starts with '### ')")
    for b in blocks:
        title = b.split("\n", 1)[0][:60]
        for need in ("Keywords:", "Answer:", "Papers:"):
            if need not in b:
                fail(f"{path.name}: '{title}' is missing '{need}'")
        if not re.search(r"[“\"][^”\"]{12,}[”\"] \([1-3]? ?[A-Z][a-z]+ \d+:\d+", b):
            fail(f"{path.name}: '{title}' has no quoted verse with a reference")
        for page in re.findall(r"([\w-]+\.html)", b.split("Papers:", 1)[1]):
            if page not in pages:
                fail(f"{path.name}: '{title}' cites {page}, which is not in the header's paper list")


def scan_red_flags(label: str, text: str) -> None:
    for why, pat in RED_FLAGS.items():
        m = re.search(pat, text)
        if m:
            fail(f"{label}: red flag ({why}): '{m.group(0)}'")


def to_plain(md: str) -> str:
    """Markdown headings become plain lines so the kit reads the same in every assistant."""
    out = []
    for line in md.splitlines():
        line = re.sub(r"^#+\s*", "", line)
        out.append(line.rstrip())
    return "\n".join(out).strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--website-out", type=Path, required=True)
    ap.add_argument("--no-pdf", action="store_true")
    args = ap.parse_args()

    header = read("header.txt")
    pages = set(re.findall(r"https://scripturescjc\.com/([\w-]+\.(?:html|txt))", header))

    index = read("question-index.md")
    scan_red_flags("question-index.md", index)

    objections = []
    for path in sorted((SRC / "objections").glob("*.md")):
        text = path.read_text(encoding="utf-8").strip()
        check_objections(path, text, pages)
        # The claim lines state the other view on purpose, so only the answers are scanned.
        answers = "\n".join(l for l in text.splitlines() if not l.startswith(("### ", "Keywords:")))
        scan_red_flags(path.name, answers)
        objections.append(to_plain(text))

    entries = []
    for path in sorted((SRC / "entries").glob("*.md")):
        text = path.read_text(encoding="utf-8").strip()
        status = re.search(r"^STATUS:\s*(\w+)", text, re.M)
        if not status or status.group(1).lower() != "approved":
            print(f"Skipping {path.name} (not approved)")
            continue
        check_entry(path, text, pages)
        scan_red_flags(path.name, text)
        entries.append(to_plain(text))

    parts = [
        header,
        "SETTLED POSITIONS\n\n" + to_plain(read("positions.md")),
        "TIMELINE\n\n" + to_plain(read("timeline.md")),
        "HOW THE DATES ARE DETERMINED\n\n" + to_plain(read("cjc-math.md")),
        "QUESTION INDEX\n\n" + to_plain(index),
        "COMMON OBJECTIONS, ANSWERED\n\n" + "\n\n".join(objections),
        "WORKED EXAMPLES (full entries)\n\n" + "\n\n----------\n\n".join(entries),
        "References: Scripture quotations are from the King James Version. The Jubilee rule for prophetic time, "
        "the censer as the start of the count, and the day-1,290 decree framework draw on the research of Larry Wilson, "
        "who presented his timelines as examples, not dates.",
    ]
    kit = "\n\n==========\n\n".join(parts) + "\n"

    (ROOT / "TribulationKit.txt").write_text(kit, encoding="utf-8")
    print("Wrote TribulationKit.txt")
    args.website_out.mkdir(parents=True, exist_ok=True)
    (args.website_out / "tribulation-kit.txt").write_text(kit, encoding="utf-8")
    print(f"Wrote {args.website_out / 'tribulation-kit.txt'}")

    if not args.no_pdf:
        from build_kit import build_docx, docx_to_pdf  # reuse the main kit's PDF styling
        with tempfile.TemporaryDirectory() as tmp:
            docx = Path(tmp) / "Tribulation_AI_Research_Kit.docx"
            build_docx(kit, docx)
            pdf = docx_to_pdf(docx, Path(tmp))
            target = ROOT / "Tribulation_AI_Research_Kit.pdf"
            target.write_bytes(pdf.read_bytes())
            print(f"Wrote {target.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
