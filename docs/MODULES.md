# DidactAI – Module Breakdown

## 1. Student Interface Module
**Responsibility:**
- Handles all user interactions
- Collects input text or topic
- Displays summaries, quizzes, analytics, and certificates

**Inputs:**
- User text / topic
- Quiz responses

**Outputs:**
- Summary views
- Quiz interface
- Performance reports
- Downloadable certificate

---

## 2. Multi-Level Summarization Module
**Responsibility:**
- Converts input text into three learning levels:
  - Basic Summary
  - Detailed Summary
  - Conceptual Summary

**Inputs:**
- Raw input text

**Outputs:**
- Three distinct summaries with different depth and structure

---

## 3. Quiz Generation Module
**Responsibility:**
- Automatically generates quizzes from summaries
- Categorizes questions into three difficulty levels

**Inputs:**
- Summary content
- Extracted keywords and concepts

**Outputs:**
- Beginner, Intermediate, and Advanced quiz questions

---

## 4. Behavioral Integrity Analyzer
**Responsibility:**
- Monitors user behavior during quizzes
- Detects suspicious activity using rule-based logic

**Inputs:**
- User interaction data
- Time and activity logs

**Outputs:**
- Integrity score
- Quiz status (continue / flag / auto-submit)

---

## 5. Analytics & Evaluation Module
**Responsibility:**
- Analyzes quiz performance
- Measures learning improvement

**Inputs:**
- Quiz results
- User interaction data

**Outputs:**
- Accuracy reports
- Learning gain metrics
- Visualization data

---

## 6. Certificate Generation Module
**Responsibility:**
- Issues digital certificates after successful completion

**Inputs:**
- Final quiz results
- User details

**Outputs:**
- Digitally generated certificate with unique ID
