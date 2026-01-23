import os
import json
from datetime import datetime

from utils.text_preprocessing import extract_text_from_input
from services.summarizer.abstractive import explain
from services.summarizer.conceptual import get_conceptual_summary

RAW_DIR = "backend/data/raw"
PROCESSED_DIR = "backend/data/processed"
INDEX_FILE = "backend/data/index.json"

os.makedirs(PROCESSED_DIR, exist_ok=True)


def load_index():
    if not os.path.exists(INDEX_FILE):
        return {}
    with open(INDEX_FILE, "r") as f:
        return json.load(f)


def save_index(index):
    with open(INDEX_FILE, "w") as f:
        json.dump(index, f, indent=2)


def preprocess_file(filename, index):
    doc_id = os.path.splitext(filename)[0]
    raw_path = os.path.join(RAW_DIR, filename)
    processed_path = os.path.join(PROCESSED_DIR, f"{doc_id}.json")

    print(f"Processing: {filename}")

    # 1️⃣ Extract text
    text = extract_text_from_input(text=None, file=open(raw_path, "rb"))
    if not text:
        print(f"Skipping empty file: {filename}")
        return

    # 2️⃣ Summaries
    basic = explain(text, mode="basic")
    detailed = explain(text, mode="detailed")

    concept_data = get_conceptual_summary(text)
    concepts = concept_data.get("key_concepts", [])

    overview_input = "Key concepts:\n" + "\n".join(f"- {c}" for c in concepts)
    overview = explain(overview_input, mode="overview")

    # 3️⃣ Build processed object
    processed = {
        "doc_id": doc_id,
        "source_file": filename,
        "summaries": {
            "basic": basic,
            "detailed": detailed,
            "overview": overview
        },
        "concepts": {
            "list": concepts,
            "source": concept_data.get("source"),
            "confidence": concept_data.get("confidence")
        },
        "metadata": {
            "preprocessed": True,
            "created_at": datetime.utcnow().isoformat()
        }
    }

    # 4️⃣ Save processed output
    with open(processed_path, "w") as f:
        json.dump(processed, f, indent=2)

    # 5️⃣ Update index
    index[doc_id] = {
        "raw_path": raw_path,
        "processed_path": processed_path
    }


def run():
    index = load_index()

    for file in os.listdir(RAW_DIR):
        if file.lower().endswith((".pdf", ".txt", ".docx")):
            if os.path.splitext(file)[0] not in index:
                preprocess_file(file, index)

    save_index(index)
    print("Preprocessing complete.")


if __name__ == "__main__":
    run()
