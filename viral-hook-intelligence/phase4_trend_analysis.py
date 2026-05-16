"""
Phase 4: Trend Analysis
Analyze hook trends over time
"""
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List
from collections import defaultdict

import pandas as pd
import numpy as np

from config import HOOKS_DIR
from logger import analyzer_logger, error_logger


class TrendAnalyzer:
    """Analyze trends in hook types and engagement"""

    def __init__(self):
        self.df = None
        self.trends = {}

    def load_hooks(self) -> pd.DataFrame:
        """Load classified hooks into DataFrame"""
        hooks_file = HOOKS_DIR / 'classified_hooks.json'

        if not hooks_file.exists():
            analyzer_logger.error("No classified hooks found. Run Phase 3 first.")
            return None

        with open(hooks_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        hooks = data.get('hooks', [])
        self.df = pd.DataFrame(hooks)

        # Parse dates
        self.df['upload_date'] = pd.to_datetime(self.df['upload_date'], utc=True)

        # Calculate engagement rate
        self.df['engagement_rate'] = (
            (self.df['likes'] + self.df['comments']) / self.df['views']
        ).fillna(0)

        self.df['engagement_rate'] = self.df['engagement_rate'].replace([np.inf, -np.inf], 0)

        return self.df

    def analyze_trends(self) -> Dict[str, Any]:
        """Analyze trends in hooks"""
        analyzer_logger.info("="*60)
        analyzer_logger.info("PHASE 4: TREND ANALYSIS")
        analyzer_logger.info("="*60)

        if self.df is None or len(self.df) == 0:
            analyzer_logger.error("No data to analyze")
            return None

        analyzer_logger.info(f"Analyzing {len(self.df)} hooks...")

        # Create time buckets
        now = datetime.now(self.df['upload_date'].dt.tz)
        last_30 = now - timedelta(days=30)
        last_90 = now - timedelta(days=90)

        buckets = {
            'last_30_days': self.df[self.df['upload_date'] >= last_30],
            '31_90_days': self.df[(self.df['upload_date'] >= last_90) & (self.df['upload_date'] < last_30)],
            '91_plus_days': self.df[self.df['upload_date'] < last_90]
        }

        results = {}

        for bucket_name, bucket_data in buckets.items():
            if len(bucket_data) == 0:
                results[bucket_name] = {
                    'count': 0,
                    'avg_views': 0,
                    'avg_engagement': 0,
                    'hook_types': {}
                }
                continue

            hook_types = bucket_data['primary_hook_type'].value_counts().to_dict()
            avg_views = bucket_data['views'].mean()
            avg_engagement = bucket_data['engagement_rate'].mean()

            results[bucket_name] = {
                'count': len(bucket_data),
                'avg_views': float(avg_views),
                'avg_engagement': float(avg_engagement),
                'hook_types': hook_types,
                'tones': bucket_data['tone'].value_counts().to_dict()
            }

        # Identify emerging hooks
        emerging = self._identify_emerging_hooks(buckets)

        # Hook type performance
        hook_performance = self._analyze_hook_performance()

        # Tone performance
        tone_performance = self._analyze_tone_performance()

        output = {
            'time_buckets': results,
            'emerging_hooks': emerging,
            'hook_performance': hook_performance,
            'tone_performance': tone_performance
        }

        # Save results
        output_file = HOOKS_DIR / 'trend_analysis.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2)

        analyzer_logger.info("\n" + "="*60)
        analyzer_logger.info("PHASE 4 COMPLETE")
        analyzer_logger.info("="*60)
        analyzer_logger.info(f"\nTrend Summary:")
        for bucket, data in results.items():
            analyzer_logger.info(f"\n{bucket}:")
            analyzer_logger.info(f"  Videos: {data['count']}")
            analyzer_logger.info(f"  Avg views: {data['avg_views']:.0f}")
            analyzer_logger.info(f"  Avg engagement: {data['avg_engagement']:.2%}")
        analyzer_logger.info(f"\nEmerging Hooks: {len(emerging)}")
        for hook in emerging[:3]:
            analyzer_logger.info(f"  • {hook['type']}: {hook['growth']:.1f}% growth")

        return output

    def _identify_emerging_hooks(self, buckets: Dict) -> List[Dict]:
        """Identify hooks with increasing frequency and engagement"""
        emerging = []

        for hook_type in buckets['last_30_days'].get('primary_hook_type', []):
            count_30 = len(buckets['last_30_days'][buckets['last_30_days']['primary_hook_type'] == hook_type])
            count_90 = len(buckets['31_90_days'][buckets['31_90_days']['primary_hook_type'] == hook_type])

            if count_90 > 0:
                growth = ((count_30 - count_90) / count_90) * 100
            else:
                growth = 100 if count_30 > 0 else 0

            engagement_30 = buckets['last_30_days'][
                buckets['last_30_days']['primary_hook_type'] == hook_type
            ]['engagement_rate'].mean()

            engagement_90 = buckets['31_90_days'][
                buckets['31_90_days']['primary_hook_type'] == hook_type
            ]['engagement_rate'].mean()

            if engagement_90 > 0:
                engagement_growth = ((engagement_30 - engagement_90) / engagement_90) * 100
            else:
                engagement_growth = 0

            if growth >= 30 or engagement_growth >= 30:
                emerging.append({
                    'type': hook_type,
                    'growth': growth,
                    'engagement_growth': engagement_growth,
                    'count_30': count_30,
                    'count_90': count_90
                })

        return sorted(emerging, key=lambda x: x['growth'], reverse=True)

    def _analyze_hook_performance(self) -> Dict[str, Dict]:
        """Analyze performance metrics by hook type"""
        performance = {}

        for hook_type in self.df['primary_hook_type'].unique():
            subset = self.df[self.df['primary_hook_type'] == hook_type]

            performance[hook_type] = {
                'count': len(subset),
                'avg_views': float(subset['views'].mean()),
                'median_views': float(subset['views'].median()),
                'avg_likes': float(subset['likes'].mean()),
                'avg_comments': float(subset['comments'].mean()),
                'avg_engagement_rate': float(subset['engagement_rate'].mean()),
                'max_views': float(subset['views'].max()),
                'outlier_count': len(subset[subset['views'] > subset['views'].quantile(0.9)])
            }

        return performance

    def _analyze_tone_performance(self) -> Dict[str, Dict]:
        """Analyze performance metrics by tone"""
        performance = {}

        for tone in self.df['tone'].unique():
            subset = self.df[self.df['tone'] == tone]

            performance[tone] = {
                'count': len(subset),
                'avg_views': float(subset['views'].mean()),
                'avg_engagement_rate': float(subset['engagement_rate'].mean()),
                'top_hook_types': subset['primary_hook_type'].value_counts().to_dict()
            }

        return performance


def main():
    """Run Phase 4"""
    analyzer = TrendAnalyzer()
    df = analyzer.load_hooks()

    if df is None:
        return None

    result = analyzer.analyze_trends()
    return result


if __name__ == '__main__':
    main()
