"""Apify API wrapper for social media scraping."""

import requests
import time
import json
from logger import setup_logger
from config import APIFY_API_KEY, APIFY_ACTORS, RATE_LIMIT_PAUSE

logger = setup_logger('apify_wrapper')

class ApifyError(Exception):
    """Custom exception for Apify errors."""
    pass

class ApifyClient:
    """Client for interacting with Apify API."""

    def __init__(self, api_key=None):
        """Initialize Apify client."""
        self.api_key = api_key or APIFY_API_KEY
        self.base_url = "https://api.apify.com/v2"
        if not self.api_key:
            raise ValueError("APIFY_API_KEY not set in environment")

    def run_actor(self, actor_id, input_data, max_retries=3):
        """
        Run an actor and wait for results.

        Args:
            actor_id: Actor ID (e.g., 'clockworks/free-tiktok-scraper')
            input_data: Input parameters for the actor
            max_retries: Number of retries on rate limit

        Returns:
            List of results from the actor run
        """
        logger.info(f"Starting actor run: {actor_id}")

        # Create run
        run_url = f"{self.base_url}/acts/{actor_id}/runs"
        headers = {'Content-Type': 'application/json'}
        params = {'token': self.api_key}

        for attempt in range(max_retries):
            try:
                response = requests.post(
                    run_url,
                    json=input_data,
                    headers=headers,
                    params=params,
                    timeout=30
                )

                if response.status_code == 429:  # Rate limit
                    logger.warning(f"Rate limited. Waiting {RATE_LIMIT_PAUSE}s before retry {attempt + 1}/{max_retries}")
                    time.sleep(RATE_LIMIT_PAUSE)
                    continue

                response.raise_for_status()
                run_data = response.json()
                run_id = run_data['data']['id']
                logger.info(f"Actor run created: {run_id}")
                break

            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    logger.error(f"Failed to create actor run after {max_retries} attempts: {e}")
                    raise ApifyError(f"Actor creation failed: {e}")
                logger.warning(f"Attempt {attempt + 1} failed, retrying...")
                time.sleep(RATE_LIMIT_PAUSE)

        # Wait for completion
        return self._wait_for_run(run_id)

    def _wait_for_run(self, run_id, check_interval=5, timeout=3600):
        """
        Wait for actor run to complete and fetch results.

        Args:
            run_id: ID of the actor run
            check_interval: Seconds between status checks
            timeout: Maximum seconds to wait

        Returns:
            List of results
        """
        run_url = f"{self.base_url}/runs/{run_id}"
        params = {'token': self.api_key}
        elapsed = 0

        while elapsed < timeout:
            response = requests.get(run_url, params=params, timeout=10)
            response.raise_for_status()
            run_data = response.json()['data']

            status = run_data.get('status')
            logger.info(f"Run {run_id} status: {status}")

            if status == 'SUCCEEDED':
                logger.info(f"Actor run completed successfully")
                return self._fetch_results(run_id)
            elif status == 'FAILED':
                error = run_data.get('exitCode', 'Unknown error')
                logger.error(f"Actor run failed with exit code: {error}")
                raise ApifyError(f"Actor run failed: {error}")
            elif status in ['ABORTED', 'TIMED-OUT']:
                logger.error(f"Actor run {status}")
                raise ApifyError(f"Actor run {status}")

            time.sleep(check_interval)
            elapsed += check_interval

        raise ApifyError(f"Actor run timeout after {timeout}s")

    def _fetch_results(self, run_id):
        """
        Fetch dataset results from completed run.

        Args:
            run_id: ID of the completed run

        Returns:
            List of results
        """
        run_url = f"{self.base_url}/runs/{run_id}"
        params = {'token': self.api_key}

        response = requests.get(run_url, params=params, timeout=10)
        response.raise_for_status()
        run_data = response.json()['data']

        dataset_id = run_data.get('defaultDatasetId')
        if not dataset_id:
            logger.warning(f"No dataset found for run {run_id}")
            return []

        # Fetch dataset items
        dataset_url = f"{self.base_url}/datasets/{dataset_id}/items"
        results = []
        offset = 0
        limit = 1000

        while True:
            response = requests.get(
                dataset_url,
                params={'token': self.api_key, 'offset': offset, 'limit': limit},
                timeout=30
            )
            response.raise_for_status()
            items = response.json()

            if not items:
                break

            results.extend(items)
            offset += limit

            if len(items) < limit:
                break

        logger.info(f"Fetched {len(results)} results from dataset")
        return results

def verify_actor_exists(actor_id):
    """
    Verify that an actor exists in Apify.

    Args:
        actor_id: Actor ID to verify

    Returns:
        True if actor exists, False otherwise
    """
    logger.info(f"Verifying actor: {actor_id}")

    try:
        client = ApifyClient()
        actor_url = f"{client.base_url}/acts/{actor_id}"
        response = requests.get(actor_url, params={'token': client.api_key}, timeout=10)

        if response.status_code == 200:
            logger.info(f"✅ Actor exists: {actor_id}")
            return True
        else:
            logger.error(f"❌ Actor not found: {actor_id}")
            return False
    except Exception as e:
        logger.error(f"Error verifying actor: {e}")
        return False
