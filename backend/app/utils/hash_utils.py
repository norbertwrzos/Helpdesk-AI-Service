import hashlib


def calculate_content_hash(text: str) -> str:
    normalized = text.strip().encode("utf-8")
    return hashlib.sha256(normalized).hexdigest()