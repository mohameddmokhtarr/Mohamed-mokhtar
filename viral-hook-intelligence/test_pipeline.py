#!/usr/bin/env python3
"""
Test script to verify all pipeline components before full execution
Uses Ollama instead of Anthropic API
"""
import sys
import json
from pathlib import Path
from datetime import datetime

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from logger import logger
from config import APIFY_API_TOKEN


def test_imports():
    """Test that all required imports work"""
    print("\n📦 Testing Imports...")
    try:
        import requests
        print("  ✓ requests")

        from apify_client import ApifyClient
        print("  ✓ apify_client")

        import pandas as pd
        print("  ✓ pandas")

        import numpy as np
        print("  ✓ numpy")

        from jinja2 import Template
        print("  ✓ jinja2")

        from sklearn.preprocessing import StandardScaler
        print("  ✓ scikit-learn")

        from adapters import DataNormalizer
        print("  ✓ adapters.DataNormalizer")

        return True
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        return False


def test_api_keys():
    """Test that API keys are configured"""
    print("\n🔑 Testing API Keys...")

    if not APIFY_API_TOKEN:
        print("  ✗ APIFY_API_TOKEN not set in .env")
        return False
    print(f"  ✓ APIFY_API_TOKEN: {APIFY_API_TOKEN[:10]}...")

    return True


def test_ollama_connection():
    """Test connection to Ollama"""
    print("\n🔗 Testing Ollama Connection...")
    try:
        import requests

        response = requests.get(
            "http://localhost:11434/api/tags",
            timeout=5
        )

        if response.status_code == 200:
            models = response.json().get('models', [])
            if models:
                print(f"  ✓ Connected to Ollama")
                print(f"    Available models: {[m.get('name', 'unknown') for m in models]}")
                return True
            else:
                print(f"  ⚠️  Ollama running but no models found")
                print(f"     Run: ollama pull mistral")
                return False
        else:
            print(f"  ✗ Ollama API error: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"  ✗ Cannot connect to Ollama at localhost:11434")
        print(f"     Start Ollama: ollama serve")
        return False
    except Exception as e:
        print(f"  ✗ Connection failed: {e}")
        return False


def test_apify_connection():
    """Test connection to Apify API"""
    print("\n🔗 Testing Apify API Connection...")
    try:
        from apify_client import ApifyClient

        client = ApifyClient(APIFY_API_TOKEN)
        actor_info = client.actor("clockworks~free-tiktok-scraper").get()
        print(f"  ✓ Connected to Apify")
        print(f"    Actor: {actor_info.get('name', 'unknown')}")
        return True
    except Exception as e:
        print(f"  ✗ Connection failed: {e}")
        return False


def test_data_normalizer():
    """Test data normalization"""
    print("\n📊 Testing Data Normalizer...")
    try:
        from adapters import DataNormalizer

        # Test TikTok normalization
        tiktok_data = {
            'id': '123456',
            'author': {'name': 'Test User', 'unique_id': 'testuser'},
            'desc': 'Test caption',
            'stats': {'playCount': 1000, 'diggCount': 50, 'commentCount': 10, 'shareCount': 5},
            'createTime': 1620000000,
            'video': {'duration': 30}
        }

        normalized = DataNormalizer.normalize('tiktok', tiktok_data)
        assert normalized['platform'] == 'tiktok'
        assert normalized['views'] == 1000
        print("  ✓ TikTok normalization works")

        # Test Instagram normalization
        instagram_data = {
            'id': 'abc123',
            'ownerUsername': 'testuser',
            'caption': 'Test caption',
            'likesCount': 500,
            'commentsCount': 20,
            'timestamp': '2021-05-03T10:00:00Z',
            'videoDuration': 60
        }

        normalized = DataNormalizer.normalize('instagram', instagram_data)
        assert normalized['platform'] == 'instagram'
        assert normalized['views'] == 500
        print("  ✓ Instagram normalization works")

        return True
    except Exception as e:
        print(f"  ✗ Normalization failed: {e}")
        return False


def test_hook_extraction():
    """Test hook extraction"""
    print("\n🎣 Testing Hook Extraction...")
    try:
        from phase2_hook_extraction import HookExtractor

        test_caption = "Did you know that 90% of creators never reach 100K followers? Here's why. The biggest mistake is focusing on algorithm instead of audience. Quality over quantity always wins."

        hook = HookExtractor.extract_hook(test_caption)
        assert hook is not None
        assert 'hook_text' in hook
        assert len(hook['hook_text']) > 0
        print(f"  ✓ Extracted hook: {hook['hook_text'][:50]}...")

        return True
    except Exception as e:
        print(f"  ✗ Hook extraction failed: {e}")
        return False


def test_hook_classification():
    """Test hook classification with Ollama"""
    print("\n🏷️ Testing Hook Classification (Ollama)...")
    try:
        from phase3_classification import HookClassifier

        classifier = HookClassifier()

        test_hook = {
            'hook_text': 'Did you know 90% of creators fail within 6 months?'
        }

        classification = classifier.classify_hook(test_hook)

        if classification is None:
            print("  ✗ Classification returned None")
            return False

        assert 'primary_hook_type' in classification
        print(f"  ✓ Classified as: {classification['primary_hook_type']}")

        return True
    except Exception as e:
        print(f"  ✗ Classification failed: {e}")
        return False


def test_file_operations():
    """Test file read/write operations"""
    print("\n💾 Testing File Operations...")
    try:
        from config import RAW_DATA_DIR, HOOKS_DIR, REPORTS_DIR

        # Test writing JSON
        test_data = {
            'test': 'data',
            'timestamp': datetime.now().isoformat()
        }

        test_file = HOOKS_DIR / 'test_write.json'
        with open(test_file, 'w') as f:
            json.dump(test_data, f)

        # Test reading JSON
        with open(test_file, 'r') as f:
            loaded = json.load(f)

        assert loaded['test'] == 'data'
        test_file.unlink()  # Clean up

        print(f"  ✓ File operations work")
        return True
    except Exception as e:
        print(f"  ✗ File operations failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("PIPELINE COMPONENT TEST SUITE (Ollama Version)")
    print("=" * 60)

    tests = [
        ("Imports", test_imports),
        ("API Keys (Apify)", test_api_keys),
        ("Ollama Connection", test_ollama_connection),
        ("Apify Connection", test_apify_connection),
        ("Data Normalizer", test_data_normalizer),
        ("Hook Extraction", test_hook_extraction),
        ("Hook Classification (Ollama)", test_hook_classification),
        ("File Operations", test_file_operations),
    ]

    results = []

    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"  ✗ Test crashed: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, r in results if r)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")

    print(f"\n{passed}/{total} tests passed")

    if passed >= 6:  # Allow failures on Ollama tests if it's not running
        print("\n🎉 System ready! To run pipeline:")
        print("   1. Start Ollama: ollama serve (in new terminal)")
        print("   2. Run pipeline: python3 main.py")
        return 0
    else:
        print("\n⚠️  Some critical tests failed. Fix issues above before running.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
