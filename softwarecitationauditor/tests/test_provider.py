# softwarecitationauditor/tests/test_provider.py

import os
import pytest
from softwarecitationauditor.providers import OpenAIProvider, ClaudeProvider, GeminiProvider, OllamaProvider


class MockOpenAIClient:
    class chat:
        class completions:
            @staticmethod
            def create(**kwargs):
                class Message:
                    content = '{"key": "value"}'
                class Choice:
                    message = Message()
                class Response:
                    choices = [Choice()]
                return Response()

class MockClaudeClient:
    def post(self, *args, **kwargs):
        class MockResponse:
            def json(self_inner):
                return {"content": [{"text": '{"key": "value"}'}]}
            def raise_for_status(self_inner):
                pass
        return MockResponse()

class MockGeminiClient:
    def generate_content(self, prompt):
        class MockResponse:
            def __iter__(self_inner):
                yield type("MockPart", (), {"text": '{"key": "value"}'})()
        return MockResponse()
    def post(self, url, json=None):
        class Response:
            status_code = 200
            def json(self):
                return {"candidates": [{"content": {"parts": [{"text": '{"key": "value"}'}]}}]}
            def raise_for_status(self):
                pass
        return Response()

class MockOllamaClient:
    def post(self, url, json=None):
        class Response:
            status_code = 200
            def json(self):
                return {"response": '{"key": "value"}'}
        return Response()

def test_openai_provider_generate():
    provider = OpenAIProvider(model="gpt-4", client=MockOpenAIClient())
    result = provider.generate("Test prompt")
    assert '"key": "value"' in result

def test_claude_provider_generate():
    provider = ClaudeProvider(model="claude-3-opus", client=MockClaudeClient())
    result = provider.generate("Test prompt")
    assert '"key": "value"' in result

def test_gemini_provider_generate():
    provider = GeminiProvider(model="gemini-pro", client=MockGeminiClient())
    result = provider.generate("Test prompt")
    assert '"key": "value"' in result

def test_ollama_provider_generate():
    provider = OllamaProvider(model="llama3", client=MockOllamaClient())
    result = provider.generate("Test prompt")
    assert '"key": "value"' in result
