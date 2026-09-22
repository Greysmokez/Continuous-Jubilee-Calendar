#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from docx import Document
from docx.shared import Pt, RGBColor
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment
from openpyxl.workbook.protection import WorkbookProtection
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas


NOTICE_FOOTER = "© 2026 Chip Welsh. All Rights Reserved. Continuous Jubilee Calendar™ and CJC™ are trademarks of Chip Welsh."
NOTICE_SHORT = "Continuous Jubilee Calendar™ / CJC™ — © 2026 Chip Welsh"
ABOUT_LINES = [
    "© 2026 Chip Welsh. All Rights Reserved.",
    "Continuous Jubilee Calendar™ and CJC™ are trademarks of Chip Welsh.",
    "Terms: see legal/legal-notice.txt (Effective Date: September 22, 2026).",
    "Notice scope: these labels communicate ownership claims and handling expectations; they do not create legal rights beyond applicable law.",
]
WATERMARK_COLOR = (140, 140, 140)
WATERMARK_OPACITY = 0.08


def ensure_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def relative_target(source_root: Path, output_root: Path, file_path: Path) -> Path:
    rel = file_path.relative_to(source_root)
    return output_root / rel


def add_docx_notice(source: Path, target: Path) -> None:
    doc = Document(str(source))
    for section in doc.sections:
        footer = section.footer
        paragraph = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        if NOTICE_FOOTER in paragraph.text:
            continue
        if paragraph.text.strip():
            paragraph.add_run("  ")
        run = paragraph.add_run(NOTICE_FOOTER)
        run.font.size = Pt(8)
        run.font.color.rgb = RGBColor(130, 130, 130)
    ensure_dir(target)
    doc.save(str(target))


def _overlay_stream(page_width: float, page_height: float, text: str, top_text: str) -> bytes:
    from io import BytesIO

    stream = BytesIO()
    c = canvas.Canvas(stream, pagesize=(page_width, page_height))
    c.setFillColor(Color(0.55, 0.55, 0.55, alpha=WATERMARK_OPACITY))
    c.setFont("Helvetica", 8)
    c.drawCentredString(page_width / 2, 14, text)
    c.drawString(12, page_height - 14, top_text)
    c.save()
    stream.seek(0)
    return stream.read()


def add_pdf_notice(source: Path, target: Path) -> None:
    from io import BytesIO

    reader = PdfReader(str(source))
    writer = PdfWriter()
    for page in reader.pages:
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        overlay_bytes = _overlay_stream(width, height, NOTICE_FOOTER, NOTICE_SHORT)
        overlay_page = PdfReader(BytesIO(overlay_bytes)).pages[0]
        page.merge_page(overlay_page, over=True)
        writer.add_page(page)
    ensure_dir(target)
    with target.open("wb") as fh:
        writer.write(fh)


def add_xlsx_about_sheet(source: Path, target: Path, workbook_password: str | None = None) -> None:
    wb = load_workbook(filename=str(source))
    if "About" in wb.sheetnames:
        del wb["About"]
    about = wb.create_sheet("About", 0)
    for idx, line in enumerate(ABOUT_LINES, start=1):
        cell = about.cell(row=idx, column=1, value=line)
        cell.font = Font(color="808080", size=10, bold=(idx == 1))
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    about.column_dimensions["A"].width = 120
    about.protection.sheet = True
    if workbook_password:
        wb.security = WorkbookProtection(lockStructure=True, workbookPassword=workbook_password)
    ensure_dir(target)
    wb.save(str(target))


def add_image_margin_watermark(source: Path, target: Path) -> None:
    with Image.open(source) as original:
        image = original.convert("RGBA")
        margin = max(16, int(min(image.width, image.height) * 0.04))
        canvas_img = Image.new(
            "RGBA",
            (image.width + margin * 2, image.height + margin * 2),
            (255, 255, 255, 255),
        )
        canvas_img.paste(image, (margin, margin))

        layer = Image.new("RGBA", canvas_img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(layer)
        font = ImageFont.load_default()
        alpha = int(255 * WATERMARK_OPACITY)
        fill = (*WATERMARK_COLOR, alpha)
        text = NOTICE_SHORT
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        draw.text(((canvas_img.width - text_w) / 2, 4), text, fill=fill, font=font)
        draw.text(
            ((canvas_img.width - text_w) / 2, canvas_img.height - text_h - 4),
            text,
            fill=fill,
            font=font,
        )

        merged = Image.alpha_composite(canvas_img, layer).convert("RGB")
        ensure_dir(target)
        merged.save(target)


def copy_textual_notice(source: Path, target: Path) -> None:
    ensure_dir(target)
    shutil.copy2(source, target)


def process(source_root: Path, output_root: Path, workbook_password: str | None = None) -> dict:
    supported = {".pdf", ".docx", ".xlsx", ".xlsm", ".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff"}
    skipped = []
    processed = []
    for file_path in source_root.rglob("*"):
        if not file_path.is_file():
            continue
        if output_root in file_path.parents or ".git" in file_path.parts:
            continue
        target = relative_target(source_root, output_root, file_path)
        suffix = file_path.suffix.lower()
        try:
            if suffix == ".pdf":
                add_pdf_notice(file_path, target)
                processed.append(str(file_path.relative_to(source_root)))
            elif suffix == ".docx":
                add_docx_notice(file_path, target)
                processed.append(str(file_path.relative_to(source_root)))
            elif suffix in {".xlsx", ".xlsm"}:
                add_xlsx_about_sheet(file_path, target, workbook_password=workbook_password)
                processed.append(str(file_path.relative_to(source_root)))
            elif suffix in {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff"}:
                add_image_margin_watermark(file_path, target)
                processed.append(str(file_path.relative_to(source_root)))
            elif suffix == ".txt" and file_path.name == "legal-notice.txt":
                copy_textual_notice(file_path, target)
                processed.append(str(file_path.relative_to(source_root)))
            elif suffix not in supported:
                skipped.append(str(file_path.relative_to(source_root)))
        except Exception as exc:  # pragma: no cover - operational reporting
            skipped.append(f"{file_path.relative_to(source_root)} ({exc})")

    output_root.mkdir(parents=True, exist_ok=True)
    report = {
        "effective_date": "September 22, 2026",
        "watermark_opacity": WATERMARK_OPACITY,
        "watermark_color": WATERMARK_COLOR,
        "margin_only": True,
        "processed_files": sorted(processed),
        "skipped_files": sorted(skipped),
    }
    (output_root / "processing-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply legal labels/watermarks to source assets without editing originals.")
    parser.add_argument(
        "--source",
        type=Path,
        default=Path("."),
        help="Source directory containing original documents/assets.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("protected-assets"),
        help="Output directory where protected copies are written.",
    )
    parser.add_argument(
        "--workbook-password",
        default=None,
        help="Optional workbook structure password for spreadsheet outputs.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = process(args.source.resolve(), args.output.resolve(), workbook_password=args.workbook_password)
    print(f"Processed files: {len(report['processed_files'])}")
    print(f"Skipped files: {len(report['skipped_files'])}")
    print(f"Report: {args.output / 'processing-report.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
