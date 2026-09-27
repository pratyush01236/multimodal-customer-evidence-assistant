from fastapi import FastAPI, File, Form, UploadFile
from evidence.queue import get_job
from evidence.service import process_uploads

app = FastAPI(title="Multimodal Customer Evidence Assistant", version="1.0.0")

@app.get("/")
def health():
    return {"name": "multimodal-customer-evidence-assistant", "status": "ok"}

@app.post("/analyze")
async def analyze(message: str = Form(...), files: list[UploadFile] = File(...)):
    uploads = [(f.filename or "upload.bin", await f.read()) for f in files]
    return process_uploads(message, uploads).__dict__

@app.get("/jobs/{job_id}")
def job_status(job_id: str):
    result = get_job(job_id)
    return result or {"status": "not_found"}
