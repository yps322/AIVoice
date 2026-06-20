export default function LeadInfo({ lead }) {
  if (!lead || !lead.name && !lead.phone && !lead.email) return null;

  return (
    <div className="lead-info">
      <h3>Lead Details</h3>
      {lead.name && <p><strong>Name:</strong> {lead.name}</p>}
      {lead.age && <p><strong>Age:</strong> {lead.age}</p>}
      {lead.city && <p><strong>City:</strong> {lead.city}</p>}
      {lead.phone && <p><strong>Phone:</strong> {lead.phone}</p>}
      {lead.email && <p><strong>Email:</strong> {lead.email}</p>}
      {lead.insurance_type && <p><strong>Interest:</strong> {lead.insurance_type}</p>}
      {lead.health_info && <p><strong>Health:</strong> {lead.health_info}</p>}
      {lead.qualified && <p className="qualified">✅ Qualified Lead</p>}
    </div>
  );
}
