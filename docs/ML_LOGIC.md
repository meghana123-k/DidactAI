# DidactAI – Machine Learning & Logic Design

## 1. Summarization Strategies

### Basic Summary (Extractive)
- Uses TF-IDF / TextRank
- Ranks sentences based on importance
- Selects top-k sentences
- Preserves original wording

Purpose: Quick overview

The extractive summarization module generates a basic overview by selecting the most
informative sentences directly from the original text.

### Methodology
1. The input text is segmented into sentences using an NLP-based tokenizer.
2. Very short or non-informative sentences are filtered using word-count thresholds.
3. Each sentence is treated as an individual document and represented using TF-IDF vectors.
4. Sentence importance is computed using the mean TF-IDF score.
5. Sentences are ranked by importance and a fixed proportion is selected.
6. The selected sentences are reordered to preserve the original document flow.

### Rationale
TF-IDF is chosen for extractive summarization due to its explainability and efficiency.
Using mean TF-IDF prevents bias toward longer sentences while maintaining relevance.
Preserving sentence order ensures coherence and readability in the final summary.

---

### Detailed Summary (Abstractive)
- Uses pretrained transformer models (T5 / BART)
- Rewrites content into concise explanations
- Controls output length via decoding parameters

Purpose: In-depth understanding


The abstractive summarization module generates rewritten summaries that preserve the
semantic meaning of the original text.

### Methodology
1. The input text is segmented into sentence-based chunks to respect transformer
   context-length constraints.
2. Each chunk is summarized independently using a pretrained transformer-based
   sequence-to-sequence model.
3. The intermediate summaries are merged and summarized again to ensure coherence
   across the entire document.
4. Summary length is controlled using deterministic decoding parameters.

### Rationale
Transformer-based models such as T5 and BART are capable of generating fluent and
context-aware summaries. Hierarchical summarization ensures scalability to long
documents while maintaining readability and coherence.


---

### Conceptual Summary
- Performs keyword extraction and Named Entity Recognition
- Uses dependency parsing to identify relationships
- Generates concept-focused explanations

Purpose: Conceptual clarity and reasoning


The conceptual summarization module focuses on extracting key concepts
and their relationships rather than generating rewritten text.
Concept normalization and filtering are applied to reduce noise and ensure that extracted concepts are meaningful and relevant.
### Methodology
1. The input text is processed using spaCy for Named Entity Recognition
   and dependency parsing.
2. Important concepts are identified using named entities and frequent
   noun phrases.
3. Concepts are ranked based on frequency and relevance.
4. Simple subject–verb–object relationships are extracted to capture
   conceptual connections.
5. Structured explanations are generated to support conceptual clarity.

### Rationale
Unlike abstractive summarization, conceptual summarization emphasizes
understanding relationships and core ideas, enabling learners to grasp
the underlying structure of the topic.

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
