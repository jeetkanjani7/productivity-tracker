#!/usr/bin/env python3
"""
Test the fixed app functionality
"""

import requests
import time

def test_app():
    print("🔍 Testing App Functionality...")
    print("=" * 40)
    
    # Wait for app to start
    print("⏳ Waiting for app to start...")
    time.sleep(3)
    
    try:
        # Test main app
        response = requests.get("http://localhost:8501", timeout=10)
        if response.status_code == 200:
            print("✅ Main app is running at http://localhost:8501")
        else:
            print(f"❌ Main app returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Main app error: {e}")
    
    try:
        # Test demo app
        response = requests.get("http://localhost:8502", timeout=10)
        if response.status_code == 200:
            print("✅ Demo app is running at http://localhost:8502")
        else:
            print(f"❌ Demo app returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Demo app error: {e}")
    
    print("\n🎯 What to test:")
    print("1. Main app (http://localhost:8501):")
    print("   - Sign up with real email")
    print("   - Check if activity logging form appears")
    print("   - Try logging an activity")
    print("   - Refresh page - should stay logged in")
    print("\n2. Demo app (http://localhost:8502):")
    print("   - No authentication required")
    print("   - All features work with sample data")
    print("   - Activity logging form should be visible")

if __name__ == "__main__":
    test_app()
