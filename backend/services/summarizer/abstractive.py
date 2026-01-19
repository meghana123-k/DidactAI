from transformers import pipeline
import nltk
from typing import List

nltk.download("punkt", quiet=True)
from nltk.tokenize import sent_tokenize


class AbstractiveSummarizer:
    """
    Abstractive summarization using transformer-based models (BART/T5)
    with hierarchical summarization for long documents.
    """

    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        self.summarizer = pipeline(
            "summarization",
            model=model_name,
            tokenizer=model_name
        )
        self.max_sentences_per_chunk = 10
        self.min_length = 60
        self.max_length = 150

    def _chunk_text(self, text: str) -> List[str]:
        """Split text into sentence-based chunks."""
        sentences = sent_tokenize(text)
        chunks = []

        for i in range(0, len(sentences), self.max_sentences_per_chunk):
            chunk = " ".join(sentences[i:i + self.max_sentences_per_chunk])
            if chunk.strip():
                chunks.append(chunk)

        return chunks

    def _summarize(self, text: str) -> str:
        """Summarize a given text chunk."""
        input_length = len(text.split())

        max_len = min(self.max_length, max(30, input_length))
        min_len = min(self.min_length, max(10, input_length // 2))

        summary = self.summarizer(
            text,
            max_length=max_len,
            min_length=min_len,
            do_sample=False
        )


        return summary[0]["summary_text"]

    def summarize(self, text: str) -> str:
        """
        Generate a coherent abstractive summary for long documents.
        """

        if not text or not text.strip():
            return ""

        chunks = self._chunk_text(text)

        if not chunks:
            return ""

        # Summarize each chunk
        chunk_summaries = [self._summarize(chunk) for chunk in chunks]

        # Merge summaries and summarize again for coherence
        merged_summary = " ".join(chunk_summaries)

        final_summary = self._summarize(merged_summary)

        return final_summary
