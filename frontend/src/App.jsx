import { useState, useCallback } from "react";
import { v4 as uuidv4 } from "uuid";
import CallButton from "./components/CallButton";
import Transcript from "./components/Transcript";
import AgentResponse from "./components/AgentResponse";
import LeadInfo from "./components/LeadInfo";
import BookingForm from "./components/BookingForm";
import HandoffNotice from "./components/HandoffNotice";
import { sendAudio, sendChat } from "./api";
import "./App.css";

function App() {
  const [sessionId] = useState(() => uuidv4());
  const [transcript, setTranscript] = useState("");
  const [reply, setReply] = useState("");
  const [audioUrl, setAudioUrl] = useState("");
  const [lead, setLead] = useState(null);
  const [handoff, setHandoff] = useState(false);
  const [bookingDone, setBookingDone] = useState(false);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  const handleAudioReady = useCallback(async (blob) => {
    setLoading(true);
    try {
      const { data } = await sendAudio(blob, sessionId);
      setTranscript(data.user_text);
      setReply(data.reply);
      setAudioUrl(data.audio_url);
      setLead(data.lead);
      if (data.handoff_required) setHandoff(true);
      setHistory((prev) => [
        ...prev,
        { role: "user", text: data.user_text },
        { role: "agent", text: data.reply },
      ]);
    } catch {
      setReply("Sorry, something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  }, [sessionId]);

  const handleTextSend = useCallback(async () => {
    if (!transcript.trim()) return;
    setLoading(true);
    try {
      const { data } = await sendChat(transcript, sessionId);
      setReply(data.reply);
      setLead(data.lead);
      if (data.lead?.handoff_required) setHandoff(true);
      setHistory((prev) => [
        ...prev,
        { role: "user", text: transcript },
        { role: "agent", text: data.reply },
      ]);
    } catch {
      setReply("Sorry, something went wrong.");
    } finally {
      setLoading(false);
      setTranscript("");
    }
  }, [transcript, sessionId]);

  return (
    <div className="app">
      <header>
        <h1>AI Insurance Voice Agent</h1>
        <p>Get insurance advice and book a consultation — free and instant</p>
      </header>

      <main>
        <div className="controls">
          <CallButton onAudioReady={handleAudioReady} disabled={loading} />
          <div className="text-input">
            <input
              type="text"
              placeholder="Or type your message..."
              value={transcript}
              onChange={(e) => setTranscript(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleTextSend()}
            />
            <button onClick={handleTextSend} disabled={loading || !transcript.trim()}>
              Send
            </button>
          </div>
        </div>

        {loading && <div className="spinner">Processing...</div>}

        <div className="conversation">
          {history.map((entry, i) =>
            entry.role === "user" ? (
              <Transcript key={i} text={entry.text} />
            ) : (
              <AgentResponse
                key={i}
                text={entry.text}
                audioUrl={i === history.length - 1 ? audioUrl : null}
              />
            )
          )}
        </div>

        <LeadInfo lead={lead} />

        {lead?.qualified && !bookingDone && !handoff && (
          <BookingForm sessionId={sessionId} onBooked={() => setBookingDone(true)} />
        )}

        {handoff && <HandoffNotice sessionId={sessionId} />}
      </main>
    </div>
  );
}

export default App;
