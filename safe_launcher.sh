#!/bin/bash
# Safe Productivity Tracker Launcher
# This script safely launches the app with proper cleanup

echo "🍑 Safe Productivity Tracker Launcher"
echo "====================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking dependencies..."
python3 -c "import webview, psutil" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing required packages..."
    pip3 install pywebview psutil
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install required packages"
        exit 1
    fi
fi

# Clean up any existing processes first
echo "🧹 Cleaning up any existing processes..."
python3 cleanup_processes.py

# Wait a moment for cleanup to complete
sleep 2

# Launch the safe desktop app
echo "🚀 Launching Productivity Tracker Desktop App (Safe Version)..."
python3 desktop_app.py

# Clean up when done
echo "🧹 Final cleanup..."
python3 cleanup_processes.py

echo "✅ App closed safely"

