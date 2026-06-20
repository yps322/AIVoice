from database import SessionLocal
from models import Conversation


def save_message(session_id: str, role: str, content: str):
    db = SessionLocal()
    try:
        msg = Conversation(
            session_id=session_id,
            role=role,
            content=content
        )
        db.add(msg)
        db.commit()
    finally:
        db.close()


def get_history(session_id: str) -> list:
    db = SessionLocal()
    try:
        rows = (
            db.query(Conversation)
            .filter(Conversation.session_id == session_id)
            .order_by(Conversation.created_at)
            .all()
        )
        return [
            {"role": r.role, "content": r.content}
            for r in rows
        ]
    finally:
        db.close()
