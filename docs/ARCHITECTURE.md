# DidactAI – System Architecture

## Architecture Overview
DidactAI follows a modular client–server architecture where the frontend communicates
with a Flask-based backend that integrates multiple AI-driven components.

---

## Components
- Frontend (React): User interaction and visualization
- Backend (Flask): API handling and business logic
- AI Engine: NLP processing and analytics
- Database: Persistent storage

---

## Data Flow
1. User submits text via frontend
2. Backend forwards text to Summarization Module
3. Summaries are generated and stored
4. Quiz Generator creates questions from summaries
5. User attempts quiz while Integrity Analyzer tracks behavior
6. Results are analyzed by Analytics Module
7. Certificate is generated if criteria are met

---

## API Interactions
- `/summarize` → Generates multi-level summaries
- `/generate-quiz` → Creates quizzes
- `/submit-quiz` → Stores responses and triggers evaluation
- `/analytics` → Returns performance metrics
- `/certificate` → Generates and downloads certificate

---

## Design Principles
- Modular separation of concerns
- Explainable AI logic
- Scalable and maintainable architecture
