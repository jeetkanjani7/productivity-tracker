#!/usr/bin/env python3
"""
Setup script for Productivity Tracker
This will help you configure your Supabase credentials
"""

import os

def setup_environment():
    print("🚀 Productivity Tracker Setup")
    print("=" * 40)
    
    print("\n📋 Step 1: Get your Supabase credentials")
    print("1. Go to your Supabase project dashboard")
    print("2. Navigate to Settings → API")
    print("3. Copy your Project URL and anon public key")
    
    print("\n🔑 Step 2: Enter your credentials")
    
    url = input("\nEnter your Supabase Project URL: ").strip()
    key = input("Enter your Supabase anon public key: ").strip()
    
    if not url or not key:
        print("❌ Please provide both URL and key")
        return False
    
    # Create .env file
    env_content = f"""# Environment variables for Supabase
SUPABASE_URL={url}
SUPABASE_KEY={key}
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("\n✅ Environment file created successfully!")
        print("📁 Created: .env")
        
        # Test connection
        print("\n🔍 Testing connection...")
        test_connection(url, key)
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating .env file: {str(e)}")
        return False

def test_connection(url, key):
    try:
        from supabase import create_client
        
        supabase = create_client(url, key)
        
        # Test basic connection
        response = supabase.table("categories").select("*").execute()
        
        if response.data:
            print("✅ Connection successful!")
            print(f"   Found {len(response.data)} categories")
            print("\n🎉 Setup complete! You can now run:")
            print("   streamlit run app.py")
        else:
            print("⚠️  Connection successful but no categories found.")
            print("   Make sure you ran the SQL schema setup.")
            
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        print("   Please check your credentials and try again.")

if __name__ == "__main__":
    setup_environment()
