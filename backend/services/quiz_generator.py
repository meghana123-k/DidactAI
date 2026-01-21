import os
import json
import random
import re
from typing import List, Dict, Tuple
from dotenv import load_dotenv

# ---------- LLM CLIENTS ----------
from openai import OpenAI          # Used for Groq (OpenAI-compatible)
from mistralai import Mistral      # Secondary fallback

load_dotenv()

# Groq (PRIMARY)
groq_client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# Mistral (SECONDARY)
mistral_client = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY")
)

# ---------- SHARED CLEANING ----------
GENERIC_TERMS = {
    "programming", "software", "system",
    "process", "method", "concept", "idea", "approach"
}

def clean_concepts(concepts: List[str]) -> List[str]:
    """Final deterministic sanitation."""
    cleaned = []
    for c in concepts:
        c = c.strip()
        if not (1 <= len(c.split()) <= 3):
            continue
        if c.lower() in GENERIC_TERMS:
            continue
        cleaned.append(c)
    return list(dict.fromkeys(cleaned))


# ---------- CONCEPT EXTRACTION (PRIMARY: GROQ) ----------
def extract_concepts_groq(summary: str) -> List[str]:
    prompt = f"""
Extract academic concepts for assessment generation.

STRICT RULES:
- ONLY concepts explicitly present in the text
- Canonical textbook terms only
- 1–3 words per concept
- No generic terms (programming, system, process)
- No definitions or verb phrases
- No fragments
- Output STRICT JSON only

Format:
{{ "concepts": [] }}

Text:
{summary}
"""
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        response_format={"type": "json_object"}
    )

    data = json.loads(response.choices[0].message.content)
    return data.get("concepts", [])


# ---------- CONCEPT EXTRACTION (SECONDARY: MISTRAL) ----------
def extract_concepts_mistral(summary: str) -> List[str]:
    prompt = f"""
Extract academic concepts for assessment generation.

Rules:
- Concepts must appear in text
- Canonical textbook terms
- 1–3 words
- No generic terms
- JSON ONLY

Format:
{{ "concepts": [] }}

Text:
{summary}
"""
    response = mistral_client.chat.complete(
        model="mistral-small-latest",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    data = json.loads(response.choices[0].message.content)
    return data.get("concepts", [])


# ---------- FINAL FALLBACK (DETERMINISTIC, TEXT-ONLY) ----------
def extract_noun_phrases(summary: str) -> List[str]:
    """
    Last-resort extraction: multi-word capitalized phrases.
    NO invention.
    """
    phrases = re.findall(
        r'\b[A-Z][a-z]+(?:[-\s][A-Z][a-z]+){1,2}\b',
        summary
    )
    return list(dict.fromkeys(phrases))


# ---------- ADAPTIVE CONCEPT EXTRACTION ----------
def get_concepts_adaptive(summary: str, max_concepts: int = 8) -> List[str]:
    """
    Provider-agnostic, resilient extraction.
    """
    extractors = [
        extract_concepts_groq,
        extract_concepts_mistral
    ]

    for extractor in extractors:
        try:
            concepts = extractor(summary)
            concepts = clean_concepts(concepts)
            if len(concepts) >= 3:
                return concepts[:max_concepts]
        except Exception as e:
            print(f"[Extractor failed: {extractor.__name__}] {e}")

    # FINAL fallback
    concepts = clean_concepts(extract_noun_phrases(summary))
    return concepts[:max_concepts]

QUESTIONS_PER_LEVEL = 5
LEVELS = 3
# ---------- PARTITIONING ----------
def partition_concepts(
    
    concepts: List[str],
    per_level: int = QUESTIONS_PER_LEVEL
) -> Tuple[List[str], List[str], List[str]]:
    """
    Partition concepts into 3 levels (beginner, intermediate, advanced).

    - If concepts >= required → no reuse
    - If concepts < required → deterministic cyclic reuse
    """

    if not concepts:
        return [], [], []

    n = len(concepts)
    total_needed = per_level * LEVELS  # 15

    # Case 1: Enough unique concepts (no reuse)
    if n >= total_needed:
        return (
            concepts[:per_level],
            concepts[per_level:2 * per_level],
            concepts[2 * per_level:3 * per_level],
        )

    # Case 2: Deterministic cyclic reuse
    def take(start_index: int) -> List[str]:
        return [
            concepts[(start_index + i) % n]
            for i in range(per_level)
        ]

    return (
        take(0),              # beginner
        take(per_level),      # intermediate
        take(2 * per_level),  # advanced
    )


# ---------- MCQ GENERATION (GROQ) ----------
def llm_generate_mcq(concept: str, difficulty: str, summary: str) -> Dict:
    difficulty_focus = {
        "beginner": "definition or recognition",
        "intermediate": "usage or relationship",
        "advanced": "edge case or limitation"
    }

    prompt = f"""
You are an expert educator writing MCQs.

Rules:
- Topic MUST be exactly: {concept}
- Difficulty: {difficulty} ({difficulty_focus[difficulty]})
- Correct answer MUST be exactly "{concept}"
- 3 plausible distractors
- Same grammatical form
- JSON ONLY

Format:
{{"question":"","options":["{concept}","d1","d2","d3"],"answer":"{concept}"}}

Context:
{summary[:800]}
"""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.25,
            response_format={"type": "json_object"}
        )

        mcq = json.loads(response.choices[0].message.content)

        if mcq.get("answer") != concept:
            raise ValueError("Answer mismatch")

        random.shuffle(mcq["options"])
        mcq["difficulty"] = difficulty
        mcq["answer"] = concept
        return mcq

    except Exception as e:
        print(f"[MCQ FALLBACK] {concept} → {e}")
        opts = [concept, "Option A", "Option B", "Option C"]
        random.shuffle(opts)
        return {
            "question": f"What best describes {concept}?",
            "options": opts,
            "answer": concept,
            "difficulty": difficulty
        }


# ---------- PUBLIC API ----------
def generate_quiz_from_summary(summary: str, mode: str = "conceptual") -> Dict:
    """
    INPUT: summary text (basic / detailed / conceptual)
    OUTPUT: quiz aligned to summary
    """
    concepts = get_concepts_adaptive(summary)
    b, i, a = partition_concepts(concepts)

    quiz = {
        "beginner": [llm_generate_mcq(c, "beginner", summary) for c in b],
        "intermediate": [llm_generate_mcq(c, "intermediate", summary) for c in i],
        "advanced": [llm_generate_mcq(c, "advanced", summary) for c in a]
    }

    return {
        "quiz": quiz,
        "meta": {
            "source": "summary",
            "mode": mode,
            "concepts": concepts,
            "n_concepts": len(concepts),
            "llm_primary": "groq",
            "llm_fallback": "mistral"
        }
    }
