from sqlalchemy import Column, Integer, String
from app.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    channel = Column(String, nullable=False)