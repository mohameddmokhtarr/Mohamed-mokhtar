"""
Phase 1: Content Scraping
Scrape TikTok and Instagram Reels using Apify actors
"""
import json
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
import requests

from config import (
    APIFY_API_TOKEN, APIFY_ACTORS, CREATORS,
    RAW_DATA_DIR, APIFY_TIMEOUT_SECONDS, PLATFORMS
)
from logger import scraper_logger, error_logger
from adapters import DataNormalizer


class ContentScraper:
    """Scrape content from social platforms using Apify actors"""

    def __init__(self):
        self.base_url = 'https://api.apify.com/v2'
        self.headers = {
            'Authorization': f'Bearer {APIFY_API_TOKEN}',
            'Content-Type': 'application/json'
        }
        self.scraped_videos = {}
        self.errors = []

    def scrape_platform(self, platform: str, handles: List[str]) -> Dict[str, Any]:
        """Scrape multiple handles from a platform"""
        scraper_logger.info(f"[{platform.upper()}] Starting scrape for {len(handles)} handles")

        actor_id = APIFY_ACTORS[platform]
        platform_data = {}

        for handle in handles:
            scraper_logger.info(f"[{platform.upper()}] Scraping {handle}...")
            try:
                videos = self._run_actor(actor_id, platform, handle)
                platform_data[handle] = videos
                scraper_logger.info(
                    f"[{platform.upper()}] ✓ {handle} — {len(videos)} videos scraped"
                )
            except Exception as e:
                error_msg = f"[{platform.upper()}] ✗ {handle} failed: {str(e)}"
                scraper_logger.error(error_msg)
                error_logger.error(error_msg)
                self.errors.append({'handle': handle, 'platform': platform, 'error': str(e)})
                continue

        return platform_data

    def _run_actor(self, actor_id: str, platform: str, handle: str) -> List[Dict[str, Any]]:
        """Run Apify actor and return normalized results"""
        # Create actor run
        run_url = f"{self.base_url}/acts/{actor_id}/runs"

        input_data = self._get_actor_input(platform, handle)
        scraper_logger.info(f"  Sending request to Apify...")

        response = requests.post(
            run_url,
            json={'input': input_data},
            headers=self.headers,
            timeout=30
        )

        if response.status_code not in [200, 201]:
            raise Exception(f"Apify API error: {response.status_code} - {response.text}")

        run_data = response.json()
        run_id = run_data['data']['id']
        scraper_logger.info(f"  Actor run started: {run_id}")

        # Wait for run to complete
        results = self._wait_for_actor_completion(run_id, actor_id, platform)
        return results

    def _wait_for_actor_completion(self, run_id: str, actor_id: str, platform: str) -> List[Dict]:
        """Poll actor until completion and fetch results"""
        url = f"{self.base_url}/acts/{actor_id}/runs/{run_id}"
        start_time = time.time()

        while time.time() - start_time < APIFY_TIMEOUT_SECONDS:
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code != 200:
                raise Exception(f"Failed to get run status: {response.status_code}")

            run = response.json()['data']
            status = run['status']

            if status == 'SUCCEEDED':
                scraper_logger.info(f"  Actor completed successfully")
                return self._fetch_results(run_id, actor_id, platform)

            elif status in ['FAILED', 'ABORTED']:
                raise Exception(f"Actor run {status}: {run.get('statusMessage', 'Unknown error')}")

            scraper_logger.info(f"  Waiting... (status: {status})")
            time.sleep(5)

        raise Exception(f"Actor run timeout after {APIFY_TIMEOUT_SECONDS}s")

    def _fetch_results(self, run_id: str, actor_id: str, platform: str) -> List[Dict]:
        """Fetch dataset results from completed actor run"""
        url = f"{self.base_url}/acts/{actor_id}/runs/{run_id}/dataset/items"

        response = requests.get(url, headers=self.headers, timeout=30)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch results: {response.status_code}")

        items = response.json()
        normalized = []

        for item in items:
            try:
                normalized_item = DataNormalizer.normalize(platform, item)
                normalized.append(normalized_item)
            except Exception as e:
                error_logger.error(f"Failed to normalize item from {platform}: {str(e)}")
                continue

        return normalized

    def _get_actor_input(self, platform: str, handle: str) -> Dict[str, Any]:
        """Get input configuration for each platform's actor"""
        clean_handle = handle.lstrip('@')

        if platform == 'tiktok':
            return {
                'startUrls': [{'url': f'https://www.tiktok.com/@{clean_handle}'}],
                'maxItems': 100,
                'downloadVideos': False,
                'downloadCovers': False
            }
        elif platform == 'instagram':
            return {
                'startUrls': [{'url': f'https://www.instagram.com/{clean_handle}/'}],
                'maxItems': 100,
                'downloadVideos': False
            }
        elif platform == 'youtube':
            return {
                'channelUrls': [f'https://www.youtube.com/@{clean_handle}'],
                'maxItems': 100
            }
        else:
            raise ValueError(f"Unknown platform: {platform}")

    def save_raw_data(self, platform: str, handle: str, data: List[Dict]):
        """Save raw scraped data to JSON file"""
        filename = RAW_DATA_DIR / f"{platform}-{handle.lstrip('@')}.json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'platform': platform,
                'handle': handle,
                'scraped_at': datetime.now().isoformat(),
                'count': len(data),
                'videos': data
            }, f, indent=2, ensure_ascii=False)

        scraper_logger.info(f"  Saved {len(data)} items to {filename}")
        return filename

    def run(self) -> Dict[str, Any]:
        """Run Phase 1: Scrape all platforms"""
        scraper_logger.info("="*60)
        scraper_logger.info("PHASE 1: CONTENT SCRAPING")
        scraper_logger.info("="*60)

        all_data = {}
        stats = {
            'total_videos': 0,
            'handles_completed': 0,
            'handles_failed': 0,
            'platforms': {}
        }

        # Scrape my account
        for platform in PLATFORMS:
            my_handle = CREATORS['my_account']
            scraper_logger.info(f"\nScraping MY ACCOUNT (@mokhtarsays_)")
            platform_data = self.scrape_platform(platform, [my_handle])

            for handle, videos in platform_data.items():
                self.save_raw_data(platform, handle, videos)
                all_data[f"{platform}:{handle}"] = videos
                stats['total_videos'] += len(videos)
                stats['handles_completed'] += 1

                if platform not in stats['platforms']:
                    stats['platforms'][platform] = {}
                stats['platforms'][platform][handle] = len(videos)

        # Scrape competitors
        scraper_logger.info(f"\nScraping COMPETITORS")
        for platform in PLATFORMS:
            competitors = CREATORS['competitors']
            platform_data = self.scrape_platform(platform, competitors)

            for handle, videos in platform_data.items():
                self.save_raw_data(platform, handle, videos)
                all_data[f"{platform}:{handle}"] = videos
                stats['total_videos'] += len(videos)
                stats['handles_completed'] += 1

                if platform not in stats['platforms']:
                    stats['platforms'][platform] = {}
                stats['platforms'][platform][handle] = len(videos)

        stats['handles_failed'] = len(self.errors)

        scraper_logger.info("\n" + "="*60)
        scraper_logger.info("PHASE 1 COMPLETE")
        scraper_logger.info("="*60)
        scraper_logger.info(f"Total videos: {stats['total_videos']}")
        scraper_logger.info(f"Handles completed: {stats['handles_completed']}")
        scraper_logger.info(f"Handles failed: {stats['handles_failed']}")

        if self.errors:
            scraper_logger.warning(f"\nErrors encountered:")
            for error in self.errors:
                scraper_logger.warning(f"  • {error['platform']}: {error['handle']} - {error['error']}")

        return {
            'data': all_data,
            'stats': stats,
            'errors': self.errors
        }


def main():
    """Run Phase 1"""
    scraper = ContentScraper()
    result = scraper.run()
    return result


if __name__ == '__main__':
    main()
