# AI Integration Setup & Testing Guide

## Overview

The Gradlink application now includes integrated AI-powered features:

- **ASK_ALUM (RAG)**: Retrieval-augmented generation for alumni advice queries
- **RESUME_UPLOAD (ATS)**: Applicant Tracking System scoring for resume uploads
- **MCS_RECOMMENDER (DB-MCS)**: Database-backed mentor compatibility scoring

All features are **gated behind feature flags** in `config/feature_flags.py` and default to **enabled** for development.

---

## Feature Flags

All features are enabled by default for dev. To disable/enable:

```python
# config/feature_flags.py
FEATURE_FLAGS = {
    "NEW_THEME": True,           # New UI theme
    "RESUME_UPLOAD": True,       # ATS resume scoring
    "MCS_RECOMMENDER": True,     # Mentor compatibility matching
    "ASK_ALUM": True,            # RAG alumni advice
}
```

Or use environment variables (overrides config defaults):

```powershell
$env:FEATURE_ASK_ALUM = "true"
$env:FEATURE_RESUME_UPLOAD = "true"
$env:FEATURE_MCS = "true"
```

---

## Quick Start (Local Dev)

### 1. Install Base Dependencies

```powershell
cd "C:\Users\BENITA GRACE\Downloads\AMP-Devs-main\AMP-Devs"
python -m venv venv
.\\venv\\Scripts\\Activate.ps1
pip install -U pip
pip install Flask Flask-Login Flask-SQLAlchemy python-dotenv
```

### 2. Install Optional AI Packages (for full functionality)

```powershell
pip install openai faiss-cpu numpy scikit-learn pdfminer.six python-docx spacy
python -m spacy download en_core_web_sm
```

### 3. Set OpenAI API Key (optional, for RAG generation)

```powershell
$env:OPENAI_API_KEY = "sk-your-key-here"
```

**Important**: Do NOT commit `OPENAI_API_KEY` to the repo. Use environment variables or `.env` file (add to `.gitignore`).

### 4. Run the App

```powershell
.\\venv\\Scripts\\python.exe app.py
```

App runs at: **http://localhost:5000**

---

## Testing the Features

### A. ATS Resume Scoring (`/resume`)

1. Navigate to: **http://localhost:5000/resume**
2. Upload a resume (PDF, DOCX, or TXT)
3. The system will:
   - Extract text from the file
   - Score against a default job description
   - Return skill matches, education detection, and feedback

**Expected response**:

```json
{
  "score": 65.2,
  "skills_found": ["python", "sql", "machine learning"],
  "has_education": true,
  "num_skills": 3,
  "advice": "Add more relevant keywords..."
}
```

---

### B. RAG Alumni Advice (`/ask/rag`)

**Endpoint**: `POST /ask/rag`

**Request**:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"query": "How do I prepare for tech interviews?"}' \
  http://127.0.0.1:5000/ask/rag
```

**Expected response** (with OpenAI/FAISS available):

```json
{
  "query": "How do I prepare for tech interviews?",
  "answer": "Based on alumni advice: Focus on internships and practical projects...",
  "sources": [
    {
      "id": "advice_1",
      "text": "Focus on internships and practical projects.",
      "metadata": { "author": "Alumnus A" },
      "score": 0.15
    }
  ]
}
```

**Graceful fallback** (if OpenAI/FAISS missing):

```json
{
  "error": "RAG feature not available"
}
```

---

### C. Mentor Compatibility Scoring (`/mcs/recommend`)

**Endpoint**: `GET /mcs/recommend`

Navigate to: **http://localhost:5000/mcs/recommend**

The page displays mentor recommendations based on:

- Skill vector matching (TF-IDF)
- Timezone compatibility
- Availability overlap
- Historical mentor ratings

**Expected output**:

```
Recommendations:
1. A. Mentor - Compatibility: 85.3%, Skill Match: 91.2%
2. B. Mentor - Compatibility: 72.1%, Skill Match: 68.5%
```

---

## Seeding RAG Index (Development)

To populate the RAG in-memory index with sample advice:

```powershell
.\\venv\\Scripts\\python.exe scripts/import_advice.py
```

**Output**:

```
Imported advice_1
Imported advice_2
Imported advice_3

Imported 3 documents into the RAG index (dev only)
```

---

## Running Tests

Unit tests for AI modules (offline, no external API calls):

```powershell
pip install pytest
.\\venv\\Scripts\\python.exe -m pytest -v
```

**Test files**:

- `tests/test_imports.py` — Verifies AI modules import
- `tests/test_ats.py` — ATS extraction and scoring tests

**Expected output**:

```
tests/test_imports.py::test_ai_modules_importable PASSED
tests/test_ats.py::test_extract_skills_simple PASSED
tests/test_ats.py::test_ats_score_basic PASSED

3 passed in 1.10s
```

---

## Offline Smoke Test

Test AI modules without external network calls:

```powershell
.\\venv\\Scripts\\python.exe test_ai_modules.py
```

**Output**:

```
=== AI Modules Smoke Test ===

[rag_faiss] module imported
  faiss available: False
  openai available: False
  ...

[ats] module imported
  extract_skills_simple -> ['docker', 'python', 'sql']

[db_mcs] module imported

=== Smoke test complete ===
```

---

## Architecture

```
extensions/
├── ai/
│   ├── __init__.py
│   ├── rag_faiss.py         # RAG with FAISS + OpenAI
│   └── ats.py               # Resume ATS scoring
├── ask_alum/
│   ├── __init__.py
│   ├── views.py             # /ask and /ask/rag routes
│   └── templates/ask/
│       └── form.html
├── resume/
│   ├── __init__.py
│   ├── views.py             # /resume route (ATS integration)
│   └── templates/resume/
│       ├── upload.html
│       └── result.html
└── matching/
    ├── __init__.py
    ├── views.py             # /mcs/recommend route
    ├── mcs.py               # Compatibility scoring algorithm
    ├── db_mcs.py            # DB-backed recommendation
    └── templates/mcs/
        └── recommend.html

scripts/
└── import_advice.py         # One-time RAG seeder
```

---

## Production Checklist

- [ ] Set `OPENAI_API_KEY` via secrets manager (e.g., AWS Secrets Manager, HashiCorp Vault)
- [ ] Use `pgvector` PostgreSQL extension instead of in-memory FAISS for persistent RAG index
- [ ] Add rate limiting to `/ask/rag` and `/resume` endpoints
- [ ] Implement PII redaction for resume uploads
- [ ] Set up background workers (Celery) for async resume processing
- [ ] Log all AI requests with user/query metadata for audit trails
- [ ] Add monitoring/alerting for OpenAI API failures and costs
- [ ] Test graceful degradation when external APIs are unavailable
- [ ] Use environment-specific feature flags (dev, staging, production)

---

## Troubleshooting

### "faiss not installed"

```powershell
pip install faiss-cpu
```

### "openai package not installed"

```powershell
pip install openai
```

### "OPENAI_API_KEY not set"

The RAG will fall back to brute-force cosine similarity. Set the key for full AI generation:

```powershell
$env:OPENAI_API_KEY = "sk-..."
```

### "RuntimeError: Working outside of application context"

Tests must run within Flask app context. Example:

```python
from app import app
with app.app_context():
    result = my_function()
```

### "ModuleNotFoundError: No module named 'sklearn'"

```powershell
pip install scikit-learn
```

---

## Next Steps

1. **Test locally** using the quick start guide above
2. **Enable in staging** by setting feature flags via environment
3. **Add telemetry** to track usage and costs
4. **Gather feedback** from users on AI recommendations
5. **Migrate to pgvector** for production scalability
6. **Integrate with admin dashboard** to manage seeded advice and job descriptions

---

For more info, see `README.md` and the feature flag docs in `config/feature_flags.py`.
