"""Phase 5: Performance analysis - identify outliers and patterns."""

import json
from pathlib import Path
from statistics import median, mean
from logger import setup_logger
from config import HOOKS_DIR, RAW_DATA_DIR, OUTLIER_THRESHOLD, OUTLIER_WINDOW

logger = setup_logger('phase_5_performance')

def find_outliers(items, window=5):
    """
    Find outlier videos using local median comparison.

    Outlier definition:
    - Compare video against 5 before + 5 after by upload_date
    - If >=2x local median views: mark as outlier

    Args:
        items: List of items sorted by date
        window: Number of items before/after to compare

    Returns:
        List of (index, outlier_data) tuples
    """
    outliers = []

    # Sort by views (for analysis)
    items_with_idx = [(i, item) for i, item in enumerate(items)]

    for idx, item in items_with_idx:
        # Get window: 5 before + item + 5 after
        start = max(0, idx - window)
        end = min(len(items), idx + window + 1)
        window_items = items[start:end]

        views = [i.get('views', 0) or 0 for i in window_items]
        if not views or len(views) < 3:
            continue

        local_median = median(views)

        item_views = item.get('views', 0) or 0

        if local_median > 0 and item_views >= local_median * OUTLIER_THRESHOLD:
            outliers.append({
                'post_id': item.get('post_id'),
                'platform': item.get('platform'),
                'views': item_views,
                'local_median': local_median,
                'multiplier': item_views / local_median,
                'hook_type': item.get('primary_type', 'unknown'),
            })

    return outliers

def calculate_performance_by_hook_type(classified_hooks):
    """
    Calculate average performance by hook type.

    Args:
        classified_hooks: List of classified hooks

    Returns:
        Performance dict
    """
    by_type = {}

    for hook in classified_hooks:
        hook_type = hook.get('primary_type', 'unknown')

        if hook_type not in by_type:
            by_type[hook_type] = {
                'count': 0,
                'views': [],
                'likes': [],
                'comments': [],
                'engagement': [],
            }

        views = hook.get('views', 0) or 0
        likes = hook.get('likes', 0) or 0
        comments = hook.get('comments', 0) or 0
        engagement = max(views, likes + comments)

        by_type[hook_type]['count'] += 1
        by_type[hook_type]['views'].append(views)
        by_type[hook_type]['likes'].append(likes)
        by_type[hook_type]['comments'].append(comments)
        by_type[hook_type]['engagement'].append(engagement)

    # Calculate averages
    performance = {}
    for hook_type, data in by_type.items():
        performance[hook_type] = {
            'count': data['count'],
            'avg_views': round(mean(data['views'])) if data['views'] else 0,
            'avg_likes': round(mean(data['likes'])) if data['likes'] else 0,
            'avg_comments': round(mean(data['comments'])) if data['comments'] else 0,
            'avg_engagement': round(mean(data['engagement'])) if data['engagement'] else 0,
        }

    return performance

def run_phase_5():
    """Execute Phase 5: Performance Analysis."""
    logger.info("="*60)
    logger.info("PHASE 5: PERFORMANCE ANALYSIS")
    logger.info("="*60)

    all_analysis = {}

    # Find all classified hooks files
    hooks_files = list(HOOKS_DIR.glob('*-classified.json'))

    for hooks_file in hooks_files:
        # Parse filename
        parts = hooks_file.stem.replace('-classified', '').split('-', 1)
        if len(parts) != 2:
            continue

        platform, handle = parts
        logger.info(f"\nAnalyzing performance: {platform} (@{handle})...")

        with open(hooks_file, 'r') as f:
            classified_hooks = json.load(f)

        if not classified_hooks:
            logger.warning(f"No classified hooks for {platform}-{handle}")
            continue

        # Sort by upload date for outlier detection
        sorted_hooks = sorted(
            classified_hooks,
            key=lambda x: x.get('upload_date', '') or ''
        )

        # Find outliers
        outliers = find_outliers(sorted_hooks)

        # Calculate performance by hook type
        performance = calculate_performance_by_hook_type(classified_hooks)

        analysis = {
            'total_videos': len(classified_hooks),
            'outlier_count': len(outliers),
            'outlier_rate': round(len(outliers) / len(classified_hooks), 3) if classified_hooks else 0,
            'outliers': outliers,
            'performance_by_type': performance,
        }

        all_analysis[f"{platform}-{handle}"] = analysis

        logger.info(f"  Total videos: {analysis['total_videos']}")
        logger.info(f"  Outliers found: {analysis['outlier_count']} ({analysis['outlier_rate']*100:.1f}%)")
        logger.info(f"  Hook types: {len(performance)}")

    # Save performance report
    performance_file = HOOKS_DIR / 'performance-analysis.json'
    with open(performance_file, 'w') as f:
        json.dump(all_analysis, f, indent=2, default=str)

    logger.info(f"\n✅ Phase 5 complete: Performance analysis saved")
    return all_analysis

if __name__ == '__main__':
    run_phase_5()
