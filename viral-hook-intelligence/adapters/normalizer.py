"""
Platform Data Normalizer
Converts platform-specific responses to standardized format
"""
from datetime import datetime
from typing import Dict, Any, Optional
import json

class DataNormalizer:
    """Normalize scraped data from different platforms"""

    @staticmethod
    def normalize_tiktok(data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize TikTok scraper output"""
        return {
            'platform': 'tiktok',
            'creator': data.get('author', {}).get('name', 'unknown'),
            'creator_handle': data.get('author', {}).get('unique_id', 'unknown'),
            'post_id': data.get('id', ''),
            'url': f"https://www.tiktok.com/@{data.get('author', {}).get('unique_id')}/video/{data.get('id')}",
            'caption': data.get('desc', '') or data.get('caption', ''),
            'views': data.get('stats', {}).get('playCount', 0) or data.get('play_count', 0),
            'likes': data.get('stats', {}).get('diggCount', 0) or data.get('digg_count', 0),
            'comments': data.get('stats', {}).get('commentCount', 0) or data.get('comment_count', 0),
            'shares': data.get('stats', {}).get('shareCount', 0) or data.get('share_count', 0),
            'upload_date': DataNormalizer._parse_timestamp(data.get('createTime')),
            'media_type': 'video',
            'video_duration': data.get('video', {}).get('duration', 0),
            'raw_data': data
        }

    @staticmethod
    def normalize_instagram(data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize Instagram Reels scraper output"""
        return {
            'platform': 'instagram',
            'creator': data.get('ownerUsername', 'unknown'),
            'creator_handle': data.get('ownerUsername', 'unknown'),
            'post_id': data.get('id', ''),
            'url': f"https://www.instagram.com/p/{data.get('id')}/",
            'caption': data.get('caption', ''),
            'views': data.get('likesCount', 0),
            'likes': data.get('likesCount', 0),
            'comments': data.get('commentsCount', 0),
            'shares': 0,
            'upload_date': DataNormalizer._parse_timestamp(data.get('timestamp')),
            'media_type': 'video',
            'video_duration': data.get('videoDuration', 0),
            'raw_data': data
        }

    @staticmethod
    def normalize_youtube(data: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize YouTube scraper output"""
        return {
            'platform': 'youtube',
            'creator': data.get('channelTitle', 'unknown'),
            'creator_handle': data.get('channelId', 'unknown'),
            'post_id': data.get('videoId', ''),
            'url': f"https://www.youtube.com/watch?v={data.get('videoId')}",
            'caption': data.get('title', '') + '\n' + (data.get('description', '') or ''),
            'views': data.get('viewCount', 0),
            'likes': data.get('likeCount', 0),
            'comments': data.get('commentCount', 0),
            'shares': 0,
            'upload_date': DataNormalizer._parse_timestamp(data.get('publishedAt')),
            'media_type': 'video',
            'video_duration': data.get('duration', 0),
            'raw_data': data
        }

    @staticmethod
    def normalize(platform: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Route to appropriate normalizer"""
        normalizers = {
            'tiktok': DataNormalizer.normalize_tiktok,
            'instagram': DataNormalizer.normalize_instagram,
            'youtube': DataNormalizer.normalize_youtube
        }

        normalizer = normalizers.get(platform.lower())
        if not normalizer:
            raise ValueError(f"Unknown platform: {platform}")

        return normalizer(data)

    @staticmethod
    def _parse_timestamp(ts: Any) -> str:
        """Parse various timestamp formats"""
        if isinstance(ts, str):
            try:
                dt = datetime.fromisoformat(ts)
                return dt.isoformat()
            except:
                return ts
        elif isinstance(ts, int):
            # Unix timestamp
            return datetime.fromtimestamp(ts).isoformat()
        elif isinstance(ts, dict) and 'iso' in ts:
            return ts['iso']
        return datetime.now().isoformat()
