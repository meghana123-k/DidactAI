import os
import json
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
def _get_concepts_openai(text: str) -> List[str]:
    from openai import OpenAI

    client = OpenAI(api_key=OPENAI_API_KEY)

    prompt = f"""
Extract ONLY important domain concepts explicitly present in the text.

STRICT RULES:
- Copy phrases exactly as they appear in the text
- Do NOT add external knowledge
- Do NOT explain
- Do NOT include generic words (data, system, process, thing)
- Output ONLY valid JSON

Format:
{{ "key_concepts": [] }}

Text:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=150
    )

    content = response.choices[0].message.content.strip()
    return json.loads(content)["key_concepts"]
def _get_concepts_gemini(text: str) -> List[str]:
    from google import genai

    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = f"""
Extract domain-specific concepts explicitly mentioned in the text.

Rules:
- Preserve full phrases
- No explanations
- No generic words
- Output STRICT JSON only

Format:
{{ "key_concepts": [] }}

Text:
{text}
"""

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    data = json.loads(response.text)
    return data["key_concepts"]
def _get_concepts_spacy(text: str) -> List[str]:
    import spacy

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    concepts = set()

    for chunk in doc.noun_chunks:
        if len(chunk.text.split()) > 1:
            concepts.add(chunk.text.lower())

    return list(concepts)
def get_conceptual_summary(text: str) -> Dict:
    if not text or not text.strip():
        return {"key_concepts": [], "source": "none", "confidence": "low"}

    # 1️⃣ GEMINI — PRIMARY
    if GEMINI_API_KEY:
        try:
            concepts = _get_concepts_gemini(text)
            if concepts:
                return {
                    "key_concepts": concepts,
                    "source": "gemini",
                    "confidence": "high"
                }
        except Exception as e:
            print("Gemini concept extraction failed:", e)

    # 2️⃣ OPENAI — SECONDARY
    if OPENAI_API_KEY:
        try:
            concepts = _get_concepts_openai(text)
            if concepts:
                return {
                    "key_concepts": concepts,
                    "source": "openai",
                    "confidence": "high"
                }
        except Exception as e:
            print("OpenAI concept extraction failed:", e)

    # 3️⃣ SPACY — FINAL FALLBACK
    try:
        concepts = _get_concepts_spacy(text)
        return {
            "key_concepts": concepts[:10],
            "source": "spacy",
            "confidence": "low"
        }
    except Exception as e:
        print("spaCy concept extraction failed:", e)

    return {"key_concepts": [], "source": "none", "confidence": "low"}
