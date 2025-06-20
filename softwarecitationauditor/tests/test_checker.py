# softwarecitationauditor/tests/test_checker.py

import os
import json
import tempfile
import pytest
from softwarecitationauditor import checker

class MockLLM:
    def __init__(self, model=None, client=None):
        self.calls = []

    def generate(self, prompt):
        self.calls.append(prompt)
        # Return a valid JSON string
        return json.dumps({"software": ["MockTool"], "citation": "Properly cited"})

@pytest.mark.parametrize("provider_name", ["openai", "claude", "gemini", "ollama"])
def test_extract_and_check_software(monkeypatch, provider_name):
    dummy_body = "This paper uses MockTool for analysis."
    dummy_bib = "References include proper citations."
    dummy_pdf = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False).name

    monkeypatch.setattr(checker, "OpenAIProvider", lambda model, client=None: MockLLM())
    monkeypatch.setattr(checker, "ClaudeProvider", lambda model, client=None: MockLLM())
    monkeypatch.setattr(checker, "GeminiProvider", lambda model, client=None: MockLLM())
    monkeypatch.setattr(checker, "OllamaProvider", lambda model, client=None: MockLLM())

    checker.extract_and_check_software(
        body_text=dummy_body,
        bibliography_text=dummy_bib,
        pdf_filename=dummy_pdf,
        provider=provider_name,
        model="mock-model",
        save_report=True
    )

    report_path = os.path.join("reports", f"{os.path.splitext(os.path.basename(dummy_pdf))[0]}_report.md")
    assert os.path.exists(report_path)

    with open(report_path) as f:
        contents = f.read()
        assert "MockTool" in contents