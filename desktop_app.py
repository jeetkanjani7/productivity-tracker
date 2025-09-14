#!/usr/bin/env python3
"""
Productivity Tracker Desktop App - SAFE VERSION
Run this script to launch the desktop app with proper process management
"""

import webview
import sys
import os
import subprocess
import signal
import atexit
import psutil
import socket
import time
import threading
import fcntl
import tempfile

# Global variable to track the Streamlit process
streamlit_process = None
app_lock = None

def cleanup_processes():
    """Clean up any running Streamlit processes"""
    global streamlit_process, app_lock
    
    try:
        # Kill our tracked process
        if streamlit_process and streamlit_process.poll() is None:
            print("🧹 Cleaning up Streamlit process...")
            streamlit_process.terminate()
            try:
                streamlit_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("⚠️ Force killing Streamlit process...")
                streamlit_process.kill()
        
        # Also kill any other Streamlit processes on port 8501
        killed_count = 0
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] and 'streamlit' in proc.info['name'].lower():
                    cmdline = ' '.join(proc.info['cmdline'] or [])
                    if '8501' in cmdline or 'app.py' in cmdline:
                        print(f"🧹 Killing orphaned Streamlit process: {proc.info['pid']}")
                        proc.kill()
                        killed_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        if killed_count > 0:
            print(f"✅ Cleaned up {killed_count} Streamlit processes")
            # Wait a bit for processes to fully terminate
            time.sleep(1)
                
    except Exception as e:
        print(f"⚠️ Error during cleanup: {e}")
    finally:
        # Release the lock file
        if app_lock:
            try:
                app_lock.close()
                os.unlink(app_lock.name)
            except:
                pass

def is_port_in_use(port):
    """Check if a port is already in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def acquire_app_lock():
    """Acquire a lock to prevent multiple app instances"""
    global app_lock
    
    lock_file = os.path.join(tempfile.gettempdir(), 'productivity_tracker.lock')
    
    try:
        app_lock = open(lock_file, 'w')
        fcntl.flock(app_lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        app_lock.write(str(os.getpid()))
        app_lock.flush()
        return True
    except (IOError, OSError):
        # Lock is already held by another process
        return False

def check_existing_instance():
    """Check if another instance is already running"""
    lock_file = os.path.join(tempfile.gettempdir(), 'productivity_tracker.lock')
    
    if not os.path.exists(lock_file):
        return False
    
    try:
        with open(lock_file, 'r') as f:
            pid = int(f.read().strip())
        
        # Check if the process is still running
        try:
            proc = psutil.Process(pid)
            if proc.is_running():
                return True
        except psutil.NoSuchProcess:
            # Process is dead, remove stale lock file
            os.unlink(lock_file)
            return False
    except (ValueError, IOError):
        # Invalid lock file, remove it
        try:
            os.unlink(lock_file)
        except:
            pass
        return False
    
    return False

def start_streamlit():
    """Start Streamlit server with safety checks"""
    global streamlit_process
    
    try:
        # Check if port is already in use
        if is_port_in_use(8501):
            print("⚠️ Port 8501 is already in use. Using existing server...")
            return
        
        # Start Streamlit server
        streamlit_process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501", "--server.headless", "true",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print("🚀 Streamlit server starting...")
        
        # Wait for server to be ready
        max_wait = 10
        for i in range(max_wait):
            if is_port_in_use(8501):
                print("✅ Streamlit server is ready!")
                break
            time.sleep(1)
        else:
            print("⚠️ Streamlit server may not have started properly")
        
    except Exception as e:
        print(f"❌ Error starting Streamlit: {e}")

def main():
    # Default URL - change this to your deployed URL
    URL = "http://localhost:8501"  # Change to your Streamlit Cloud URL
    
    print("🚀 Launching Productivity Tracker Desktop App - Safe Version...")
    print(f"📱 URL: {URL}")
    
    # Check if another instance is already running
    if check_existing_instance():
        print("⚠️ Another instance of Productivity Tracker is already running!")
        print("💡 If you think this is an error, run: python3 cleanup_processes.py")
        print("🌐 Opening existing instance in browser...")
        import webbrowser
        webbrowser.open(URL)
        return
    
    # Try to acquire app lock
    if not acquire_app_lock():
        print("⚠️ Could not acquire app lock. Another instance may be starting.")
        print("🌐 Opening in browser instead...")
        import webbrowser
        webbrowser.open(URL)
        return
    
    print("🔒 App lock acquired successfully")
    
    # Register cleanup function
    atexit.register(cleanup_processes)
    signal.signal(signal.SIGINT, lambda s, f: cleanup_processes())
    signal.signal(signal.SIGTERM, lambda s, f: cleanup_processes())
    
    # Clean up any existing processes first
    print("🧹 Checking for existing processes...")
    cleanup_processes()
    
    # Wait a moment for cleanup to complete
    time.sleep(2)
    
    # Check if we're already running
    if is_port_in_use(8501):
        print("✅ Streamlit server already running, connecting to existing instance...")
    else:
        # Start Streamlit server
        start_streamlit()
    
    try:
        webview.create_window(
            title="Productivity Tracker",
            url=URL,
            width=1200,
            height=800,
            resizable=True,
            fullscreen=False,
            minimized=False,
            on_top=False
        )
        webview.start(debug=False)
    except Exception as e:
        print(f"❌ Error launching app: {e}")
        print("💡 Make sure pywebview is installed: pip install pywebview")
    finally:
        # Ensure cleanup happens
        cleanup_processes()

if __name__ == "__main__":
    main()
