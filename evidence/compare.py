from .models import Evidence

def compare_message_with_evidence(message: str, evidence: list[Evidence]) -> tuple[list[str], list[str]]:
    conflicts, clarification = [], []
    safe = [e for e in evidence if e.safe]
    if not safe:
        return [], ["Please upload a safe, readable file containing the requested evidence."]

    text = " ".join(e.text for e in safe).lower()
    checks = {
        "order ID": ("order_id",),
        "date": ("date",),
        "amount": ("amount",),
        "product": ("product",),
    }
    msg = message.lower()
    for label, attrs in checks.items():
        mentioned = any(word in msg for word in (label, label.replace(" ", "_")))
        if mentioned and not any(getattr(e, attrs[0]) for e in safe):
            clarification.append(f"Please clarify the {label}; it is not visible in the uploaded evidence.")

    # If the customer explicitly supplies a value, require it to occur in trusted OCR/text.
    import re
    patterns = {
        "order ID": r"\b(?:ORD|ORDER|INV|INVOICE)[-:# ]?[A-Z0-9]{3,}\b",
        "amount": r"(?:₹|INR|USD|\$|€|£)\s?\d+(?:[,.]\d{2})?",
        "error code": r"\b(?:ERR|ERROR|E)[-_ ]?\d{3,6}\b",
    }
    for label, pattern in patterns.items():
        values = re.findall(pattern, message, re.I)
        for value in values:
            if value.lower() not in text:
                conflicts.append(f"{label} in the message ({value}) does not match the uploaded evidence.")

    if any(e.quality < 0.35 for e in safe):
        clarification.append("The uploaded image appears too blurred or low quality to verify reliably. Please upload a clearer file.")
    return conflicts, clarification
