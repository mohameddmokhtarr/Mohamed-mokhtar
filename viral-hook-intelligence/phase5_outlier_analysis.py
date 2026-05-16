"""
Phase 5: Performance Analysis
Identify viral outliers and top performers
"""
import json
from pathlib import Path
from typing import Dict, Any, List

import pandas as pd
import numpy as np

from config import HOOKS_DIR
from logger import analyzer_logger, error_logger


class OutlierAnalyzer:
    """Find viral outliers and performance patterns"""

    def __init__(self):
        self.df = None
        self.outliers = []

    def load_hooks(self) -> pd.DataFrame:
        """Load classified hooks"""
        hooks_file = HOOKS_DIR / 'classified_hooks.json'

        with open(hooks_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        hooks = data.get('hooks', [])
        self.df = pd.DataFrame(hooks)
        self.df['upload_date'] = pd.to_datetime(self.df['upload_date'], utc=True)

        return self.df

    def find_outliers(self) -> Dict[str, Any]:
        """Identify viral outliers"""
        analyzer_logger.info("="*60)
        analyzer_logger.info("PHASE 5: OUTLIER ANALYSIS")
        analyzer_logger.info("="*60)

        if len(self.df) == 0:
            analyzer_logger.error("No data to analyze")
            return None

        analyzer_logger.info(f"Analyzing {len(self.df)} videos for outliers...")

        self.df = self.df.sort_values('upload_date')
        outliers = []

        # For each video, compare against 5 before + 5 after
        for idx, row in self.df.iterrows():
            position = self.df.index.get_loc(idx)

            # Get surrounding videos
            start = max(0, position - 5)
            end = min(len(self.df), position + 6)
            neighbors = self.df.iloc[start:end]

            # Calculate local median
            local_median = neighbors['views'].median()
            local_mean = neighbors['views'].mean()

            # Check if this video is >= 2x the local median
            if local_median > 0 and row['views'] >= local_median * 2:
                outliers.append({
                    'position': position,
                    'post_id': row['post_id'],
                    'creator': row['creator'],
                    'views': int(row['views']),
                    'likes': int(row['likes']),
                    'comments': int(row['comments']),
                    'hook_text': row['hook_text'],
                    'primary_hook_type': row.get('primary_hook_type', 'unknown'),
                    'tone': row.get('tone', 'unknown'),
                    'upload_date': row['upload_date'].isoformat(),
                    'local_median': float(local_median),
                    'performance_ratio': float(row['views'] / local_median) if local_median > 0 else 0,
                    'engagement_rate': float((row['likes'] + row['comments']) / row['views']) if row['views'] > 0 else 0
                })

        outliers = sorted(outliers, key=lambda x: x['views'], reverse=True)

        # Outlier patterns
        patterns = self._analyze_outlier_patterns(outliers)

        # Hook type effectiveness
        hook_effectiveness = self._analyze_hook_effectiveness()

        output = {
            'total_outliers': len(outliers),
            'outliers': outliers,
            'outlier_patterns': patterns,
            'hook_effectiveness': hook_effectiveness,
            'stats': {
                'total_videos': len(self.df),
                'total_views': int(self.df['views'].sum()),
                'avg_views': float(self.df['views'].mean()),
                'median_views': float(self.df['views'].median()),
                'outlier_percentage': float(len(outliers) / len(self.df) * 100)
            }
        }

        # Save results
        output_file = HOOKS_DIR / 'outlier_analysis.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2)

        analyzer_logger.info("\n" + "="*60)
        analyzer_logger.info("PHASE 5 COMPLETE")
        analyzer_logger.info("="*60)
        analyzer_logger.info(f"Outliers found: {len(outliers)} ({len(outliers)/len(self.df)*100:.1f}%)")
        analyzer_logger.info(f"Total videos analyzed: {len(self.df)}")
        analyzer_logger.info(f"Avg views per video: {self.df['views'].mean():.0f}")
        analyzer_logger.info(f"Median views: {self.df['views'].median():.0f}")

        if outliers:
            analyzer_logger.info(f"\nTop 5 Viral Hooks:")
            for i, outlier in enumerate(outliers[:5], 1):
                analyzer_logger.info(
                    f"  {i}. {outlier['primary_hook_type']} ({outlier['tone']}) - "
                    f"{outlier['views']:,} views"
                )

        return output

    def _analyze_outlier_patterns(self, outliers: List[Dict]) -> Dict[str, Any]:
        """Analyze patterns in outliers"""
        patterns = {
            'hook_types': {},
            'tones': {},
            'creators': {}
        }

        for outlier in outliers:
            hook_type = outlier['primary_hook_type']
            tone = outlier['tone']
            creator = outlier['creator']

            patterns['hook_types'][hook_type] = patterns['hook_types'].get(hook_type, 0) + 1
            patterns['tones'][tone] = patterns['tones'].get(tone, 0) + 1
            patterns['creators'][creator] = patterns['creators'].get(creator, 0) + 1

        # Rank patterns
        patterns['hook_types'] = dict(sorted(patterns['hook_types'].items(), key=lambda x: x[1], reverse=True))
        patterns['tones'] = dict(sorted(patterns['tones'].items(), key=lambda x: x[1], reverse=True))
        patterns['creators'] = dict(sorted(patterns['creators'].items(), key=lambda x: x[1], reverse=True))

        return patterns

    def _analyze_hook_effectiveness(self) -> Dict[str, Dict]:
        """Analyze how well each hook type performs"""
        effectiveness = {}

        for hook_type in self.df['primary_hook_type'].unique():
            subset = self.df[self.df['primary_hook_type'] == hook_type]

            # Calculate outlier rate
            local_outliers = 0
            for _, row in subset.iterrows():
                position = self.df.index.get_loc(self.df[self.df['post_id'] == row['post_id']].index[0])
                start = max(0, position - 5)
                end = min(len(self.df), position + 6)
                neighbors = self.df.iloc[start:end]
                local_median = neighbors['views'].median()

                if local_median > 0 and row['views'] >= local_median * 2:
                    local_outliers += 1

            effectiveness[hook_type] = {
                'total_uses': len(subset),
                'avg_views': float(subset['views'].mean()),
                'median_views': float(subset['views'].median()),
                'outlier_rate': float(local_outliers / len(subset) * 100) if len(subset) > 0 else 0,
                'avg_engagement_rate': float(((subset['likes'] + subset['comments']) / subset['views']).mean()),
                'performance_rank': 0  # Will set after sorting
            }

        # Rank by effectiveness
        ranked = sorted(effectiveness.items(), key=lambda x: x[1]['outlier_rate'], reverse=True)
        for rank, (hook_type, metrics) in enumerate(ranked, 1):
            effectiveness[hook_type]['performance_rank'] = rank

        return effectiveness


def main():
    """Run Phase 5"""
    analyzer = OutlierAnalyzer()
    df = analyzer.load_hooks()

    if df is None or len(df) == 0:
        return None

    result = analyzer.find_outliers()
    return result


if __name__ == '__main__':
    main()
