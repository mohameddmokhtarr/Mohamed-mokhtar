import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from models import Config, Campaign
from instagram import get_post_details

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["api"])


class ConfigCreate(BaseModel):
    instagram_access_token: str
    instagram_business_account_id: str
    facebook_page_id: str | None = None


class CampaignCreate(BaseModel):
    post_id: str
    keywords: str
    comment_reply: str
    dm_message: str


class CampaignUpdate(BaseModel):
    keywords: str | None = None
    comment_reply: str | None = None
    dm_message: str | None = None
    active: bool | None = None


@router.post("/config")
async def save_config(config: ConfigCreate, db: Session = Depends(get_db)):
    """Save or update Instagram configuration."""
    existing = db.query(Config).first()

    if existing:
        existing.instagram_access_token = config.instagram_access_token
        existing.instagram_business_account_id = config.instagram_business_account_id
        existing.facebook_page_id = config.facebook_page_id
        db.commit()
        logger.info("Config updated")
        return {"status": "updated", "config": existing}
    else:
        new_config = Config(**config.dict())
        db.add(new_config)
        db.commit()
        logger.info("Config created")
        return {"status": "created", "config": new_config}


@router.get("/config")
async def get_config(db: Session = Depends(get_db)):
    """Get current Instagram configuration."""
    config = db.query(Config).first()
    if not config:
        return None
    return {
        "id": config.id,
        "instagram_business_account_id": config.instagram_business_account_id,
        "facebook_page_id": config.facebook_page_id,
    }


@router.post("/campaigns")
async def create_campaign(
    campaign: CampaignCreate, db: Session = Depends(get_db)
):
    """Create a new campaign."""
    config = db.query(Config).first()
    if not config:
        raise HTTPException(status_code=400, detail="Please configure Instagram credentials first")

    # Fetch post details
    try:
        post_details = await get_post_details(
            campaign.post_id, config.instagram_access_token
        )
    except Exception as e:
        logger.error(f"Failed to fetch post details: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to fetch post details: {str(e)}")

    new_campaign = Campaign(
        post_id=campaign.post_id,
        keywords=campaign.keywords,
        comment_reply=campaign.comment_reply,
        dm_message=campaign.dm_message,
        post_caption=post_details.get("caption", ""),
        post_media_url=post_details.get("media_url", ""),
    )
    db.add(new_campaign)
    db.commit()
    logger.info(f"Campaign created for post {campaign.post_id}")
    return new_campaign


@router.get("/campaigns")
async def list_campaigns(db: Session = Depends(get_db)):
    """List all campaigns."""
    campaigns = db.query(Campaign).all()
    return campaigns


@router.get("/campaigns/{campaign_id}")
async def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    """Get a specific campaign."""
    campaign = db.query(Campaign).filter_by(id=campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign


@router.put("/campaigns/{campaign_id}")
async def update_campaign(
    campaign_id: int,
    updates: CampaignUpdate,
    db: Session = Depends(get_db),
):
    """Update a campaign."""
    campaign = db.query(Campaign).filter_by(id=campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    if updates.keywords:
        campaign.keywords = updates.keywords
    if updates.comment_reply:
        campaign.comment_reply = updates.comment_reply
    if updates.dm_message:
        campaign.dm_message = updates.dm_message
    if updates.active is not None:
        campaign.active = updates.active

    db.commit()
    logger.info(f"Campaign {campaign_id} updated")
    return campaign


@router.delete("/campaigns/{campaign_id}")
async def delete_campaign(campaign_id: int, db: Session = Depends(get_db)):
    """Delete a campaign."""
    campaign = db.query(Campaign).filter_by(id=campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    db.delete(campaign)
    db.commit()
    logger.info(f"Campaign {campaign_id} deleted")
    return {"status": "deleted"}


@router.post("/campaigns/{campaign_id}/toggle")
async def toggle_campaign(campaign_id: int, db: Session = Depends(get_db)):
    """Toggle campaign active status."""
    campaign = db.query(Campaign).filter_by(id=campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    campaign.active = not campaign.active
    db.commit()
    logger.info(f"Campaign {campaign_id} toggled to {campaign.active}")
    return campaign
