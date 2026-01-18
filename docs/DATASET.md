# Dataset Description – DidactAI

## 1. Dataset Overview
The dataset is used to evaluate the effectiveness of the DidactAI system in generating
multi-level summaries, quizzes, and learning analytics.

The dataset consists of educational and informational documents covering multiple domains
such as computer science, science, mathematics, economics, history, and civics. Each document
represents a single topic and contains sufficient content to test summarization depth and
concept extraction.

- Number of documents: 19
- Minimum length: ~1000 words
- Maximum length: ~3000 words
- Content type: Educational and conceptual topics

---

## 2. Data Sources
The dataset content is collected from publicly available educational resources such as:
- Open educational PDFs
- Academic notes and study material
- Informational documents intended for learning purposes

The dataset is **not user-generated** and is used only for system evaluation and testing.
User-provided input is processed dynamically at runtime and is not part of the stored dataset.

---

## 3. Data Format
The raw dataset is stored in document formats and later converted into plain text for
processing.

- Raw formats: `.pdf`, `.docx`
- Processed format: `.txt`

Each document corresponds to one topic and is stored as a separate file.

---

## 4. Preprocessing Steps
Before processing, all documents undergo the following preprocessing steps:

1. Lowercasing – to ensure uniform text representation  
2. Removal of special characters and unnecessary symbols  
3. Sentence segmentation – to support extractive summarization  
4. Tokenization – to split text into words and sentences  
5. Stopword handling – selectively applied to extractive summarization tasks  
6. Lemmatization – to normalize words to their base forms  

Stopwords are **not aggressively removed** for abstractive summarization, as transformer-based
models rely on sentence structure and context.

---

## 5. Dataset Usage

### Summarization
- Raw text is provided as input to the extractive and abstractive summarization modules
- Extractive methods use preprocessed text
- Abstractive models operate on minimally processed text

### Quiz Generation
- Concepts and keywords extracted from summaries are used to generate quiz questions
- The dataset helps evaluate question relevance and difficulty levels

### Evaluation
- The dataset is used for qualitative and quantitative evaluation of summaries
- Metrics such as ROUGE scores and readability comparisons are computed

Since pretrained models are used, the dataset is intended for evaluation and experimentation
rather than training or fine-tuning.
