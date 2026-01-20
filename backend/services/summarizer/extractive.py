import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Ensure sentence tokenizer is available
nltk.download('punkt', quiet=True)
from nltk.tokenize import sent_tokenize


def extractive_summary(text: str, ratio: float = 0.3) -> str:
    """
    Generates an extractive summary using TF-IDF sentence scoring.

    Args:
        text (str): Input text to summarize
        ratio (float): Proportion of sentences to include in the summary

    Returns:
        str: Extractive summary text
    """

    if not text or not text.strip():
        return ""

    # Step 1: Sentence segmentation (NLP-safe)
    sentences = sent_tokenize(text)

    # Step 2: Filter very short or non-informative sentences (word-based)
    clean_sentences = [
        sent.strip() for sent in sentences if len(sent.split()) >= 5
    ]

    if not clean_sentences:
        return ""

    # Step 3: TF-IDF vectorization (sentence-level)
    # Handle very short texts safely
    if len(clean_sentences) < 3:
        return " ".join(clean_sentences)

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(clean_sentences)

    # Step 4: Sentence scoring using mean TF-IDF
    sentence_scores = np.asarray(tfidf_matrix.mean(axis=1)).ravel()

    # Step 5: Rank sentences by importance
    ranked_indices = np.argsort(sentence_scores)[::-1]

    # Step 6: Select top-ranked sentences
    num_sentences = max(1, int(len(clean_sentences) * ratio))
    selected_indices = sorted(ranked_indices[:num_sentences])

    # Step 7: Preserve original order
    summary = " ".join(clean_sentences[i] for i in selected_indices)

    return summary
