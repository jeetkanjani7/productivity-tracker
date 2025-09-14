#!/usr/bin/env python3
"""
Debug authentication issues
"""

import os
from dotenv import load_dotenv
from supabase import create_client

def debug_auth():
    print("🔍 Debugging Authentication Issues...")
    print("=" * 50)
    
    # Load environment
    load_dotenv()
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    
    print(f"✅ Environment loaded")
    print(f"   URL: {url}")
    print(f"   Key: {key[:20]}...")
    
    try:
        supabase = create_client(url, key)
        print("✅ Supabase client created")
        
        # Test with a simple email
        test_email = "test@test.com"
        test_password = "password123"
        
        print(f"\n📝 Testing with email: {test_email}")
        
        # Try sign up
        print("1. Testing sign up...")
        try:
            signup_response = supabase.auth.sign_up({
                "email": test_email,
                "password": test_password
            })
            print(f"   Sign up response: {signup_response}")
            if signup_response and signup_response.user:
                print(f"   ✅ User created: {signup_response.user.id}")
            else:
                print("   ❌ No user in response")
        except Exception as e:
            print(f"   ❌ Sign up error: {e}")
        
        # Try sign in
        print("2. Testing sign in...")
        try:
            signin_response = supabase.auth.sign_in_with_password({
                "email": test_email,
                "password": test_password
            })
            print(f"   Sign in response: {signin_response}")
            if signin_response and signin_response.user:
                print(f"   ✅ User signed in: {signin_response.user.id}")
                
                # Test session
                print("3. Testing session...")
                session = supabase.auth.get_session()
                print(f"   Session: {session}")
                if session and session.user:
                    print(f"   ✅ Session valid: {session.user.id}")
                else:
                    print("   ❌ No valid session")
                    
            else:
                print("   ❌ No user in sign in response")
        except Exception as e:
            print(f"   ❌ Sign in error: {e}")
            
    except Exception as e:
        print(f"❌ Client creation error: {e}")

if __name__ == "__main__":
    debug_auth()
