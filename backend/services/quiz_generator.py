import os
import random
from typing import List, Dict
from dotenv import load_dotenv
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

from openai import OpenAI

load_dotenv()

nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

STOPWORDS = set(stopwords.words("english"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_keywords(text: str, max_keywords: int = 8) -> List[str]:
    words = word_tokenize(text.lower())
    candidates = [
        w for w in words
        if w.isalpha() and w not in STOPWORDS and len(w) > 3
    ]

    freq = {}
    for w in candidates:
        freq[w] = freq.get(w, 0) + 1

    return sorted(freq, key=freq.get, reverse=True)[:max_keywords]
def llm_generate_mcq(concept: str, difficulty: str, context: str) -> Dict:
    """
    LLM generates phrasing + distractors.
    Correct answer is ALWAYS the concept itself.
    """

    prompt = f"""
Create ONE multiple-choice question.

CONSTRAINTS:
- Topic: {concept}
- Difficulty: {difficulty}
- Context is for understanding ONLY
- One correct answer must be: "{concept}"
- Generate 3 plausible distractors
- Output STRICT JSON only

Format:
{{
  "question": "",
  "options": ["{concept}", "distractor1", "distractor2", "distractor3"],
  "answer": "{concept}"
}}

Context:
{context}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=200
    )

    return eval(response.choices[0].message.content)
def generate_beginner_questions(text: str, num_questions: int = 3) -> List[Dict]:
    keywords = extract_keywords(text)
    questions = []

    for concept in keywords[:num_questions]:
        mcq = llm_generate_mcq(concept, "beginner", text)
        mcq["difficulty"] = "beginner"
        questions.append(mcq)

    return questions
def generate_intermediate_questions(text: str, num_questions: int = 3) -> List[Dict]:
    keywords = extract_keywords(text)
    questions = []

    for concept in keywords[:num_questions]:
        mcq = llm_generate_mcq(concept, "intermediate", text)
        mcq["difficulty"] = "intermediate"
        questions.append(mcq)

    return questions
def generate_advanced_questions(text: str, num_questions: int = 2) -> List[Dict]:
    keywords = extract_keywords(text)
    questions = []

    for concept in keywords[:num_questions]:
        mcq = llm_generate_mcq(concept, "advanced", text)
        mcq["difficulty"] = "advanced"
        questions.append(mcq)

    return questions
def generate_quiz(text: str) -> Dict:
    """
    Generates a quiz with three difficulty levels.
    """

    return {
        "beginner": generate_beginner_questions(text),
        "intermediate": generate_intermediate_questions(text),
        "advanced": generate_advanced_questions(text)
    }
