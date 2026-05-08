#!/usr/bin/env python3
"""
Demo mode - Run system with mock data for testing without real APIs.

Useful for:
- Testing pipeline without Apify/OpenAI API keys
- Demonstrating functionality
- Developing new phases
"""

import json
import random
from pathlib import Path
from datetime import datetime, timedelta
from logger import setup_logger
from config import RAW_DATA_DIR, TRANSCRIPTS_DIR, HOOKS_DIR

logger = setup_logger('demo')

MOCK_HOOKS = [
    "What if I told you everything you know about [topic] is wrong?",
    "This ONE trick changed my entire [field] career",
    "The truth about [claim] nobody wants to admit",
    "Watch what happens when you [action] instead of [alternative]",
    "I learned [lesson] the hard way so you don't have to",
    "⚠️ WARNING: [danger] is more common than you think",
    "How to [achieve goal] in just [timeframe]",
    "Here's why [successful person] does [habit] every day",
    "The biggest mistake people make with [topic]",
    "This [type] method [claim] in just [timeframe]",
]

HOOK_TYPES = ['curiosity', 'shock', 'authority', 'contrarian', 'storytelling',
              'fear', 'aspiration', 'direct_benefit', 'mistake_based', 'comparison']

def generate_mock_raw_data(platform, handle, count=50):
    """Generate mock raw scraped data."""
    data = []
    base_date = datetime.now() - timedelta(days=90)

    for i in range(count):
        upload_date = base_date + timedelta(days=random.randint(0, 90))
        views = random.randint(1000, 500000)

        item = {
            'platform': platform,
            'creator': handle.lstrip('@'),
            'post_id': f"{platform}-{handle}-{i}",
            'url': f'https://{platform}.com/{handle}/{i}',
            'caption': random.choice(MOCK_HOOKS),
            'views': views,
            'likes': int(views * random.uniform(0.01, 0.15)),
            'comments': int(views * random.uniform(0.001, 0.05)),
            'shares': int(views * random.uniform(0.0001, 0.01)),
            'upload_date': upload_date.isoformat(),
            'media_type': 'video',
        }
        data.append(item)

    return data

def generate_mock_hooks(raw_data):
    """Generate mock hooks from raw data."""
    hooks = []

    for item in raw_data:
        hook = {
            'post_id': item['post_id'],
            'platform': item['platform'],
            'url': item['url'],
            'caption': item['caption'],
            'hook_text': item['caption'][:80],  # Simulate extraction
            'source': 'caption',
            'views': item['views'],
            'likes': item['likes'],
            'comments': item['comments'],
            'upload_date': item['upload_date'],
        }
        hooks.append(hook)

    return hooks

def generate_mock_classified(hooks):
    """Generate mock classified hooks."""
    classified = []

    for hook in hooks:
        primary_type = random.choice(HOOK_TYPES)
        confidence = random.uniform(0.6, 0.99)

        classified_hook = {
            **hook,
            'primary_type': primary_type,
            'secondary_types': random.sample(HOOK_TYPES, k=2),
            'confidence': confidence,
            'tone': random.choice(['casual', 'professional', 'enthusiastic', 'dark']),
            'pacing': random.choice(['slow', 'moderate', 'fast']),
            'sentence_length': len(hook['hook_text'].split()),
            'reading_complexity': random.choice(['simple', 'intermediate', 'advanced']),
        }
        classified.append(classified_hook)

    return classified

def setup_demo_data():
    """Generate and save mock data for all phases."""
    logger.info("\n" + "="*60)
    logger.info("🎬 GENERATING DEMO DATA")
    logger.info("="*60)

    accounts = ['@competitor1', '@competitor2', '@myhandle']
    platforms = ['tiktok', 'instagram', 'youtube']

    for platform in platforms:
        for account in accounts:
            # Generate raw data
            raw_data = generate_mock_raw_data(platform, account, count=50)
            raw_file = RAW_DATA_DIR / f"{platform}-{account.lstrip('@')}.json"

            with open(raw_file, 'w') as f:
                json.dump(raw_data, f, indent=2)

            logger.info(f"✅ Generated raw data: {raw_file.name}")

            # Generate hooks
            hooks = generate_mock_hooks(raw_data)
            hooks_file = TRANSCRIPTS_DIR / f"{platform}-{account.lstrip('@')}-hooks.json"

            with open(hooks_file, 'w') as f:
                json.dump(hooks, f, indent=2)

            logger.info(f"✅ Generated hooks: {hooks_file.name}")

            # Generate classified hooks
            classified = generate_mock_classified(hooks)
            classified_file = HOOKS_DIR / f"{platform}-{account.lstrip('@')}-classified.json"

            with open(classified_file, 'w') as f:
                json.dump(classified, f, indent=2, default=str)

            logger.info(f"✅ Generated classified: {classified_file.name}")

    logger.info("\n✅ Demo data generated successfully")
    logger.info("   You can now run phases 4-8 with: python -c \"from phase_4_trends import run_phase_4; run_phase_4()\"")

if __name__ == '__main__':
    setup_demo_data()

    logger.info("\n" + "="*60)
    logger.info("📋 NEXT STEPS")
    logger.info("="*60)
    logger.info("""
To continue with demo:

1. Run trend analysis:
   python -c "from phase_4_trends import run_phase_4; run_phase_4()"

2. Run performance analysis:
   python -c "from phase_5_performance import run_phase_5; run_phase_5()"

3. Build swipe database:
   python -c "from phase_6_swipe_db import run_phase_6; run_phase_6()"

4. Generate HTML report:
   python -c "from phase_7_html_report import run_phase_7; run_phase_7()"

5. Run audit:
   python -c "from phase_8_audit import run_phase_8; run_phase_8()"

Or run all phases 4-8:
   python -c "
from phase_4_trends import run_phase_4
from phase_5_performance import run_phase_5
from phase_6_swipe_db import run_phase_6
from phase_7_html_report import run_phase_7
from phase_8_audit import run_phase_8
run_phase_4()
run_phase_5()
run_phase_6()
run_phase_7()
run_phase_8()
"
    """)
