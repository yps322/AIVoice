import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000",
});

export const sendChat = (message, sessionId) =>
  API.post("/chat", { message, session_id: sessionId });

export const sendAudio = (blob, sessionId) => {
  const form = new FormData();
  form.append("audio", blob, "recording.webm");
  form.append("session_id", sessionId);
  return API.post("/conversation", form);
};

export const transcribeAudio = (blob) => {
  const form = new FormData();
  form.append("audio", blob, "recording.webm");
  return API.post("/transcribe", form);
};

export const bookMeeting = (sessionId, meetingTime) =>
  API.post("/book-meeting", { session_id: sessionId, meeting_time: meetingTime });

export const requestHandoff = (sessionId) =>
  API.post("/handoff", { session_id: sessionId });
