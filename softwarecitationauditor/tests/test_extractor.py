from softwarecitationauditor import extractor
import os

def test_extract_text_from_pdf():
    # Using an empty dummy PDF for simplicity
    import fitz
    filename = "dummy.pdf"
    doc = fitz.open()
    doc.new_page()
    doc.save(filename)
    body, biblio = extractor.extract_text_from_pdf(filename)
    assert isinstance(body, str)
    assert isinstance(biblio, str)
    doc.close()
    os.remove(filename)