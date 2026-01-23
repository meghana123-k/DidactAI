import requests
import json
import os

OLLAMA_URL = os.getenv("OLLAMA_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
TIMEOUT = 120


def ollama_generate(prompt: str) -> str:
    """
    Sends a prompt to Ollama and returns generated text.
    Safe, blocking, no streaming.
    """

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload,
            timeout=TIMEOUT
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "").strip()

    except Exception as e:
        print("Ollama failed:", e)
        return ""
