"""Global configuration for Viral Hook Intelligence System."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Paths
BASE_DIR = Path(__file__).parent
RAW_DATA_DIR = BASE_DIR / "raw-data"
HOOKS_DIR = BASE_DIR / "hooks"
TRANSCRIPTS_DIR = BASE_DIR / "transcripts"
ADAPTERS_DIR = BASE_DIR / "adapters"
REPORTS_DIR = BASE_DIR / "reports"
ERRORS_LOG = BASE_DIR / "errors.log"

# Ensure directories exist
for dir_path in [RAW_DATA_DIR, HOOKS_DIR, TRANSCRIPTS_DIR, ADAPTERS_DIR, REPORTS_DIR]:
    dir_path.mkdir(exist_ok=True)

# API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
APIFY_API_KEY = os.getenv('APIFY_API_KEY')

# Settings
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
NUM_WORKERS = int(os.getenv('NUM_WORKERS', 4))
RATE_LIMIT_PAUSE = int(os.getenv('RATE_LIMIT_PAUSE', 60))

# Apify Actors (exact IDs - DO NOT CHANGE)
APIFY_ACTORS = {
    'tiktok': 'clockworks/free-tiktok-scraper',
    'instagram': 'apify/instagram-reel-scraper',
    'youtube': 'streamers/youtube-scraper',
}

# Social media platforms
PLATFORMS = ['tiktok', 'instagram', 'youtube']

# Test accounts
COMPETITORS = ['@competitor1', '@competitor2', '@competitor3']
MY_ACCOUNT = '@myhandle'

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

# Time buckets for trend analysis (days)
TIME_BUCKETS = {
    'last_30_days': 30,
    'days_31_90': (31, 90),
    'days_91_plus': 91,
}

# Minimum dataset threshold
MIN_DATASET_SIZE = 20

# Outlier definition
OUTLIER_THRESHOLD = 2.0  # >=2x local median
OUTLIER_WINDOW = 5  # 5 before + 5 after

# Performance trending
EMERGING_ENGAGEMENT_INCREASE = 0.30  # >=30% increase

# Report generation
TOP_HOOKS_COUNT = 100

# Normalized schema
NORMALIZED_SCHEMA = {
    'platform': str,
    'creator': str,
    'post_id': str,
    'url': str,
    'caption': str,
    'views': int,
    'likes': int,
    'comments': int,
    'shares': int,
    'upload_date': str,
    'media_type': str,
}
