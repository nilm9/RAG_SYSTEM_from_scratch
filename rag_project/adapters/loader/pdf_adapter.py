
import pdfplumber

def extract_pdf_text(file_path: str) -> str:
    """Extracts text from a PDF file."""
    with pdfplumber.open(file_path) as pdf:
        return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
