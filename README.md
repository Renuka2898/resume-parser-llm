# AI-Powered Resume Parser

An LLM-powered resume parsing application that extracts structured information from PDF and DOCX resumes using Ollama, FastAPI, and Streamlit.

## Features

- Extract text from PDF and DOCX files.
- Use an LLM to extract contact information, professional summary, work experience, education, skills, and certifications.
- FastAPI REST API with structured responses and Pydantic validation.
- Upload resumes through a Streamlit web interface.
- Retrieve previously parsed results using a unique document ID.
- Input validation, logging, and error handling.

## Technology Stack

- Python
- FastAPI
- Streamlit
- Ollama
- Llama 3.2
- Pydantic
- PDF and DOCX parsing libraries

## Prerequisites

- Python 3.10 or later
- Git
- Ollama installed locally
- The `llama3.2` model downloaded in Ollama

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Renuka2898/resume-parser-llm.git
cd resume-parser-llm
```

### 2. Create and activate a virtual environment

Windows:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Ollama

Install Ollama from https://ollama.com/ if it is not already installed.

Download the model:

```bash
ollama pull llama3.2
```

Make sure Ollama is running and accessible at:

`http://localhost:11434`

The application uses the locally running Ollama service and does not require an OpenAI API key when configured for Ollama.

## Run the Backend

Open a terminal in the project directory:

```bash
python -m uvicorn app.main:app --reload
```

API documentation:

http://127.0.0.1:8001/docs

Health check:

http://127.0.0.1:8001/health

## Run the Streamlit UI

Open a second terminal in the project directory:

```bash
python -m streamlit run ui/streamlit_app.py
```

Open:

http://localhost:8501

## API Endpoints

- `POST /api/upload` — Upload a PDF or DOCX resume and receive extracted information and a document ID.
- `GET /api/resume/{document_id}` — Retrieve parsed resume information using the document ID.
- `GET /health` — Check backend health.

## Run Tests

```bash
pytest -q
```

## Limitations

- Parsed results are stored in memory and are lost when the backend restarts.
- Scanned PDFs may require OCR if they do not contain selectable text.
- LLM extraction may be incomplete or inaccurate; verify the output against the original resume.
- Ollama must be running locally with the configured model available.

## Security

- Do not commit API keys, `.env` files, or real resumes to GitHub.
- Use sample resumes that you have permission to process.
