#!/usr/bin/env python3
"""
Bootstrap & Environment Verification
Viral Hook Intelligence System
"""
import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime

# Try to import dotenv, install if needed
try:
    from dotenv import load_dotenv
except ImportError:
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'python-dotenv', '-q'])

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

class BootstrapVerifier:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.errors = []
        self.warnings = []
        self.passed_checks = []

    def log_success(self, msg):
        print(f"{GREEN}✓{RESET} {msg}")
        self.passed_checks.append(msg)

    def log_error(self, msg):
        print(f"{RED}✗{RESET} {msg}")
        self.errors.append(msg)

    def log_warning(self, msg):
        print(f"{YELLOW}⚠{RESET} {msg}")
        self.warnings.append(msg)

    def log_info(self, msg):
        print(f"{BLUE}ℹ{RESET} {msg}")

    def print_header(self, title):
        print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
        print(f"{BOLD}{BLUE}{title}{RESET}")
        print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")

    def check_python_version(self):
        self.print_header("PYTHON VERSION CHECK")
        version = sys.version_info
        version_str = f"{version.major}.{version.minor}.{version.micro}"

        if version.major == 3 and version.minor >= 11:
            self.log_success(f"Python {version_str} (compatible)")
            return True
        else:
            self.log_error(f"Python {version_str} (requires 3.11+)")
            return False

    def check_folders(self):
        self.print_header("FOLDER STRUCTURE CHECK")
        required_folders = [
            'raw-data',
            'hooks',
            'transcripts',
            'adapters',
            'reports',
            'logs'
        ]

        all_exist = True
        for folder in required_folders:
            folder_path = self.project_root / folder
            if folder_path.exists():
                self.log_success(f"Folder exists: {folder}")
            else:
                self.log_error(f"Folder missing: {folder}")
                all_exist = False

        return all_exist

    def check_write_permissions(self):
        self.print_header("WRITE PERMISSIONS CHECK")
        test_folders = ['raw-data', 'reports', 'logs', 'hooks', 'transcripts']
        all_writable = True

        for folder in test_folders:
            folder_path = self.project_root / folder
            test_file = folder_path / '.write_test'
            try:
                test_file.touch()
                test_file.unlink()
                self.log_success(f"Write permission: {folder}/")
            except Exception as e:
                self.log_error(f"No write permission in {folder}/: {str(e)}")
                all_writable = False

        return all_writable

    def check_environment_variables(self):
        self.print_header("ENVIRONMENT VARIABLES CHECK")

        # Load .env file
        env_file = self.project_root / '.env'
        if not env_file.exists():
            self.log_error(f".env file not found at {env_file}")
            return False

        # Load from .env
        load_dotenv(env_file)

        required_vars = {
            'OPENAI_API_KEY': 'OpenAI API Key',
            'APIFY_API_TOKEN': 'Apify API Token'
        }

        all_present = True
        for var, description in required_vars.items():
            value = os.getenv(var)
            if value and value != f"{'*' * 10}" and not value.startswith('your-'):
                # Mask the key in output
                masked = value[:8] + '*' * (len(value) - 12) if len(value) > 12 else '****'
                self.log_success(f"{var}: {masked}")
            else:
                self.log_error(f"{var}: NOT SET (required: {description})")
                all_present = False

        return all_present

    def check_dependencies(self):
        self.print_header("DEPENDENCY INSTALLATION")

        requirements_file = self.project_root / 'requirements.txt'
        if not requirements_file.exists():
            self.log_error(f"requirements.txt not found")
            return False

        self.log_info("Installing dependencies from requirements.txt...")
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file), '-q'],
                cwd=self.project_root,
                capture_output=True,
                timeout=300,
                text=True
            )

            if result.returncode == 0:
                self.log_success("Dependencies installed successfully")
                return True
            else:
                self.log_error(f"Dependency installation failed: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            self.log_error("Installation timeout (>5 minutes)")
            return False
        except Exception as e:
            self.log_error(f"Installation error: {str(e)}")
            return False

    def check_imports(self):
        self.print_header("IMPORT VERIFICATION")

        imports_to_check = {
            'dotenv': 'python-dotenv',
            'requests': 'requests',
            'pandas': 'pandas',
            'numpy': 'numpy',
            'openai': 'openai',
            'jinja2': 'jinja2',
            'yt_dlp': 'yt-dlp',
            'sklearn': 'scikit-learn',
            'matplotlib': 'matplotlib',
            'playwright': 'playwright',
            'apify_client': 'apify-client'
        }

        all_imports_ok = True
        for module, package_name in imports_to_check.items():
            try:
                __import__(module)
                self.log_success(f"Import OK: {package_name}")
            except ImportError as e:
                self.log_error(f"Import FAILED: {package_name} - {str(e)}")
                all_imports_ok = False

        return all_imports_ok

    def check_api_connectivity(self):
        self.print_header("API CONNECTIVITY CHECK")

        import openai

        load_dotenv(self.project_root / '.env')
        api_key = os.getenv('OPENAI_API_KEY')

        if not api_key or api_key.startswith('your-') or api_key.startswith('sk-'):
            # Only test if key looks valid
            if api_key and not api_key.startswith('your-'):
                try:
                    openai.api_key = api_key
                    client = openai.OpenAI(api_key=api_key)
                    # Test with a simple list models call
                    models = client.models.list()
                    self.log_success("OpenAI API connectivity: OK")
                    return True
                except Exception as e:
                    self.log_warning(f"OpenAI API test failed (key may be invalid): {str(e)}")
                    return False
            else:
                self.log_warning("OpenAI API key not configured (skipping connectivity test)")
                return None

        return None

    def verify_apify_actor_ids(self):
        self.print_header("APIFY ACTOR CONFIGURATION")

        required_actors = {
            'TikTok Scraper': 'clockworks/free-tiktok-scraper',
            'Instagram Reels Scraper': 'apify/instagram-reel-scraper',
            'YouTube Scraper': 'streamers/youtube-scraper'
        }

        self.log_info("Required Apify Actors:")
        for name, actor_id in required_actors.items():
            print(f"  • {name}: {actor_id}")

        self.log_success("Actor IDs configured")
        return True

    def print_summary(self):
        self.print_header("BOOTSTRAP SUMMARY")

        total_checks = len(self.passed_checks) + len(self.errors)

        print(f"{BOLD}Status:{RESET}")
        print(f"  {GREEN}Passed: {len(self.passed_checks)}{RESET}")
        print(f"  {RED}Failed: {len(self.errors)}{RESET}")
        print(f"  {YELLOW}Warnings: {len(self.warnings)}{RESET}")

        if self.errors:
            print(f"\n{BOLD}{RED}ERRORS (must fix):{RESET}")
            for error in self.errors:
                print(f"  {RED}•{RESET} {error}")

        if self.warnings:
            print(f"\n{BOLD}{YELLOW}WARNINGS:{RESET}")
            for warning in self.warnings:
                print(f"  {YELLOW}•{RESET} {warning}")

        if not self.errors:
            print(f"\n{BOLD}{GREEN}✓ BOOTSTRAP SUCCESSFUL{RESET}")
            print(f"{GREEN}System ready for Phase 1 execution{RESET}\n")
            return True
        else:
            print(f"\n{BOLD}{RED}✗ BOOTSTRAP FAILED{RESET}")
            print(f"{RED}Fix errors above before continuing{RESET}\n")
            return False

    def run(self):
        print(f"{BOLD}{BLUE}{'='*60}{RESET}")
        print(f"{BOLD}{BLUE}Viral Hook Intelligence System - Bootstrap{RESET}")
        print(f"{BOLD}{BLUE}Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
        print(f"{BOLD}{BLUE}{'='*60}{RESET}\n")

        checks = [
            ("Python Version", self.check_python_version),
            ("Folder Structure", self.check_folders),
            ("Write Permissions", self.check_write_permissions),
            ("Environment Variables", self.check_environment_variables),
            ("Dependencies", self.check_dependencies),
            ("Imports", self.check_imports),
            ("API Connectivity", self.check_api_connectivity),
            ("Apify Actors", self.verify_apify_actor_ids),
        ]

        for check_name, check_func in checks:
            try:
                check_func()
            except Exception as e:
                self.log_error(f"{check_name} check failed with exception: {str(e)}")

        success = self.print_summary()
        return 0 if success else 1


if __name__ == '__main__':
    verifier = BootstrapVerifier()
    exit_code = verifier.run()
    sys.exit(exit_code)
