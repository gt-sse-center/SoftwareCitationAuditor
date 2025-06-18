import sys
from pathlib import Path
import typer
from colorama import Fore, Style, init as colorama_init
colorama_init()
from .downloader import download_pdf
from .extractor import extract_text_from_pdf
from .checker import extract_and_check_software

app = typer.Typer(help="Audit software mentions and citations in research papers.")

def process_paper(pdf_input, provider, model, save_report: bool = True):
    pdf_file = download_pdf(pdf_input)
    body_text, bibliography = extract_text_from_pdf(pdf_file)
    extract_and_check_software(body_text, bibliography, pdf_file, provider, model, save_report=save_report)
    Path(pdf_file).unlink()  # Clean up the downloaded PDF
    
@app.command()
def audit(
    pdf: str = typer.Argument(None, help="Single PDF path or URL."),
    input_file: str = typer.Option(None, "--input-file", "-i", help="Path to file with list of PDFs."),
    provider: str = typer.Option("openai", "--provider", "-p", help="LLM provider", show_default=True, case_sensitive=False),
    model: str = typer.Option("gpt-3.5-turbo", "--model", "-m", help="LLM model to use", show_default=True),
    save_report: bool = typer.Option(False, "--save-report", help="Save the final audit report to disk")
):
    if not pdf and not input_file:
        typer.echo(f"{Fore.RED}❌ You must provide either a PDF path or --input-file{Style.RESET_ALL}")
        raise typer.Exit(code=1)

    inputs = []
    if input_file:
        with open(input_file, "r") as f:
            inputs = [line.strip() for line in f if line.strip()]
    elif pdf:
        inputs = [pdf]

    for i, pdf_input in enumerate(inputs, start=1):
        typer.echo(f"{Fore.YELLOW}\n📄 [{i}/{len(inputs)}] Processing: {pdf_input}{Style.RESET_ALL}")
        process_paper(pdf_input, provider, model, save_report)

def cli():
    app()