import os
import uuid
import asyncio
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq_client import generate_response
from stt import transcribe_audio
from tts import speak
from lead_extractor import extract_lead
from lead_repository import save_lead, book_meeting, mark_handoff
from conversation_store import save_message, get_history
from database import engine
from models import Base

AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


class BookMeetingRequest(BaseModel):
    session_id: str
    meeting_time: str


class HandoffRequest(BaseModel):
    session_id: str


@app.post("/chat")
def chat(req: ChatRequest):
    save_message(req.session_id, "user", req.message)
    history = get_history(req.session_id)
    reply = generate_response(req.message, history)
    save_message(req.session_id, "assistant", reply)

    conversation_text = "\n".join(
        f"{m['role']}: {m['content']}" for m in get_history(req.session_id)
    )
    lead_data = extract_lead(conversation_text)
    save_lead(req.session_id, lead_data)

    return {
        "success": True,
        "reply": reply,
        "lead": lead_data
    }


@app.post("/transcribe")
async def transcribe(audio: UploadFile = File(...)):
    ext = audio.filename.split(".")[-1] if "." in audio.filename else "wav"
    temp_path = os.path.join(AUDIO_DIR, f"upload_{uuid.uuid4().hex}.{ext}")

    with open(temp_path, "wb") as f:
        f.write(await audio.read())

    try:
        text = transcribe_audio(temp_path)
        return {"success": True, "text": text}
    finally:
        os.remove(temp_path)


@app.post("/conversation")
async def conversation(
    audio: UploadFile = File(...),
    session_id: str = Form("default")
):
    ext = audio.filename.split(".")[-1] if "." in audio.filename else "wav"
    temp_path = os.path.join(AUDIO_DIR, f"upload_{uuid.uuid4().hex}.{ext}")

    with open(temp_path, "wb") as f:
        f.write(await audio.read())

    try:
        user_text = transcribe_audio(temp_path)
    finally:
        os.remove(temp_path)

    save_message(session_id, "user", user_text)
    history = get_history(session_id)
    reply = generate_response(user_text, history)
    save_message(session_id, "assistant", reply)

    conversation_text = "\n".join(
        f"{m['role']}: {m['content']}" for m in get_history(session_id)
    )
    lead_data = extract_lead(conversation_text)
    save_lead(session_id, lead_data)

    tts_filename = f"{session_id}_reply.mp3"
    tts_path = os.path.join(AUDIO_DIR, tts_filename)
    await speak(reply, tts_path)

    audio_url = f"/audio/{tts_filename}"

    return {
        "success": True,
        "user_text": user_text,
        "reply": reply,
        "audio_url": audio_url,
        "lead": lead_data,
        "handoff_required": lead_data.get("handoff_required", False)
    }


@app.post("/book-meeting")
def book_meeting_endpoint(req: BookMeetingRequest):
    try:
        meeting_time = datetime.fromisoformat(req.meeting_time)
    except:
        return {"success": False, "error": "Invalid date format. Use ISO 8601."}

    book_meeting(req.session_id, meeting_time)
    return {"success": True, "message": "Meeting booked successfully."}


@app.post("/handoff")
def handoff_endpoint(req: HandoffRequest):
    mark_handoff(req.session_id)
    return {"success": True, "message": "Human handoff requested. An agent will contact the lead."}


@app.get("/audio/{filename}")
def get_audio(filename: str):
    file_path = os.path.join(AUDIO_DIR, filename)
    if not os.path.exists(file_path):
        return {"error": "File not found"}, 404
    return FileResponse(file_path, media_type="audio/mpeg")
