import os
from typing import Optional, Dict
from dotenv import load_dotenv
from openai import OpenAI

from services.llm.ollama_client import ollama_generate

load_dotenv()

# ============================================================
# LLM POLICY — SUMMARIZER
#
# 1️⃣ Ollama  (local / offline / dev)
# 2️⃣ GPT     (cloud primary)
# 3️⃣ Gemini  (cloud fallback)
# 4️⃣ Extract (deterministic fallback)
# ============================================================

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

openai_client: Optional[OpenAI] = None
if OPENAI_API_KEY:
    openai_client = OpenAI(api_key=OPENAI_API_KEY)

gemini_client = None
if GEMINI_API_KEY:
    try:
        from google import genai
        gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception:
        gemini_client = None


# ============================================================
# PROMPTS
# ============================================================

PROMPTS = {
    "basic": "Explain like teaching a child. Use simple words and examples.",
    "detailed": (
        "Explain clearly and in detail. Cover ALL major concepts. "
        "Do not ignore any important idea."
    ),
    "overview": (
        "Explain at a high conceptual level. Start from general ideas "
        "and show how concepts relate."
    ),
}


def _format_prompt(text: str, mode: str) -> str:
    return f"""
{PROMPTS[mode]}

CONTENT:
{text}

RULES:
- Stay concise
- Do not hallucinate
- Follow the instruction strictly
"""


# ============================================================
# EXPLAIN (SINGLE SOURCE OF TRUTH)
# ============================================================

def explain(text: str, mode: str) -> Dict:
    if not text or not text.strip():
        return {"text": "", "source": "none", "confidence": "low"}

    prompt = _format_prompt(text, mode)

    # 1️⃣ OLLAMA — LOCAL FIRST
    ollama_output = ollama_generate(prompt)
    if ollama_output:
        return {
            "text": ollama_output,
            "source": "ollama",
            "confidence": "medium"
        }

    # 2️⃣ GPT — CLOUD PRIMARY
    if openai_client:
        try:
            return {
                "text": _explain_openai(text, mode),
                "source": "gpt",
                "confidence": "high"
            }
        except Exception as e:
            print("GPT failed:", e)

    # 3️⃣ GEMINI — CLOUD FALLBACK
    if gemini_client:
        try:
            return {
                "text": _explain_gemini(text, mode),
                "source": "gemini",
                "confidence": "medium"
            }
        except Exception as e:
            print("Gemini failed:", e)

    # 4️⃣ FINAL DETERMINISTIC FALLBACK
    sentences = text.split(".")
    return {
        "text": ". ".join(sentences[:3]).strip() + "...",
        "source": "fallback",
        "confidence": "low"
    }


# ============================================================
# PROVIDER-SPECIFIC HELPERS
# ============================================================

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


def _explain_gemini(text: str, mode: str) -> str:
    prompt = PROMPTS[mode] + "\n\n" + text
    response = gemini_client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )
    return response.text.strip()
