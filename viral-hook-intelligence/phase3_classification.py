"""
Phase 3: Hook Classification
Classify hooks using Anthropic Claude API
"""
import json
from pathlib import Path
from typing import Dict, Any, List
from anthropic import Anthropic

from config import HOOKS_DIR, ANTHROPIC_API_KEY, CLAUDE_MODEL, HOOK_TYPES, TONE_TYPES
from logger import classifier_logger, error_logger


class HookClassifier:
    """Classify hooks using Claude API"""

    def __init__(self):
        self.client = Anthropic(api_key=ANTHROPIC_API_KEY)
        self.model = CLAUDE_MODEL
        self.classified_hooks = []

    def classify_hook(self, hook: Dict[str, Any]) -> Dict[str, Any]:
        """Classify a single hook using Claude"""
        hook_text = hook.get('hook_text', '')

        if not hook_text:
            return None

        prompt = f"""Analyze this social media hook and classify it.

HOOK TEXT:
"{hook_text}"

Provide a JSON response with:
1. primary_hook_type: One of {HOOK_TYPES}
2. secondary_hook_types: List of up to 2 others from {HOOK_TYPES}
3. tone: One of {TONE_TYPES}
4. predicted_engagement: "high", "medium", or "low"
5. key_elements: List of 2-3 key elements that make this hook work
6. improvement_suggestion: One way to improve this hook (or null if excellent)

Format as valid JSON only, no markdown."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                messages=[
                    {'role': 'user', 'content': prompt}
                ]
            )

            response_text = response.content[0].text.strip()

            # Parse JSON response
            try:
                classification = json.loads(response_text)
            except json.JSONDecodeError:
                # Try to extract JSON if wrapped in markdown
                if '```json' in response_text:
                    response_text = response_text.split('```json')[1].split('```')[0].strip()
                    classification = json.loads(response_text)
                elif '```' in response_text:
                    response_text = response_text.split('```')[1].split('```')[0].strip()
                    classification = json.loads(response_text)
                else:
                    raise

            return classification

        except Exception as e:
            error_logger.error(f"Classification failed for hook: {str(e)}")
            return None

    def process_hooks(self) -> Dict[str, Any]:
        """Process all extracted hooks"""
        classifier_logger.info("="*60)
        classifier_logger.info("PHASE 3: HOOK CLASSIFICATION")
        classifier_logger.info("="*60)

        hooks_file = HOOKS_DIR / 'all_hooks.json'

        if not hooks_file.exists():
            classifier_logger.error("No hooks found. Run Phase 2 first.")
            return None

        with open(hooks_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        hooks = data.get('hooks', [])
        classified = []
        stats = {
            'total_hooks': len(hooks),
            'classified': 0,
            'failed': 0,
            'hook_type_distribution': {},
            'tone_distribution': {}
        }

        classifier_logger.info(f"Classifying {len(hooks)} hooks...")

        for i, hook in enumerate(hooks):
            if i % 5 == 0:
                classifier_logger.info(f"Progress: {i}/{len(hooks)}")

            classification = self.classify_hook(hook)

            if classification:
                classified_hook = {**hook, **classification}
                classified.append(classified_hook)
                stats['classified'] += 1

                # Update distributions
                hook_type = classification.get('primary_hook_type', 'unknown')
                tone = classification.get('tone', 'unknown')

                stats['hook_type_distribution'][hook_type] = \
                    stats['hook_type_distribution'].get(hook_type, 0) + 1
                stats['tone_distribution'][tone] = \
                    stats['tone_distribution'].get(tone, 0) + 1
            else:
                stats['failed'] += 1

        # Save classified hooks
        output_file = HOOKS_DIR / 'classified_hooks.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'total': len(classified),
                'hooks': classified,
                'stats': stats
            }, f, indent=2, ensure_ascii=False)

        classifier_logger.info("\n" + "="*60)
        classifier_logger.info("PHASE 3 COMPLETE")
        classifier_logger.info("="*60)
        classifier_logger.info(f"Classified: {stats['classified']}")
        classifier_logger.info(f"Failed: {stats['failed']}")
        classifier_logger.info(f"\nHook Type Distribution:")
        for hook_type, count in sorted(stats['hook_type_distribution'].items(), key=lambda x: x[1], reverse=True):
            classifier_logger.info(f"  {hook_type}: {count}")
        classifier_logger.info(f"\nTone Distribution:")
        for tone, count in sorted(stats['tone_distribution'].items(), key=lambda x: x[1], reverse=True):
            classifier_logger.info(f"  {tone}: {count}")

        return {
            'classified_hooks': classified,
            'stats': stats
        }


def main():
    """Run Phase 3"""
    classifier = HookClassifier()
    result = classifier.process_hooks()
    return result


if __name__ == '__main__':
    main()
