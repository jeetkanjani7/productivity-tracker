#!/usr/bin/env python3
"""
Test script to verify the infinite instances fix
"""

import subprocess
import time
import os
import sys

def test_app_launch():
    """Test that the app launches correctly without infinite instances"""
    print("🧪 Testing Productivity Tracker Launch Fix")
    print("=" * 40)
    
    # First, clean up any existing processes
    print("1. Cleaning up existing processes...")
    try:
        result = subprocess.run([sys.executable, "cleanup_processes.py"], 
                              capture_output=True, text=True, timeout=30)
        print("✅ Cleanup completed")
        if result.stdout:
            print(result.stdout)
    except subprocess.TimeoutExpired:
        print("⚠️ Cleanup timed out")
    except Exception as e:
        print(f"⚠️ Cleanup error: {e}")
    
    # Wait for cleanup to complete
    time.sleep(3)
    
    print("\n2. Testing singleton pattern...")
    
    # Try to launch the app
    try:
        print("🚀 Launching app...")
        process = subprocess.Popen([sys.executable, "desktop_app.py"], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 text=True)
        
        # Wait a moment for the app to start
        time.sleep(5)
        
        # Check if the process is still running
        if process.poll() is None:
            print("✅ App launched successfully")
            
            # Try to launch a second instance (should be prevented)
            print("\n3. Testing second instance prevention...")
            try:
                second_process = subprocess.Popen([sys.executable, "desktop_app.py"], 
                                                stdout=subprocess.PIPE, 
                                                stderr=subprocess.PIPE,
                                                text=True)
                
                # Wait a moment
                time.sleep(3)
                
                # Check if second process exited (should happen due to singleton)
                if second_process.poll() is not None:
                    stdout, stderr = second_process.communicate()
                    if "Another instance" in stdout or "app lock" in stdout:
                        print("✅ Second instance correctly prevented!")
                    else:
                        print("⚠️ Second instance exited but reason unclear")
                        print(f"Output: {stdout}")
                        print(f"Error: {stderr}")
                else:
                    print("❌ Second instance was not prevented!")
                    second_process.terminate()
                    
            except Exception as e:
                print(f"⚠️ Error testing second instance: {e}")
            
            # Clean up the first process
            print("\n4. Cleaning up...")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            
        else:
            stdout, stderr = process.communicate()
            print("❌ App failed to launch")
            print(f"Output: {stdout}")
            print(f"Error: {stderr}")
            
    except Exception as e:
        print(f"❌ Error launching app: {e}")
    
    # Final cleanup
    print("\n5. Final cleanup...")
    try:
        result = subprocess.run([sys.executable, "cleanup_processes.py"], 
                              capture_output=True, text=True, timeout=30)
        print("✅ Final cleanup completed")
    except Exception as e:
        print(f"⚠️ Final cleanup error: {e}")
    
    print("\n🎉 Test completed!")
    print("💡 If you see 'Second instance correctly prevented!' above, the fix is working!")

if __name__ == "__main__":
    test_app_launch()
