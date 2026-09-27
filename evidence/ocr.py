from pathlib import Path
from .models import Evidence
from .security import contains_prompt_injection

def _ocr_image(path: Path) -> tuple[str, float]:
    try:
        from PIL import Image
        import pytesseract
        image = Image.open(path)
        # Simple blur/quality heuristic: tiny images are considered low quality.
        quality = min(1.0, (image.width * image.height) / 1_000_000)
        text = pytesseract.image_to_string(image)
        return text, quality
    except Exception:
        return "", 0.0

def _read_pdf(path: Path) -> tuple[str, float]:
    try:
        import fitz
        doc = fitz.open(path)
        text = "\n".join(page.get_text() for page in doc)
        quality = 1.0 if text.strip() else 0.25
        return text, quality
    except Exception:
        return "", 0.0

def extract_text(path: str) -> tuple[str, float]:
    p = Path(path)
    if p.suffix.lower() == ".pdf":
        return _read_pdf(p)
    if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
        return _ocr_image(p)
    return p.read_text(encoding="utf-8", errors="replace"), 1.0

def inspect_file(path: str, source: str) -> Evidence:
    text, quality = extract_text(path)
    evidence = Evidence(source=source, text=text, quality=quality)
    if contains_prompt_injection(text):
        evidence.safe = False
        evidence.rejection_reason = "prompt-injection instructions detected in extracted content"
    return evidence
