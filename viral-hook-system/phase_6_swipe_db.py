"""Phase 6: Build swipe database of top hooks and templates."""

import json
import re
from pathlib import Path
from logger import setup_logger
from config import HOOKS_DIR, TOP_HOOKS_COUNT

logger = setup_logger('phase_6_swipe_db')

def extract_templates(hook_text, hook_type):
    """
    Extract reusable template patterns from hooks.

    Args:
        hook_text: Hook text
        hook_type: Hook type classification

    Returns:
        List of template patterns
    """
    templates = []

    # Generic templates based on hook type
    if hook_type == 'curiosity':
        templates = [
            "[noun] you didn't know about [topic]",
            "what [verb] [noun]?",
            "here's why [claim]",
        ]
    elif hook_type == 'shock':
        templates = [
            "not what [noun] looks like",
            "[noun] is [surprising adjective]",
            "wait till you see [noun]",
        ]
    elif hook_type == 'authority':
        templates = [
            "as someone who [credential]",
            "[number] years of [experience]",
            "research shows [claim]",
        ]
    elif hook_type == 'contrarian':
        templates = [
            "the truth about [topic]",
            "you're wrong about [topic]",
            "myth: [common belief]",
        ]
    elif hook_type == 'storytelling':
        templates = [
            "one day [event]",
            "my story with [topic]",
            "back when [time], [event]",
        ]
    elif hook_type == 'fear':
        templates = [
            "⚠️ warning: [danger]",
            "don't [action] because [consequence]",
            "[noun] is more dangerous than [comparison]",
        ]
    elif hook_type == 'aspiration':
        templates = [
            "dream of becoming [aspiration]?",
            "how to achieve [goal]",
            "from [current] to [aspirational]",
        ]
    elif hook_type == 'direct_benefit':
        templates = [
            "save [amount] by [action]",
            "[verb] in [timeframe]",
            "this one trick [benefit]",
        ]
    elif hook_type == 'mistake_based':
        templates = [
            "biggest mistake: [mistake]",
            "i learned [lesson] the hard way",
            "never do [action] if [consequence]",
        ]
    elif hook_type == 'comparison':
        templates = [
            "[option A] vs [option B]",
            "[noun A] is better than [noun B]",
            "why [claim] instead of [alternative]",
        ]

    return templates

def rank_hooks(all_classified_hooks, metric='views'):
    """
    Rank hooks by engagement metric.

    Args:
        all_classified_hooks: All classified hooks across datasets
        metric: Ranking metric ('views', 'engagement', 'confidence')

    Returns:
        Sorted list of hooks with scores
    """
    hooks_with_scores = []

    for hook in all_classified_hooks:
        if metric == 'views':
            score = hook.get('views', 0) or 0
        elif metric == 'engagement':
            views = hook.get('views', 0) or 0
            likes = hook.get('likes', 0) or 0
            comments = hook.get('comments', 0) or 0
            score = max(views, likes + comments)
        elif metric == 'confidence':
            score = hook.get('confidence', 0) or 0
        else:
            score = 0

        hooks_with_scores.append((hook, score))

    hooks_with_scores.sort(key=lambda x: x[1], reverse=True)
    return [h[0] for h in hooks_with_scores]

def build_swipe_database():
    """
    Build comprehensive swipe database from all classified hooks.

    Returns:
        Swipe database dict
    """
    all_classified_hooks = []

    # Load all classified hooks
    hooks_files = list(HOOKS_DIR.glob('*-classified.json'))
    for hooks_file in hooks_files:
        with open(hooks_file, 'r') as f:
            hooks = json.load(f)
            all_classified_hooks.extend(hooks)

    if not all_classified_hooks:
        logger.warning("No classified hooks found")
        return {}

    logger.info(f"Building database from {len(all_classified_hooks)} hooks")

    # Rank by different metrics
    by_views = rank_hooks(all_classified_hooks, 'views')
    by_engagement = rank_hooks(all_classified_hooks, 'engagement')
    by_confidence = rank_hooks(all_classified_hooks, 'confidence')

    # Top N hooks
    top_hooks = by_views[:TOP_HOOKS_COUNT]

    # Templates by hook type
    templates_by_type = {}
    for hook_type in [
        'curiosity', 'shock', 'authority', 'contrarian', 'storytelling',
        'fear', 'aspiration', 'direct_benefit', 'mistake_based', 'comparison'
    ]:
        templates = extract_templates("", hook_type)
        templates_by_type[hook_type] = {
            'templates': templates,
            'examples': [
                h['hook_text'] for h in top_hooks
                if h.get('primary_type') == hook_type
            ][:5],  # Top 5 examples
        }

    # Build fill-in-the-blank structures
    blanks = {}
    for hook_type, data in templates_by_type.items():
        blanks[hook_type] = {
            'templates': data['templates'],
            'placeholders': _extract_placeholders(data['templates']),
        }

    swipe_db = {
        'metadata': {
            'total_hooks': len(all_classified_hooks),
            'top_hooks_count': len(top_hooks),
        },
        'top_hooks': [
            {
                'rank': i+1,
                'hook_text': h['hook_text'],
                'type': h.get('primary_type'),
                'views': h.get('views'),
                'engagement': h.get('engagement', 0),
                'confidence': h.get('confidence'),
            }
            for i, h in enumerate(top_hooks[:TOP_HOOKS_COUNT])
        ],
        'templates_by_type': templates_by_type,
        'fill_in_blanks': blanks,
        'top_performers': {
            'by_views': [h['hook_text'] for h in by_views[:10]],
            'by_engagement': [h['hook_text'] for h in by_engagement[:10]],
            'by_confidence': [h['hook_text'] for h in by_confidence[:10]],
        },
    }

    return swipe_db

def _extract_placeholders(templates):
    """Extract placeholder names from templates."""
    placeholders = set()
    for template in templates:
        matches = re.findall(r'\[([^\]]+)\]', template)
        placeholders.update(matches)
    return list(placeholders)

def run_phase_6():
    """Execute Phase 6: Build Swipe Database."""
    logger.info("="*60)
    logger.info("PHASE 6: BUILD SWIPE DATABASE")
    logger.info("="*60)

    swipe_db = build_swipe_database()

    if not swipe_db:
        logger.warning("Failed to build swipe database")
        return {}

    # Save swipe database
    swipe_file = HOOKS_DIR / 'swipe-database.json'
    with open(swipe_file, 'w') as f:
        json.dump(swipe_db, f, indent=2, default=str)

    logger.info(f"✅ Swipe database saved: {swipe_file}")
    logger.info(f"  - Top {swipe_db['metadata']['top_hooks_count']} hooks")
    logger.info(f"  - Templates for {len(swipe_db['templates_by_type'])} hook types")
    logger.info(f"  - {sum(len(data['templates']) for data in swipe_db['templates_by_type'].values())} reusable templates")

    return swipe_db

if __name__ == '__main__':
    run_phase_6()
