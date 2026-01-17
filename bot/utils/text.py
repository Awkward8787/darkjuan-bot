import hashlib
import re


SECRET_REGEX = re.compile(r"(sk_[a-zA-Z0-9]{16,}|token_[A-Za-z0-9]{12,}|api[_-]?key[=:\\s]+[A-Za-z0-9]{12,})")


def sanitize_snippet(text: str, max_length: int = 120) -> str:
    cleaned = re.sub(r"\s+", " ", text).strip()
    return cleaned[:max_length]


def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def redact_secrets(text: str) -> str:
    return SECRET_REGEX.sub("[redacted]", text)
