import io
import os


def extract_text(data: bytes, filename: str) -> str:
    """
    Extract text from various file formats.

    Supported formats:
        - .txt:  Decode as UTF-8 text
        - .docx: Extract paragraphs using python-docx
        - .pdf:  Extract text using PyMuPDF (fitz)
        - Other: Returns empty string (e.g., images)

    Args:
        data: Raw file bytes
        filename: Original filename to determine format

    Returns:
        Extracted text content, or empty string if unsupported format
    """
    ext = os.path.splitext(filename)[1].lower()

    if ext == ".txt":
        return data.decode("utf-8", errors="ignore")

    elif ext == ".docx":
        from docx import Document

        doc = Document(io.BytesIO(data))
        return "\n".join([p.text for p in doc.paragraphs])

    elif ext == ".pdf":
        import fitz

        doc = fitz.open(stream=data, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text

    else:
        return ""
