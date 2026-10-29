# AI-Powered Resume Parser

An LLM-powered resume parsing application for PDF/DOCX files, with a FastAPI REST API and Streamlit interface.

## Features
- PDF/DOCX text extraction
- LLM extraction for contact details, summary, work experience, education, skills and certifications
- Pydantic validation, file size/type checks, logging and error responses
- API endpoints and a Streamlit UI with JSON download

## Setup
Install Python 3.10+. Create/activate a virtual environment and run:
```bash
pip install -r requirements.txt
```
Copy `.env.example` to `.env`, then set `OPENAI_API_KEY` and a model available to your account. Never commit `.env`.

## Run backend
```bash
uvicorn app.main:app --reload
```
API docs: http://127.0.0.1:8000/docs

## Run frontend (second terminal)
```bash
streamlit run ui/streamlit_app.py
```
UI: http://localhost:8501

## API
- `POST /api/upload` — upload PDF/DOCX and receive parsed data plus a document ID.
- `GET /api/resume/{document_id}` — retrieve parsed data or return 404.
- `GET /health` — health check.

## Tests
```bash
pytest -q
```

## Limitations
Parsed results are held in memory and disappear when the backend restarts. Scanned PDFs without selectable text are not OCR-processed. LLM output may be imperfect; review it against the source resume. Use test resumes you have permission to process.
