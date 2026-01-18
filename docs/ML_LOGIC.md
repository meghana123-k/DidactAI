# DidactAI – Machine Learning & Logic Design

## 1. Summarization Strategies

### Basic Summary (Extractive)
- Uses TF-IDF / TextRank
- Ranks sentences based on importance
- Selects top-k sentences
- Preserves original wording

Purpose: Quick overview

---

### Detailed Summary (Abstractive)
- Uses pretrained transformer models (T5 / BART)
- Rewrites content into concise explanations
- Controls output length via decoding parameters

Purpose: In-depth understanding

---

### Conceptual Summary
- Performs keyword extraction and Named Entity Recognition
- Uses dependency parsing to identify relationships
- Generates concept-focused explanations

Purpose: Conceptual clarity and reasoning

---

## 2. Quiz Generation Logic
- Extracts key concepts from summaries
- Maps concepts to predefined question templates
- Assigns difficulty levels:
  - Beginner: factual recall
  - Intermediate: conceptual understanding
  - Advanced: analytical reasoning
- Generates distractors to avoid obvious answers

---

## 3. Behavioral Integrity Scoring
- Tracks:
  - Time per question
  - Idle duration
  - Tab switching
  - Rapid answering patterns
- Computes a rule-based suspicion score
- Flags or auto-submits quiz if threshold is exceeded

Note: This module is rule-based with ML-inspired reasoning and is not claimed as deep learning.
