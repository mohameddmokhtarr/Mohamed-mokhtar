"""Phase 3: Classify hooks by type and characteristics."""

import json
import re
from pathlib import Path
from logger import setup_logger
from config import TRANSCRIPTS_DIR, HOOKS_DIR, HOOK_TYPES

logger = setup_logger('phase_3_classification')

class HookClassifier:
    """Classify hooks by type and characteristics."""

    PATTERNS = {
        'curiosity': [
            r'what if', r'you won\'t believe', r'here\'s why', r'discover',
            r'never knew', r'shocking truth', r'wait until', r'secrets?',
        ],
        'shock': [
            r'omg', r'insane', r'unbelievable', r'not what', r'did not',
            r'mind blown', r'never', r'impossible', r'can\'t believe',
        ],
        'authority': [
            r'according to', r'research shows', r'studies prove', r'experts say',
            r'i learned', r'for \d+ years', r'as a', r'decade of',
        ],
        'contrarian': [
            r'actually', r'really', r'the truth is', r'opposite', r'wrong',
            r'don\'t', r'myth', r'mistake', r'instead of', r'bet you',
        ],
        'storytelling': [
            r'one day', r'story', r'happened', r'told me', r'learned',
            r'changed my', r'when i', r'remember', r'back then',
        ],
        'fear': [
            r'danger', r'careful', r'avoid', r'warning', r'critical',
            r'failing', r'loss', r'risk', r'problem',
        ],
        'aspiration': [
            r'dream', r'goal', r'success', r'achieve', r'become',
            r'transform', r'level up', r'breakthrough', r'possible',
        ],
        'direct_benefit': [
            r'save', r'money', r'time', r'easy', r'quick', r'free',
            r'boost', r'increase', r'better', r'improve', r'double',
        ],
        'mistake_based': [
            r'biggest mistake', r'i was wrong', r'learned hard', r'failed',
            r'broke', r'lost', r'never again', r'regret',
        ],
        'comparison': [
            r'vs', r'versus', r'rather than', r'instead of', r'better than',
            r'different from', r'unlike', r'compared to',
        ],
    }

    def classify(self, hook_text):
        """
        Classify a hook and return characteristics.

        Args:
            hook_text: Hook text to classify

        Returns:
            Classification dict
        """
        if not hook_text:
            return self._empty_classification()

        text_lower = hook_text.lower()
        classification = {
            'hook_text': hook_text,
            'primary_type': 'unknown',
            'secondary_types': [],
            'confidence': 0.0,
            'tone': self._classify_tone(text_lower),
            'pacing': self._classify_pacing(text_lower),
            'sentence_length': len(hook_text.split()),
            'reading_complexity': self._classify_complexity(text_lower),
        }

        # Find matching hook types
        matches = []
        for hook_type, patterns in self.PATTERNS.items():
            score = sum(1 for p in patterns if re.search(p, text_lower))
            if score > 0:
                matches.append((hook_type, score))

        if matches:
            matches.sort(key=lambda x: x[1], reverse=True)
            classification['primary_type'] = matches[0][0]
            classification['confidence'] = min(matches[0][1] / 5.0, 1.0)  # Normalize

            if len(matches) > 1:
                classification['secondary_types'] = [t[0] for t in matches[1:3]]

        return classification

    def _classify_tone(self, text):
        """Classify tone: casual, professional, enthusiastic, dark."""
        casual_words = ['lol', 'omg', 'gonna', 'wanna', 'like', 'really']
        professional_words = ['research', 'according', 'studies', 'evidence']
        enthusiastic_words = ['amazing', 'incredible', 'awesome', 'love', 'best']
        dark_words = ['danger', 'warning', 'careful', 'afraid', 'scary']

        casual_count = sum(1 for w in casual_words if w in text)
        prof_count = sum(1 for w in professional_words if w in text)
        enth_count = sum(1 for w in enthusiastic_words if w in text)
        dark_count = sum(1 for w in dark_words if w in text)

        counts = [
            ('casual', casual_count),
            ('professional', prof_count),
            ('enthusiastic', enth_count),
            ('dark', dark_count),
        ]
        counts.sort(key=lambda x: x[1], reverse=True)

        return counts[0][0] if counts[0][1] > 0 else 'neutral'

    def _classify_pacing(self, text):
        """Classify pacing: slow, moderate, fast."""
        # Count short sentences (paces faster)
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        if not sentences:
            return 'moderate'

        avg_length = sum(len(s.split()) for s in sentences) / len(sentences)

        if avg_length < 5:
            return 'fast'
        elif avg_length > 15:
            return 'slow'
        else:
            return 'moderate'

    def _classify_complexity(self, text):
        """Classify reading complexity: simple, intermediate, advanced."""
        # Simple heuristic: word length
        words = text.split()
        if not words:
            return 'intermediate'

        avg_word_len = sum(len(w) for w in words) / len(words)

        if avg_word_len < 4:
            return 'simple'
        elif avg_word_len > 6:
            return 'advanced'
        else:
            return 'intermediate'

    def _empty_classification(self):
        """Return empty classification."""
        return {
            'hook_text': '',
            'primary_type': 'unknown',
            'secondary_types': [],
            'confidence': 0.0,
            'tone': 'unknown',
            'pacing': 'unknown',
            'sentence_length': 0,
            'reading_complexity': 'unknown',
        }

def classify_hooks_file(hooks_file):
    """
    Classify all hooks in a file.

    Args:
        hooks_file: Path to hooks JSON file

    Returns:
        List of classified hooks
    """
    if not hooks_file.exists():
        logger.warning(f"Hooks file not found: {hooks_file}")
        return []

    with open(hooks_file, 'r') as f:
        hooks = json.load(f)

    classifier = HookClassifier()
    classified = []

    for hook in hooks:
        hook_text = hook.get('hook_text', '')
        classification = classifier.classify(hook_text)

        # Merge with original hook data
        classified_hook = {**hook, **classification}
        classified.append(classified_hook)

    return classified

def save_classified_hooks(platform, handle, classified_hooks):
    """Save classified hooks to file."""
    if not classified_hooks:
        logger.warning(f"No classified hooks for {platform}-{handle}")
        return None

    output_file = HOOKS_DIR / f"{platform}-{handle.replace('@', '')}-classified.json"
    with open(output_file, 'w') as f:
        json.dump(classified_hooks, f, indent=2, default=str)

    logger.info(f"Classified hooks saved: {output_file}")
    return output_file

def run_phase_3():
    """Execute Phase 3: Hook Classification."""
    logger.info("="*60)
    logger.info("PHASE 3: HOOK CLASSIFICATION")
    logger.info("="*60)

    all_classified = {}

    # Find all hooks files
    hooks_files = list(TRANSCRIPTS_DIR.glob('*-hooks.json'))

    for hooks_file in hooks_files:
        # Parse filename: {platform}-{handle}-hooks.json
        parts = hooks_file.stem.replace('-hooks', '').split('-', 1)
        if len(parts) != 2:
            continue

        platform, handle = parts
        logger.info(f"\nClassifying hooks: {platform} (@{handle})...")

        classified = classify_hooks_file(hooks_file)
        if classified:
            save_classified_hooks(platform, f"@{handle}", classified)
            all_classified[f"{platform}-{handle}"] = classified

            # Log summary
            type_counts = {}
            for hook in classified:
                h_type = hook.get('primary_type', 'unknown')
                type_counts[h_type] = type_counts.get(h_type, 0) + 1

            logger.info(f"  Hook types distribution: {type_counts}")

    logger.info(f"\n✅ Phase 3 complete: Classified {len(all_classified)} datasets")
    return all_classified

if __name__ == '__main__':
    run_phase_3()
