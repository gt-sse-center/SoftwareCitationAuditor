import sys
import os
import typer
from tqdm import tqdm
from .downloader import download_pdf
from .extractor import extract_text_from_pdf
from .openai_checker import extract_and_check_software

app = typer.Typer(help="Audit software mentions and citations in research papers.")

def process_paper(pdf_input, provider, model):
    pdf_file = download_pdf(pdf_input)
    body_text, bibliography = extract_text_from_pdf(pdf_file)
    extract_and_check_software(body_text, bibliography, pdf_file, provider, model)
    os.remove(pdf_file)  # Clean up the downloaded PDF file

@app.command()
def audit(
    pdf: str = typer.Argument(None, help="Single PDF path or URL."),
    input_file: str = typer.Option(None, "--input-file", "-i", help="Path to file with list of PDFs."),
    provider: str = typer.Option("openai", "--provider", "-p", help="LLM provider", show_default=True, case_sensitive=False),
    model: str = typer.Option("gpt-3.5-turbo", "--model", "-m", help="LLM model to use", show_default=True)
):
    if not pdf and not input_file:
        typer.echo("❌ You must provide either a PDF path or --input-file")
        raise typer.Exit(code=1)

    inputs = []
    if input_file:
        with open(input_file, "r") as f:
            inputs = [line.strip() for line in f if line.strip()]
    elif pdf:
        inputs = [pdf]

    for pdf_input in tqdm(inputs, desc="Processing PDFs", unit="pdf"):
        typer.echo(f"\n📄 Processing: {pdf_input}")
        process_paper(pdf_input, provider, model)

def cli():
    app()