from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Lead(Base):

    __tablename__ = "leads"

    id = Column(Integer, primary_key=True)

    session_id = Column(String(100), unique=True)

    name = Column(String(100))

    age = Column(Integer)

    city = Column(String(100))

    phone = Column(String(20))

    email = Column(String(100))

    insurance_type = Column(String(100))

    health_info = Column(Text)

    qualified = Column(Boolean, default=False)

    meeting_time = Column(DateTime, nullable=True)

    meeting_booked = Column(Boolean, default=False)

    handoff_requested = Column(Boolean, default=False)


class Conversation(Base):

    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)

    session_id = Column(String(100), nullable=False)

    role = Column(String(20), nullable=False)

    content = Column(Text, nullable=False)

    created_at = Column(DateTime, server_default=func.now())