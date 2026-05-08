#!/usr/bin/env python3
"""
Viral Hook Intelligence System - Main Orchestrator

Executes all 8 phases of viral hook analysis:
1. SCRAPE: Collect content from TikTok, Instagram, YouTube
2. TRANSCRIPT: Extract hooks from videos or captions
3. CLASSIFY: Categorize hooks by type and characteristics
4. TRENDS: Analyze viral trends across time buckets
5. PERFORMANCE: Identify outliers and performance patterns
6. SWIPE DB: Build reusable hook templates database
7. REPORT: Generate comprehensive HTML report
8. AUDIT: Verify all outputs and system integrity
"""

import sys
import time
from pathlib import Path
from logger import setup_logger, root_logger

# Import all phases
from phase_1_scraper import run_phase_1
from phase_2_transcription import run_phase_2
from phase_3_classification import run_phase_3
from phase_4_trends import run_phase_4
from phase_5_performance import run_phase_5
from phase_6_swipe_db import run_phase_6
from phase_7_html_report import run_phase_7
from phase_8_audit import run_phase_8

logger = setup_logger('main_orchestrator')

def print_banner():
    """Print system banner."""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║     🚀 VIRAL HOOK INTELLIGENCE SYSTEM v1.0 🚀              ║
    ║                                                              ║
    ║     Production-Grade Social Media Content Analysis           ║
    ║     8-Phase Pipeline for Viral Hook Discovery               ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def run_pipeline():
    """Run complete 8-phase pipeline."""
    start_time = time.time()
    print_banner()

    phases = [
        ("PHASE 1: SCRAPE CONTENT", run_phase_1),
        ("PHASE 2: EXTRACT TRANSCRIPTS", run_phase_2),
        ("PHASE 3: CLASSIFY HOOKS", run_phase_3),
        ("PHASE 4: ANALYZE TRENDS", run_phase_4),
        ("PHASE 5: PERFORMANCE ANALYSIS", run_phase_5),
        ("PHASE 6: BUILD SWIPE DATABASE", run_phase_6),
        ("PHASE 7: GENERATE REPORT", run_phase_7),
    ]

    results = {}
    failed_phases = []

    for phase_name, phase_func in phases:
        try:
            logger.info(f"\n{'='*60}")
            logger.info(f"🚀 Starting {phase_name}")
            logger.info(f"{'='*60}")

            result = phase_func()
            results[phase_name] = result
            logger.info(f"✅ {phase_name} completed successfully")

        except Exception as e:
            logger.error(f"❌ {phase_name} failed: {e}", exc_info=True)
            failed_phases.append((phase_name, str(e)))
            # Continue to next phase to collect as much data as possible

    # Run audit
    logger.info(f"\n{'='*60}")
    logger.info(f"🔍 Starting PHASE 8: SELF AUDIT")
    logger.info(f"{'='*60}")

    try:
        audit_passed = run_phase_8()
    except Exception as e:
        logger.error(f"Audit failed: {e}", exc_info=True)
        audit_passed = False

    # Print completion summary
    elapsed = time.time() - start_time
    print_completion_summary(results, failed_phases, audit_passed, elapsed)

    return len(failed_phases) == 0 and audit_passed

def print_completion_summary(results, failed_phases, audit_passed, elapsed):
    """Print completion summary."""
    logger.info("\n" + "="*60)
    logger.info("🎯 EXECUTION SUMMARY")
    logger.info("="*60)

    logger.info(f"Total execution time: {elapsed:.1f}s")
    logger.info(f"Phases completed: {len(results)}")
    logger.info(f"Failed phases: {len(failed_phases)}")
    logger.info(f"Audit status: {'✅ PASSED' if audit_passed else '❌ FAILED'}")

    if failed_phases:
        logger.warning("\nFailed phases:")
        for phase_name, error in failed_phases:
            logger.warning(f"  - {phase_name}: {error}")

    logger.info("\n" + "="*60)
    logger.info("📋 OUTPUT FILES")
    logger.info("="*60)

    from config import RAW_DATA_DIR, HOOKS_DIR, TRANSCRIPTS_DIR, REPORTS_DIR

    outputs = {
        "Raw Data": list(RAW_DATA_DIR.glob("*.json")),
        "Hooks": list(HOOKS_DIR.glob("*.json")),
        "Transcripts": list(TRANSCRIPTS_DIR.glob("*.json")),
        "Reports": list(REPORTS_DIR.glob("*.html")),
    }

    for category, files in outputs.items():
        if files:
            logger.info(f"\n{category}:")
            for f in files:
                logger.info(f"  - {f.name}")

    logger.info("\n" + "="*60)

    if len(failed_phases) == 0 and audit_passed:
        logger.info("✅ SYSTEM READY FOR PRODUCTION")
        logger.info("\nNext steps:")
        logger.info("1. Open reports/viral-hook-report.html in browser")
        logger.info("2. Review top hooks and emerging trends")
        logger.info("3. Use swipe-database.json for content creation")
        logger.info("4. Monitor hooks directory for ongoing analysis data")
    else:
        logger.warning("⚠️  System completed with errors - Review audit results")

    logger.info("="*60 + "\n")

if __name__ == '__main__':
    try:
        success = run_pipeline()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.warning("\n\n⚠️  System interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
