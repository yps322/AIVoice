import { useState, useRef } from "react";

export default function CallButton({ onAudioReady, disabled }) {
  const [recording, setRecording] = useState(false);
  const mediaRecorder = useRef(null);
  const chunks = useRef([]);

  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder.current = new MediaRecorder(stream, { mimeType: "audio/webm" });
    chunks.current = [];

    mediaRecorder.current.ondataavailable = (e) => {
      if (e.data.size > 0) chunks.current.push(e.data);
    };

    mediaRecorder.current.onstop = () => {
      const blob = new Blob(chunks.current, { type: "audio/webm" });
      stream.getTracks().forEach((t) => t.stop());
      onAudioReady(blob);
    };

    mediaRecorder.current.start();
    setRecording(true);
  };

  const stopRecording = () => {
    mediaRecorder.current?.stop();
    setRecording(false);
  };

  return (
    <button
      className={`call-btn ${recording ? "recording" : ""}`}
      onClick={recording ? stopRecording : startRecording}
      disabled={disabled}
    >
      {recording ? "⏹ Stop" : "🎤 Start Call"}
    </button>
  );
}
