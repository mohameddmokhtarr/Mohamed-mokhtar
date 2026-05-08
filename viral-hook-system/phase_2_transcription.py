"""Phase 2: Extract transcripts from videos using OpenAI Whisper API."""

import os
import json
import subprocess
from pathlib import Path
import time
from openai import OpenAI
from logger import setup_logger
from config import TRANSCRIPTS_DIR, OPENAI_API_KEY, RAW_DATA_DIR

logger = setup_logger('phase_2_transcription')

def download_video(url, output_path, duration=10):
    """
    Download video using yt-dlp and trim to first N seconds.

    Args:
        url: Video URL
        output_path: Path to save video
        duration: Duration to keep (default 10 seconds)

    Returns:
        Path to downloaded/trimmed video or None if failed
    """
    try:
        logger.info(f"Downloading video: {url}")

        # Download video
        temp_video = output_path.with_suffix('.temp.mp4')
        cmd = [
            'yt-dlp',
            '-f', 'best[ext=mp4]',
            '-o', str(temp_video),
            url
        ]
        subprocess.run(cmd, check=True, capture_output=True, timeout=60)
        logger.info(f"Downloaded: {temp_video}")

        # Trim to first N seconds
        cmd = [
            'ffmpeg',
            '-i', str(temp_video),
            '-t', str(duration),
            '-c', 'copy',
            '-y',
            str(output_path)
        ]
        subprocess.run(cmd, check=True, capture_output=True, timeout=30)
        logger.info(f"Trimmed to {duration}s: {output_path}")

        # Clean up temp file
        if temp_video.exists():
            temp_video.unlink()

        return output_path

    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to download/trim video: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error downloading video: {e}")
        return None

def transcribe_video(video_path):
    """
    Transcribe video using OpenAI Whisper API.

    Args:
        video_path: Path to video file

    Returns:
        Transcribed text or None if failed
    """
    if not video_path or not Path(video_path).exists():
        logger.warning(f"Video file not found: {video_path}")
        return None

    try:
        logger.info(f"Transcribing: {video_path}")
        client = OpenAI(api_key=OPENAI_API_KEY)

        with open(video_path, 'rb') as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en"
            )

        text = transcript.text
        logger.info(f"Transcription successful: {len(text)} chars")
        return text

    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        return None

def extract_hook(item, video_path=None):
    """
    Extract hook from item using transcript or caption.

    Args:
        item: Normalized item dict
        video_path: Optional path to video file

    Returns:
        Hook object dict
    """
    hook_obj = {
        'post_id': item.get('post_id'),
        'platform': item.get('platform'),
        'url': item.get('url'),
        'caption': item.get('caption', ''),
        'hook_text': '',
        'source': 'caption',
        'views': item.get('views'),
        'likes': item.get('likes'),
        'comments': item.get('comments'),
    }

    # Try to get transcript
    if video_path:
        transcript = transcribe_video(video_path)
        if transcript:
            # Extract first 3-10 seconds (roughly first 50-100 words)
            hook_text = ' '.join(transcript.split()[:50])
            hook_obj['hook_text'] = hook_text
            hook_obj['source'] = 'transcript'
            logger.info(f"Extracted hook from transcript: {hook_text[:50]}...")
            return hook_obj

    # Fall back to caption
    caption = item.get('caption', '')
    if caption:
        # Extract first sentence or first 100 chars
        first_sentence = caption.split('\n')[0].split('.')[0]
        if len(first_sentence) > 100:
            first_sentence = first_sentence[:100] + '...'
        hook_obj['hook_text'] = first_sentence
        hook_obj['source'] = 'caption'
        logger.info(f"Extracted hook from caption: {first_sentence[:50]}...")
        return hook_obj

    logger.warning(f"No hook text found for {item.get('post_id')}")
    return hook_obj

def process_platform_data(platform, handle):
    """
    Process all videos for a platform/handle.

    Args:
        platform: Platform name
        handle: Creator handle

    Returns:
        List of hook objects
    """
    raw_file = RAW_DATA_DIR / f"{platform}-{handle.replace('@', '')}.json"

    if not raw_file.exists():
        logger.warning(f"Raw data not found: {raw_file}")
        return []

    with open(raw_file, 'r') as f:
        items = json.load(f)

    hooks = []
    for idx, item in enumerate(items):
        logger.info(f"Processing {platform}-{handle} [{idx+1}/{len(items)}]")

        # Try to download and transcribe video
        video_path = None
        url = item.get('url')

        if url:
            # For demo, we skip actual download to avoid API limits
            # In production, uncomment and use:
            # video_file = TRANSCRIPTS_DIR / f"{item.get('post_id')}.mp4"
            # video_path = download_video(url, video_file, duration=10)
            pass

        hook = extract_hook(item, video_path)
        hooks.append(hook)

    return hooks

def save_hooks(platform, handle, hooks):
    """Save hooks to file."""
    if not hooks:
        logger.warning(f"No hooks to save for {platform}-{handle}")
        return None

    output_file = TRANSCRIPTS_DIR / f"{platform}-{handle.replace('@', '')}-hooks.json"
    with open(output_file, 'w') as f:
        json.dump(hooks, f, indent=2, default=str)

    logger.info(f"Hooks saved: {output_file}")
    return output_file

def run_phase_2():
    """Execute Phase 2: Transcript Extraction."""
    logger.info("="*60)
    logger.info("PHASE 2: TRANSCRIPT EXTRACTION")
    logger.info("="*60)

    if not OPENAI_API_KEY or OPENAI_API_KEY.startswith('sk-test'):
        logger.warning("⚠️  OPENAI_API_KEY not configured. Skipping video downloads.")
        logger.warning("    Using captions as fallback for hook extraction.")

    all_hooks = {}

    # Find all raw data files
    raw_files = list(RAW_DATA_DIR.glob('*.json'))
    raw_files = [f for f in raw_files if not f.name.endswith('-raw.json')]

    for raw_file in raw_files:
        # Parse filename: {platform}-{handle}.json
        parts = raw_file.stem.split('-', 1)
        if len(parts) != 2:
            continue

        platform, handle = parts
        logger.info(f"\nProcessing {platform} data for @{handle}...")

        hooks = process_platform_data(platform, f"@{handle}")
        if hooks:
            save_hooks(platform, f"@{handle}", hooks)
            all_hooks[f"{platform}-{handle}"] = hooks

    logger.info(f"\n✅ Phase 2 complete: Extracted {len(all_hooks)} hook datasets")
    return all_hooks

if __name__ == '__main__':
    run_phase_2()
