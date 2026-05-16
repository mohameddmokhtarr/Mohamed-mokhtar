"""
Phase 3: Hook Classification
Classify hooks using Ollama (free local model)
"""
import json
from pathlib import Path
from typing import Dict, Any, List
import requests

from config import HOOKS_DIR, HOOK_TYPES, TONE_TYPES
from logger import classifier_logger, error_logger


class HookClassifier:
    """Classify hooks using Ollama"""

    def __init__(self, ollama_host: str = "http://localhost:11434"):
        self.ollama_host = ollama_host
        self.model = "mistral"
        self.classified_hooks = []

    def classify_hook(self, hook: Dict[str, Any]) -> Dict[str, Any]:
        """Classify a single hook using Ollama"""
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
            # Call Ollama API
            response = requests.post(
                f"{self.ollama_host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": 0.3
                },
                timeout=60
            )

            if response.status_code != 200:
                raise Exception(f"Ollama API error: {response.status_code}")

            response_data = response.json()
            response_text = response_data.get("response", "").strip()

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
                    # If JSON parsing fails, provide a default classification
                    classifier_logger.warning(f"Could not parse JSON response: {response_text[:100]}")
                    return self._get_default_classification(hook_text)

            return classification

        except requests.exceptions.ConnectionError:
            error_logger.error(f"Could not connect to Ollama at {self.ollama_host}")
            error_logger.error("Make sure Ollama is running: ollama serve")
            return self._get_default_classification(hook_text)
        except Exception as e:
            error_logger.error(f"Classification failed for hook: {str(e)}")
            return self._get_default_classification(hook_text)

    @staticmethod
    def _get_default_classification(hook_text: str) -> Dict[str, Any]:
        """Return a default classification based on content analysis"""
        hook_lower = hook_text.lower()

        # Simple heuristic-based classification
        if any(word in hook_lower for word in ['did you know', 'know what', 'know this', 'did you']):
            primary = 'curiosity'
        elif any(word in hook_lower for word in ['shocking', 'unbelievable', 'crazy', 'insane', 'wow']):
            primary = 'shock'
        elif any(word in hook_lower for word in ['expert', 'pro', 'years of', 'proven', 'research']):
            primary = 'authority'
        elif any(word in hook_lower for word in ['mistake', 'wrong', 'fail', 'failing']):
            primary = 'mistake_based'
        elif any(word in hook_lower for word in ['vs', 'instead of', 'unlike', 'different']):
            primary = 'comparison'
        elif any(word in hook_lower for word in ['dream', 'want', 'achieve', 'goal', 'success']):
            primary = 'aspiration'
        elif any(word in hook_lower for word in ['problem', 'struggle', 'pain', 'suffer', 'hard']):
            primary = 'fear'
        elif any(word in hook_lower for word in ['here', 'check out', 'see how', 'learn', 'discover']):
            primary = 'direct_benefit'
        elif any(word in hook_lower for word in ['everyone', 'people', 'everyone else', 'typical']):
            primary = 'contrarian'
        else:
            primary = 'storytelling'

        # Determine tone based on length and punctuation
        if '!' in hook_text:
            tone = 'urgent'
        elif '?' in hook_text:
            tone = 'conversational'
        elif len(hook_text) > 150:
            tone = 'informative'
        else:
            tone = 'conversational'

        return {
            'primary_hook_type': primary,
            'secondary_hook_types': [],
            'tone': tone,
            'predicted_engagement': 'medium',
            'key_elements': ['content-driven'],
            'improvement_suggestion': None,
            'classification_method': 'heuristic'
        }

    def process_hooks(self) -> Dict[str, Any]:
        """Process all extracted hooks"""
        classifier_logger.info("="*60)
        classifier_logger.info("PHASE 3: HOOK CLASSIFICATION (Using Ollama)")
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

        classifier_logger.info(f"Classifying {len(hooks)} hooks using Ollama...")
        classifier_logger.info("(Make sure Ollama is running: ollama serve)")

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
