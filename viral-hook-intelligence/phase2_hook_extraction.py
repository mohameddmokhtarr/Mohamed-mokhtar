"""
Phase 2: Hook Extraction
Extract hooks from captions (no video transcription needed)
"""
import json
from pathlib import Path
from typing import List, Dict, Any
import re

from config import RAW_DATA_DIR, HOOKS_DIR
from logger import analyzer_logger, error_logger


class HookExtractor:
    """Extract hooks from video captions"""

    def __init__(self):
        self.hooks = []

    @staticmethod
    def extract_hook(caption: str) -> Dict[str, Any]:
        """Extract hook information from caption"""
        if not caption or not caption.strip():
            return None

        caption = caption.strip()

        # Get first 3-10 sentences or first 100 chars (whichever comes first)
        sentences = re.split(r'[.!?]+', caption)
        hook_text = ''
        for i, sentence in enumerate(sentences):
            if i >= 3:  # Max 3 sentences
                break
            hook_text += sentence.strip() + ' '
            if len(hook_text) >= 100:  # Min 100 chars for complete thought
                break

        hook_text = hook_text.strip()

        if not hook_text:
            hook_text = caption[:100]

        return {
            'hook_text': hook_text,
            'full_caption': caption,
            'word_count': len(hook_text.split()),
            'char_count': len(hook_text),
            'sentence_count': len([s for s in sentences if s.strip()]),
            'has_emoji': any(ord(c) > 127 for c in caption),
            'has_hashtag': '#' in caption,
            'has_mention': '@' in caption,
            'has_question': '?' in caption,
            'has_exclamation': '!' in caption,
            'has_caps': any(c.isupper() for c in caption)
        }

    def process_files(self) -> Dict[str, Any]:
        """Process all raw data files and extract hooks"""
        analyzer_logger.info("="*60)
        analyzer_logger.info("PHASE 2: HOOK EXTRACTION")
        analyzer_logger.info("="*60)

        hooks_by_platform = {}
        stats = {
            'total_hooks': 0,
            'files_processed': 0,
            'files_failed': 0,
            'empty_captions': 0
        }

        # Process each raw data file
        for raw_file in RAW_DATA_DIR.glob('*.json'):
            analyzer_logger.info(f"\nProcessing {raw_file.name}...")

            try:
                with open(raw_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                platform = data['platform']
                handle = data['handle']
                videos = data.get('videos', [])

                hooks = []
                for video in videos:
                    caption = video.get('caption', '')

                    if not caption or not caption.strip():
                        stats['empty_captions'] += 1
                        continue

                    hook = self.extract_hook(caption)
                    if hook:
                        hook['platform'] = platform
                        hook['creator'] = video.get('creator', '')
                        hook['creator_handle'] = video.get('creator_handle', '')
                        hook['post_id'] = video.get('post_id', '')
                        hook['url'] = video.get('url', '')
                        hook['views'] = video.get('views', 0)
                        hook['likes'] = video.get('likes', 0)
                        hook['comments'] = video.get('comments', 0)
                        hook['upload_date'] = video.get('upload_date', '')

                        hooks.append(hook)

                hooks_by_platform[f"{platform}:{handle}"] = hooks
                stats['total_hooks'] += len(hooks)
                stats['files_processed'] += 1

                analyzer_logger.info(f"  ✓ Extracted {len(hooks)} hooks from {len(videos)} videos")

            except Exception as e:
                error_msg = f"Failed to process {raw_file.name}: {str(e)}"
                analyzer_logger.error(error_msg)
                error_logger.error(error_msg)
                stats['files_failed'] += 1
                continue

        # Save hooks to file
        self._save_hooks(hooks_by_platform)

        analyzer_logger.info("\n" + "="*60)
        analyzer_logger.info("PHASE 2 COMPLETE")
        analyzer_logger.info("="*60)
        analyzer_logger.info(f"Total hooks extracted: {stats['total_hooks']}")
        analyzer_logger.info(f"Files processed: {stats['files_processed']}")
        analyzer_logger.info(f"Files failed: {stats['files_failed']}")
        analyzer_logger.info(f"Videos with empty captions: {stats['empty_captions']}")

        if stats['total_hooks'] < 20:
            analyzer_logger.warning(f"⚠ WARNING: Only {stats['total_hooks']} hooks found")
            analyzer_logger.warning("  Dataset may be too small for reliable analysis")

        return {
            'hooks_by_platform': hooks_by_platform,
            'stats': stats
        }

    def _save_hooks(self, hooks_by_platform: Dict[str, List[Dict]]):
        """Save extracted hooks to JSON file"""
        output_file = HOOKS_DIR / 'all_hooks.json'

        all_hooks = []
        for platform_handle, hooks in hooks_by_platform.items():
            all_hooks.extend(hooks)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'extracted_at': Path(__file__).parent / '__init__.py',
                'total_hooks': len(all_hooks),
                'hooks': all_hooks
            }, f, indent=2, ensure_ascii=False)

        analyzer_logger.info(f"Saved {len(all_hooks)} hooks to {output_file}")


def main():
    """Run Phase 2"""
    extractor = HookExtractor()
    result = extractor.process_files()
    return result


if __name__ == '__main__':
    main()
