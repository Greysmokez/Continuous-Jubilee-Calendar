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
  kit-source/tribulation/revelation-guide.md Revelation chapter by chapter
  kit-source/tribulation/revelation-kjv.txt  the full KJV text of Revelation (appendix)
  scripts/data/kjv.txt                       the full KJV Bible, used only to check quotations

Outputs:
  TribulationKit.txt                   this repo
  Tribulation_AI_Research_Kit.pdf      this repo
  <website-out>/tribulation-kit.txt    pushed to CJC-Website by the workflow

Checks (the build stops and publishes nothing if any fail):
  - every approved entry has a QUICK ANSWER, a FULL STUDY, a quoted verse, and a scripturescjc.com paper link
  - every paper link names a page listed in the header
  - the red-flag phrases never appear in the index or the entries
  - every Scripture quotation followed by a reference matches the KJV word for word

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
    "false prophet called Lucifer": r"false prophet[^.\n]{0,20}(is|was|=) (Lucifer|Satan|the devil)",
    "Jude 14 or Zechariah 14:4-5 at the last trump": r"(Jude 14|Zechariah 14:[45])[^.\n]{0,120}last trump",
    "Babylon called Jerusalem": r"Babylon[^.\n]{0,40}(is|was) Jerusalem",
    "Revelation 10:6 tied to the censer": r"(10:6|time no longer)[^.\n]{0,120}censer",
    "two witnesses called the Old and New Testaments": r"two witnesses[^.\n]{0,80}(Old and New|Old Testament and the New|two testaments)",
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


def _norm(s: str) -> str:
    s = s.lower().replace("\u2019", "'").replace("\u00e6", "ae")
    s = re.sub(r"\[[^\]]*\]", " ", s)          # [insertions] are not Scripture
    s = re.sub(r"[^a-z' ]+", " ", s).replace("'", "")
    return " " + re.sub(r"\s+", " ", s).strip() + " "


_BIBLE = None
_QUOTE = re.compile(
    r"[\"\u201c]([^\"\u201c\u201d\n]{8,}?)[\"\u201d]"
    r"\s*,?\s*\(?\s*(?:see\s+)?(?:[1-3] )?(?:[A-Z][a-z]+(?: of [A-Z][a-z]+)? )?\d+:\d+"
)


def check_quotes(label: str, text: str) -> None:
    """Every quotation followed by a verse reference must appear word for word in the KJV.
    '...' marks an omission; each piece of three words or more is checked."""
    global _BIBLE
    if _BIBLE is None:
        lines = (ROOT / "scripts" / "data" / "kjv.txt").read_text(encoding="utf-8").splitlines()
        _BIBLE = _norm(" ".join(l.split("\t", 1)[1] for l in lines if "\t" in l))
    for m in _QUOTE.finditer(text):
        for seg in re.split(r"\.\.\.|\u2026", m.group(1)):
            words = _norm(seg).split()
            if len(words) >= 3 and " " + " ".join(words) + " " not in _BIBLE:
                fail(f"{label}: quotation does not match the KJV: \"{seg.strip()}\"")


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
    for need in ("21. Some questions belong to the companion CJC Research Kit", "https://scripturescjc.com/kit.txt"):
        if need not in header:
            fail(f"header.txt: missing required text: {need}")
    pages = set(re.findall(r"https://scripturescjc\.com/([\w-]+\.(?:html|txt))", header))

    index = read("question-index.md")
    scan_red_flags("question-index.md", index)
    guide = read("revelation-guide.md")
    scan_red_flags("revelation-guide.md", guide)
    for name, body in (("positions.md", read("positions.md")), ("timeline.md", read("timeline.md")),
                       ("question-index.md", index), ("revelation-guide.md", guide)):
        check_quotes(name, body)
    revelation = read("revelation-kjv.txt")
    if revelation.count("\n") < 420 or "22:21 The grace of our Lord Jesus Christ be with you all. Amen." not in revelation:
        fail("revelation-kjv.txt looks incomplete (expected all 404 verses)")

    objections = []
    for path in sorted((SRC / "objections").glob("*.md")):
        text = path.read_text(encoding="utf-8").strip()
        check_objections(path, text, pages)
        check_quotes(path.name, text)
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
        check_quotes(path.name, text)
        scan_red_flags(path.name, text)
        entries.append(to_plain(text))

    parts = [
        header,
        "SETTLED POSITIONS\n\n" + to_plain(read("positions.md")),
        "TIMELINE\n\n" + to_plain(read("timeline.md")),
        "HOW THE DATES ARE DETERMINED\n\n" + to_plain(read("cjc-math.md")),
        "QUESTION INDEX\n\n" + to_plain(index),
        "REVELATION, CHAPTER BY CHAPTER\n\n" + to_plain(guide),
        "COMMON OBJECTIONS, ANSWERED\n\n" + "\n\n".join(objections),
        "WORKED EXAMPLES (full entries)\n\n" + "\n\n----------\n\n".join(entries),
        "APPENDIX: " + revelation,
        "References: Scripture quotations are from the King James Version. The Jubilee rule for prophetic time, "
        "the censer as the start of the count, and the day-1,290 decree framework draw on the research of Larry Wilson, "
        "who presented his timelines as examples, not dates.",
    ]
    kit = "\n\n==========\n\n".join(parts) + "\n"
    # The author is named only in the header's "who wrote this" rule, plus (optionally) the copyright notice line.
    notice = "\u00a9 2026 Chip Welsh. All Rights Reserved."
    n = kit.count("Chip")
    if "Chip Welsh, the author" not in kit or not (n == 1 or (n == 2 and notice in kit)):
        fail("The author's name may appear only in the header rule for when a user asks who wrote the research, and in the copyright notice.")

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
