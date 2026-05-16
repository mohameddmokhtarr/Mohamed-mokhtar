# Viral Hook Intelligence System

A production-grade platform for analyzing viral content hooks across TikTok and Instagram Reels using Apify for scraping and Anthropic Claude for intelligent classification.

## 🎯 Features

- **8-Phase Pipeline**: Automated content analysis from scraping to report generation
- **Anthropic Claude API**: Intelligent hook classification (curiosity, shock, authority, etc.)
- **Apify Integration**: Reliable scraping of TikTok and Instagram Reels
- **Viral Pattern Detection**: Identify what makes hooks go viral
- **Swipe Database**: 100 top-performing hooks + 50 reusable templates
- **HTML Reports**: Beautiful, data-driven reports with insights
- **Recovery Mode**: Resume from failures without re-scraping

## 📋 System Architecture

```
Phase 1: Content Scraping (Apify)
    ↓
Phase 2: Hook Extraction (Caption parsing)
    ↓
Phase 3: Hook Classification (Claude API)
    ↓
Phase 4: Trend Analysis (Time-based patterns)
    ↓
Phase 5: Outlier Analysis (Viral detection)
    ↓
Phase 6: Swipe Database (Templates + top 100)
    ↓
Phase 7: Report Generation (HTML)
    ↓
Phase 8: System Audit (Verification)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- API Keys:
  - Anthropic Claude: https://console.anthropic.com/account/keys
  - Apify: https://console.apify.com/account/integrations

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Configure API keys
# Edit .env and add:
# ANTHROPIC_API_KEY=sk-ant-...
# APIFY_API_TOKEN=apify_api_...

# Verify setup
python3 bootstrap.py
```

### Run Full Pipeline

```bash
python3 main.py
```

This runs all 8 phases and generates outputs in:
- `hooks/classified_hooks.json` - All classified hooks
- `hooks/swipe_database.json` - Top 100 + templates
- `hooks/trend_analysis.json` - Trend patterns
- `hooks/outlier_analysis.json` - Viral outliers
- `reports/viral-hook-report.html` - Beautiful report

### Run Individual Phases

```bash
# Phase 1: Scrape content
python3 phase1_scraper.py

# Phase 2: Extract hooks
python3 phase2_hook_extraction.py

# Phase 3: Classify hooks
python3 phase3_classification.py

# Phase 4: Analyze trends
python3 phase4_trend_analysis.py

# Phase 5: Find outliers
python3 phase5_outlier_analysis.py

# Phase 6: Build swipe database
python3 phase6_swipe_database.py

# Phase 7: Generate report
python3 phase7_report.py

# Phase 8: Run audit
python3 phase8_audit.py
```

## 📊 Data Flow

### Input
- TikTok profiles: @mokhtarsays_, @abdulosama90, @ai_bilarabi, @mabuzant
- Instagram profiles: same handles
- Data: Captions (no video downloads)

### Processing
- Normalize data from different platforms
- Extract first 3-10 sentences from captions as hooks
- Classify hooks using Claude (haiku-4-5-20251001)
- Analyze trends across 30/90/365 day periods
- Identify outliers (≥2x local median views)
- Generate templates from patterns

### Output
- **classified_hooks.json**: All hooks with classifications
- **swipe_database.json**: Top 100 hooks + 50 templates
- **trend_analysis.json**: Time-based trend patterns
- **outlier_analysis.json**: Viral hooks + patterns
- **viral-hook-report.html**: Executive summary report

## 🔍 Hook Classification

### Hook Types (10)
- **Curiosity**: Questions or mysteries
- **Shock**: Surprising/unexpected statements
- **Authority**: Credibility-based hooks
- **Contrarian**: Against conventional wisdom
- **Storytelling**: Narrative-driven
- **Fear**: Problem/pain highlighting
- **Aspiration**: Desirable outcomes
- **Direct Benefit**: Clear value proposition
- **Mistake-Based**: Common mistakes revealed
- **Comparison**: Comparison-driven

### Tones (6)
- Conversational
- Authoritative
- Humorous
- Urgent
- Inspirational
- Informative

## 📈 Analysis Metrics

- **Engagement Rate**: (Likes + Comments) / Views
- **Outlier Ratio**: Videos ≥2x local median views
- **Hook Effectiveness**: Outlier rate by hook type
- **Emerging Hooks**: ≥30% growth in past 30 days
- **Performance Rank**: By outlier rate

## ⚙️ Configuration

Edit `config.py` to customize:

```python
CREATORS = {
    'my_account': '@mokhtarsays_',
    'competitors': ['@abdulosama90', '@ai_bilarabi', '@mabuzant']
}

HOOK_TYPES = [
    'curiosity', 'shock', 'authority', ...
]

PLATFORMS = ['tiktok', 'instagram']
```

## 🛡️ Error Handling

- **Recovery Mode**: Checks for existing outputs, skips completed phases
- **Rate Limiting**: Auto-retry with exponential backoff on Apify 429 errors
- **Graceful Degradation**: Continues on individual failures, logs all errors
- **Comprehensive Logging**: `logs/system.log`, `logs/scraper.log`, `logs/errors.log`

## 📁 Folder Structure

```
viral-hook-intelligence/
├── raw-data/              # Raw API responses (Phase 1)
├── hooks/                 # Extracted & analyzed hooks (Phases 2-6)
├── transcripts/          # (Reserved for future use)
├── adapters/             # Platform normalizers
├── reports/              # HTML reports (Phase 7)
├── logs/                 # Detailed logs
├── config.py             # Configuration
├── logger.py             # Logging setup
├── main.py               # Orchestrator
├── phase1_scraper.py     # Content scraping
├── phase2_hook_extraction.py
├── phase3_classification.py  # Claude API
├── phase4_trend_analysis.py
├── phase5_outlier_analysis.py
├── phase6_swipe_database.py
├── phase7_report.py
├── phase8_audit.py
└── README.md
```

## 🔧 Dependencies

- **anthropic**: Claude API client
- **apify-client**: Apify actor runner
- **pandas/numpy**: Data analysis
- **jinja2**: Report templating
- **matplotlib**: (Reserved for charts)
- **scikit-learn**: Outlier detection

## 📋 Output Examples

### classified_hooks.json
```json
{
  "hook_text": "Did you know...",
  "primary_hook_type": "curiosity",
  "secondary_hook_types": ["shock"],
  "tone": "conversational",
  "views": 45000,
  "engagement_rate": 0.087
}
```

### swipe_database.json
```json
{
  "top_100_hooks": [...],
  "templates": [
    {
      "template": "Did you know [fact about DOMAIN]?",
      "hook_type": "curiosity",
      "example": "Did you know 90% of creators..."
    }
  ]
}
```

## 🚨 Troubleshooting

### "No hooks extracted"
- Check if captions are empty in raw data
- Minimum dataset: 20 videos with captions

### "Classification failed"
- Verify ANTHROPIC_API_KEY is set correctly
- Check rate limits on Claude API

### "Apify actor failed"
- Verify APIFY_API_TOKEN is valid
- Check if actor ID is correct
- Actor may be under maintenance

### "Report not generated"
- Verify classified_hooks.json exists
- Check if hooks directory is writable

## 📊 Report Interpretation

The HTML report includes:

1. **Executive Summary**: Key metrics at a glance
2. **Top 100 Hooks**: Highest-performing hooks by engagement
3. **Hook Type Analysis**: Performance by hook type
4. **Emerging Trends**: Growing hook patterns
5. **Templates**: Reusable patterns for your content
6. **Recommendations**: Actionable next steps

## 🔐 Security

- API keys stored in `.env` (never committed)
- `.gitignore` prevents accidental credential exposure
- No video downloads (captions only)
- All data processing is local

## 📝 License

Proprietary - Content Intelligence

## 🤝 Support

For issues or improvements, check:
- `logs/errors.log` for detailed errors
- `logs/system.log` for execution flow
- Console output for real-time progress

---

**Version**: 1.0.0  
**Last Updated**: 2026-05-16  
**Status**: Production Ready ✅
