import hashlib
import hmac
import logging
import os
from fastapi import APIRouter, Query, Request, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models import Campaign, ProcessedComment, Config
from instagram import reply_to_comment, send_dm

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/webhook", tags=["webhook"])


def verify_webhook_signature(request_body: bytes, x_hub_signature: str) -> bool:
    """Verify the webhook signature from Facebook."""
    app_secret = os.getenv("FACEBOOK_APP_SECRET", "")
    expected_signature = hmac.new(
        app_secret.encode(),
        request_body,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected_signature, x_hub_signature)


@router.get("/instagram")
async def verify_webhook(
    hub_mode: str = Query(None),
    hub_challenge: str = Query(None),
    hub_verify_token: str = Query(None),
):
    """Webhook verification endpoint for Facebook."""
    expected_token = os.getenv("WEBHOOK_VERIFY_TOKEN", "")

    if hub_mode == "subscribe" and hub_verify_token == expected_token:
        logger.info("Webhook verified successfully")
        return int(hub_challenge)
    else:
        logger.warning(f"Webhook verification failed. Mode: {hub_mode}, Token match: {hub_verify_token == expected_token}")
        raise HTTPException(status_code=403, detail="Verification failed")


@router.post("/instagram")
async def handle_webhook(
    request: Request,
    db: Session = Depends(get_db),
):
    """Handle incoming Instagram comment events."""
    try:
        body = await request.body()
        x_hub_signature = request.headers.get("X-Hub-Signature-256", "")

        # Verify signature
        if not verify_webhook_signature(body, x_hub_signature):
            logger.warning("Webhook signature verification failed")
            raise HTTPException(status_code=403, detail="Signature verification failed")

        data = await request.json()
        logger.info(f"Webhook received: {data}")

        # Get config from database
        config = db.query(Config).first()
        if not config:
            logger.error("No config found in database")
            return {"status": "error", "message": "No config found"}

        # Process each entry in the webhook payload
        for entry in data.get("entry", []):
            for messaging in entry.get("messaging", []):
                # Check if this is a comment event
                if "message" in messaging:
                    await process_comment_event(
                        messaging, db, config
                    )

        return {"status": "ok"}

    except Exception as e:
        logger.error(f"Error handling webhook: {e}")
        return {"status": "error", "message": str(e)}


async def process_comment_event(
    messaging: dict,
    db: Session,
    config: "Config",
):
    """Process a comment event and trigger actions if keywords match."""
    try:
        # Extract comment data
        comment_id = messaging.get("object_id", "")
        message_text = messaging.get("message", {}).get("text", "").lower()
        sender_id = messaging.get("from", {}).get("id", "")
        post_id = messaging.get("post_id", "")

        if not all([comment_id, message_text, sender_id, post_id]):
            logger.warning(f"Incomplete comment data: {messaging}")
            return

        # Check if comment already processed
        existing = db.query(ProcessedComment).filter_by(comment_id=comment_id).first()
        if existing:
            logger.info(f"Comment {comment_id} already processed")
            return

        # Find matching campaign
        campaign = db.query(Campaign).filter_by(post_id=post_id, active=True).first()
        if not campaign:
            logger.info(f"No active campaign for post {post_id}")
            return

        # Check if any keyword matches
        keywords = [k.strip().lower() for k in campaign.keywords.split(",")]
        matched = any(keyword in message_text for keyword in keywords)

        if not matched:
            logger.info(f"No keyword match in comment: {message_text}")
            return

        logger.info(f"Keyword match found. Comment: {message_text}, Campaign: {campaign.id}")

        # Reply to comment
        try:
            await reply_to_comment(
                comment_id,
                campaign.comment_reply,
                config.instagram_access_token,
            )
            logger.info(f"Replied to comment {comment_id}")
        except Exception as e:
            logger.error(f"Failed to reply to comment: {e}")

        # Send DM
        try:
            await send_dm(
                sender_id,
                campaign.dm_message,
                config.instagram_business_account_id,
                config.instagram_access_token,
            )
            logger.info(f"Sent DM to user {sender_id}")
        except Exception as e:
            logger.error(f"Failed to send DM: {e}")

        # Record processed comment
        processed_comment = ProcessedComment(
            comment_id=comment_id,
            post_id=post_id,
            instagram_user_id=sender_id,
        )
        db.add(processed_comment)
        db.commit()
        logger.info(f"Recorded processed comment {comment_id}")

    except Exception as e:
        logger.error(f"Error processing comment event: {e}")
        db.rollback()
