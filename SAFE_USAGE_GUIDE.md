# 🍑 Productivity Tracker - Safe Usage Guide

## ⚠️ IMPORTANT: Fixed Infinite Copies Issue

The Mac app has been updated to prevent the infinite copies and crash issue. Here's what was fixed and how to use it safely.

## 🔧 What Was Fixed

### The Problem
- The original app started Streamlit servers without proper cleanup
- When the app was closed, Streamlit processes kept running
- Launching the app again would try to start more servers, causing conflicts
- This led to infinite copies and system crashes
- No singleton pattern to prevent multiple instances

### The Solution
- **Process Management**: Added proper cleanup of Streamlit processes with timeout handling
- **Port Checking**: App now checks if port 8501 is already in use
- **Signal Handling**: Proper handling of app termination signals
- **Cleanup Scripts**: Enhanced tools to manually clean up orphaned processes and lock files
- **Singleton Pattern**: App lock mechanism prevents multiple instances from running
- **Graceful Fallback**: If another instance is detected, opens browser instead
- **Improved Cleanup**: Better process termination with proper timeouts

## 🚀 Safe Usage Instructions

### Option 1: Use the Safe Launcher (Recommended)
```bash
./safe_launcher.sh
```

This script:
- ✅ Checks dependencies
- ✅ Cleans up existing processes and lock files
- ✅ Waits for cleanup to complete
- ✅ Launches the app safely with singleton protection
- ✅ Cleans up when done

### Test the Fix
```bash
python3 test_app_launch.py
```

This will test that:
- ✅ The app launches correctly
- ✅ Multiple instances are prevented
- ✅ Cleanup works properly

### Option 2: Manual Launch
```bash
# First, clean up any existing processes
python3 cleanup_processes.py

# Then launch the safe version
python3 desktop_app.py
```

### Option 3: Use the Native App (Fixed Version)
```bash
# Clean up first
python3 cleanup_processes.py

# Launch the native app
python3 native_peach_tracker.py
```

## 🛠️ Troubleshooting

### If You Still Have Issues

1. **Kill all processes manually:**
   ```bash
   python3 cleanup_processes.py
   ```

2. **Check for running processes:**
   ```bash
   ps aux | grep streamlit
   ps aux | grep webview
   ```

3. **Force kill if necessary:**
   ```bash
   pkill -f streamlit
   pkill -f webview
   ```

### If the App Won't Start

1. **Check if port 8501 is free:**
   ```bash
   lsof -i :8501
   ```

2. **Kill processes using the port:**
   ```bash
   sudo lsof -ti:8501 | xargs kill -9
   ```

3. **Try launching again:**
   ```bash
   ./safe_launcher.sh
   ```

## 📱 App Features

- **Safe Process Management**: No more infinite copies
- **Automatic Cleanup**: Processes are cleaned up when app closes
- **Port Conflict Detection**: Prevents multiple servers on same port
- **Error Handling**: Better error messages and recovery

## 🔒 Best Practices

1. **Always close the app properly** (Cmd+Q, not force-quit)
2. **Use the safe launcher** for best results
3. **Run cleanup script** if you experience issues
4. **Don't launch multiple instances** simultaneously

## 📋 Dependencies

Make sure you have these installed:
```bash
pip3 install pywebview psutil streamlit
```

Or install all requirements:
```bash
pip3 install -r requirements.txt
```

## 🎯 What's Different Now

### Before (Problematic)
- ❌ No process cleanup
- ❌ Multiple servers could run simultaneously
- ❌ Infinite copies when launched multiple times
- ❌ System crashes

### After (Fixed)
- ✅ Automatic process cleanup
- ✅ Port conflict detection
- ✅ Single instance management
- ✅ Safe termination handling
- ✅ Manual cleanup tools

## 🆘 Emergency Cleanup

If you're still experiencing issues, run this emergency cleanup:

```bash
# Kill all Python processes (be careful!)
pkill -f python

# Kill all Streamlit processes
pkill -f streamlit

# Kill all webview processes
pkill -f webview

# Then restart your terminal and try again
```

## 📞 Support

If you continue to have issues:
1. Run the cleanup script
2. Check the console output for error messages
3. Make sure all dependencies are installed
4. Try the safe launcher instead of direct launch

The app should now work reliably without causing system crashes or infinite copies!

