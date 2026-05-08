"""Phase 1: Scrape content from social media platforms."""

import json
from pathlib import Path
from datetime import datetime
from apify_wrapper import ApifyClient, ApifyError, verify_actor_exists
from logger import setup_logger
from config import (
    RAW_DATA_DIR, APIFY_ACTORS, COMPETITORS, MY_ACCOUNT, PLATFORMS
)

logger = setup_logger('phase_1_scraper')

def scrape_platform(platform, handles):
    """
    Scrape content from a platform for given handles.

    Args:
        platform: Platform name ('tiktok', 'instagram', 'youtube')
        handles: List of creator handles to scrape

    Returns:
        List of scraped items
    """
    if platform not in APIFY_ACTORS:
        logger.error(f"Unsupported platform: {platform}")
        return []

    actor_id = APIFY_ACTORS[platform]

    # Verify actor exists
    if not verify_actor_exists(actor_id):
        logger.error(f"Actor not found: {actor_id}. Skipping {platform}")
        return []

    client = ApifyClient()
    all_results = []

    for handle in handles:
        logger.info(f"Scraping {platform} for {handle}...")

        # Build input based on platform
        input_data = _build_input(platform, handle)

        try:
            results = client.run_actor(actor_id, input_data)
            logger.info(f"✅ Scraped {len(results)} items from {handle}")

            # Log raw response before processing
            raw_file = RAW_DATA_DIR / f"{platform}-{handle.replace('@', '')}-raw.json"
            with open(raw_file, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            logger.info(f"Raw data saved: {raw_file}")

            all_results.extend(results)

        except ApifyError as e:
            logger.error(f"Scraping failed for {handle}: {e}")
            logger.error(f"Skipping {handle}, continuing with others")
            continue

    return all_results

def _build_input(platform, handle):
    """Build actor input based on platform."""
    handle = handle.lstrip('@')

    if platform == 'tiktok':
        return {
            'hashtags': [],
            'usernames': [handle],
            'urls': [],
            'resultsLimit': 100,
            'resultsType': 'posts',
        }
    elif platform == 'instagram':
        return {
            'usernames': [handle],
            'postsLimit': 100,
        }
    elif platform == 'youtube':
        return {
            'channelUrl': f'https://www.youtube.com/@{handle}',
            'videosLimit': 100,
        }

    return {}

def normalize_item(item, platform):
    """
    Normalize scraped item to standard schema.

    Args:
        item: Raw scraped item
        platform: Platform name

    Returns:
        Normalized item dict
    """
    normalized = {
        'platform': platform,
        'creator': item.get('creator', item.get('author', item.get('channelName', ''))),
        'post_id': item.get('id', item.get('postId', item.get('videoId', ''))),
        'url': item.get('url', item.get('link', '')),
        'caption': item.get('caption', item.get('description', item.get('title', ''))),
        'views': int(item.get('views', item.get('viewCount', 0)) or 0),
        'likes': int(item.get('likes', item.get('likeCount', 0)) or 0),
        'comments': int(item.get('comments', item.get('commentCount', 0)) or 0),
        'shares': int(item.get('shares', item.get('shareCount', 0)) or 0),
        'upload_date': item.get('createDate', item.get('publishedDate', item.get('createdAt', ''))),
        'media_type': 'video',
    }

    # Validate required fields
    if not normalized['post_id']:
        logger.warning(f"Missing post_id in item: {item}")
    if not normalized['url']:
        logger.warning(f"Missing URL in item: {item}")

    return normalized

def save_normalized_data(platform, handle, items):
    """Save normalized data to file."""
    if not items:
        logger.warning(f"No items to save for {platform}-{handle}")
        return None

    normalized = [normalize_item(item, platform) for item in items]

    output_file = RAW_DATA_DIR / f"{platform}-{handle.replace('@', '')}.json"
    with open(output_file, 'w') as f:
        json.dump(normalized, f, indent=2, default=str)

    logger.info(f"Normalized data saved: {output_file}")
    return output_file

def run_phase_1():
    """Execute Phase 1: Content Scraping."""
    logger.info("="*60)
    logger.info("PHASE 1: SCRAPE CONTENT")
    logger.info("="*60)

    handles = COMPETITORS + [MY_ACCOUNT]
    all_data = {}

    for platform in PLATFORMS:
        logger.info(f"\nScraping {platform.upper()}...")
        platform_data = scrape_platform(platform, handles)

        if platform_data:
            for handle in handles:
                handle_items = [
                    item for item in platform_data
                    if item.get('creator', '').lower() == handle.lstrip('@').lower()
                    or item.get('author', '').lower() == handle.lstrip('@').lower()
                ]
                if handle_items:
                    save_normalized_data(platform, handle, handle_items)
                    all_data[f"{platform}-{handle}"] = handle_items

    logger.info(f"\n✅ Phase 1 complete: Scraped {len(all_data)} datasets")
    return all_data

if __name__ == '__main__':
    run_phase_1()
