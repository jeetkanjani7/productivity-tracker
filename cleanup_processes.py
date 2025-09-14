#!/usr/bin/env python3
"""
Process Cleanup Script for Productivity Tracker
Kills any orphaned Streamlit processes that might be causing issues
"""

import psutil
import sys

def cleanup_streamlit_processes():
    """Clean up any running Streamlit processes"""
    print("🧹 Cleaning up Streamlit processes...")
    
    killed_count = 0
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] and 'streamlit' in proc.info['name'].lower():
                cmdline = ' '.join(proc.info['cmdline'] or [])
                if '8501' in cmdline or 'app.py' in cmdline or 'productivity' in cmdline.lower():
                    print(f"🧹 Killing Streamlit process: {proc.info['pid']} - {cmdline}")
                    try:
                        proc.terminate()
                        proc.wait(timeout=3)
                    except psutil.TimeoutExpired:
                        proc.kill()
                    killed_count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    if killed_count > 0:
        print(f"✅ Cleaned up {killed_count} Streamlit processes")
        # Wait for processes to fully terminate
        import time
        time.sleep(1)
    else:
        print("✅ No Streamlit processes found to clean up")
    
    return killed_count

def cleanup_webview_processes():
    """Clean up any running webview processes"""
    print("🧹 Cleaning up webview processes...")
    
    killed_count = 0
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] and ('webview' in proc.info['name'].lower() or 'python' in proc.info['name'].lower()):
                cmdline = ' '.join(proc.info['cmdline'] or [])
                if 'webview' in cmdline.lower() or 'desktop_app.py' in cmdline or 'productivity' in cmdline.lower():
                    print(f"🧹 Killing webview process: {proc.info['pid']} - {cmdline}")
                    try:
                        proc.terminate()
                        proc.wait(timeout=3)
                    except psutil.TimeoutExpired:
                        proc.kill()
                    killed_count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    if killed_count > 0:
        print(f"✅ Cleaned up {killed_count} webview processes")
        # Wait for processes to fully terminate
        import time
        time.sleep(1)
    else:
        print("✅ No webview processes found to clean up")
    
    return killed_count

def cleanup_lock_files():
    """Clean up any stale lock files"""
    print("🧹 Cleaning up lock files...")
    
    import os
    import tempfile
    
    lock_file = os.path.join(tempfile.gettempdir(), 'productivity_tracker.lock')
    
    if os.path.exists(lock_file):
        try:
            os.unlink(lock_file)
            print("✅ Removed stale lock file")
            return 1
        except OSError:
            print("⚠️ Could not remove lock file")
            return 0
    else:
        print("✅ No lock files found")
        return 0

def main():
    print("🍑 Productivity Tracker Process Cleanup")
    print("=" * 40)
    
    # Clean up Streamlit processes
    streamlit_count = cleanup_streamlit_processes()
    
    # Clean up webview processes
    webview_count = cleanup_webview_processes()
    
    # Clean up lock files
    lock_count = cleanup_lock_files()
    
    total_cleaned = streamlit_count + webview_count + lock_count
    
    if total_cleaned > 0:
        print(f"\n🎉 Successfully cleaned up {total_cleaned} items!")
        print("✅ You can now safely launch the app again")
    else:
        print("\n✅ No processes or files needed cleaning")
        print("✅ System is clean and ready")
    
    print("\n💡 To prevent future issues:")
    print("   - Always close the app properly (Cmd+Q)")
    print("   - Don't force-quit the app unless necessary")
    print("   - Run this cleanup script if you experience issues")
    print("   - Use the safe launcher: ./safe_launcher.sh")

if __name__ == "__main__":
    main()

