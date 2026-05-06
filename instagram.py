import asyncio
import httpx
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

GRAPH_API_VERSION = "v18.0"
BASE_URL = f"https://graph.instagram.com/{GRAPH_API_VERSION}"


async def reply_to_comment(
    comment_id: str, message: str, access_token: str
) -> Dict[str, Any]:
    """Reply to an Instagram comment using Graph API."""
    url = f"{BASE_URL}/{comment_id}/replies"
    params = {"message": message, "access_token": access_token}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, params=params, timeout=10)
            response.raise_for_status()
            logger.info(f"Replied to comment {comment_id}: {response.json()}")
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to reply to comment {comment_id}: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error replying to comment {comment_id}: {e}")
            raise


async def send_dm(
    instagram_user_id: str, message: str, business_account_id: str, access_token: str
) -> Dict[str, Any]:
    """Send a DM to an Instagram user using Graph API.

    Note: The user must have previously messaged the business account,
    or the business must have instagram_manage_messages permission approved.
    """
    url = f"{BASE_URL}/{business_account_id}/messages"
    data = {
        "recipient": {"id": instagram_user_id},
        "message": {"text": message},
        "access_token": access_token,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=data, timeout=10)
            response.raise_for_status()
            logger.info(f"Sent DM to user {instagram_user_id}: {response.json()}")
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to send DM to user {instagram_user_id}: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error sending DM to user {instagram_user_id}: {e}")
            raise


async def get_post_details(
    post_id: str, access_token: str
) -> Dict[str, Any]:
    """Fetch post details including caption and media URL."""
    url = f"{BASE_URL}/{post_id}"
    params = {
        "fields": "caption,media_type,media_url,timestamp",
        "access_token": access_token,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Failed to fetch post details for {post_id}: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error fetching post details for {post_id}: {e}")
            raise
