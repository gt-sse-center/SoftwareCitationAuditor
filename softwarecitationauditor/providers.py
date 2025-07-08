import os
import json
import logging
from abc import ABC, abstractmethod

from openai import OpenAI as OpenAIClient
from openai import AuthenticationError as OpenAIAuthError
import requests

logger = logging.getLogger(__name__)

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass


class OpenAIProvider(LLMProvider):
    def __init__(self, model, client=None):
        self.client = client or OpenAIClient()
        self.model = model

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
            )
            return response.choices[0].message.content.strip()
        except OpenAIAuthError as e:
            logger.error(f"❌ OpenAI authentication failed: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ OpenAI request failed: {e}")
            raise


class ClaudeProvider(LLMProvider):
    def __init__(self, model, client=None):
        self.model = model
        self.client = client or requests.Session()
        self.api_url = "https://api.anthropic.com/v1/messages"

    def generate(self, prompt: str) -> str:
        headers = {
            "x-api-key": os.environ.get("CLAUDE_API_KEY", ""),
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        data = {
            "model": self.model,
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}]
        }
        response = self.client.post(self.api_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["content"][0]["text"].strip()


class GeminiProvider(LLMProvider):
    def __init__(self, model, client=None):
        self.model = model
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
        self.client = client or requests.Session()

    def generate(self, prompt: str) -> str:
        api_key = os.environ.get("GEMINI_API_KEY", "")
        data = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        response = self.client.post(f"{self.api_url}?key={api_key}", json=data)
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()


class OllamaProvider(LLMProvider):
    def __init__(self, model, client=None):
        self.model = model
        self.client = client or requests.Session()
        self.api_url = "http://localhost:11434/api/generate"

    def generate(self, prompt: str) -> str:
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        response = self.client.post(self.api_url, json=data)
        if response.status_code != 200:
            raise RuntimeError(f"Ollama REST call failed: {response.text} (status code: {response.status_code})")
        return response.json()["response"].strip()