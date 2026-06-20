import { useEffect, useState } from "react";
import { requestHandoff } from "../api";

export default function HandoffNotice({ sessionId }) {
  const [sent, setSent] = useState(false);

  useEffect(() => {
    if (!sent) {
      requestHandoff(sessionId).then(() => setSent(true)).catch(() => {});
    }
  }, [sessionId, sent]);

  return (
    <div className="handoff-notice">
      <h3>🔄 Connecting to a Human Agent</h3>
      <p>A licensed insurance advisor will call you shortly at the phone number you provided.</p>
    </div>
  );
}
