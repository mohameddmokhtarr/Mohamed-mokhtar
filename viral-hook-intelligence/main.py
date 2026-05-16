"""
Viral Hook Intelligence System
Main orchestrator for all 8 phases
"""
import sys
import time
from datetime import datetime
from pathlib import Path

from logger import logger

# Import phase modules
from phase1_scraper import ContentScraper
from phase2_hook_extraction import HookExtractor
from phase3_classification import HookClassifier
from phase4_trend_analysis import TrendAnalyzer
from phase5_outlier_analysis import OutlierAnalyzer
from phase6_swipe_database import SwipeDatabase


def print_banner(title: str):
    """Print a formatted banner"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def run_phase(phase_num: int, phase_name: str, phase_func, skip_if_exists=None):
    """Run a single phase with error handling"""
    print_banner(f"PHASE {phase_num}: {phase_name}")

    # Check if output already exists (for recovery)
    if skip_if_exists and skip_if_exists.exists():
        file_size = skip_if_exists.stat().st_size
        if file_size > 0:
            logger.info(f"Phase {phase_num} output already exists ({file_size} bytes)")
            logger.info("Skipping phase (recovery mode)")
            return {'recovered': True}

    try:
        start_time = time.time()
        result = phase_func()
        duration = time.time() - start_time

        logger.info(f"Phase {phase_num} completed in {duration:.1f}s")
        return {'success': True, 'duration': duration, 'data': result}

    except Exception as e:
        logger.error(f"Phase {phase_num} failed: {str(e)}")
        return {'success': False, 'error': str(e)}


def main():
    """Run complete viral hook intelligence pipeline"""
    print_banner("VIRAL HOOK INTELLIGENCE SYSTEM")

    logger.info(f"Started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    results = {
        'start_time': datetime.now().isoformat(),
        'phases': {}
    }

    # Phase 1: Content Scraping
    logger.info("\n[1/8] Content Scraping...")
    scraper = ContentScraper()
    phase1_result = run_phase(
        1, "CONTENT SCRAPING",
        lambda: scraper.run(),
        skip_if_exists=Path('raw-data/.phase1_complete')
    )
    results['phases'][1] = phase1_result

    if not phase1_result.get('success', False) and not phase1_result.get('recovered', False):
        logger.error("Phase 1 failed. Cannot continue.")
        return results

    # Phase 2: Hook Extraction
    logger.info("\n[2/8] Hook Extraction...")
    extractor = HookExtractor()
    phase2_result = run_phase(
        2, "HOOK EXTRACTION",
        lambda: extractor.process_files(),
        skip_if_exists=Path('hooks/all_hooks.json')
    )
    results['phases'][2] = phase2_result

    if not phase2_result.get('success', False) and not phase2_result.get('recovered', False):
        logger.error("Phase 2 failed. Cannot continue.")
        return results

    # Phase 3: Hook Classification
    logger.info("\n[3/8] Hook Classification...")
    classifier = HookClassifier()
    phase3_result = run_phase(
        3, "HOOK CLASSIFICATION",
        lambda: classifier.process_hooks(),
        skip_if_exists=Path('hooks/classified_hooks.json')
    )
    results['phases'][3] = phase3_result

    if not phase3_result.get('success', False) and not phase3_result.get('recovered', False):
        logger.warning("Phase 3 failed. Continuing with available data...")

    # Phase 4: Trend Analysis
    logger.info("\n[4/8] Trend Analysis...")
    trend_analyzer = TrendAnalyzer()
    phase4_result = run_phase(
        4, "TREND ANALYSIS",
        lambda: (trend_analyzer.load_hooks(), trend_analyzer.analyze_trends())[1],
        skip_if_exists=Path('hooks/trend_analysis.json')
    )
    results['phases'][4] = phase4_result

    # Phase 5: Outlier Analysis
    logger.info("\n[5/8] Outlier Analysis...")
    outlier_analyzer = OutlierAnalyzer()
    phase5_result = run_phase(
        5, "OUTLIER ANALYSIS",
        lambda: (outlier_analyzer.load_hooks(), outlier_analyzer.find_outliers())[1],
        skip_if_exists=Path('hooks/outlier_analysis.json')
    )
    results['phases'][5] = phase5_result

    # Phase 6: Swipe Database
    logger.info("\n[6/8] Swipe Database...")
    swipe_db = SwipeDatabase()
    phase6_result = run_phase(
        6, "SWIPE DATABASE",
        lambda: (swipe_db.load_hooks(), swipe_db.build_database())[1],
        skip_if_exists=Path('hooks/swipe_database.json')
    )
    results['phases'][6] = phase6_result

    # Phase 7: Report Generation (import here to avoid circular imports)
    logger.info("\n[7/8] Report Generation...")
    try:
        from phase7_report import ReportGenerator
        reporter = ReportGenerator()
        phase7_result = run_phase(
            7, "REPORT GENERATION",
            lambda: reporter.generate_report(),
            skip_if_exists=Path('reports/viral-hook-report.html')
        )
        results['phases'][7] = phase7_result
    except Exception as e:
        logger.error(f"Phase 7 failed: {str(e)}")
        results['phases'][7] = {'success': False, 'error': str(e)}

    # Phase 8: Self-Audit
    logger.info("\n[8/8] System Audit...")
    try:
        from phase8_audit import SystemAudit
        auditor = SystemAudit()
        phase8_result = run_phase(
            8, "SYSTEM AUDIT",
            lambda: auditor.run_audit()
        )
        results['phases'][8] = phase8_result
    except Exception as e:
        logger.error(f"Phase 8 failed: {str(e)}")
        results['phases'][8] = {'success': False, 'error': str(e)}

    results['end_time'] = datetime.now().isoformat()

    # Print final summary
    print_banner("EXECUTION COMPLETE")
    logger.info(f"Completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    return results


if __name__ == '__main__':
    results = main()
