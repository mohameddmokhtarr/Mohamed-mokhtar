"""
Configuration Management
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent
RAW_DATA_DIR = PROJECT_ROOT / 'raw-data'
HOOKS_DIR = PROJECT_ROOT / 'hooks'
TRANSCRIPTS_DIR = PROJECT_ROOT / 'transcripts'
ADAPTERS_DIR = PROJECT_ROOT / 'adapters'
REPORTS_DIR = PROJECT_ROOT / 'reports'
LOGS_DIR = PROJECT_ROOT / 'logs'

# API Configuration
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
APIFY_API_TOKEN = os.getenv('APIFY_API_TOKEN')
CLAUDE_MODEL = os.getenv('CLAUDE_MODEL', 'claude-haiku-4-5-20251001')

# System Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
APIFY_TIMEOUT_SECONDS = int(os.getenv('APIFY_TIMEOUT_SECONDS', 3600))

# Apify Actor IDs
APIFY_ACTORS = {
    'tiktok': 'clockworks/free-tiktok-scraper',
    'instagram': 'apify/instagram-reel-scraper',
    'youtube': 'streamers/youtube-scraper'
}

# Content creators to scrape
CREATORS = {
    'my_account': '@mokhtarsays_',
    'competitors': [
        '@abdulosama90',
        '@ai_bilarabi',
        '@mabuzant'
    ]
}

# Platforms
PLATFORMS = ['tiktok', 'instagram']

# Hook classification types
HOOK_TYPES = [
    'curiosity',
    'shock',
    'authority',
    'contrarian',
    'storytelling',
    'fear',
    'aspiration',
    'direct_benefit',
    'mistake_based',
    'comparison'
]

# Tone types
TONE_TYPES = [
    'conversational',
    'authoritative',
    'humorous',
    'urgent',
    'inspirational',
    'informative'
]

# Ensure all directories exist
for directory in [RAW_DATA_DIR, HOOKS_DIR, TRANSCRIPTS_DIR, ADAPTERS_DIR, REPORTS_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
