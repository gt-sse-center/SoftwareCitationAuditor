import os
from softwarecitationauditor import openai_checker

def test_extract_and_check_software_mocked(monkeypatch):
    def fake_create(*args, **kwargs):
        class FakeMessage:
            content = "Mocked answer"
        class FakeChoice:
            message = FakeMessage()
        class FakeResponse:
            choices = [FakeChoice()]
        return FakeResponse()

    monkeypatch.setattr(openai_checker.client.chat.completions, "create", fake_create)

    openai_checker.extract_and_check_software("body text", "bibliography text")
    assert os.path.exists("report.md")