import os
import requests
import uuid

def download_pdf(pdf_input):
    os.makedirs("downloads", exist_ok=True)
    
    if pdf_input.startswith("http"):
        unique_name = f"{uuid.uuid4()}.pdf"
        filename = os.path.join("downloads", unique_name)
        response = requests.get(pdf_input)
        with open(filename, "wb") as f:
            f.write(response.content)
        return filename
    elif os.path.isfile(pdf_input):
        # Copy local file into downloads/ with a unique name
        unique_name = f"{uuid.uuid4()}_{os.path.basename(pdf_input)}"
        filename = os.path.join("downloads", unique_name)
        with open(pdf_input, "rb") as src, open(filename, "wb") as dst:
            dst.write(src.read())
        return filename
    else:
        raise FileNotFoundError(f"File {pdf_input} not found")