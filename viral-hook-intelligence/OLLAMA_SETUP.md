# 🎯 Running with Ollama (Free Local AI)

Your system is configured to use **Ollama** for hook classification - completely free and runs locally on your machine!

---

## 📋 Prerequisites

- Ollama installed: https://ollama.ai
- 4GB RAM minimum (8GB+ recommended)
- 5GB disk space for Mistral model

---

## 🚀 Quick Start

### 1. Install Ollama
```bash
# macOS
brew install ollama

# Linux
curl https://ollama.ai/install.sh | sh

# Windows
Download from https://ollama.ai
```

### 2. Download Mistral Model
```bash
ollama pull mistral
```
This downloads ~4GB model (one-time)

### 3. Start Ollama Server
```bash
# Open NEW terminal window and keep it running
ollama serve
```
You should see: `Listening on 127.0.0.1:11434`

### 4. Run Pipeline (in another terminal)
```bash
cd viral-hook-intelligence
python3 main.py
```

---

## ⚙️ System Requirements

### Minimum
- CPU: Dual-core
- RAM: 4GB
- Disk: 5GB free

### Recommended
- CPU: Quad-core (faster processing)
- RAM: 8GB+ (allows other apps to run)
- Disk: 10GB free
- GPU: NVIDIA/AMD (optional, speeds up 5-10x)

---

## 🔧 Troubleshooting

### "Connection refused" Error

**Problem**: Can't connect to Ollama

**Solution**:
1. Verify Ollama is running: `ollama serve`
2. Check port 11434 is open: `curl http://localhost:11434/api/tags`
3. Restart Ollama server

### "Model not found" Error

**Problem**: Mistral model not loaded

**Solution**:
```bash
ollama pull mistral
ollama list  # Verify it shows "mistral"
```

### Slow Processing

**Problem**: Classification taking >10 seconds per hook

**Solution**:
- Install GPU drivers for your system
- Use GPU: https://ollama.ai/library/mistral (has GPU instructions)
- Reduce model size: `ollama pull neural-chat` (smaller, faster)

### Out of Memory

**Problem**: "Killed" process during classification

**Solution**:
- Close other applications
- Upgrade RAM if possible
- Use smaller model: `ollama pull orca-mini` (1.7GB)

---

## 📊 Performance Benchmarks

These are typical times per hook classification:

| Setup | Time/Hook | Total (100 hooks) |
|-------|-----------|------------------|
| CPU only (4-core) | 3-5s | 5-10 min |
| CPU only (8-core) | 2-3s | 3-5 min |
| With GPU (NVIDIA) | 0.5-1s | 1-2 min |

---

## 🎯 Alternative Models

If Mistral is slow, try these lighter models:

```bash
# Faster, smaller (good balance)
ollama pull neural-chat

# Very fast, lower quality
ollama pull orca-mini

# More capable but slower
ollama pull llama2
```

**Recommended**: Start with `mistral`, switch if needed.

---

## 🔍 How Ollama Works

1. **Local Processing**: All classification happens on your computer (no cloud)
2. **Privacy**: Your data never leaves your machine
3. **Speed**: No network latency
4. **Cost**: Free (just GPU power)

---

## 📈 Pipeline Execution Timeline

With Ollama (CPU):

```
Phase 1: Scraping     ████████  8-10 min
Phase 2: Extraction   ██        2-3 min
Phase 3: Classification (Ollama) ███████████  30-60 min ⚠️
Phase 4: Trends       ███       2-3 min
Phase 5: Outliers     ██        2-3 min
Phase 6: Swipes       ██        1-2 min
Phase 7: Report       ██        1-2 min
Phase 8: Audit        █         30 sec
─────────────────────────────────────────
Total                           50-90 min
```

**Note**: Phase 3 (classification) is the main bottleneck with CPU. Use GPU for significant speedup.

---

## ✨ Features Available

With Ollama, you get:
- ✅ All 8 phases working
- ✅ TikTok & Instagram scraping
- ✅ Hook classification (heuristic fallback if model fails)
- ✅ Trend analysis
- ✅ Viral detection
- ✅ Beautiful HTML reports
- ✅ Zero cost (after initial setup)

---

## 🚀 Running Everything

### Full Pipeline Command
```bash
# Terminal 1 (keep running)
ollama serve

# Terminal 2
cd viral-hook-intelligence
python3 main.py
```

### Check Progress
```bash
tail -f logs/system.log
```

### View Results
After ~50-90 minutes:
```
✅ reports/viral-hook-report.html       # Open in browser!
✅ hooks/classified_hooks.json
✅ hooks/swipe_database.json
✅ hooks/trend_analysis.json
✅ hooks/outlier_analysis.json
```

---

## 🎓 Customization

### Use Different Model
Edit `phase3_classification.py` line 19:
```python
self.model = "neural-chat"  # Change this
```

Then run:
```bash
ollama pull neural-chat
```

### Change Ollama Port
If port 11434 is taken:
```bash
OLLAMA_HOST=0.0.0.0:9999 ollama serve
```

Then update `phase3_classification.py` line 16:
```python
def __init__(self, ollama_host: str = "http://localhost:9999"):
```

---

## 📝 Next Steps

1. ✅ Install Ollama
2. ✅ Download Mistral: `ollama pull mistral`
3. ✅ Start server: `ollama serve`
4. ✅ Run pipeline: `python3 main.py`
5. ✅ View report: `reports/viral-hook-report.html`

---

## 💡 Pro Tips

- **First Run**: Model loads ~2GB into RAM (takes 1-2 min)
- **Keep Ollama Running**: Don't stop it mid-classification
- **Monitor RAM**: Use `top` to see if you're swapping
- **Speed Up**: Use GPU or smaller model for faster results
- **Fallback**: If Ollama unavailable, system uses heuristic classification

---

**Status**: ✅ Ready to run with Ollama  
**Cost**: FREE (local operation)  
**Privacy**: 100% (no cloud)
