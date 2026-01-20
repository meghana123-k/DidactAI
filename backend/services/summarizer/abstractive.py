import os
import json
from typing import Optional

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# ---------- OpenAI Client ----------
openai_client: Optional[OpenAI] = None
if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)


# ---------- Gemini Client ----------
gemini_client = None
if GEMINI_API_KEY:
    try:
        from google import genai
        gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception:
        gemini_client = None


# ---------- Prompt Templates ----------
PROMPTS = {
    "basic": (
        "Explain the following content like teaching a child. "
        "Use very simple words, short sentences, and intuitive examples. "
        "Avoid technical jargon unless clearly explained."
    ),
    "detailed": (
        "Explain the content clearly and in detail.Cover ALL major concepts present.If multiple techniques or approaches are discussed, explain EACH of them and compare them where relevant.Do not ignore any important concept."
    ),
    "overview": (
        "Explain the following content at a conceptual, high level. "
        "Start from general ideas and explain how the concepts relate to each other. "
        "Focus on the big picture."
    )
}


# ---------- OpenAI Explanation ----------
def _explain_openai(text: str, mode: str) -> str:
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": PROMPTS[mode]},
            {"role": "user", "content": text}
        ],
        temperature=0,
        max_tokens=400
    )

    return response.choices[0].message.content.strip()


# ---------- Gemini Explanation ----------
def _explain_gemini(text: str, mode: str) -> str:
    prompt = PROMPTS[mode] + "\n\n" + text

    response = gemini_client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    return response.text.strip()


# ---------- Public API ----------
def explain(text: str, mode: str) -> str:
    """
    Central LLM explanation gateway.

    mode ∈ {"basic", "detailed", "overview"}
    """

    if not text or not text.strip():
        return ""

    if mode not in PROMPTS:
        raise ValueError(f"Invalid mode: {mode}")

    # 1️⃣ Try OpenAI first
    if openai_client:
        try:
            return _explain_openai(text, mode)
        except Exception as e:
            print("OpenAI failed:", e)

    # 2️⃣ Fallback to Gemini
    if gemini_client:
        try:
            return _explain_gemini(text, mode)
        except Exception as e:
            print("Gemini failed:", e)

    # 3️⃣ Final graceful fallback (no fake AI)
    sentences = text.split(".")
    return ". ".join(sentences[:3]).strip() + "..."
