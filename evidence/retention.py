from datetime import datetime, timedelta
from pathlib import Path
from config import RETENTION_HOURS, UPLOAD_DIR

def cleanup_expired():
    root = Path(UPLOAD_DIR)
    if not root.exists():
        return 0
    cutoff = datetime.now().timestamp() - timedelta(hours=RETENTION_HOURS).total_seconds()
    deleted = 0
    for path in root.rglob("*"):
        if path.is_file() and path.stat().st_mtime < cutoff:
            path.unlink()
            deleted += 1
    return deleted
