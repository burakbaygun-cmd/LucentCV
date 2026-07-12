import io
from app.repositories.analysis_repository import AnalysisRepository
from app.core.logging import logger
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

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
            
        report_text = analysis.get("report", "No report available.")
        
        # Create PDF using ReportLab
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Add a simple custom style for body text if needed
        body_style = styles["BodyText"]
        title_style = styles["Title"]
        
        flowables = []
        flowables.append(Paragraph("LucentCV - Analysis Report", title_style))
        flowables.append(Spacer(1, 12))
        
        # Simple Markdown parser for ReportLab (very basic support)
        # Just splits by newline and adds Paragraphs
        for line in report_text.split("\n"):
            line = line.strip()
            if not line:
                flowables.append(Spacer(1, 12))
                continue
                
            if line.startswith("# "):
                flowables.append(Paragraph(line[2:], styles["Heading1"]))
            elif line.startswith("## "):
                flowables.append(Paragraph(line[3:], styles["Heading2"]))
            elif line.startswith("### "):
                flowables.append(Paragraph(line[4:], styles["Heading3"]))
            else:
                flowables.append(Paragraph(line, body_style))
                
        doc.build(flowables)
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
