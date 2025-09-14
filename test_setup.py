#!/usr/bin/env python3
"""
Test script to verify the productivity tracker setup.
Run this after setting up your environment to check if everything is working.
"""

import os
import sys
from dotenv import load_dotenv
from supabase import create_client

def test_environment():
    """Test if environment variables are set correctly"""
    print("🔍 Testing environment variables...")
    
    load_dotenv()
    
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url:
        print("❌ SUPABASE_URL not found in environment")
        return False
    
    if not key:
        print("❌ SUPABASE_KEY not found in environment")
        return False
    
    if "your_supabase_url_here" in url or "your_supabase_anon_key_here" in key:
        print("❌ Please update your .env file with actual Supabase credentials")
        return False
    
    print("✅ Environment variables are set correctly")
    return True

def test_supabase_connection():
    """Test connection to Supabase"""
    print("🔍 Testing Supabase connection...")
    
    try:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
        supabase = create_client(url, key)
        
        # Test basic connection by fetching categories
        response = supabase.table("categories").select("*").execute()
        
        if response.data:
            print(f"✅ Connected to Supabase successfully")
            print(f"   Found {len(response.data)} categories")
            return True
        else:
            print("❌ No categories found. Please run the database schema setup.")
            return False
            
    except Exception as e:
        print(f"❌ Supabase connection failed: {str(e)}")
        return False

def test_database_schema():
    """Test if database schema is set up correctly"""
    print("🔍 Testing database schema...")
    
    try:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
        supabase = create_client(url, key)
        
        # Test categories table
        categories_response = supabase.table("categories").select("*").execute()
        if not categories_response.data:
            print("❌ Categories table is empty or doesn't exist")
            return False
        
        # Test logs table structure (should not error)
        logs_response = supabase.table("logs").select("*").limit(1).execute()
        print("✅ Database schema is set up correctly")
        return True
        
    except Exception as e:
        print(f"❌ Database schema test failed: {str(e)}")
        return False

def test_dependencies():
    """Test if all required packages are installed"""
    print("🔍 Testing dependencies...")
    
    required_packages = [
        'streamlit',
        'supabase',
        'pandas',
        'plotly',
        'python-dotenv',
        'click'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed")
    return True

def main():
    """Run all tests"""
    print("🚀 Productivity Tracker Setup Test")
    print("=" * 40)
    
    tests = [
        test_dependencies,
        test_environment,
        test_supabase_connection,
        test_database_schema
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test failed with error: {str(e)}")
            print()
    
    print("=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Run: streamlit run app.py")
        print("2. Open your browser to the provided URL")
        print("3. Create an account and start tracking!")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
