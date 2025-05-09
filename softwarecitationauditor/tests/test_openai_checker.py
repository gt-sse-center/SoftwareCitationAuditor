import os
from softwarecitationauditor import openai_checker

class FakeOpenAIClient:
    class chat:
        class completions:
            @staticmethod
            def create(model, messages):
                class FakeMessage:
                    content = "Mocked answer"
                class FakeChoice:
                    message = FakeMessage()
                class FakeResponse:
                    choices = [FakeChoice()]
                return FakeResponse()

def test_extract_and_check_software_mocked():
    os.makedirs("reports", exist_ok=True)
    report_file = "reports/dummy_report.md"
    if os.path.exists(report_file):
        os.remove(report_file)

    openai_checker.extract_and_check_software(
        "body text", "bibliography text", "dummy.pdf",
        "openai", "gpt-3.5-turbo",
        client=FakeOpenAIClient()
    )

    assert os.path.exists(report_file)