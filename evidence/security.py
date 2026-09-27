import re
from pathlib import Path

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".pdf", ".txt"}
INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"ignore\s+(the\s+)?system\s+prompt",
    r"reveal\s+(the\s+)?system\s+prompt",
    r"developer\s+message",
    r"follow\s+these\s+instructions\s+instead",
    r"disregard\s+security",
]

def contains_prompt_injection(text: str) -> bool:
    value = text.lower()
    return any(re.search(pattern, value) for pattern in INJECTION_PATTERNS)

def validate_extension(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS

def validate_bytes(data: bytes) -> tuple[bool, str]:
    if not data:
        return False, "empty file"
    if data.startswith(b"MZ") or data.startswith(b"PK" + bytes([3, 4])):
        return False, "potentially unsafe executable/archive content"
    return True, ""

def sanitize_for_log(text: str) -> str:
    if not text:
        return text
    text = re.sub(r"\b(?:\d[ -]?){13,19}\b", "[CARD_REDACTED]", text)
    text = re.sub(r"\b\d{3,4}\b(?=\s*(?:CVV|CVC|PIN)\b)", "[PAYMENT_REDACTED]", text, flags=re.I)
    text = re.sub(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", "[EMAIL_REDACTED]", text, flags=re.I)
    text = re.sub(r"\b(?:\+?\d[\d\s().-]{8,}\d)\b", "[PHONE_REDACTED]", text)
    return text
