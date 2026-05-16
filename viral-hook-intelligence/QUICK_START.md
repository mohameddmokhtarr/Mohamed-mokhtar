# 🚀 Quick Start Guide

Get your viral hook analysis running in **3 steps**:

---

## Step 1️⃣: Setup (5 min)

```bash
cd viral-hook-intelligence

# Install/verify dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env and add:
# APIFY_API_TOKEN=apify_api_...
```

---

## Step 2️⃣: Install Ollama (Free AI)

```bash
# Download & install from: https://ollama.ai
# Then download the model:
ollama pull mistral
```

---

## Step 3️⃣: Run Pipeline

Open **2 terminal windows**:

**Terminal 1** (keep this running):
```bash
ollama serve
```

**Terminal 2** (your working directory):
```bash
cd viral-hook-intelligence
python3 main.py
```

---

## ✅ Done!

Wait ~50 minutes, then view:

```
📊 reports/viral-hook-report.html
```

Open in browser → See all insights!

---

## 📊 What You Get

- 🔥 Top 100 viral hooks analyzed
- 📈 Trending hook patterns
- 🎯 50 reusable templates
- 💡 Actionable recommendations
- 📋 Complete competitor analysis

---

## 🎯 Check Progress

In another terminal:
```bash
tail -f viral-hook-intelligence/logs/system.log
```

---

## 💾 Output Files

```
✅ reports/viral-hook-report.html       ← Main report
✅ hooks/classified_hooks.json          ← All classified hooks
✅ hooks/swipe_database.json            ← Top 100 + templates
✅ hooks/trend_analysis.json            ← Trends
✅ hooks/outlier_analysis.json          ← Viral hooks
```

---

## 🚀 Single Phase Run

Test a single phase first:

```bash
# Just extract hooks (no AI needed)
python3 phase2_hook_extraction.py

# Just classify with Ollama
python3 phase3_classification.py

# Run any phase individually
python3 phase1_scraper.py           # Scrape data
python3 phase4_trend_analysis.py    # Analyze trends
python3 phase7_report.py            # Generate report
```

---

## 🆘 Troubleshooting

**"Can't connect to Ollama"**
- Make sure Ollama is running in Terminal 1
- Check: `curl http://localhost:11434/api/tags`

**"No data scraped"**
- Check if raw-data/ folder has JSON files
- Verify APIFY_API_TOKEN in .env

**"Report not generated"**
- Check logs: `tail logs/system.log`
- Ensure Phase 1-6 completed first

---

## 📚 Full Docs

- **SETUP_INSTRUCTIONS.md** - Complete setup guide
- **RUN_PIPELINE.md** - Detailed execution info
- **OLLAMA_SETUP.md** - Ollama details
- **README.md** - Full system documentation

---

## ⚡ Speed Tips

- **Use GPU**: Install NVIDIA/AMD drivers for 5-10x speedup
- **Smaller Model**: Use `neural-chat` instead of `mistral` (faster)
- **More RAM**: 8GB+ recommended for smooth operation

---

**Ready?** → `ollama serve` + `python3 main.py` 🎯
