# softwarecitationauditor/tests/test_provider.py

import pytest
from softwarecitationauditor.providers import OpenAIProvider, ClaudeProvider, GeminiProvider, OllamaProvider

class MockClient:
    def chat_completions(self, **kwargs):
        return {"choices": [{"message": {"content": '{"key": "value"}'}}]}

    def create_completion(self, **kwargs):
        return {"choices": [{"message": {"content": '{"key": "value"}'}}]}

    def __call__(self, prompt):
        return {"response": '{"key": "value"}'}

def test_openai_provider_generate():
    provider = OpenAIProvider(model="gpt-4", client=MockClient())
    result = provider.generate("Test prompt")
    assert '"key": "value"' in result

def test_claude_provider_generate():
    provider = ClaudeProvider(model="claude-3-opus", client=MockClient())
    result = provider.generate("Test prompt")
    assert '"key": "value"' in result

def test_gemini_provider_generate():
    provider = GeminiProvider(model="gemini-pro", client=MockClient())
    result = provider.generate("Test prompt")
    assert '"key": "value"' in result

def test_ollama_provider_generate():
    provider = OllamaProvider(model="llama3", client=MockClient())
    result = provider.generate("Test prompt")
    assert '"key": "value"' in result
