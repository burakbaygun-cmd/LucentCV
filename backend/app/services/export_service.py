import io
import os
import html
from app.repositories.analysis_repository import AnalysisRepository
from app.core.logging import logger
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---------------------------------------------------------------------------
# Turkish-character-safe font setup
# ---------------------------------------------------------------------------
# We try to register a bundled TTF font that covers the full Latin-Extended
# block (ğ ş ı ç ö ü İ Ğ Ş Ç Ö Ü ...).  DejaVu Sans ships with many Linux /
# macOS environments; if it is not present we fall back to Helvetica and log
# a warning so developers know to supply the font file.

def _try_register_turkish_font() -> str:
    """
    Attempt to register a Unicode-capable TTF font and return its name.
    Priority order:
      1. ArialUnicode.ttf  — bundled under services/fonts/ (covers all Turkish chars)
      2. DejaVuSans.ttf    — common on Linux / Homebrew macOS
      3. LiberationSans    — CI / Docker fallback
      4. Helvetica         — ReportLab built-in (no Turkish support; last resort)
    """
    _fonts_dir = os.path.join(os.path.dirname(__file__), "fonts")
    font_map = [
        # (font_name_to_register, path)
        ("ArialUnicode",  os.path.join(_fonts_dir, "ArialUnicode.ttf")),
        ("DejaVuSans",    os.path.join(_fonts_dir, "DejaVuSans.ttf")),
        # macOS system / Homebrew
        ("ArialUnicode",  "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"),
        ("DejaVuSans",    "/Library/Fonts/DejaVuSans.ttf"),
        ("DejaVuSans",    "/usr/local/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        # Linux (Debian / Ubuntu / Alpine)
        ("DejaVuSans",    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        ("DejaVuSans",    "/usr/share/fonts/dejavu/DejaVuSans.ttf"),
        # CI / Docker
        ("LiberationSans", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"),
    ]
    for font_name, path in font_map:
        if os.path.isfile(path):
            try:
                pdfmetrics.registerFont(TTFont(font_name, path))
                logger.info(f"Registered Turkish-compatible font '{font_name}' from: {path}")
                return font_name
            except Exception as exc:
                logger.warning(f"Could not register font at {path}: {exc}")

    logger.warning(
        "No Unicode TTF font found for Turkish characters. "
        "PDF output may show replacement boxes for Turkish chars (ğ ş ı ç ö ü etc.). "
        "Bundled ArialUnicode.ttf in backend/app/services/fonts/ is missing."
    )
    return "Helvetica"


_FONT_NAME = _try_register_turkish_font()


def _safe(text: str) -> str:
    """
    Escape XML/HTML special characters so ReportLab's Paragraph XML parser
    does not crash or silently drop content containing &, <, >.
    """
    return html.escape(text, quote=False)


class ExportService:
    def __init__(self):
        self.analysis_repo = AnalysisRepository()

    def generate_markdown(self, analysis_id: str) -> str:
        logger.info(f"Generating Markdown export for analysis {analysis_id}")
        analysis = self.analysis_repo.get_analysis(analysis_id)
        if not analysis:
            raise ValueError(f"Analysis {analysis_id} not found")

        return analysis.get("report", "No report available.")

    def generate_pdf(self, analysis_id: str) -> bytes:
        logger.info(f"Generating PDF export for analysis {analysis_id}")
        analysis = self.analysis_repo.get_analysis(analysis_id)
        if not analysis:
            raise ValueError(f"Analysis {analysis_id} not found")

        report_text: str = analysis.get("report", "No report available.")

        # ---------------------------------------------------------------
        # Build PDF with UTF-8 / Turkish-character-safe configuration
        # ---------------------------------------------------------------
        buffer = io.BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=2 * cm,
            leftMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
        )

        base_styles = getSampleStyleSheet()

        # Override every style to use the Unicode-capable font
        title_style = ParagraphStyle(
            "TurkishTitle",
            parent=base_styles["Title"],
            fontName=_FONT_NAME,
            fontSize=20,
            spaceAfter=16,
        )
        h1_style = ParagraphStyle(
            "TurkishH1",
            parent=base_styles["Heading1"],
            fontName=_FONT_NAME,
            fontSize=16,
            spaceAfter=10,
        )
        h2_style = ParagraphStyle(
            "TurkishH2",
            parent=base_styles["Heading2"],
            fontName=_FONT_NAME,
            fontSize=13,
            spaceAfter=8,
        )
        h3_style = ParagraphStyle(
            "TurkishH3",
            parent=base_styles["Heading3"],
            fontName=_FONT_NAME,
            fontSize=11,
            spaceAfter=6,
        )
        body_style = ParagraphStyle(
            "TurkishBody",
            parent=base_styles["BodyText"],
            fontName=_FONT_NAME,
            fontSize=10,
            leading=14,
        )
        bullet_style = ParagraphStyle(
            "TurkishBullet",
            parent=body_style,
            leftIndent=16,
            spaceAfter=4,
        )

        flowables = []
        flowables.append(Paragraph("LucentCV - Analiz Raporu", title_style))
        flowables.append(Spacer(1, 12))

        # Markdown -> ReportLab with XML-safe escaping
        for line in report_text.split("\n"):
            line = line.strip()
            if not line:
                flowables.append(Spacer(1, 8))
                continue

            if line.startswith("### "):
                flowables.append(Paragraph(_safe(line[4:]), h3_style))
            elif line.startswith("## "):
                flowables.append(Paragraph(_safe(line[3:]), h2_style))
            elif line.startswith("# "):
                flowables.append(Paragraph(_safe(line[2:]), h1_style))
            elif line.startswith("- ") or line.startswith("* "):
                flowables.append(Paragraph(f"\u2022 {_safe(line[2:])}", bullet_style))
            else:
                flowables.append(Paragraph(_safe(line), body_style))

        doc.build(flowables)

        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
