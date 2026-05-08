"""Phase 4: Analyze viral trends in hook usage."""

import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
from logger import setup_logger
from config import HOOKS_DIR, RAW_DATA_DIR, EMERGING_ENGAGEMENT_INCREASE, TIME_BUCKETS

logger = setup_logger('phase_4_trends')

def parse_date(date_str):
    """Parse ISO date string to datetime."""
    if not date_str:
        return None

    try:
        # Try ISO format
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except:
        try:
            # Try alternative formats
            return datetime.strptime(date_str[:10], '%Y-%m-%d')
        except:
            logger.warning(f"Could not parse date: {date_str}")
            return None

def get_time_bucket(upload_date):
    """
    Determine time bucket for a date.

    Args:
        upload_date: Date string or datetime

    Returns:
        Bucket key: 'last_30_days', 'days_31_90', or 'days_91_plus'
    """
    if isinstance(upload_date, str):
        date = parse_date(upload_date)
    else:
        date = upload_date

    if not date:
        return None

    # Make date naive if it has timezone
    if date.tzinfo:
        date = date.replace(tzinfo=None)

    today = datetime.now()
    days_ago = (today - date).days

    if days_ago <= 30:
        return 'last_30_days'
    elif days_ago <= 90:
        return 'days_31_90'
    else:
        return 'days_91_plus'

def calculate_engagement(hook_data):
    """Calculate engagement metric (views + likes + comments)."""
    views = hook_data.get('views', 0) or 0
    likes = hook_data.get('likes', 0) or 0
    comments = hook_data.get('comments', 0) or 0

    return max(views, likes + comments)  # Use views if available, else engagement sum

def analyze_hook_trends(classified_hooks):
    """
    Analyze trends in hook types across time buckets.

    Args:
        classified_hooks: List of classified hook dicts

    Returns:
        Trend analysis dict
    """
    trends = {
        'last_30_days': defaultdict(list),
        'days_31_90': defaultdict(list),
        'days_91_plus': defaultdict(list),
    }

    # Organize hooks by time bucket and type
    for hook in classified_hooks:
        bucket = get_time_bucket(hook.get('upload_date'))
        if not bucket:
            continue

        hook_type = hook.get('primary_type', 'unknown')
        engagement = calculate_engagement(hook)

        trends[bucket][hook_type].append({
            'post_id': hook.get('post_id'),
            'engagement': engagement,
            'confidence': hook.get('confidence', 0),
        })

    # Calculate statistics per type per bucket
    analysis = {}
    for hook_type in ['curiosity', 'shock', 'authority', 'contrarian', 'storytelling',
                       'fear', 'aspiration', 'direct_benefit', 'mistake_based', 'comparison']:
        analysis[hook_type] = {}

        for bucket in ['last_30_days', 'days_31_90', 'days_91_plus']:
            items = trends[bucket][hook_type]

            if items:
                avg_engagement = sum(i['engagement'] for i in items) / len(items)
                frequency = len(items)

                analysis[hook_type][bucket] = {
                    'count': frequency,
                    'avg_engagement': avg_engagement,
                    'median_confidence': sorted(
                        [i['confidence'] for i in items]
                    )[len(items)//2] if items else 0,
                }
            else:
                analysis[hook_type][bucket] = {
                    'count': 0,
                    'avg_engagement': 0,
                    'median_confidence': 0,
                }

    return analysis

def find_emerging_hooks(trend_analysis):
    """
    Identify emerging hook types based on frequency and engagement trends.

    Rules:
    - Hook frequency increases across time buckets (91+ → 31-90 → 30)
    - Engagement rises ≥30%

    Returns:
        List of emerging hook types
    """
    emerging = []

    for hook_type, buckets in trend_analysis.items():
        data_91 = buckets.get('days_91_plus', {})
        data_31_90 = buckets.get('days_31_90', {})
        data_30 = buckets.get('last_30_days', {})

        count_91 = data_91.get('count', 0)
        count_31_90 = data_31_90.get('count', 0)
        count_30 = data_30.get('count', 0)

        eng_91 = data_91.get('avg_engagement', 0)
        eng_31_90 = data_31_90.get('avg_engagement', 0)
        eng_30 = data_30.get('avg_engagement', 0)

        # Check frequency increase
        freq_increasing = (count_91 < count_31_90 < count_30)

        # Check engagement increase
        eng_increase = 0
        if eng_91 > 0:
            eng_increase = (eng_30 - eng_91) / eng_91

        is_emerging = freq_increasing and eng_increase >= EMERGING_ENGAGEMENT_INCREASE

        if is_emerging:
            emerging.append({
                'hook_type': hook_type,
                'frequency_trend': f"{count_91} → {count_31_90} → {count_30}",
                'engagement_increase': f"{eng_increase*100:.1f}%",
                'current_avg_engagement': eng_30,
            })

    return sorted(emerging, key=lambda x: x['engagement_increase'], reverse=True)

def run_phase_4():
    """Execute Phase 4: Trend Analysis."""
    logger.info("="*60)
    logger.info("PHASE 4: TREND ANALYSIS")
    logger.info("="*60)

    all_trends = {}
    all_emerging = []

    # Find all classified hooks files
    hooks_files = list(HOOKS_DIR.glob('*-classified.json'))

    for hooks_file in hooks_files:
        # Parse filename
        parts = hooks_file.stem.replace('-classified', '').split('-', 1)
        if len(parts) != 2:
            continue

        platform, handle = parts
        logger.info(f"\nAnalyzing trends: {platform} (@{handle})...")

        with open(hooks_file, 'r') as f:
            classified_hooks = json.load(f)

        if not classified_hooks:
            logger.warning(f"No classified hooks for {platform}-{handle}")
            continue

        trend_analysis = analyze_hook_trends(classified_hooks)
        emerging = find_emerging_hooks(trend_analysis)

        all_trends[f"{platform}-{handle}"] = {
            'analysis': trend_analysis,
            'emerging': emerging,
        }

        if emerging:
            logger.info(f"  ✅ Found {len(emerging)} emerging hook types:")
            for item in emerging:
                logger.info(f"    - {item['hook_type']}: {item['engagement_increase']}")
        else:
            logger.info(f"  No emerging trends detected")

        all_emerging.extend(emerging)

    # Save trend report
    trend_report_file = HOOKS_DIR / 'trend-analysis.json'
    with open(trend_report_file, 'w') as f:
        json.dump({
            'per_dataset': all_trends,
            'all_emerging': all_emerging,
        }, f, indent=2, default=str)

    logger.info(f"\n✅ Phase 4 complete: Trend analysis saved")
    return all_trends

if __name__ == '__main__':
    run_phase_4()
