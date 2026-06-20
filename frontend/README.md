# Frontend — AI Insurance Voice Agent
# Deploy on Vercel: https://vercel.com

## Setup
```bash
cd frontend
npm install
npm run dev
```

## Environment Variables (set in Vercel Dashboard)
- `VITE_API_URL` — URL of your deployed backend (e.g., https://insurance-ai-backend.onrender.com)

## Features
- 🎤 Microphone recording (MediaRecorder API)
- 💬 Text chat fallback
- 🔊 AI response with auto-play audio
- 📋 Lead details extraction display
- 📅 Meeting booking form
- 🔄 Human handoff

Backend:
- stt.py â Whisper base model STT
- models.py â Added meeting_time, meeting_booked, handoff_requested, Conversation table
- conversation_store.py â NEW: PostgreSQL-persisted conversation history
- lead_repository.py â Added book_meeting(), mark_handoff()
- main.py â 5 endpoints + CORS + auto table creation
- database.py â PostgreSQL support + SQLite fallback for dev
- lead_extractor.py â Added handoff_required field
- tts.py â Accepts custom output path
- render.yaml â Render deployment config
- .gitignore â Backend ignores
Frontend (React + Vite):
- src/api.js â Axios API client
- src/components/CallButton.jsx â Mic record/stop (MediaRecorder)
- src/components/Transcript.jsx â User speech display
- src/components/AgentResponse.jsx â AI text + auto-play audio
- src/components/LeadInfo.jsx â Extracted lead card
- src/components/BookingForm.jsx â Date/time picker
- src/components/HandoffNotice.jsx â Human callback notice
- src/App.jsx â Full UI orchestrator
- src/App.css â Dark theme styling
- vite.config.js â Dev proxy to backend
- vercel.json â Vercel deployment config
To Run Locally
# Backend
cd backend && .\venv\Scripts\activate && uvicorn main:app --reload --port 8000

# Frontend (separate terminal)
cd frontend && npm run dev
To Deploy
1. Backend â Push to GitHub â Deploy on Render (set env vars: GROQ_API_KEY, DATABASE_URL)
2. Frontend â Push to GitHub â Deploy on Vercel (set VITE_API_URL to Render backend URL)
3. Database â Already connected to your Aiven PostgreSQL instance

