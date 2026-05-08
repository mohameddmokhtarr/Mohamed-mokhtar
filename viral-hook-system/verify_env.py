#!/usr/bin/env python3
"""Verify the Viral Hook Intelligence System environment."""

import sys
import os
from pathlib import Path

def check_python_version():
    """Verify Python 3.11+."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print(f"❌ Python 3.11+ required, found {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor} OK")
    return True

def check_imports():
    """Verify all required packages are installed."""
    packages = [
        'requests',
        'pandas',
        'numpy',
        'openai',
        'jinja2',
        'yt_dlp',
        'sklearn',
        'matplotlib',
        'playwright',
        'dotenv'
    ]

    all_ok = True
    for pkg in packages:
        try:
            __import__(pkg)
            print(f"✅ {pkg} installed")
        except ImportError:
            print(f"❌ {pkg} NOT installed")
            all_ok = False
    return all_ok

def check_folders():
    """Verify folder structure exists."""
    required_dirs = [
        'raw-data',
        'hooks',
        'transcripts',
        'adapters',
        'reports'
    ]

    base = Path(__file__).parent
    all_ok = True
    for dir_name in required_dirs:
        dir_path = base / dir_name
        if dir_path.exists() and dir_path.is_dir():
            print(f"✅ {dir_name}/ exists")
        else:
            print(f"❌ {dir_name}/ NOT found")
            all_ok = False
    return all_ok

def check_env_file():
    """Verify .env file exists."""
    env_path = Path(__file__).parent / '.env'
    if env_path.exists():
        print(f"✅ .env file exists")
        return True
    else:
        print(f"❌ .env file NOT found")
        return False

def load_env():
    """Load environment variables."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ .env loaded via python-dotenv")
        return True
    except Exception as e:
        print(f"❌ Failed to load .env: {e}")
        return False

if __name__ == '__main__':
    print("\n🔍 Verifying Viral Hook Intelligence System Environment\n")

    results = [
        ("Python Version", check_python_version()),
        ("Required Packages", check_imports()),
        ("Folder Structure", check_folders()),
        ("Environment File", check_env_file()),
        ("Environment Loading", load_env()),
    ]

    print("\n" + "="*50)
    print("VERIFICATION SUMMARY")
    print("="*50)
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name:.<40} {status}")

    all_passed = all(result for _, result in results)
    print("="*50)

    if all_passed:
        print("\n✅ Environment is ready for Phase 1!")
        sys.exit(0)
    else:
        print("\n❌ Environment verification failed. Fix issues above.")
        sys.exit(1)
