"""
Phase 6: Swipe Database
Build a database of top hooks and reusable templates
"""
import json
import re
from pathlib import Path
from typing import Dict, Any, List

import pandas as pd

from config import HOOKS_DIR
from logger import analyzer_logger, error_logger


class SwipeDatabase:
    """Build and generate swipe files"""

    def __init__(self):
        self.df = None
        self.top_hooks = []
        self.templates = []

    def load_hooks(self) -> pd.DataFrame:
        """Load classified hooks with outlier data"""
        hooks_file = HOOKS_DIR / 'classified_hooks.json'

        with open(hooks_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        hooks = data.get('hooks', [])
        self.df = pd.DataFrame(hooks)
        self.df['upload_date'] = pd.to_datetime(self.df['upload_date'], utc=True)

        return self.df

    def build_database(self) -> Dict[str, Any]:
        """Build swipe database from top-performing hooks"""
        analyzer_logger.info("="*60)
        analyzer_logger.info("PHASE 6: SWIPE DATABASE GENERATION")
        analyzer_logger.info("="*60)

        if len(self.df) == 0:
            analyzer_logger.error("No hooks to process")
            return None

        # Sort by views + engagement
        self.df['engagement_score'] = (
            self.df['views'] * 0.7 +
            (self.df['likes'] + self.df['comments']) * 0.3
        )
        self.df = self.df.sort_values('engagement_score', ascending=False)

        # Get top 100
        self.top_hooks = self.df.head(100).to_dict('records')

        analyzer_logger.info(f"Selected top 100 hooks by engagement score")

        # Generate templates from top hooks
        self.templates = self._generate_templates()

        # Organize by category
        output = {
            'top_100_hooks': self._format_top_hooks(),
            'templates_by_type': self._organize_templates_by_type(),
            'templates': self.templates,
            'quick_reference': self._build_quick_reference(),
            'stats': {
                'total_hooks_analyzed': len(self.df),
                'templates_generated': len(self.templates),
                'hook_types_covered': len(set(h['primary_hook_type'] for h in self.top_hooks))
            }
        }

        # Save database
        output_file = HOOKS_DIR / 'swipe_database.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        analyzer_logger.info("\n" + "="*60)
        analyzer_logger.info("PHASE 6 COMPLETE")
        analyzer_logger.info("="*60)
        analyzer_logger.info(f"Top hooks collected: {len(self.top_hooks)}")
        analyzer_logger.info(f"Templates generated: {len(self.templates)}")
        analyzer_logger.info(f"Hook types: {output['stats']['hook_types_covered']}")

        return output

    def _format_top_hooks(self) -> List[Dict]:
        """Format top hooks for swipe file"""
        formatted = []

        for i, hook in enumerate(self.top_hooks, 1):
            formatted.append({
                'rank': i,
                'hook_text': hook['hook_text'],
                'creator': hook['creator'],
                'hook_type': hook.get('primary_hook_type', 'unknown'),
                'tone': hook.get('tone', 'unknown'),
                'views': int(hook['views']),
                'engagement': int(hook.get('likes', 0) + hook.get('comments', 0)),
                'url': hook.get('url', ''),
                'why_it_works': hook.get('key_elements', [])
            })

        return formatted

    def _generate_templates(self) -> List[Dict]:
        """Generate reusable templates from top hooks"""
        templates = []
        template_patterns = set()

        for hook in self.top_hooks:
            hook_text = hook['hook_text']
            hook_type = hook.get('primary_hook_type', 'unknown')

            # Extract template patterns
            template = self._extract_template(hook_text, hook_type)

            if template and template not in template_patterns:
                template_patterns.add(template)
                templates.append({
                    'template': template,
                    'hook_type': hook_type,
                    'tone': hook.get('tone', 'unknown'),
                    'example': hook_text,
                    'usage_instructions': self._get_template_instructions(hook_type)
                })

        return templates[:50]  # Limit to 50 templates

    def _extract_template(self, text: str, hook_type: str) -> str:
        """Extract template pattern from hook text"""
        # Remove specific details and create placeholders
        text = re.sub(r'\d+', '[NUMBER]', text)
        text = re.sub(r'@\w+', '[MENTION]', text)
        text = re.sub(r'#\w+', '[HASHTAG]', text)

        # Generalize names and specific entities
        if hook_type == 'shock':
            text = re.sub(r'[A-Z][a-z]+', '[NAME]', text)

        # If template is similar to existing one, skip
        if len(text) < 20:
            return None

        return text

    def _organize_templates_by_type(self) -> Dict[str, List]:
        """Organize templates by hook type"""
        organized = {}

        for template in self.templates:
            hook_type = template['hook_type']
            if hook_type not in organized:
                organized[hook_type] = []
            organized[hook_type].append(template)

        return organized

    def _get_template_instructions(self, hook_type: str) -> str:
        """Get usage instructions for hook type"""
        instructions = {
            'curiosity': 'Create a question or mystery that makes viewers want to click. Focus on the "gap" between what they know and what they want to know.',
            'shock': 'Lead with something surprising or unexpected. Break pattern interrupt to grab attention.',
            'authority': 'Establish credibility with data, experience, or results. Show why you\'re qualified to speak.',
            'contrarian': 'Go against conventional wisdom. State an unpopular opinion that challenges the norm.',
            'storytelling': 'Start with a relatable situation. Build tension and resolve with a lesson.',
            'fear': 'Highlight a problem or pain point your audience experiences. Promise a solution.',
            'aspiration': 'Show a desirable outcome or transformation. Make viewers want that result.',
            'direct_benefit': 'Clearly state what viewers will gain. Be specific and valuable.',
            'mistake_based': 'Reveal a common mistake people make. Position yourself as the guide.',
            'comparison': 'Compare two approaches, ideas, or products. Show why one is better.'
        }

        return instructions.get(hook_type, 'Adapt this hook to your content.')

    def _build_quick_reference(self) -> Dict[str, Any]:
        """Build quick reference guide"""
        hook_types = {}
        tones = {}

        for hook in self.top_hooks:
            ht = hook.get('primary_hook_type', 'unknown')
            tone = hook.get('tone', 'unknown')

            if ht not in hook_types:
                hook_types[ht] = {
                    'count': 0,
                    'avg_views': 0,
                    'examples': []
                }
            if tone not in tones:
                tones[tone] = {'count': 0, 'examples': []}

            hook_types[ht]['count'] += 1
            hook_types[ht]['avg_views'] += hook['views']
            if len(hook_types[ht]['examples']) < 3:
                hook_types[ht]['examples'].append(hook['hook_text'][:50])

            tones[tone]['count'] += 1
            if len(tones[tone]['examples']) < 3:
                tones[tone]['examples'].append(hook['hook_text'][:50])

        # Calculate averages
        for ht in hook_types:
            hook_types[ht]['avg_views'] = int(hook_types[ht]['avg_views'] / hook_types[ht]['count'])

        return {
            'hook_types': hook_types,
            'tones': tones,
            'total_in_reference': len(self.top_hooks)
        }


def main():
    """Run Phase 6"""
    database = SwipeDatabase()
    df = database.load_hooks()

    if df is None or len(df) == 0:
        return None

    result = database.build_database()
    return result


if __name__ == '__main__':
    main()
