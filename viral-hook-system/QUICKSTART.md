# Quick Start Guide

## 5-Minute Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Verify setup
```bash
python verify_env.py
```

## Running the System

### Option A: Full Production Pipeline
Requires: Apify API key + OpenAI API key

```bash
python main.py
```

### Option B: Demo Mode (Recommended First Run)
No API keys needed. Uses mock data.

```bash
# Generate demo data
python demo.py

# Run phases 4-8 (trend analysis → report)
python -c "
from phase_4_trends import run_phase_4
from phase_5_performance import run_phase_5
from phase_6_swipe_db import run_phase_6
from phase_7_html_report import run_phase_7
from phase_8_audit import run_phase_8
run_phase_4()
run_phase_5()
run_phase_6()
run_phase_7()
run_phase_8()
"
```

### Option C: Individual Phases
```python
from phase_1_scraper import run_phase_1
from phase_2_transcription import run_phase_2
from phase_3_classification import run_phase_3

# Run just the phases you need
data = run_phase_1()
hooks = run_phase_2()
classified = run_phase_3()
```

## View Results

### Open HTML Report
```bash
# macOS
open reports/viral-hook-report.html

# Linux
xdg-open reports/viral-hook-report.html

# Windows
start reports/viral-hook-report.html
```

### Inspect JSON Outputs
```bash
# Raw scraped data
cat raw-data/tiktok-competitor1.json | head -20

# Classified hooks
cat hooks/tiktok-competitor1-classified.json | python -m json.tool

# Swipe database
cat hooks/swipe-database.json | python -m json.tool | head -50

# Trend analysis
cat hooks/trend-analysis.json | python -m json.tool

# Performance analysis
cat hooks/performance-analysis.json | python -m json.tool
```

## Get API Keys

### OpenAI API Key
1. Go to https://platform.openai.com/account/api-keys
2. Create new secret key
3. Copy to `.env`: `OPENAI_API_KEY=sk-...`

### Apify API Key
1. Go to https://apify.com/sign-up
2. Create account
3. Go to Account settings → Integrations
4. Copy API token
5. Copy to `.env`: `APIFY_API_KEY=...`

## Customize Target Accounts

Edit `config.py`:
```python
COMPETITORS = ['@competitor1', '@competitor2', '@competitor3']
MY_ACCOUNT = '@myhandle'
```

## Troubleshooting

### "OPENAI_API_KEY not configured"
- Edit `.env` with your actual key (not placeholder)
- Restart Python process

### "Actor not found"
- Check internet connection
- Verify Apify API key is valid
- Use `demo.py` instead

### No hooks generated in Phase 2
- This is normal without real API keys
- Use `demo.py` for testing

### Report won't open
- Clear browser cache (Ctrl+Shift+Delete)
- Try Chrome instead of Safari
- Check `reports/viral-hook-report.html` exists

## What Each Phase Does

| Phase | Input | Output | Time |
|-------|-------|--------|------|
| 1 | Accounts | raw-data/ | 5-10m |
| 2 | raw-data/ | transcripts/ | 10-15m |
| 3 | transcripts/ | hooks/*-classified.json | 1m |
| 4 | classified | trend-analysis.json | 30s |
| 5 | classified | performance-analysis.json | 1m |
| 6 | classified | swipe-database.json | 1m |
| 7 | all above | viral-hook-report.html | 2m |
| 8 | all outputs | audit report | 30s |

## Common Use Cases

### Case 1: Find trending hooks (demo)
```bash
python demo.py && python -c "from phase_4_trends import run_phase_4; run_phase_4()"
```

### Case 2: Analyze competitor (production)
```bash
# Edit config.py, set COMPETITORS, then:
python main.py
```

### Case 3: Generate content templates (from existing data)
```bash
python -c "from phase_6_swipe_db import run_phase_6; run_phase_6()"
```

### Case 4: Full analysis from scratch (production)
```bash
# Configure API keys, customize accounts, then:
python main.py
```

## Next Steps

1. **Try demo first**: `python demo.py`
2. **View report**: Open `reports/viral-hook-report.html`
3. **Review templates**: Check `hooks/swipe-database.json`
4. **Get API keys** for production use
5. **Customize accounts**: Edit `config.py`
6. **Run full pipeline**: `python main.py`

## Getting Help

- Check `errors.log` for system errors
- Run `python verify_env.py` to diagnose issues
- Review Phase 8 audit results
- See README.md for detailed documentation

---

**Ready to discover viral hooks?** Start with: `python demo.py`
