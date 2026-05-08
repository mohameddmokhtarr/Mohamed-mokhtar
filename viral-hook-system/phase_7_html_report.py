"""Phase 7: Generate comprehensive HTML report."""

import json
from pathlib import Path
from jinja2 import Template
from logger import setup_logger
from config import HOOKS_DIR, REPORTS_DIR

logger = setup_logger('phase_7_html_report')

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Viral Hook Intelligence Report</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 40px;
            text-align: center;
        }

        .header h1 {
            font-size: 3em;
            margin-bottom: 10px;
        }

        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }

        .content {
            padding: 40px;
        }

        .section {
            margin-bottom: 50px;
            border-left: 4px solid #667eea;
            padding-left: 30px;
        }

        .section h2 {
            font-size: 2em;
            margin-bottom: 20px;
            color: #667eea;
        }

        .section h3 {
            font-size: 1.5em;
            margin-top: 20px;
            margin-bottom: 15px;
            color: #764ba2;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }

        .card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #e9ecef;
        }

        .card h4 {
            color: #667eea;
            margin-bottom: 10px;
        }

        .metric {
            font-size: 2em;
            color: #764ba2;
            font-weight: bold;
            margin: 10px 0;
        }

        .metric-label {
            color: #666;
            font-size: 0.9em;
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
            background: #f8f9fa;
            font-weight: 600;
            color: #667eea;
        }

        tr:hover {
            background: #f8f9fa;
        }

        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }

        .badge-primary {
            background: #e3f2fd;
            color: #1976d2;
        }

        .badge-success {
            background: #e8f5e9;
            color: #388e3c;
        }

        .badge-warning {
            background: #fff3e0;
            color: #f57c00;
        }

        .hook-box {
            background: #f5f5f5;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #667eea;
            border-radius: 4px;
        }

        .hook-text {
            font-size: 1.1em;
            margin: 10px 0;
            font-style: italic;
            color: #333;
        }

        .hook-meta {
            font-size: 0.9em;
            color: #666;
            margin-top: 10px;
        }

        .stat-row {
            display: flex;
            justify-content: space-between;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }

        .stat-label {
            color: #666;
        }

        .stat-value {
            font-weight: bold;
            color: #333;
        }

        .list-item {
            margin: 15px 0;
            padding: 15px;
            background: #fafafa;
            border-radius: 6px;
        }

        .ranking {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .rank-num {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 50%;
            font-weight: bold;
            font-size: 1.2em;
        }

        .rank-content {
            flex: 1;
        }

        .footer {
            background: #f8f9fa;
            padding: 20px 40px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }

        .no-data {
            text-align: center;
            padding: 40px;
            color: #999;
        }

        ul {
            margin-left: 20px;
        }

        li {
            margin: 8px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Viral Hook Intelligence</h1>
            <p>Social Media Trend Analysis & Performance Report</p>
        </div>

        <div class="content">
            <!-- Executive Summary -->
            <div class="section">
                <h2>📊 Executive Summary</h2>
                <div class="grid">
                    <div class="card">
                        <h4>Total Videos Analyzed</h4>
                        <div class="metric">{{ summary.total_videos }}</div>
                    </div>
                    <div class="card">
                        <h4>Hook Types Discovered</h4>
                        <div class="metric">{{ summary.hook_types }}</div>
                    </div>
                    <div class="card">
                        <h4>Emerging Trends</h4>
                        <div class="metric">{{ summary.emerging_count }}</div>
                    </div>
                    <div class="card">
                        <h4>Top Hooks Ranked</h4>
                        <div class="metric">{{ summary.top_hooks }}</div>
                    </div>
                </div>
            </div>

            <!-- Top 20 Performing Hooks -->
            <div class="section">
                <h2>🏆 Top 20 Performing Hooks</h2>
                {% if top_hooks %}
                    {% for hook in top_hooks[:20] %}
                    <div class="list-item">
                        <div class="ranking">
                            <div class="rank-num">{{ loop.index }}</div>
                            <div class="rank-content">
                                <div class="hook-text">"{{ hook.hook_text }}"</div>
                                <div class="hook-meta">
                                    <span class="badge badge-primary">{{ hook.type }}</span>
                                    <span style="margin-left: 10px;">👁 {{ hook.views }} views</span>
                                    <span style="margin-left: 10px;">💬 {{ hook.engagement }} engagement</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                {% else %}
                    <div class="no-data">No top hooks data available</div>
                {% endif %}
            </div>

            <!-- Hook Types Performance -->
            <div class="section">
                <h2>📈 Hook Type Performance</h2>
                {% if performance_by_type %}
                    <table>
                        <thead>
                            <tr>
                                <th>Hook Type</th>
                                <th>Count</th>
                                <th>Avg Views</th>
                                <th>Avg Engagement</th>
                                <th>Performance Rank</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for hook_type in performance_by_type %}
                                {% set perf = performance_by_type[hook_type] %}
                            <tr>
                                <td><strong>{{ hook_type }}</strong></td>
                                <td>{{ perf.count }}</td>
                                <td>{{ perf.avg_views }}</td>
                                <td>{{ perf.avg_engagement }}</td>
                                <td>
                                    {% if perf.avg_views > avg_views_overall %}
                                        <span class="badge badge-success">Above Average</span>
                                    {% else %}
                                        <span class="badge badge-warning">Below Average</span>
                                    {% endif %}
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                {% else %}
                    <div class="no-data">No performance data available</div>
                {% endif %}
            </div>

            <!-- Emerging Trends -->
            <div class="section">
                <h2>🔥 Emerging Trends</h2>
                {% if emerging_hooks %}
                    {% for trend in emerging_hooks %}
                    <div class="card">
                        <h4>{{ trend.hook_type }}</h4>
                        <div class="stat-row">
                            <span class="stat-label">Frequency Trend:</span>
                            <span class="stat-value">{{ trend.frequency_trend }}</span>
                        </div>
                        <div class="stat-row">
                            <span class="stat-label">Engagement Increase:</span>
                            <span class="stat-value" style="color: #4caf50;">{{ trend.engagement_increase }}</span>
                        </div>
                        <div class="stat-row">
                            <span class="stat-label">Current Avg Engagement:</span>
                            <span class="stat-value">{{ trend.current_avg_engagement }}</span>
                        </div>
                    </div>
                    {% endfor %}
                {% else %}
                    <div class="no-data">No emerging trends detected</div>
                {% endif %}
            </div>

            <!-- Swipe Templates -->
            <div class="section">
                <h2>📋 Reusable Hook Templates</h2>
                <p>Ready-to-use templates extracted from top-performing hooks. Fill in the blanks for instant content hooks.</p>
                {% if templates %}
                    {% for hook_type in templates %}
                        {% set data = templates[hook_type] %}
                        <h3>{{ hook_type|replace('_', ' ')|title }}</h3>
                        {% if data.templates %}
                            <div class="card">
                                <strong>Templates:</strong>
                                <ul>
                                    {% for template in data.templates %}
                                        <li><code>{{ template }}</code></li>
                                    {% endfor %}
                                </ul>
                                {% if data.examples %}
                                    <strong style="margin-top: 15px; display: block;">Examples from top performers:</strong>
                                    <ul>
                                        {% for example in data.examples %}
                                            <li>{{ example }}</li>
                                        {% endfor %}
                                    </ul>
                                {% endif %}
                            </div>
                        {% endif %}
                    {% endfor %}
                {% else %}
                    <div class="no-data">No templates available</div>
                {% endif %}
            </div>

            <!-- Outlier Analysis -->
            <div class="section">
                <h2>⚡ Viral Outliers (2x+ Local Median)</h2>
                {% if outliers %}
                    <p><strong>{{ outliers|length }} viral outliers detected</strong></p>
                    <table>
                        <thead>
                            <tr>
                                <th>Hook Type</th>
                                <th>Views</th>
                                <th>Local Median</th>
                                <th>Multiplier</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for outlier in outliers[:20] %}
                            <tr>
                                <td>{{ outlier.hook_type }}</td>
                                <td>{{ outlier.views }}</td>
                                <td>{{ outlier.local_median }}</td>
                                <td><strong>{{ outlier.multiplier|round(2) }}x</strong></td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                {% else %}
                    <div class="no-data">No viral outliers detected</div>
                {% endif %}
            </div>

            <!-- Recommendations -->
            <div class="section">
                <h2>💡 Strategic Recommendations</h2>
                <ul>
                    {% if emerging_hooks %}
                        <li><strong>Focus on emerging trends:</strong> {{ emerging_hooks|length }} hook types are showing ≥30% engagement growth</li>
                    {% endif %}
                    {% if top_hook_type %}
                        <li><strong>Lead with {{ top_hook_type }}:</strong> This hook type consistently outperforms others</li>
                    {% endif %}
                    <li><strong>Use templates:</strong> Fill-in-the-blank templates above provide proven frameworks</li>
                    <li><strong>Test outlier hooks:</strong> Study viral outliers for breakthrough patterns</li>
                    <li><strong>Monitor time buckets:</strong> Track weekly performance changes in hook effectiveness</li>
                </ul>
            </div>
        </div>

        <div class="footer">
            <p>Generated by Viral Hook Intelligence System | Analysis covers all scraped social media content</p>
        </div>
    </div>
</body>
</html>
'''

def load_swipe_database():
    """Load the swipe database."""
    swipe_file = HOOKS_DIR / 'swipe-database.json'
    if swipe_file.exists():
        with open(swipe_file, 'r') as f:
            return json.load(f)
    return {}

def load_performance_analysis():
    """Load performance analysis."""
    perf_file = HOOKS_DIR / 'performance-analysis.json'
    if perf_file.exists():
        with open(perf_file, 'r') as f:
            return json.load(f)
    return {}

def load_trend_analysis():
    """Load trend analysis."""
    trend_file = HOOKS_DIR / 'trend-analysis.json'
    if trend_file.exists():
        with open(trend_file, 'r') as f:
            return json.load(f)
    return {}

def generate_report():
    """Generate comprehensive HTML report."""
    swipe_db = load_swipe_database()
    performance = load_performance_analysis()
    trends = load_trend_analysis()

    # Prepare data for template
    summary = {
        'total_videos': 0,
        'hook_types': len(swipe_db.get('templates_by_type', {})),
        'emerging_count': len(trends.get('all_emerging', [])),
        'top_hooks': swipe_db.get('metadata', {}).get('top_hooks_count', 0),
    }

    # Count total videos
    for dataset in performance.values():
        summary['total_videos'] += dataset.get('total_videos', 0)

    # Extract data
    top_hooks = swipe_db.get('top_hooks', [])
    performance_by_type = {}

    for dataset in performance.values():
        for hook_type, perf in dataset.get('performance_by_type', {}).items():
            if hook_type not in performance_by_type:
                performance_by_type[hook_type] = {
                    'count': 0,
                    'avg_views': 0,
                    'avg_engagement': 0,
                }
            performance_by_type[hook_type]['count'] += perf['count']
            performance_by_type[hook_type]['avg_views'] += perf['avg_views']
            performance_by_type[hook_type]['avg_engagement'] += perf['avg_engagement']

    # Calculate overall averages
    avg_views_overall = 0
    if performance_by_type:
        avg_views_overall = sum(
            p['avg_views'] for p in performance_by_type.values()
        ) / len(performance_by_type)

    # Collect outliers
    all_outliers = []
    for dataset in performance.values():
        all_outliers.extend(dataset.get('outliers', []))

    all_outliers.sort(key=lambda x: x.get('multiplier', 0), reverse=True)

    emerging_hooks = trends.get('all_emerging', [])

    templates = swipe_db.get('templates_by_type', {})

    top_hook_type = None
    if performance_by_type:
        top_hook_type = max(
            performance_by_type.items(),
            key=lambda x: x[1]['avg_engagement']
        )[0]

    # Render template
    template = Template(HTML_TEMPLATE)
    html = template.render(
        summary=summary,
        top_hooks=top_hooks,
        performance_by_type=performance_by_type,
        avg_views_overall=avg_views_overall,
        emerging_hooks=emerging_hooks,
        templates=templates,
        outliers=all_outliers,
        top_hook_type=top_hook_type,
    )

    return html

def run_phase_7():
    """Execute Phase 7: HTML Report Generation."""
    logger.info("="*60)
    logger.info("PHASE 7: GENERATE HTML REPORT")
    logger.info("="*60)

    html = generate_report()

    # Save report
    report_file = REPORTS_DIR / 'viral-hook-report.html'
    with open(report_file, 'w') as f:
        f.write(html)

    logger.info(f"✅ HTML report generated: {report_file}")
    logger.info(f"   Open in browser to view interactive report")

    return report_file

if __name__ == '__main__':
    run_phase_7()
