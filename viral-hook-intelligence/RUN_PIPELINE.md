# 🚀 Running the Complete Viral Hook Intelligence Pipeline

## Quick Start

### 1. **Setup Environment**

```bash
# Install dependencies
pip install -r requirements.txt

# Create and configure .env
cp .env.example .env

# Add your API keys:
# ANTHROPIC_API_KEY=sk-ant-...
# APIFY_API_TOKEN=apify_api_...
```

### 2. **Run Full Pipeline (All 8 Phases)**

```bash
python3 main.py
```

This runs:
- **Phase 1**: Scrape TikTok & Instagram (@mokhtarsays_, competitors)
- **Phase 2**: Extract hooks from captions (first 3-10 sentences)
- **Phase 3**: Classify hooks using Claude AI (10 types + 6 tones)
- **Phase 4**: Analyze trends (30/90/365 day patterns)
- **Phase 5**: Identify viral outliers (≥2x local median views)
- **Phase 6**: Build swipe database (top 100 hooks + 50 templates)
- **Phase 7**: Generate HTML report with insights
- **Phase 8**: System audit & verification

### 3. **View Results**

After execution, outputs appear in:

```
✅ reports/viral-hook-report.html          # Interactive HTML report
✅ hooks/classified_hooks.json             # All classified hooks
✅ hooks/swipe_database.json               # Top 100 + 50 templates
✅ hooks/trend_analysis.json               # Trend patterns
✅ hooks/outlier_analysis.json             # Viral hooks
✅ logs/system.log                         # Execution log
```

---

## Run Individual Phases

### Phase 1: Content Scraping
```bash
python3 phase1_scraper.py
```
**Output**: `raw-data/tiktok-*.json`, `raw-data/instagram-*.json`

### Phase 2: Hook Extraction
```bash
python3 phase2_hook_extraction.py
```
**Output**: `hooks/all_hooks.json` (captions → 3-10 sentence hooks)

### Phase 3: Hook Classification
```bash
python3 phase3_classification.py
```
**Output**: `hooks/classified_hooks.json` (Claude AI classification)

### Phase 4: Trend Analysis
```bash
python3 phase4_trend_analysis.py
```
**Output**: `hooks/trend_analysis.json` (30/90/365 day buckets)

### Phase 5: Outlier Analysis
```bash
python3 phase5_outlier_analysis.py
```
**Output**: `hooks/outlier_analysis.json` (viral detection)

### Phase 6: Swipe Database
```bash
python3 phase6_swipe_database.py
```
**Output**: `hooks/swipe_database.json` (templates + top 100)

### Phase 7: Report Generation
```bash
python3 phase7_report.py
```
**Output**: `reports/viral-hook-report.html` (beautiful report)

### Phase 8: System Audit
```bash
python3 phase8_audit.py
```
**Output**: Audit results + final verification

---

## Data Collection Details

### Creators Analyzed
- **Your Account**: @mokhtarsays_
- **Competitors**: @abdulosama90, @ai_bilarabi, @mabuzant
- **Platforms**: TikTok, Instagram

### What Gets Scraped
- ✅ Captions (text only)
- ✅ View counts, likes, comments
- ✅ Upload dates
- ✅ Video duration
- ❌ No video downloads (captions only)

### Hook Classification
**10 Hook Types**:
- Curiosity (questions, mysteries)
- Shock (surprising statements)
- Authority (credibility-based)
- Contrarian (against conventional wisdom)
- Storytelling (narrative-driven)
- Fear (problem/pain highlighting)
- Aspiration (desirable outcomes)
- Direct Benefit (clear value)
- Mistake-Based (common mistakes)
- Comparison (comparison-driven)

**6 Tones**:
- Conversational, Authoritative, Humorous
- Urgent, Inspirational, Informative

---

## Recovery Mode

The system automatically skips completed phases:

```bash
# If Phase 1-3 succeeded but Phase 4 failed:
python3 main.py  # Resumes from Phase 4
```

To force re-run all phases:
```bash
rm -rf raw-data/*.json hooks/*.json reports/*.html
python3 main.py
```

---

## Troubleshooting

### "Apify API error: 404"
- Check actor IDs in `config.py` use tildes: `clockworks~free-tiktok-scraper`
- Verify `APIFY_API_TOKEN` in `.env`

### "ANTHROPIC_API_KEY not found"
- Add to `.env`: `ANTHROPIC_API_KEY=sk-ant-...`
- Verify key at: https://console.anthropic.com/account/keys

### "No hooks extracted"
- Ensure Phase 1 scraped data (check `raw-data/`)
- Minimum 20 videos with captions required

### "Classification failed"
- Check API rate limits
- Verify Anthropic account has credits
- Check logs: `tail -f logs/system.log`

---

## Key Metrics in Report

- **Engagement Rate**: (Likes + Comments) / Views
- **Outlier Ratio**: Videos ≥2x local median views
- **Hook Effectiveness**: Outlier rate by hook type
- **Emerging Hooks**: ≥30% growth in past 30 days

---

## Output File Examples

### classified_hooks.json
```json
{
  "hooks": [
    {
      "hook_text": "Did you know...",
      "primary_hook_type": "curiosity",
      "secondary_hook_types": ["shock"],
      "tone": "conversational",
      "views": 45000,
      "likes": 2100,
      "engagement_rate": 0.087
    }
  ]
}
```

### swipe_database.json
```json
{
  "top_100_hooks": [...],
  "templates": [
    {
      "template": "Did you know [FACT about DOMAIN]?",
      "hook_type": "curiosity",
      "tone": "conversational",
      "example": "Did you know 90% of creators..."
    }
  ]
}
```

---

## API Costs

- **Apify**: ~$0.50-2.00 per run (depending on data volume)
- **Anthropic Claude**: ~$0.01-0.05 per 100 hooks
- **Total**: ~$1-3 per complete run

---

## Next Steps After Report

1. **Review Top Hooks** in the HTML report
2. **Identify Patterns** in emerging hook types
3. **Test Templates** with your own content
4. **A/B Test** hook types with your audience
5. **Monitor Performance** of new hooks

---

**Version**: 1.0.0  
**Last Updated**: 2026-05-16  
**Status**: Production Ready ✅
