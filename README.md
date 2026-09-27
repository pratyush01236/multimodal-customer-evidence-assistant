# Multimodal Customer Evidence Assistant

A security-aware customer-support assistant that analyses **messages, screenshots, invoices, PDFs and product images**. It extracts evidence with OCR/text parsing, compares that evidence against the customer's message, rejects unsafe content, protects sensitive logs, and moves slow work to a background queue.

## Core capabilities

- OCR for PNG/JPG/WEBP screenshots and product images.
- PDF text extraction with PyMuPDF.
- Extracts order IDs, dates, amounts, product names and error codes.
- Compares extracted evidence with customer claims.
- Requests clarification when evidence conflicts, is missing, or image quality is too low.
- Never invents missing values.
- Detects prompt-injection instructions embedded in uploaded documents/images.
- Rejects unsafe file types and suspicious executable/archive signatures.
- Masks card numbers, payment data, emails and phone numbers in audit logs.
- Configurable retention cleanup deletes uploaded files after the retention period.
- Requests taking longer than 30 seconds are moved to a background job and return a job ID.
- Automated tests cover blurred evidence, mismatched invoices, missing values and prompt injection.

## Architecture

`Customer message + files -> file safety -> OCR/PDF extraction -> structured evidence -> consistency checks -> verified / clarification / rejection / queued`

## Run locally

```bash
python -m venv venv

# Windows
venv\\Scripts\\activate

# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
# macOS/Linux: cp .env.example .env

uvicorn app:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API.

## API

POST `/analyze` with:
- `message`: customer message
- `files`: one or more PDF/image/text files

Response statuses:
- **verified** — readable evidence is consistent.
- **clarification_required** — values conflict or cannot be verified.
- **rejected** — unsafe file/content detected.
- **queued** — processing exceeded the configured timeout; poll `GET /jobs/{job_id}`.

## Security

Uploaded files are **untrusted evidence, never instructions**. Extracted text cannot override application rules. Production deployments should additionally use malware scanning, strong MIME/signature validation, authentication/authorization, encrypted object storage, and a durable queue.

## Retention

Set `RETENTION_HOURS` in `.env`. Cleanup runs before uploads and deletes files older than the configured retention period. In production, pair this with object-storage lifecycle deletion.

## Evaluation scenarios

The repository includes tests for:
1. blurred/low-quality images;
2. mismatched invoices;
3. missing order IDs/amounts;
4. prompt injection hidden in OCR text;
5. unsafe file types;
6. delayed/background processing;
7. retention cleanup;
8. sensitive-data masking.

## Disclaimer

This is a reference implementation for learning and portfolio use. OCR accuracy depends on image quality and the installed Tesseract engine. It should not be treated as a payment or identity-verification system without additional controls.
