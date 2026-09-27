import logging
import time
from pathlib import Path
from config import BACKGROUND_TIMEOUT_SECONDS, UPLOAD_DIR, MAX_FILE_MB, LOG_FILE
from .compare import compare_message_with_evidence
from .extract import enrich
from .models import AnalysisResult
from .ocr import inspect_file
from .queue import submit
from .retention import cleanup_expired
from .security import sanitize_for_log, validate_bytes, validate_extension

Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)

def _analyse(message, paths):
    started = time.monotonic()
    evidence = []
    for path in paths:
        ev = enrich(inspect_file(path, Path(path).name))
        evidence.append(ev)
    conflicts, clarification = compare_message_with_evidence(message, evidence)
    unsafe = [e for e in evidence if not e.safe]
    if unsafe:
        return AnalysisResult("rejected", "The uploaded file contains unsafe or hidden instructions and was rejected.", evidence, conflicts, clarification)
    if clarification or conflicts:
        return AnalysisResult("clarification_required", "I need clarification before I can reliably verify the evidence.", evidence, conflicts, clarification)
    return AnalysisResult("verified", "The uploaded evidence was extracted and is consistent with the customer message.", evidence)

def process_uploads(message: str, uploads: list[tuple[str, bytes]]):
    cleanup_expired()
    paths = []
    for filename, data in uploads:
        if not validate_extension(filename):
            return AnalysisResult("rejected", "Unsupported or unsafe file type.")
        if len(data) > MAX_FILE_MB * 1024 * 1024:
            return AnalysisResult("rejected", "File exceeds the configured size limit.")
        safe, reason = validate_bytes(data)
        if not safe:
            return AnalysisResult("rejected", f"File rejected: {reason}")
        target = Path(UPLOAD_DIR) / Path(filename).name
        target.write_bytes(data)
        paths.append(str(target))

    started = time.monotonic()
    result = _analyse(message, paths)
    elapsed = time.monotonic() - started
    logging.info("analysis status=%s elapsed=%.2f message=%s", result.status, elapsed, sanitize_for_log(message))

    if elapsed > BACKGROUND_TIMEOUT_SECONDS:
        job_id = submit(_analyse, message, paths)
        return AnalysisResult("queued", "Processing is taking longer than expected. Your request has been moved to the background queue.", background_job_id=job_id)
    return result
