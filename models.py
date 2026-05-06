from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Config(Base):
    __tablename__ = "config"

    id = Column(Integer, primary_key=True)
    instagram_access_token = Column(String, nullable=False)
    instagram_business_account_id = Column(String, nullable=False)
    facebook_page_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Campaign(Base):
    __tablename__ = "campaign"

    id = Column(Integer, primary_key=True)
    post_id = Column(String, nullable=False, unique=True)
    post_caption = Column(String, nullable=True)
    post_media_url = Column(String, nullable=True)
    keywords = Column(Text, nullable=False)  # comma-separated
    comment_reply = Column(Text, nullable=False)
    dm_message = Column(Text, nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ProcessedComment(Base):
    __tablename__ = "processed_comment"

    id = Column(Integer, primary_key=True)
    comment_id = Column(String, unique=True, nullable=False)
    post_id = Column(String, nullable=False)
    instagram_user_id = Column(String, nullable=False)
    processed_at = Column(DateTime, default=datetime.utcnow)
