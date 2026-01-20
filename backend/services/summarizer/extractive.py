import nltk
import numpy as np
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer

# Ensure tokenizer is available
nltk.download("punkt", quiet=True)
from nltk.tokenize import sent_tokenize
def extractive_summary(text: str, ratio: float = 0.35) -> str:
    """
    Performs extractive summarization using TF-IDF sentence scoring.

    Args:
        text (str): Input text
        ratio (float): Proportion of sentences to keep (0.1 – 0.5 recommended)

    Returns:
        str: Extracted important sentences in original order
    """

    if not text or not text.strip():
        return ""

    # Step 1: Sentence segmentation
    sentences: List[str] = sent_tokenize(text)

    # Step 2: Filter very short / non-informative sentences
    clean_sentences = [
        s.strip() for s in sentences if len(s.split()) >= 5
    ]

    if not clean_sentences:
        return ""

    # If text is already short, return as-is
    if len(clean_sentences) <= 3:
        return " ".join(clean_sentences)

    # Clamp ratio safely
    ratio = min(max(ratio, 0.1), 0.5)

    # Step 3: TF-IDF vectorization (sentence-level)
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(clean_sentences)

    # Step 4: Sentence scoring (length-normalized)
    sentence_scores = np.asarray(tfidf_matrix.sum(axis=1)).ravel()
    sentence_lengths = np.array([len(s.split()) for s in clean_sentences])

    # Normalize to avoid bias toward long sentences
    sentence_scores = sentence_scores / np.sqrt(sentence_lengths)

    # Step 5: Rank sentences by importance
    ranked_indices = np.argsort(sentence_scores)[::-1]

    # Step 6: Select top-ranked sentences
    num_sentences = max(1, int(len(clean_sentences) * ratio))
    selected_indices = sorted(ranked_indices[:num_sentences])

    # Step 7: Preserve original order
    summary_sentences = [clean_sentences[i] for i in selected_indices]

    return " ".join(summary_sentences)
