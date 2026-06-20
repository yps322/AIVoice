# Backend — AI Insurance Voice Agent
# Deploy on Render: https://render.com

## Environment Variables (set in Render Dashboard)
# GROQ_API_KEY     — from https://console.groq.com
# DATABASE_URL     — from Neon or Aiven PostgreSQL

## Local Development
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## Database Schema (auto-created on startup)
- `leads` — stores lead information, qualification, meeting bookings
- `conversations` — stores full conversation history per session

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/chat` | Text-based conversation |
| POST | `/transcribe` | Audio → Whisper STT → text |
| POST | `/conversation` | Audio → STT → LLM → TTS → audio URL |
| POST | `/book-meeting` | Save meeting booking |
| POST | `/handoff` | Request human agent callback |
| GET | `/audio/{filename}` | Serve generated TTS audio |
