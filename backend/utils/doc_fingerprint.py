import hashlib

def generate_doc_id(text: str) -> str:
    """
    Generates a stable document fingerprint from content.

    Same text → same doc_id
    Different text → different doc_id
    """
    normalized = " ".join(text.lower().split())
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]
