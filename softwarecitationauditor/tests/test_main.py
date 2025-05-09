import sys
import tempfile
from softwarecitationauditor import main

def test_process_paper(monkeypatch):
    called = []

    def fake_process_paper(pdf_input, provider, model):
        called.append(pdf_input)

    monkeypatch.setattr(main, "process_paper", fake_process_paper)
    main.process_paper("dummy.pdf", "openai", "gpt-3.5-turbo")
    assert "dummy.pdf" in called

def test_cli_with_input_file(monkeypatch):
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        f.write("file1.pdf\nfile2.pdf\n")
        file_name = f.name

    called = []

    def fake_process_paper(pdf_input, provider, model):
        called.append(pdf_input)

    monkeypatch.setattr(main, "process_paper", fake_process_paper)
    monkeypatch.setattr(sys, "argv", ["program", "--input-file", file_name])

    main.cli()

    assert "file1.pdf" in called
    assert "file2.pdf" in called

def test_cli_with_single_pdf(monkeypatch):
    called = []

    def fake_process_paper(pdf_input, provider, model):
        called.append(pdf_input)

    monkeypatch.setattr(main, "process_paper", fake_process_paper)
    monkeypatch.setattr(sys, "argv", ["program", "file1.pdf"])

    main.cli()

    assert "file1.pdf" in called