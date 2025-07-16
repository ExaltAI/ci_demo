from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Simple Message API", version="1.0.0")

# In-memory storage for messages
messages: dict[str, str] = {}


class MessageRequest(BaseModel):
    message: str


class MessageResponse(BaseModel):
    id: str
    message: str


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "message": "Simple Message API is running"}


@app.post("/messages", response_model=MessageResponse)
async def post_message(request: MessageRequest):
    """Post a new message"""
    message_id = str(len(messages) + 1)
    messages[message_id] = request.message
    return MessageResponse(id=message_id, message=request.message)


@app.get("/messages/{message_id}", response_model=MessageResponse)
async def get_message(message_id: str):
    """Get a message by ID"""
    if message_id not in messages:
        raise HTTPException(status_code=404, detail="Message not found")
    return MessageResponse(id=message_id, message=messages[message_id])


@app.delete("/messages/{message_id}")
async def delete_message(message_id: str):
    """Delete a message by ID"""
    if message_id not in messages:
        raise HTTPException(status_code=404, detail="Message not found")
    del messages[message_id]
    return {"message": f"Message {message_id} deleted successfully"}


@app.get("/messages")
async def list_messages():
    """List all messages"""
    return {
        "messages": [{"id": msg_id, "message": msg} for msg_id, msg in messages.items()]
    }
