#!/usr/bin/env python3
"""
Test authentication functionality
"""

import os
from dotenv import load_dotenv
from supabase import create_client

def test_auth():
    print("🔍 Testing Authentication...")
    
    load_dotenv()
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    
    if not url or not key:
        print("❌ Environment variables not found")
        return False
    
    try:
        supabase = create_client(url, key)
        
        # Test sign up
        test_email = "test@example.com"
        test_password = "testpassword123"
        
        print("📝 Testing sign up...")
        try:
            signup_response = supabase.auth.sign_up({
                "email": test_email,
                "password": test_password
            })
            if signup_response and signup_response.user:
                print("✅ Sign up successful")
            else:
                print("ℹ️  User might already exist")
        except Exception as e:
            if "already registered" in str(e).lower():
                print("ℹ️  User already exists (this is expected)")
            else:
                print(f"❌ Sign up error: {e}")
        
        # Test sign in
        print("🔑 Testing sign in...")
        try:
            signin_response = supabase.auth.sign_in_with_password({
                "email": test_email,
                "password": test_password
            })
            if signin_response and signin_response.user:
                print("✅ Sign in successful")
                print(f"   User ID: {signin_response.user.id}")
                print(f"   Email: {signin_response.user.email}")
                
                # Test session
                session = supabase.auth.get_session()
                if session and session.user:
                    print("✅ Session valid")
                else:
                    print("❌ Session invalid")
                    
                return True
            else:
                print("❌ Sign in failed")
                return False
        except Exception as e:
            print(f"❌ Sign in error: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    test_auth()
