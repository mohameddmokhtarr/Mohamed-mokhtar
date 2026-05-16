"""
Viral Hook Intelligence System
Production-grade content hook analysis pipeline
"""

__version__ = '1.0.0'
__author__ = 'Content Intelligence Team'

from config import (
    ANTHROPIC_API_KEY,
    APIFY_API_TOKEN,
    CLAUDE_MODEL,
    PLATFORMS,
    CREATORS
)

__all__ = [
    'ANTHROPIC_API_KEY',
    'APIFY_API_TOKEN',
    'CLAUDE_MODEL',
    'PLATFORMS',
    'CREATORS'
]
