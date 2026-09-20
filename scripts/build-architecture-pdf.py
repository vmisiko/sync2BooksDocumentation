#!/usr/bin/env python3
"""Render the TIS technology architecture markdown as the PDF we upload to KRA.

Usage:
    python3 scripts/build-architecture-pdf.py [SOURCE.md] [OUTPUT.pdf]

Defaults to ../sync2books-compliance-api/.docs/TIS_TECHNOLOGY_ARCHITECTURE_V2.md ->
assets/sync2books-TIS-Technology-Architecture-v2.pdf, so the markdown stays the
single source of truth and the PDF is a build artifact, never hand-edited.

Supports the markdown subset the document actually uses: headings, paragraphs,
bullet/numbered lists, pipe tables, fenced code blocks (ASCII diagrams, kept
verbatim), blockquotes, horizontal rules, and inline bold/italic/code/strikethrough.
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)

INK = colors.HexColor("#1A1A1A")
ACCENT = colors.HexColor("#0B5D33")
GREY = colors.HexColor("#5A5F5C")
RULE = colors.HexColor("#D4DCD7")
HEAD_BG = colors.HexColor("#EDF3EF")
CODE_BG = colors.HexColor("#F5F6F5")
QUOTE_BG = colors.HexColor("#F7F9F8")

PAGE_W, PAGE_H = A4
MARGIN = 18 * mm
CONTENT_W = PAGE_W - 2 * MARGIN


def _style(name: str, **kw) -> ParagraphStyle:
    base = dict(
        fontName="Helvetica",
        fontSize=9,
        leading=12.6,
        textColor=INK,
        spaceAfter=0,
        spaceBefore=0,
    )
    base.update(kw)
    return ParagraphStyle(name, **base)


S = {
    "title": _style("title", fontName="Helvetica-Bold", fontSize=19, leading=23,
                    textColor=ACCENT, spaceAfter=6),
    "subtitle": _style("subtitle", fontSize=11, leading=15, textColor=INK, spaceAfter=10),
    "h2": _style("h2", fontName="Helvetica-Bold", fontSize=13, leading=16,
                 textColor=ACCENT, spaceBefore=13, spaceAfter=5),
    "h3": _style("h3", fontName="Helvetica-Bold", fontSize=10.5, leading=13.5,
                 textColor=INK, spaceBefore=9, spaceAfter=4),
    "body": _style("body", spaceAfter=5),
    "bullet": _style("bullet", leftIndent=10, bulletIndent=2, spaceAfter=3),
    "quote": _style("quote", leftIndent=8, rightIndent=6, textColor=colors.HexColor("#33403A"),
                    spaceAfter=4),
    "cell": _style("cell", fontSize=8.1, leading=11),
    "cellhead": _style("cellhead", fontSize=8.1, leading=11, fontName="Helvetica-Bold"),
    "code": _style("code", fontName="Courier", fontSize=7.2, leading=8.8),
    "footer": _style("footer", fontSize=7.5, leading=10, textColor=GREY),
}

INLINE_CODE = re.compile(r"`([^`]+)`")
BOLD = re.compile(r"\*\*([^*]+)\*\*")
ITALIC = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)")
STRIKE = re.compile(r"~~([^~]+)~~")
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def inline(text: str) -> str:
    """Markdown inline formatting -> reportlab mini-HTML."""
    out = html.escape(text, quote=False)
    out = LINK.sub(r"\1", out)  # a printed PDF cannot be clicked; keep the label
    out = INLINE_CODE.sub(r'<font face="Courier" size="8">\1</font>', out)
    out = BOLD.sub(r"<b>\1</b>", out)
    out = STRIKE.sub(r"<strike>\1</strike>", out)
    out = ITALIC.sub(r"<i>\1</i>", out)
    return out


def split_row(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def build_table(rows: list[list[str]]) -> Table:
    header, *body = rows
    ncols = max(len(r) for r in rows)
    data = []
    for i, row in enumerate(rows):
        padded = row + [""] * (ncols - len(row))
        style = S["cellhead"] if i == 0 else S["cell"]
        data.append([Paragraph(inline(c), style) for c in padded])

    # A first column carrying labels reads better narrow; otherwise share evenly.
    if ncols == 2:
        widths = [CONTENT_W * 0.30, CONTENT_W * 0.70]
    else:
        widths = [CONTENT_W / ncols] * ncols

    table = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HEAD_BG),
                ("TEXTCOLOR", (0, 0), (-1, 0), ACCENT),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("GRID", (0, 0), (-1, -1), 0.4, RULE),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 3.5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
            ]
        )
    )
    return table


# The base-14 Courier face carries no box-drawing glyphs, so a diagram using them
# prints as gaps. Rather than embed a platform font (licensing, and the build would
# stop working off macOS), fold them onto ASCII that Courier does have.
BOX_TO_ASCII = str.maketrans({
    "\u250c": "+", "\u2510": "+", "\u2514": "+", "\u2518": "+",  # corners
    "\u252c": "+", "\u2534": "+", "\u251c": "+", "\u2524": "+", "\u253c": "+",  # tees, cross
    "\u2500": "-", "\u2502": "|",  # rules
    "\u2550": "=", "\u2551": "|", "\u2554": "+", "\u2557": "+", "\u255a": "+", "\u255d": "+",
    "\u25b6": ">", "\u25c0": "<", "\u25bc": "v", "\u25b2": "^",  # arrow heads
    "\u2192": "->", "\u2190": "<-", "\u2193": "v", "\u2191": "^",
    "\u2022": "*", "\u00b7": ".",
})


def code_block(lines: list[str]) -> Table:
    """ASCII diagrams must not reflow, so they are drawn verbatim on a tinted panel."""
    lines = [l.translate(BOX_TO_ASCII) for l in lines]
    longest = max((len(l) for l in lines), default=0)
    size = 7.2
    if longest > 96:  # shrink rather than clip a wide diagram
        size = max(4.6, 7.2 * 96 / longest)
    style = ParagraphStyle("codeblock", parent=S["code"], fontSize=size, leading=size * 1.22)
    body = Preformatted("\n".join(lines), style)
    panel = Table([[body]], colWidths=[CONTENT_W], hAlign="LEFT")
    panel.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), CODE_BG),
                ("BOX", (0, 0), (-1, -1), 0.4, RULE),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return panel


def quote_block(lines: list[str]) -> Table:
    paras = []
    buf: list[str] = []

    def flush():
        if buf:
            paras.append(Paragraph(inline(" ".join(buf)), S["quote"]))
            buf.clear()

    for line in lines:
        if not line.strip():
            flush()
        elif line.lstrip().startswith(("- ", "* ")):
            flush()
            paras.append(Paragraph(inline(line.lstrip()[2:]), S["quote"], bulletText="•"))
        else:
            buf.append(line.strip())
    flush()

    panel = Table([[paras]], colWidths=[CONTENT_W], hAlign="LEFT")
    panel.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), QUOTE_BG),
                ("LINEBEFORE", (0, 0), (0, -1), 2, ACCENT),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return panel


def convert(md: str) -> list:
    lines = md.splitlines()
    flow: list = []
    para: list[str] = []
    i = 0

    def flush_para():
        if para:
            flow.append(Paragraph(inline(" ".join(para)), S["body"]))
            para.clear()

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_para()
            i += 1
            block: list[str] = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i])
                i += 1
            i += 1
            flow.append(Spacer(1, 3))
            flow.append(code_block(block))
            flow.append(Spacer(1, 6))
            continue

        if stripped.startswith(">"):
            flush_para()
            block = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                block.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            flow.append(Spacer(1, 3))
            flow.append(quote_block(block))
            flow.append(Spacer(1, 6))
            continue

        if stripped.startswith("|"):
            flush_para()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = lines[i].strip()
                if not re.fullmatch(r"\|[\s:\-|]+\|", row):  # separator row
                    rows.append(split_row(row))
                i += 1
            if rows:
                flow.append(Spacer(1, 3))
                flow.append(build_table(rows))
                flow.append(Spacer(1, 7))
            continue

        if stripped in ("---", "***", "___"):
            flush_para()
            flow.append(Spacer(1, 4))
            flow.append(HRFlowable(width="100%", thickness=0.5, color=RULE))
            flow.append(Spacer(1, 4))
            i += 1
            continue

        if stripped.startswith("# "):
            flush_para()
            flow.append(Paragraph(inline(stripped[2:]), S["title"]))
            i += 1
            continue

        if stripped.startswith("## "):
            flush_para()
            heading = Paragraph(inline(stripped[3:]), S["h2"])
            # The document's one <h2> without a section number is the subtitle.
            flow.append(heading if re.match(r"^\d", stripped[3:]) or flow else heading)
            i += 1
            continue

        if stripped.startswith("### "):
            flush_para()
            flow.append(KeepTogether([Paragraph(inline(stripped[4:]), S["h3"])]))
            i += 1
            continue

        if stripped.startswith(("- ", "* ")):
            flush_para()
            flow.append(Paragraph(inline(stripped[2:]), S["bullet"], bulletText="•"))
            i += 1
            continue

        numbered = re.match(r"^(\d+)\.\s+(.*)", stripped)
        if numbered:
            flush_para()
            flow.append(
                Paragraph(inline(numbered.group(2)), S["bullet"],
                          bulletText=f"{numbered.group(1)}.")
            )
            i += 1
            continue

        if not stripped:
            flush_para()
            i += 1
            continue

        para.append(stripped)
        i += 1

    flush_para()
    return flow


def page_furniture(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.4)
    canvas.line(MARGIN, MARGIN - 4 * mm, PAGE_W - MARGIN, MARGIN - 4 * mm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(GREY)
    canvas.drawString(
        MARGIN,
        MARGIN - 8 * mm,
        "Sync2Books — TIS ↔ KRA eTIMS (OSCU) Technology Architecture v2.0",
    )
    canvas.drawRightString(PAGE_W - MARGIN, MARGIN - 8 * mm, f"Page {canvas.getPageNumber()}")
    canvas.restoreState()


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else (
        root.parent / "sync2books-compliance-api/.docs/TIS_TECHNOLOGY_ARCHITECTURE_V2.md"
    )
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else (
        root / "assets/sync2books-TIS-Technology-Architecture-v2.pdf"
    )

    doc = BaseDocTemplate(
        str(out),
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN + 6 * mm,
        title="Sync2Books TIS ↔ KRA eTIMS (OSCU) Technology Architecture v2.0",
        author="Sync2Books",
        subject="KRA eTIMS third-party integrator certification",
    )
    frame = Frame(MARGIN, MARGIN + 6 * mm, CONTENT_W,
                  PAGE_H - MARGIN - (MARGIN + 6 * mm), id="body")
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=page_furniture)])
    doc.build(convert(src.read_text(encoding="utf-8")))
    print(f"{out} ({out.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
