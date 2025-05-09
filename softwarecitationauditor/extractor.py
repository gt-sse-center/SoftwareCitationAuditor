
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    if "references" in text.lower():
        body, biblio = text.lower().split("references", 1)
    else:
        body, biblio = text, ""
    return body, biblio
