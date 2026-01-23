import os
from typing import Optional
def extract_text_from_input(text: Optional[str] = None, file=None) -> str:
    """
    Extracts clean text from:
    - raw text input
    - uploaded PDF
    - uploaded TXT
    - uploaded DOCX

    Returns:
        str: extracted plain text
    """

    if text and text.strip():
        return text.strip()

    if file is None:
        raise ValueError("No text or file provided")

    filename = (
    file.filename.lower()
    if hasattr(file, "filename")
    else os.path.basename(file.name).lower()
)


    if filename.endswith(".pdf"):
        return _extract_from_pdf(file)

    if filename.endswith(".txt"):
        return _extract_from_txt(file)

    if filename.endswith(".docx"):
        return _extract_from_docx(file)

    raise ValueError("Unsupported file type")
def _extract_from_pdf(file) -> str:
    from PyPDF2 import PdfReader

    reader = PdfReader(file)
    pages_text = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            pages_text.append(page_text)

    text = "\n".join(pages_text).strip()

    if not text:
        raise ValueError("No readable text found in PDF")

    return text
def _extract_from_txt(file) -> str:
    try:
        content = file.read().decode("utf-8")
    except Exception:
        content = file.read().decode("latin-1")

    text = content.strip()

    if not text:
        raise ValueError("Text file is empty")

    return text
def _extract_from_docx(file) -> str:
    from docx import Document

    document = Document(file)
    paragraphs = [
        p.text.strip()
        for p in document.paragraphs
        if p.text and p.text.strip()
    ]

    if not paragraphs:
        raise ValueError("No readable text found in DOCX")

    return "\n".join(paragraphs)
