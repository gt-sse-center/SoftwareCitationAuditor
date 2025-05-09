import sys
import argparse
from tqdm import tqdm
from .downloader import download_pdf
from .extractor import extract_text_from_pdf
from .openai_checker import extract_and_check_software

def process_paper(pdf_input, provider, model):
    pdf_file = download_pdf(pdf_input)
    body_text, bibliography = extract_text_from_pdf(pdf_file)
    extract_and_check_software(body_text, bibliography, pdf_file, provider, model)

def cli():
    parser = argparse.ArgumentParser(description="GT SSE Software Citation Checker")
    parser.add_argument('pdf', nargs='?', help='Single PDF file path or URL')
    parser.add_argument('--input-file', '-i', help='Path to text file with list of PDF URLs or paths (one per line)')
    parser.add_argument('--provider', '-p', default='openai', choices=['openai', 'claude', 'gemini'], help='Provider: openai, claude, gemini (default: openai)')
    parser.add_argument('--model', '-m', default='gpt-3.5-turbo', help='Model to use (default: gpt-3.5-turbo)')
    args = parser.parse_args()

    inputs = []
    if args.input_file:
        with open(args.input_file, 'r') as f:
            inputs = [line.strip() for line in f if line.strip()]
    elif args.pdf:
        inputs = [args.pdf]
    else:
        print("Usage: softwarecitationauditor <pdf_url_or_path> or --input-file FILE")
        sys.exit(1)

    for pdf_input in tqdm(inputs, desc="Processing PDFs", unit="pdf"):
        print(f"\n📄 Processing: {pdf_input}")
        process_paper(pdf_input, args.provider, args.model)