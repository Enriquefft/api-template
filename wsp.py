"""Module to send messages using Twilio Messaging API."""

import logging
from json import dumps
from typing import Dict

from twilio.rest import Client  # pyright: ignore [reportMissingTypeStubs]

from env import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_NUMBER

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

logger = logging.getLogger(__name__)


# Sending message logic through Twilio Messaging API
def send_message(to_number: str, body_text: str) -> None:
    """Send a message to a phone number using Twilio API."""
    if not to_number.startswith("whatsapp:"):
        to_number = f"whatsapp:{to_number}"

    try:
        message = client.messages.create(
            from_=f"whatsapp:{TWILIO_NUMBER}",
            body=body_text,
            to=to_number,
        )
        logger.info("Message sent to %s: %s", to_number, message.body)
    except Exception:
        logger.exception("Error sending message to %s", to_number)


# Sending message logic through Twilio Messaging API
def send_template_message(
    to_number: str,
    template_sid: str,
    content_variables: Dict[str, str],
    messaging_service_sid: str,
) -> None:
    """Send a message to a phone number using Twilio API."""
    if not to_number.startswith("whatsapp:"):
        to_number = f"whatsapp:{to_number}"

    try:
        message = client.messages.create(
            from_=f"whatsapp:{TWILIO_NUMBER}",
            to=to_number,
            content_variables=dumps(content_variables),
            content_sid=template_sid,
            messaging_service_sid=messaging_service_sid,
        )
        logger.info("Message sent to %s: %s", to_number, message.body)
    except Exception:
        logger.exception("Error sending message to %s", to_number)
