"""Phase 8: Self audit - verify all phases completed successfully."""

import json
from pathlib import Path
from logger import setup_logger
from config import (
    RAW_DATA_DIR, HOOKS_DIR, TRANSCRIPTS_DIR, REPORTS_DIR,
    MIN_DATASET_SIZE
)

logger = setup_logger('phase_8_audit')

def audit_raw_data():
    """Audit Phase 1 outputs."""
    logger.info("\n📋 Auditing Phase 1: Raw Data")

    raw_files = list(RAW_DATA_DIR.glob('*.json'))
    raw_files = [f for f in raw_files if not f.name.endswith('-raw.json')]

    if not raw_files:
        logger.warning("❌ No raw data files found")
        return False

    all_valid = True
    for raw_file in raw_files:
        try:
            with open(raw_file, 'r') as f:
                data = json.load(f)

            if not isinstance(data, list) or len(data) == 0:
                logger.warning(f"❌ Empty or invalid: {raw_file.name}")
                all_valid = False
            elif len(data) < MIN_DATASET_SIZE:
                logger.warning(f"⚠️  Insufficient data ({len(data)} < {MIN_DATASET_SIZE}): {raw_file.name}")
            else:
                logger.info(f"✅ {raw_file.name}: {len(data)} items")
        except Exception as e:
            logger.error(f"❌ Error reading {raw_file.name}: {e}")
            all_valid = False

    return all_valid

def audit_transcripts():
    """Audit Phase 2 outputs."""
    logger.info("\n📋 Auditing Phase 2: Transcripts")

    hooks_files = list(TRANSCRIPTS_DIR.glob('*-hooks.json'))

    if not hooks_files:
        logger.warning("❌ No hooks files found")
        return False

    all_valid = True
    for hooks_file in hooks_files:
        try:
            with open(hooks_file, 'r') as f:
                data = json.load(f)

            valid_count = sum(1 for item in data if item.get('hook_text'))
            invalid_count = len(data) - valid_count

            if len(data) == 0:
                logger.warning(f"❌ Empty: {hooks_file.name}")
                all_valid = False
            else:
                status = "✅" if valid_count >= len(data) * 0.8 else "⚠️"
                logger.info(f"{status} {hooks_file.name}: {valid_count}/{len(data)} hooks extracted")

        except Exception as e:
            logger.error(f"❌ Error reading {hooks_file.name}: {e}")
            all_valid = False

    return all_valid

def audit_classification():
    """Audit Phase 3 outputs."""
    logger.info("\n📋 Auditing Phase 3: Classification")

    classified_files = list(HOOKS_DIR.glob('*-classified.json'))

    if not classified_files:
        logger.warning("❌ No classified files found")
        return False

    all_valid = True
    type_distribution = {}

    for classified_file in classified_files:
        try:
            with open(classified_file, 'r') as f:
                data = json.load(f)

            if len(data) == 0:
                logger.warning(f"❌ Empty: {classified_file.name}")
                all_valid = False
            else:
                classified_count = sum(1 for item in data if item.get('primary_type') != 'unknown')
                accuracy = (classified_count / len(data)) * 100

                for item in data:
                    h_type = item.get('primary_type', 'unknown')
                    type_distribution[h_type] = type_distribution.get(h_type, 0) + 1

                status = "✅" if accuracy >= 70 else "⚠️"
                logger.info(f"{status} {classified_file.name}: {accuracy:.1f}% classified")

        except Exception as e:
            logger.error(f"❌ Error reading {classified_file.name}: {e}")
            all_valid = False

    if type_distribution:
        logger.info(f"   Type distribution: {type_distribution}")

    return all_valid

def audit_trends():
    """Audit Phase 4 outputs."""
    logger.info("\n📋 Auditing Phase 4: Trend Analysis")

    trend_file = HOOKS_DIR / 'trend-analysis.json'

    if not trend_file.exists():
        logger.warning("❌ Trend analysis file not found")
        return False

    try:
        with open(trend_file, 'r') as f:
            trends = json.load(f)

        emerging_count = len(trends.get('all_emerging', []))
        datasets_analyzed = len(trends.get('per_dataset', {}))

        logger.info(f"✅ Trend analysis: {datasets_analyzed} datasets, {emerging_count} emerging trends")
        return True

    except Exception as e:
        logger.error(f"❌ Error reading trend analysis: {e}")
        return False

def audit_performance():
    """Audit Phase 5 outputs."""
    logger.info("\n📋 Auditing Phase 5: Performance Analysis")

    perf_file = HOOKS_DIR / 'performance-analysis.json'

    if not perf_file.exists():
        logger.warning("❌ Performance analysis file not found")
        return False

    try:
        with open(perf_file, 'r') as f:
            perf = json.load(f)

        total_videos = sum(d.get('total_videos', 0) for d in perf.values())
        total_outliers = sum(d.get('outlier_count', 0) for d in perf.values())

        logger.info(f"✅ Performance analysis: {total_videos} videos, {total_outliers} outliers")
        return True

    except Exception as e:
        logger.error(f"❌ Error reading performance analysis: {e}")
        return False

def audit_swipe_db():
    """Audit Phase 6 outputs."""
    logger.info("\n📋 Auditing Phase 6: Swipe Database")

    swipe_file = HOOKS_DIR / 'swipe-database.json'

    if not swipe_file.exists():
        logger.warning("❌ Swipe database file not found")
        return False

    try:
        with open(swipe_file, 'r') as f:
            db = json.load(f)

        top_hooks = len(db.get('top_hooks', []))
        templates_count = len(db.get('templates_by_type', {}))

        logger.info(f"✅ Swipe database: {top_hooks} top hooks, {templates_count} template types")
        return True

    except Exception as e:
        logger.error(f"❌ Error reading swipe database: {e}")
        return False

def audit_report():
    """Audit Phase 7 outputs."""
    logger.info("\n📋 Auditing Phase 7: HTML Report")

    report_file = REPORTS_DIR / 'viral-hook-report.html'

    if not report_file.exists():
        logger.warning("❌ HTML report file not found")
        return False

    try:
        with open(report_file, 'r') as f:
            html = f.read()

        if len(html) > 1000 and '<html' in html.lower():
            logger.info(f"✅ HTML report: {len(html)} bytes")
            return True
        else:
            logger.warning("❌ HTML report appears corrupted or incomplete")
            return False

    except Exception as e:
        logger.error(f"❌ Error reading HTML report: {e}")
        return False

def audit_directory_structure():
    """Verify all required directories exist."""
    logger.info("\n📋 Auditing Directory Structure")

    dirs = {
        'raw-data': RAW_DATA_DIR,
        'hooks': HOOKS_DIR,
        'transcripts': TRANSCRIPTS_DIR,
        'reports': REPORTS_DIR,
    }

    all_ok = True
    for name, path in dirs.items():
        if path.exists() and path.is_dir():
            logger.info(f"✅ {name}/ exists")
        else:
            logger.error(f"❌ {name}/ missing")
            all_ok = False

    return all_ok

def run_phase_8():
    """Execute Phase 8: Self Audit."""
    logger.info("="*60)
    logger.info("PHASE 8: SELF AUDIT")
    logger.info("="*60)

    audits = [
        ("Directory Structure", audit_directory_structure()),
        ("Phase 1: Raw Data", audit_raw_data()),
        ("Phase 2: Transcripts", audit_transcripts()),
        ("Phase 3: Classification", audit_classification()),
        ("Phase 4: Trends", audit_trends()),
        ("Phase 5: Performance", audit_performance()),
        ("Phase 6: Swipe DB", audit_swipe_db()),
        ("Phase 7: HTML Report", audit_report()),
    ]

    logger.info("\n" + "="*60)
    logger.info("AUDIT SUMMARY")
    logger.info("="*60)

    for check_name, result in audits:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{check_name:.<40} {status}")

    all_passed = all(result for _, result in audits)

    logger.info("="*60)

    if all_passed:
        logger.info("\n✅ ALL AUDITS PASSED - System ready for production")
        return True
    else:
        logger.warning("\n⚠️  Some audits failed - Review issues above")
        return False
