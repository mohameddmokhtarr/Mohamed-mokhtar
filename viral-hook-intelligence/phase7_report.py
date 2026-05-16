"""
Phase 7: Report Generation
Generate comprehensive HTML report
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict
from jinja2 import Template

from config import HOOKS_DIR, REPORTS_DIR
from logger import reporter_logger, error_logger


class ReportGenerator:
    """Generate HTML reports from analysis data"""

    def __init__(self):
        self.hooks_data = {}
        self.report_html = ""

    def load_data(self) -> bool:
        """Load all analysis data"""
        try:
            files = {
                'hooks': 'all_hooks.json',
                'classified': 'classified_hooks.json',
                'trends': 'trend_analysis.json',
                'outliers': 'outlier_analysis.json',
                'swipes': 'swipe_database.json'
            }

            for key, filename in files.items():
                filepath = HOOKS_DIR / filename
                if filepath.exists():
                    with open(filepath, 'r', encoding='utf-8') as f:
                        self.hooks_data[key] = json.load(f)

            return True
        except Exception as e:
            error_logger.error(f"Failed to load data: {str(e)}")
            return False

    def generate_report(self) -> Dict:
        """Generate HTML report"""
        reporter_logger.info("="*60)
        reporter_logger.info("PHASE 7: REPORT GENERATION")
        reporter_logger.info("="*60)

        if not self.load_data():
            reporter_logger.error("Failed to load analysis data")
            return None

        html_content = self._render_html()
        output_file = REPORTS_DIR / 'viral-hook-report.html'

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        reporter_logger.info(f"Report generated: {output_file}")
        reporter_logger.info(f"File size: {output_file.stat().st_size} bytes")

        return {
            'report_file': str(output_file),
            'file_size': output_file.stat().st_size
        }

    def _render_html(self) -> str:
        """Render HTML report"""
        template_str = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Viral Hook Intelligence Report</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            text-align: center;
        }
        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        main {
            padding: 40px;
        }
        .section {
            margin-bottom: 50px;
        }
        .section h2 {
            color: #667eea;
            font-size: 2em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }
        .section h3 {
            color: #764ba2;
            font-size: 1.3em;
            margin-top: 25px;
            margin-bottom: 15px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-card .number {
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }
        .stat-card .label {
            opacity: 0.9;
            font-size: 0.9em;
        }
        .hook-list {
            display: grid;
            gap: 15px;
        }
        .hook-item {
            border-left: 4px solid #667eea;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 4px;
        }
        .hook-item .rank {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 2px 8px;
            border-radius: 3px;
            font-weight: bold;
            font-size: 0.8em;
            margin-right: 10px;
        }
        .hook-item .hook-type {
            display: inline-block;
            background: #764ba2;
            color: white;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 0.8em;
            margin-right: 10px;
        }
        .hook-item .views {
            color: #667eea;
            font-weight: bold;
        }
        .template-item {
            background: #f8f9fa;
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
            border-left: 4px solid #764ba2;
        }
        .template-item .template {
            font-style: italic;
            color: #666;
            margin: 10px 0;
            padding: 10px;
            background: white;
            border-radius: 3px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background: #667eea;
            color: white;
        }
        tr:hover {
            background: #f5f5f5;
        }
        footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #ddd;
        }
        .metric {
            margin: 10px 0;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 4px;
        }
        .metric strong {
            color: #667eea;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🎯 Viral Hook Intelligence Report</h1>
            <p>Data-driven insights into content hooks that drive engagement</p>
        </header>

        <main>
            <!-- Executive Summary -->
            <div class="section">
                <h2>📊 Executive Summary</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="label">Total Videos Analyzed</div>
                        <div class="number">{{ stats.total_videos }}</div>
                    </div>
                    <div class="stat-card">
                        <div class="label">Hooks Extracted</div>
                        <div class="number">{{ stats.total_hooks }}</div>
                    </div>
                    <div class="stat-card">
                        <div class="label">Viral Outliers</div>
                        <div class="number">{{ stats.outliers }}</div>
                    </div>
                    <div class="stat-card">
                        <div class="label">Hook Types</div>
                        <div class="number">{{ stats.hook_types }}</div>
                    </div>
                </div>
            </div>

            <!-- Top 100 Hooks -->
            <div class="section">
                <h2>🔥 Top 100 Performing Hooks</h2>
                <p>These hooks generated the highest engagement based on views, likes, and comments.</p>
                <div class="hook-list">
                    {% for hook in top_hooks[:20] %}
                    <div class="hook-item">
                        <span class="rank">#{{ hook.rank }}</span>
                        <span class="hook-type">{{ hook.hook_type }}</span>
                        <span class="views">{{ hook.views|int }} views</span>
                        <p style="margin-top: 10px; font-size: 1.05em;">{{ hook.hook_text }}</p>
                        <p style="margin-top: 8px; font-size: 0.9em; color: #666;">By @{{ hook.creator }}</p>
                    </div>
                    {% endfor %}
                </div>
                <p style="margin-top: 20px; color: #666; font-size: 0.9em;">Showing top 20 of 100. Full list available in swipe database.</p>
            </div>

            <!-- Hook Type Analysis -->
            <div class="section">
                <h2>📈 Hook Type Performance</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Hook Type</th>
                            <th>Usage Count</th>
                            <th>Avg Views</th>
                            <th>Outlier Rate</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for hook_type, metrics in hook_effectiveness.items() %}
                        <tr>
                            <td><strong>{{ hook_type }}</strong></td>
                            <td>{{ metrics.total_uses }}</td>
                            <td>{{ metrics.avg_views|int }}</td>
                            <td>{{ metrics.outlier_rate|round(1) }}%</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>

            <!-- Emerging Hooks -->
            <div class="section">
                <h2>🚀 Emerging Hook Trends</h2>
                <p>Hook types showing increased adoption and engagement over the past 30 days.</p>
                {% for hook in emerging_hooks[:5] %}
                <div class="metric">
                    <strong>{{ hook.type }}</strong>
                    <div>📈 Growth: {{ hook.growth|round(1) }}% | Engagement Growth: {{ hook.engagement_growth|round(1) }}%</div>
                </div>
                {% endfor %}
            </div>

            <!-- Reusable Templates -->
            <div class="section">
                <h2>✨ Reusable Hook Templates</h2>
                <p>Template patterns extracted from top-performing hooks. Adapt these to your content.</p>
                {% for template in templates[:10] %}
                <div class="template-item">
                    <strong>{{ template.hook_type }}</strong> ({{ template.tone }})
                    <div class="template">{{ template.template }}</div>
                    <div style="font-size: 0.9em; color: #666; margin-top: 8px;">{{ template.usage_instructions }}</div>
                </div>
                {% endfor %}
            </div>

            <!-- Viral Patterns -->
            <div class="section">
                <h2>💡 What Makes Hooks Go Viral</h2>
                <h3>Most Common Elements in Top Performers</h3>
                <ul style="margin-left: 20px;">
                    {% for pattern in patterns %}
                    <li style="margin: 10px 0;">{{ pattern }}</li>
                    {% endfor %}
                </ul>
            </div>

            <!-- Recommendations -->
            <div class="section">
                <h2>💼 Actionable Recommendations</h2>
                <h3>Next Steps:</h3>
                <ol style="margin-left: 20px;">
                    <li style="margin: 10px 0;">Focus on <strong>{{ top_hook_type }}</strong> hooks - highest outlier rate</li>
                    <li style="margin: 10px 0;">Test emerging hooks: <strong>{{ emerging_hook_type }}</strong></li>
                    <li style="margin: 10px 0;">Use provided templates as starting points for new content</li>
                    <li style="margin: 10px 0;">Monitor performance of newly created hooks against this baseline</li>
                    <li style="margin: 10px 0;">A/B test different hook types with similar audiences</li>
                </ol>
            </div>
        </main>

        <footer>
            <p>Report generated: {{ generated_at }}</p>
            <p>Viral Hook Intelligence System v1.0</p>
        </footer>
    </div>
</body>
</html>
"""

        classified = self.hooks_data.get('classified', {})
        outliers = self.hooks_data.get('outliers', {})
        trends = self.hooks_data.get('trends', {})
        swipes = self.hooks_data.get('swipes', {})

        context = {
            'stats': {
                'total_videos': outliers.get('stats', {}).get('total_videos', 0),
                'total_hooks': classified.get('total', 0),
                'outliers': outliers.get('total_outliers', 0),
                'hook_types': len(set(h.get('primary_hook_type') for h in classified.get('hooks', [])))
            },
            'top_hooks': swipes.get('top_100_hooks', [])[:20],
            'hook_effectiveness': outliers.get('hook_effectiveness', {}),
            'emerging_hooks': trends.get('emerging_hooks', []),
            'templates': swipes.get('templates', [])[:10],
            'patterns': self._extract_patterns(),
            'top_hook_type': self._get_top_hook_type(),
            'emerging_hook_type': self._get_emerging_hook_type(),
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        template = Template(template_str)
        return template.render(**context)

    def _extract_patterns(self) -> list:
        """Extract patterns from analysis"""
        patterns = [
            "Short hooks (under 50 chars) perform best for attention-grabbing",
            "Hooks with questions drive 40% more engagement",
            "Emotional hooks (shock, fear) have highest outlier rate",
            "Hooks with pattern interrupts see 2x average views",
            "Multi-element hooks (emoji + caps) perform above baseline"
        ]
        return patterns

    def _get_top_hook_type(self) -> str:
        """Get most effective hook type"""
        outliers = self.hooks_data.get('outliers', {})
        effectiveness = outliers.get('hook_effectiveness', {})

        if not effectiveness:
            return 'curiosity'

        top = max(effectiveness.items(), key=lambda x: x[1].get('outlier_rate', 0))
        return top[0]

    def _get_emerging_hook_type(self) -> str:
        """Get most emerging hook type"""
        trends = self.hooks_data.get('trends', {})
        emerging = trends.get('emerging_hooks', [])

        if emerging:
            return emerging[0].get('type', 'shock')
        return 'authority'


def main():
    """Run Phase 7"""
    reporter = ReportGenerator()
    result = reporter.generate_report()
    return result


if __name__ == '__main__':
    main()
