import threading
import uuid
from concurrent.futures import ThreadPoolExecutor

_jobs = {}
_lock = threading.Lock()
_executor = ThreadPoolExecutor(max_workers=4)

def submit(fn, *args, **kwargs):
    job_id = str(uuid.uuid4())
    with _lock:
        _jobs[job_id] = {"status": "queued", "result": None}
    future = _executor.submit(fn, *args, **kwargs)
    def done(f):
        with _lock:
            try:
                _jobs[job_id] = {"status": "completed", "result": f.result()}
            except Exception as exc:
                _jobs[job_id] = {"status": "failed", "result": str(exc)}
    future.add_done_callback(done)
    return job_id

def get_job(job_id):
    with _lock:
        return _jobs.get(job_id)
