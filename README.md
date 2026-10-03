# PocketSmart AI

Full-stack Smart Budget & Recommendation Assistant built with FastAPI, SQLite, vanilla JavaScript and optional Google Gemini AI.

## Setup
1. Install Python 3.11+ and VS Code.
2. Open this folder in VS Code.
3. Terminal: `python -m venv .venv`
4. Windows: `.venv\\Scripts\\activate` ; macOS/Linux: `source .venv/bin/activate`
5. `pip install -r requirements.txt`
6. Copy `.env.example` to `.env` and add `GEMINI_API_KEY` if you want Gemini. The app works without it using a local fallback.
7. Run: `uvicorn app.main:app --reload`
8. Open `http://127.0.0.1:8000`
9. API docs: `http://127.0.0.1:8000/docs`
10. Test: `pytest -q`

## Features
Income + savings goal, expense CRUD, spending analysis, category chart, savings progress, AI recommendations, AI chat, CSV export, SQLite storage, API docs, and health endpoint.

## Files
`app/main.py` API/server; `app/services/budget.py` calculations; `app/services/gemini.py` AI/fallback; `app/static/` frontend; `tests/` API tests.
