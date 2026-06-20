import { useState } from "react";
import { bookMeeting } from "../api";

export default function BookingForm({ sessionId, onBooked }) {
  const [date, setDate] = useState("");
  const [time, setTime] = useState("");
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMsg("");
    try {
      const meetingTime = new Date(`${date}T${time}`).toISOString();
      await bookMeeting(sessionId, meetingTime);
      setMsg("Meeting booked! An advisor will contact you.");
      onBooked();
    } catch {
      setMsg("Booking failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="booking-form">
      <h3>Book a Consultation</h3>
      <form onSubmit={handleSubmit}>
        <label>
          Date:
          <input type="date" value={date} onChange={(e) => setDate(e.target.value)} required />
        </label>
        <label>
          Time:
          <input type="time" value={time} onChange={(e) => setTime(e.target.value)} required />
        </label>
        <button type="submit" disabled={loading}>
          {loading ? "Booking..." : "Confirm Meeting"}
        </button>
      </form>
      {msg && <p className="booking-msg">{msg}</p>}
    </div>
  );
}
