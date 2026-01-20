from transformers import pipeline
import nltk

nltk.download("punkt", quiet=True)
from nltk.tokenize import sent_tokenize


class AbstractiveSummarizer:
    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        self.summarizer = pipeline(
            "summarization",
            model=model_name,
            tokenizer=model_name
        )
        self.max_length = 150
        self.min_length = 60
        self.max_sentences_per_chunk = 10

    def _chunk_text(self, text):
        sentences = sent_tokenize(text)
        chunks = []

        for i in range(0, len(sentences), self.max_sentences_per_chunk):
            chunk = " ".join(sentences[i:i + self.max_sentences_per_chunk])
            if chunk.strip():
                chunks.append(chunk)

        return chunks

    def _summarize_chunk(self, text):
        word_count = len(text.split())

        if word_count < 50:
            return text.strip()

        max_len = min(self.max_length, int(word_count * 0.8))
        min_len = min(self.min_length, int(word_count * 0.4))

        result = self.summarizer(
            text,
            max_length=max_len,
            min_length=min_len,
            do_sample=False,
            truncation=True
        )

        return result[0]["summary_text"].strip()

    def summarize(self, text: str) -> str:
        if not text or not text.strip():
            return ""

        chunks = self._chunk_text(text)

        summaries = [self._summarize_chunk(c) for c in chunks]

        merged = " ".join(summaries)

        return self._summarize_chunk(merged)
