#!/usr/bin/env python3
"""
Quick database connection test
"""

import os
from dotenv import load_dotenv
from supabase import create_client

def test_connection():
    print("🔍 Testing Supabase Connection...")
    
    # Load environment variables
    load_dotenv()
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    
    if not url or not key:
        print("❌ Environment variables not found")
        return False
    
    print(f"URL: {url}")
    print(f"Key: {key[:20]}...")
    
    try:
        # Create client
        supabase = create_client(url, key)
        
        # Test basic connection
        response = supabase.table('categories').select('*').execute()
        
        print("✅ Connection successful!")
        print(f"📊 Found {len(response.data)} categories:")
        for cat in response.data:
            print(f"   - {cat['name']}: ${cat['rate']}/hour")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()
