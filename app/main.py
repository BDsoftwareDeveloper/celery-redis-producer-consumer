from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import Base, engine
from app.database import get_db
from app.models import Message
from app.schemas import MessageCreate
from app.pubsub_tasks import producer

app = FastAPI()
@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)  # Ensure all tables are created
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
@app.post("/messages/")
def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    db_message = Message(content=message.content, channel=message.channel)
    db.add(db_message)
    db.commit()
    producer.delay(db_message.channel, db_message.content)  # Publish message to Redis channel
    return {"id": db_message.id, "content": db_message.content, "channel": db_message.channel}