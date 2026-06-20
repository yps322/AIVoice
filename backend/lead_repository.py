from datetime import datetime
from database import SessionLocal
from models import Lead


def save_lead(session_id, lead_data):

    db = SessionLocal()

    try:

        lead = db.query(Lead).filter(
            Lead.session_id == session_id
        ).first()

        if not lead:

            lead = Lead(
                session_id=session_id
            )

            db.add(lead)

        lead.name = lead_data.get("name") or lead.name

        age = lead_data.get("age")

        if age:
            try:
                lead.age = int(age)
            except:
                pass

        lead.city = lead_data.get("city") or lead.city

        lead.phone = lead_data.get("phone") or lead.phone

        lead.email = lead_data.get("email") or lead.email

        lead.insurance_type = (
            lead_data.get("insurance_type")
            or lead.insurance_type
        )

        lead.health_info = (
            lead_data.get("health_info")
            or lead.health_info
        )

        qualified = lead_data.get("qualified")

        if qualified is not None:
            lead.qualified = qualified

        db.commit()

    finally:

        db.close()


def book_meeting(session_id: str, meeting_time: datetime):
    db = SessionLocal()
    try:
        lead = db.query(Lead).filter(
            Lead.session_id == session_id
        ).first()
        if lead:
            lead.meeting_time = meeting_time
            lead.meeting_booked = True
            db.commit()
    finally:
        db.close()


def mark_handoff(session_id: str):
    db = SessionLocal()
    try:
        lead = db.query(Lead).filter(
            Lead.session_id == session_id
        ).first()
        if lead:
            lead.handoff_requested = True
            db.commit()
    finally:
        db.close()