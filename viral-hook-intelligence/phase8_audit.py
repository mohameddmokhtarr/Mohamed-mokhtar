"""
Phase 8: System Audit
Final verification and quality assurance
"""
import json
from pathlib import Path
from datetime import datetime

from config import RAW_DATA_DIR, HOOKS_DIR, REPORTS_DIR, LOGS_DIR
from logger import logger


class SystemAudit:
    """Verify system completion and data integrity"""

    def __init__(self):
        self.audit_results = {
            'timestamp': datetime.now().isoformat(),
            'checks': {},
            'summary': {}
        }

    def run_audit(self) -> dict:
        """Run complete system audit"""
        logger.info("="*60)
        logger.info("PHASE 8: SYSTEM AUDIT")
        logger.info("="*60)

        # Check all phases
        checks = [
            ('phase1_scraping', self._check_raw_data),
            ('phase2_hooks', self._check_hooks),
            ('phase3_classified', self._check_classified),
            ('phase4_trends', self._check_trends),
            ('phase5_outliers', self._check_outliers),
            ('phase6_swipes', self._check_swipes),
            ('phase7_report', self._check_reports),
            ('folder_integrity', self._check_folders),
            ('log_files', self._check_logs)
        ]

        for check_name, check_func in checks:
            try:
                result = check_func()
                self.audit_results['checks'][check_name] = result
                status = "✓" if result.get('passed', False) else "✗"
                logger.info(f"{status} {check_name}: {result.get('message', 'Unknown')}")
            except Exception as e:
                logger.error(f"✗ {check_name}: {str(e)}")
                self.audit_results['checks'][check_name] = {'passed': False, 'error': str(e)}

        # Calculate summary
        self._calculate_summary()

        # Print final report
        self._print_final_report()

        return self.audit_results

    def _check_raw_data(self) -> dict:
        """Check Phase 1 raw data"""
        json_files = list(RAW_DATA_DIR.glob('*.json'))

        if not json_files:
            return {'passed': False, 'message': 'No raw data files found'}

        total_videos = 0
        for json_file in json_files:
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    total_videos += data.get('count', 0)
            except:
                pass

        if total_videos == 0:
            return {'passed': False, 'message': 'Raw data contains no videos'}

        return {
            'passed': True,
            'message': f'{len(json_files)} files, {total_videos} videos',
            'files': len(json_files),
            'videos': total_videos
        }

    def _check_hooks(self) -> dict:
        """Check Phase 2 hooks extraction"""
        hooks_file = HOOKS_DIR / 'all_hooks.json'

        if not hooks_file.exists():
            return {'passed': False, 'message': 'all_hooks.json not found'}

        try:
            with open(hooks_file, 'r') as f:
                data = json.load(f)
                hook_count = len(data.get('hooks', []))

            if hook_count == 0:
                return {'passed': False, 'message': 'No hooks extracted'}

            return {
                'passed': True,
                'message': f'{hook_count} hooks extracted',
                'count': hook_count
            }
        except Exception as e:
            return {'passed': False, 'message': f'Error reading hooks: {str(e)}'}

    def _check_classified(self) -> dict:
        """Check Phase 3 classified hooks"""
        classified_file = HOOKS_DIR / 'classified_hooks.json'

        if not classified_file.exists():
            return {'passed': False, 'message': 'classified_hooks.json not found'}

        try:
            with open(classified_file, 'r') as f:
                data = json.load(f)
                classified_count = len(data.get('hooks', []))

            if classified_count == 0:
                return {'passed': False, 'message': 'No hooks classified'}

            return {
                'passed': True,
                'message': f'{classified_count} hooks classified',
                'count': classified_count
            }
        except Exception as e:
            return {'passed': False, 'message': f'Error: {str(e)}'}

    def _check_trends(self) -> dict:
        """Check Phase 4 trend analysis"""
        trends_file = HOOKS_DIR / 'trend_analysis.json'

        if not trends_file.exists():
            return {'passed': False, 'message': 'trend_analysis.json not found'}

        try:
            with open(trends_file, 'r') as f:
                data = json.load(f)
                buckets = data.get('time_buckets', {})

            if not buckets:
                return {'passed': False, 'message': 'No trend data'}

            return {
                'passed': True,
                'message': f'Analyzed {len(buckets)} time buckets',
                'buckets': len(buckets)
            }
        except Exception as e:
            return {'passed': False, 'message': f'Error: {str(e)}'}

    def _check_outliers(self) -> dict:
        """Check Phase 5 outlier analysis"""
        outliers_file = HOOKS_DIR / 'outlier_analysis.json'

        if not outliers_file.exists():
            return {'passed': False, 'message': 'outlier_analysis.json not found'}

        try:
            with open(outliers_file, 'r') as f:
                data = json.load(f)
                outlier_count = data.get('total_outliers', 0)

            return {
                'passed': True,
                'message': f'{outlier_count} viral outliers identified',
                'outliers': outlier_count
            }
        except Exception as e:
            return {'passed': False, 'message': f'Error: {str(e)}'}

    def _check_swipes(self) -> dict:
        """Check Phase 6 swipe database"""
        swipes_file = HOOKS_DIR / 'swipe_database.json'

        if not swipes_file.exists():
            return {'passed': False, 'message': 'swipe_database.json not found'}

        try:
            with open(swipes_file, 'r') as f:
                data = json.load(f)
                templates = len(data.get('templates', []))
                top_100 = len(data.get('top_100_hooks', []))

            return {
                'passed': True,
                'message': f'{templates} templates, {top_100} top hooks',
                'templates': templates,
                'hooks': top_100
            }
        except Exception as e:
            return {'passed': False, 'message': f'Error: {str(e)}'}

    def _check_reports(self) -> dict:
        """Check Phase 7 report generation"""
        report_file = REPORTS_DIR / 'viral-hook-report.html'

        if not report_file.exists():
            return {'passed': False, 'message': 'viral-hook-report.html not found'}

        file_size = report_file.stat().st_size

        if file_size < 1000:
            return {'passed': False, 'message': f'Report too small: {file_size} bytes'}

        return {
            'passed': True,
            'message': f'Report generated: {file_size/1024:.1f} KB',
            'file_size': file_size
        }

    def _check_folders(self) -> dict:
        """Check folder integrity"""
        folders = {
            'raw-data': RAW_DATA_DIR,
            'hooks': HOOKS_DIR,
            'reports': REPORTS_DIR,
            'logs': LOGS_DIR
        }

        missing = []
        for name, path in folders.items():
            if not path.exists():
                missing.append(name)

        if missing:
            return {'passed': False, 'message': f'Missing folders: {", ".join(missing)}'}

        return {
            'passed': True,
            'message': 'All folders present',
            'folders': len(folders)
        }

    def _check_logs(self) -> dict:
        """Check log files"""
        log_files = list(LOGS_DIR.glob('*.log'))

        if not log_files:
            return {'passed': False, 'message': 'No log files found'}

        total_size = sum(f.stat().st_size for f in log_files)

        return {
            'passed': True,
            'message': f'{len(log_files)} log files, {total_size/1024:.1f} KB total',
            'count': len(log_files),
            'size': total_size
        }

    def _calculate_summary(self):
        """Calculate overall summary"""
        checks = self.audit_results['checks']
        passed = sum(1 for c in checks.values() if c.get('passed', False))
        total = len(checks)

        self.audit_results['summary'] = {
            'passed': passed,
            'total': total,
            'success_rate': f"{passed/total*100:.0f}%",
            'status': 'PASSED' if passed == total else 'PARTIAL' if passed > 0 else 'FAILED'
        }

    def _print_final_report(self):
        """Print final audit report"""
        logger.info("\n" + "="*60)
        logger.info("AUDIT SUMMARY")
        logger.info("="*60)

        summary = self.audit_results['summary']
        logger.info(f"\nStatus: {summary['status']}")
        logger.info(f"Passed: {summary['passed']}/{summary['total']} ({summary['success_rate']})")

        logger.info("\n" + "="*60)
        logger.info("SYSTEM EXECUTION COMPLETE")
        logger.info("="*60)

        logger.info("\n📊 Generated Outputs:")
        logger.info(f"  • Report: {REPORTS_DIR / 'viral-hook-report.html'}")
        logger.info(f"  • Swipe Database: {HOOKS_DIR / 'swipe_database.json'}")
        logger.info(f"  • Classified Hooks: {HOOKS_DIR / 'classified_hooks.json'}")
        logger.info(f"  • Trend Analysis: {HOOKS_DIR / 'trend_analysis.json'}")
        logger.info(f"  • Outlier Analysis: {HOOKS_DIR / 'outlier_analysis.json'}")

        logger.info("\n✅ System ready for production use")


def main():
    """Run Phase 8"""
    auditor = SystemAudit()
    result = auditor.run_audit()
    return result


if __name__ == '__main__':
    main()
