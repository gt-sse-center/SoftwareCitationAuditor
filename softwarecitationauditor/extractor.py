import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    # Try to find 'References' heading with various formats
    split_keywords = ["\nReferences\n", "\nREFERENCES\n", "\nBibliography\n"]
    split_pos = -1
    for keyword in split_keywords:
        split_pos = full_text.find(keyword)
        if split_pos != -1:
            break

    if split_pos != -1:
        body = full_text[:split_pos]
        biblio = full_text[split_pos + len(keyword):]
    else:
        body = full_text
        biblio = ""

    return body.strip(), biblio.strip()
