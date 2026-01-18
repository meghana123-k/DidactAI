# DidactAI – Technology Stack & Justification

## System Overview
DidactAI is built using a client–server architecture where the frontend is responsible for
user interaction, the backend acts as a central API and AI orchestrator, and dedicated NLP
modules perform summarization, assessment, and analytics tasks.

Each technology is selected based on its suitability for modular design, explainability,
and academic evaluation.

---

## Frontend Technology

### React (Frontend UI)
React is used to build the frontend due to its component-based architecture, which aligns
well with the modular structure of DidactAI.

Justification:
- Separate components for summaries, quizzes, analytics, and certificates
- Efficient state management for quiz progression and user interaction
- Seamless REST API integration with the backend
- Dynamic rendering of analytics dashboards and certificates

React enables a responsive and maintainable user interface without embedding business logic.

---

## Backend Technology

### Flask (Backend API & AI Orchestrator)
Flask is used as a lightweight backend framework that functions as an API orchestration
layer rather than a monolithic application.

Justification:
- Acts as a central controller coordinating all AI modules
- Provides RESTful APIs for frontend communication
- Minimal overhead, suitable for AI-driven workflows
- Allows fine-grained control over request routing and data flow

Flask is preferred over heavier frameworks because the backend’s primary role is orchestration,
not server-side rendering or complex authentication workflows.

---

## NLP & Machine Learning Stack

### NLP Libraries
- HuggingFace Transformers
- spaCy
- scikit-learn
- NLTK

Justification:
- HuggingFace Transformers provide access to pretrained transformer-based models for
  abstractive summarization
- spaCy is used for Named Entity Recognition and dependency parsing to support conceptual
  understanding
- scikit-learn supports traditional NLP techniques such as TF-IDF
- NLTK assists in text preprocessing tasks like tokenization and stopword removal

---

### Summarization Models

#### Abstractive Summarization (T5 / BART)
Transformer-based sequence-to-sequence models are used for abstractive summarization.

Justification:
- Capable of generating human-like rewritten summaries
- Preserve semantic meaning rather than extracting raw sentences
- Suitable for generating detailed explanations

---

#### Extractive Summarization (TF-IDF / TextRank)
Traditional extractive methods are used for basic summaries.

Justification:
- Computationally efficient
- Highly explainable
- Preserve original wording of key sentences
- Suitable for quick overview summaries

---

### Conceptual Understanding
spaCy-based Named Entity Recognition and dependency parsing are used to identify key concepts
and relationships within the text, enabling conceptual-level summaries.

---

## Database Technology

### MongoDB (Database Layer)
MongoDB is used as the primary database for DidactAI.

Justification:
- Stores semi-structured and unstructured AI-generated data efficiently
- Flexible schema supports variable-length summaries and analytics
- Well-suited for document-based data such as quizzes and certificates
- Simplifies iteration during experimentation and development

---

## Analytics & Visualization

### Chart.js / Recharts
These libraries are used to visualize learning analytics.

Justification:
- Lightweight and easy integration with React
- Effective for rendering performance trends and accuracy graphs
- Supports dynamic data updates

---

## Development & Experimentation Tools

- GitHub: Version control and collaboration
- Jupyter Notebook: Model experimentation, preprocessing, and evaluation
- VS Code / Cursor: Development environment

---

## Summary
The selected technology stack supports modularity, explainability, and scalability while
remaining appropriate for an academic major project. Each component aligns with the
functional and architectural requirements of DidactAI.
