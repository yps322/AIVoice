import { useEffect, useRef } from "react";

export default function AgentResponse({ text, audioUrl }) {
  const audioRef = useRef(null);

  useEffect(() => {
    if (audioUrl && audioRef.current) {
      audioRef.current.src =
        (import.meta.env.VITE_API_URL || "http://127.0.0.1:8000") + audioUrl;
      audioRef.current.play().catch(() => {});
    }
  }, [audioUrl]);

  if (!text) return null;

  return (
    <div className="agent-response">
      <strong>AI Agent:</strong> {text}
      <audio ref={audioRef} controls className="audio-player" />
    </div>
  );
}
