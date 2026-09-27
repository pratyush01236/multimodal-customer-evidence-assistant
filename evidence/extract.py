import re
from .models import Evidence

ORDER_RE = re.compile(r"\b(?:ORD|ORDER|INV|INVOICE)[-:# ]?[A-Z0-9]{3,}\b", re.I)
DATE_RE = re.compile(r"\b(?:20\d{2}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}[-/]\d{1,2}[-/]20\d{2})\b")
AMOUNT_RE = re.compile(r"(?:₹|INR|USD|\$|€|£)\s?\d+(?:[,.]\d{2})?")
PRODUCT_RE = re.compile(r"(?im)^\s*(?:product|item|model)\s*[:#-]\s*(.+)$")
ERROR_RE = re.compile(r"\b(?:ERR|ERROR|E)[-_ ]?\d{3,6}\b", re.I)

def enrich(evidence: Evidence) -> Evidence:
    text = evidence.text or ""
    if evidence.safe:
        evidence.order_id = (ORDER_RE.search(text) or [None])[0]
        evidence.date = (DATE_RE.search(text) or [None])[0]
        evidence.amount = (AMOUNT_RE.search(text) or [None])[0]
        product = PRODUCT_RE.search(text)
        evidence.product = product.group(1).strip() if product else None
        evidence.error_codes = sorted(set(ERROR_RE.findall(text)), key=str.lower)
    return evidence
