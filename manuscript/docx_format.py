"""DOCX layout for an Elsevier-style single-column review manuscript:
A4, 2.5 cm margins, Times New Roman 12 pt, double line spacing, continuous line numbers,
page numbers, three-line tables, title page with placeholders."""
from __future__ import annotations

import subprocess
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

FONT = "Times New Roman"


def _style_font(style, size, bold=None, italic=None):
    style.font.name = FONT
    style.font.size = Pt(size)
    style.font.color.rgb = RGBColor(0, 0, 0)
    if bold is not None:
        style.font.bold = bold
    if italic is not None:
        style.font.italic = italic
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts"); rpr.append(rfonts)
    for att in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(att), FONT)
    for att in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
        if rfonts.get(qn(att)) is not None:
            del rfonts.attrib[qn(att)]


def make_reference_doc(path: Path) -> Path:
    """Start from pandoc's default reference document and set the journal styles."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(subprocess.run(["pandoc", "-o", "-", "--print-default-data-file", "reference.docx"], check=True, capture_output=True).stdout)
    doc = Document(str(path))
    names = {s.name: s for s in doc.styles}
    for name, size, bold, italic in (("Normal", 12, None, None), ("Body Text", 12, None, None), ("First Paragraph", 12, None, None),
                                     ("Compact", 10, None, None), ("Title", 16, True, None), ("Heading 1", 13, True, False),
                                     ("Heading 2", 12, True, False), ("Heading 3", 12, False, True), ("Image Caption", 10, None, False),
                                     ("Table Caption", 10, None, False), ("Captioned Figure", 10, None, None), ("Bibliography", 11, None, None),
                                     ("Abstract", 12, None, None)):
        if name in names:
            _style_font(names[name], size, bold, italic)
    for name in ("Body Text", "First Paragraph", "Normal", "Abstract"):
        if name in names:
            pf = names[name].paragraph_format
            pf.line_spacing, pf.space_after, pf.space_before = 2.0, Pt(0), Pt(0)
            pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for name in ("Heading 1", "Heading 2", "Heading 3"):
        if name in names:
            pf = names[name].paragraph_format
            pf.space_before, pf.space_after, pf.keep_with_next, pf.line_spacing = Pt(12), Pt(6), True, 1.5
    for name in ("Image Caption", "Table Caption", "Bibliography", "Compact"):
        if name in names:
            names[name].paragraph_format.line_spacing = 1.15
            names[name].paragraph_format.space_after = Pt(6)
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    sec.left_margin = sec.right_margin = sec.top_margin = sec.bottom_margin = Cm(2.5)
    doc.save(str(path))
    return path


def _borders(cell, **edges):
    tcPr = cell._tc.get_or_add_tcPr()
    b = tcPr.find(qn("w:tcBorders"))
    if b is None:
        b = OxmlElement("w:tcBorders"); tcPr.append(b)
    for edge in ("top", "bottom", "left", "right"):
        el = b.find(qn(f"w:{edge}"))
        if el is None:
            el = OxmlElement(f"w:{edge}"); b.append(el)
        if edge in edges:
            el.set(qn("w:val"), "single"); el.set(qn("w:sz"), str(edges[edge])); el.set(qn("w:color"), "000000")
        else:
            el.set(qn("w:val"), "nil")


def _page_number_footer(section):
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    for kind, text in (("begin", None), (None, "PAGE"), ("end", None)):
        if kind:
            el = OxmlElement("w:fldChar"); el.set(qn("w:fldCharType"), kind)
        else:
            el = OxmlElement("w:instrText"); el.set(qn("xml:space"), "preserve"); el.text = text
        run._r.append(el)
    run.font.size, run.font.name = Pt(10), FONT


def postprocess(path: Path, title: str):
    doc = Document(str(path))
    # ---- tables: three-line layout, 9 pt, full width ------------------------------------------
    for t in doc.tables:
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        n = len(t.rows)
        for i, row in enumerate(t.rows):
            trPr = row._tr.get_or_add_trPr()
            cs = OxmlElement("w:cantSplit"); trPr.append(cs)
            for cell in row.cells:
                edges = {}
                if i == 0:
                    edges = {"top": 12, "bottom": 6}
                if i == n - 1:
                    edges["bottom"] = 12
                _borders(cell, **edges)
                for p in cell.paragraphs:
                    p.paragraph_format.line_spacing, p.paragraph_format.space_after, p.paragraph_format.space_before = 1.0, Pt(1), Pt(1)
                    for r in p.runs:
                        r.font.size, r.font.name = Pt(8.5), FONT
                        if i == 0:
                            r.font.bold = True
    # ---- figures: centred, kept with their caption --------------------------------------------
    for p in doc.paragraphs:
        if p._p.findall(".//" + qn("w:drawing")):
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.keep_with_next = True
            p.paragraph_format.line_spacing = 1.0
        if p.style.name in ("Table Caption",):
            p.paragraph_format.keep_with_next = True
    # ---- page breaks before major blocks ------------------------------------------------------
    for p in doc.paragraphs:
        if p.style.name == "Heading 1" and p.text.strip() in ("1. Introduction", "References", "Highlights"):
            p.paragraph_format.page_break_before = True
    # ---- continuous line numbers and page numbers ---------------------------------------------
    for sec in doc.sections:
        sectPr = sec._sectPr
        ln = sectPr.find(qn("w:lnNumType"))
        if ln is None:
            ln = OxmlElement("w:lnNumType"); sectPr.append(ln)
        ln.set(qn("w:countBy"), "1"); ln.set(qn("w:restart"), "continuous")
        _page_number_footer(sec)
    doc.core_properties.title = title
    doc.core_properties.author = "[Author names]"
    doc.save(str(path))
