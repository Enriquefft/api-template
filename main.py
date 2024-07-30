"""Main API module for the chatbot."""

# ruff: noqa: N803 (Twilio API requires Capitalized variable names)
# ruff: noqa: B008 (fastapi makes use of reusable default function calls)

import logging
from typing import Generator

from fastapi import Depends, FastAPI, Form
from sqlalchemy.orm import Session

from ai import get_response

# Internal imports
from models import SessionLocal, User

# Set up logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"msg": "up & running"}


# Dependency
def get_db() -> Generator[Session, None, None]:
    """Get a database connection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/message")
async def reply(
    Body: str = Form(),
    From: str = Form(),
    db: Session = Depends(get_db),
) -> str:
    """Reply to a WhatsApp message from the user."""
    phone_number = From.removeprefix("whatsapp:")

    user = db.query(User).filter(User.phone_number == phone_number).first()

    if not user:
        logger.info("User with phone number %s not found", phone_number)
        new_user = User(phone_number=phone_number)
        db.add(new_user)
        db.commit()

    chat_response = get_response(
        Body,
    )

    logger.info("Received a message from the user")
    logger.info("User message: %s", Body)

    if chat_response is None:
        logger.error("Failed to get a response from the chat system")
        return ""

    return chat_response
