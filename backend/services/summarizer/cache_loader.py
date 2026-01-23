import json
import os

INDEX_FILE = "backend/data/index.json"


def load_cached_document(doc_id: str):
    if not doc_id or not os.path.exists(INDEX_FILE):
        return None

    with open(INDEX_FILE, "r") as f:
        index = json.load(f)

    entry = index.get(doc_id)
    if not entry:
        return None

    processed_path = entry.get("processed_path")
    if not processed_path or not os.path.exists(processed_path):
        return None

    with open(processed_path, "r") as f:
        return json.load(f)
