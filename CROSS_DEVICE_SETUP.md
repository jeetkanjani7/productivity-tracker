# 🚀 Productivity Tracker - Cross-Device Setup Guide

This guide will help you set up the Productivity Tracker on a different laptop or device.

## 📋 Prerequisites

### System Requirements
- **Operating System**: macOS, Windows, or Linux
- **Python**: Version 3.8 or higher
- **Internet Connection**: For downloading dependencies and accessing the app

### What You'll Need
- Access to the project files (GitHub repository or file transfer)
- Terminal/Command Prompt access
- Basic familiarity with command line

## 🔧 Setup Options

### Option 1: GitHub Repository (Recommended)

#### Step 1: Clone the Repository
```bash
# Clone the repository to your new device
git clone https://github.com/YOUR_USERNAME/productivity-tracker.git
cd productivity-tracker
```

#### Step 2: Install Dependencies
```bash
# Install Python dependencies
pip3 install streamlit plotly python-dotenv supabase pywebview psutil

# Or install from requirements file (if available)
pip3 install -r requirements.txt
```

#### Step 3: Run the App
```bash
# Use the safe launcher (recommended)
./safe_launcher.sh

# Or run directly
python3 desktop_app.py
```

### Option 2: File Transfer

#### Step 1: Transfer Files
Copy these essential files to your new device:
```
📁 Productivity Tracker/
├── app.py                    # Main Streamlit application
├── desktop_app.py           # Desktop app launcher
├── cleanup_processes.py     # Process cleanup utility
├── safe_launcher.sh         # Safe launcher script
├── requirements.txt         # Python dependencies
├── config.json             # Configuration file (if exists)
└── .env                    # Environment variables (if exists)
```

#### Step 2: Install Dependencies
```bash
# Navigate to the project directory
cd /path/to/Productivity_Tracker

# Install dependencies
pip3 install streamlit plotly python-dotenv supabase pywebview psutil
```

#### Step 3: Run the App
```bash
# Make scripts executable (Linux/macOS)
chmod +x safe_launcher.sh

# Run the app
./safe_launcher.sh
```

## 🖥️ Platform-Specific Instructions

### macOS Setup
```bash
# Install Python (if not already installed)
brew install python3

# Install dependencies
pip3 install streamlit plotly python-dotenv supabase pywebview psutil

# Run the app
./safe_launcher.sh
```

### Windows Setup
```bash
# Install Python from https://python.org
# Make sure to check "Add Python to PATH"

# Open Command Prompt or PowerShell
# Navigate to project directory
cd C:\path\to\Productivity_Tracker

# Install dependencies
pip install streamlit plotly python-dotenv supabase pywebview psutil

# Run the app (Windows version)
python desktop_app.py
```

### Linux Setup
```bash
# Install Python (Ubuntu/Debian)
sudo apt update
sudo apt install python3 python3-pip

# Install dependencies
pip3 install streamlit plotly python-dotenv supabase pywebview psutil

# Make scripts executable
chmod +x safe_launcher.sh

# Run the app
./safe_launcher.sh
```

## 🌐 Web-Only Setup (Simplest Option)

If you just want to use the app without the desktop wrapper:

### Step 1: Install Streamlit
```bash
pip3 install streamlit plotly python-dotenv supabase
```

### Step 2: Run Web Version
```bash
# Navigate to project directory
cd /path/to/Productivity_Tracker

# Run Streamlit directly
streamlit run app.py
```

### Step 3: Access the App
- Open your browser
- Go to `http://localhost:8501`
- The app will be accessible in your browser

## ⚙️ Configuration

### Environment Variables (Optional)
Create a `.env` file in the project directory:
```env
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
```

### Demo Mode
If you don't have Supabase credentials, the app will run in demo mode with sample data.

## 🚨 Troubleshooting

### Common Issues

#### 1. "Module not found" errors
```bash
# Reinstall dependencies
pip3 install --upgrade streamlit plotly python-dotenv supabase pywebview psutil
```

#### 2. Permission denied on scripts
```bash
# Make scripts executable (Linux/macOS)
chmod +x safe_launcher.sh
chmod +x cleanup_processes.py
```

#### 3. Port already in use
```bash
# Clean up processes
python3 cleanup_processes.py

# Or kill processes manually
pkill -f streamlit
```

#### 4. White window issue
- The app is running but the desktop window might not display properly
- Open your browser and go to `http://localhost:8501`
- The web version works reliably across all platforms

### Getting Help
```bash
# Test the app setup
python3 test_app_launch.py

# Check if everything is working
python3 -c "import streamlit, plotly, supabase; print('All dependencies OK!')"
```

## 📱 Usage Instructions

### Starting the App
```bash
# Recommended way (with safety checks)
./safe_launcher.sh

# Alternative way
python3 desktop_app.py

# Web-only way
streamlit run app.py
```

### Stopping the App
- **Desktop App**: Close the window or press Cmd+Q (macOS) / Alt+F4 (Windows)
- **Web App**: Press Ctrl+C in the terminal
- **Force Stop**: Run `python3 cleanup_processes.py`

### Accessing the App
- **Desktop Window**: Should open automatically
- **Browser**: Go to `http://localhost:8501`
- **Mobile**: Use the same URL from your phone's browser (if on same network)

## 🔄 Syncing Data

### Option 1: Supabase (Cloud Sync)
- Set up Supabase credentials in your `.env` file
- Data will sync automatically across devices

### Option 2: Local Data Only
- App runs in demo mode with sample data
- No data persistence between sessions

## 🎯 Quick Start Commands

```bash
# 1. Get the files
git clone https://github.com/YOUR_USERNAME/productivity-tracker.git
cd productivity-tracker

# 2. Install dependencies
pip3 install streamlit plotly python-dotenv supabase pywebview psutil

# 3. Run the app
./safe_launcher.sh

# 4. Open browser to http://localhost:8501
```

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Run `python3 cleanup_processes.py` to clean up
3. Try the web-only version: `streamlit run app.py`
4. Check that all dependencies are installed correctly

---

**🎉 You're all set!** The Productivity Tracker should now be running on your new device.
