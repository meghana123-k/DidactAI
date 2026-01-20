import fitz  # PyMuPDF

def extract_text_from_pdf(file_bytes: bytes) -> str:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    pages = []

    for page in doc:
        text = page.get_text()
        if text.strip():
            pages.append(text)

    return "\n".join(pages)
