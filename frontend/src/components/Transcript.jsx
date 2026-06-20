export default function Transcript({ text }) {
  if (!text) return null;
  return (
    <div className="transcript">
      <strong>You:</strong> {text}
    </div>
  );
}
