# 🚀 Productivity Tracker - Quick Start Guide

## 📱 For Your Different Laptop/Device

### ⚡ Super Quick Setup (2 minutes)

```bash
# 1. Copy these files to your new device:
#    - app.py
#    - desktop_app.py  
#    - cleanup_processes.py
#    - safe_launcher.sh
#    - setup_new_device.py
#    - requirements.txt

# 2. Open terminal/command prompt and run:
python3 setup_new_device.py

# 3. Launch the app:
./safe_launcher.sh
```

**That's it!** 🎉

## 🌐 Alternative: Web-Only Setup (1 minute)

If you just want to use the web version:

```bash
# 1. Install Streamlit
pip3 install streamlit plotly python-dotenv supabase

# 2. Run the web app
streamlit run app.py

# 3. Open browser to: http://localhost:8501
```

## 📋 What You Get

- 📊 **Dashboard**: Track your productivity metrics
- ⏰ **Time Logging**: Log hours spent on different activities  
- 🎯 **Habit Management**: Set up habits with monetary values
- 💰 **Value Tracking**: See your productivity worth in dollars
- 📈 **Charts**: Visualize your progress over time
- ⚙️ **Settings**: Customize goals and preferences

## 🔧 Troubleshooting

### If setup fails:
```bash
# Clean install
pip3 install --upgrade streamlit plotly python-dotenv supabase pywebview psutil
```

### If app won't start:
```bash
# Clean up processes
python3 cleanup_processes.py

# Try web version instead
streamlit run app.py
```

### If you see a white window:
- Open your browser to http://localhost:8501
- The web version works perfectly

## 📱 Access Methods

1. **Desktop App**: Opens automatically with `./safe_launcher.sh`
2. **Browser**: http://localhost:8501
3. **Mobile**: Same URL from your phone (same WiFi network)

## 🌟 Features Overview

### Demo Mode
- Works immediately without any setup
- Sample data to explore features
- No account required

### Full Mode (Optional)
- Add Supabase credentials to `.env` file
- Data syncs across devices
- Persistent data storage

## 💡 Pro Tips

1. **Bookmark**: Save http://localhost:8501 as a bookmark
2. **Mobile Access**: Use the same URL from your phone
3. **Demo First**: Try demo mode to see all features
4. **Cloud Sync**: Add Supabase for cross-device sync later

## 🆘 Need Help?

1. **Check Requirements**: Python 3.8+ needed
2. **Internet Required**: For downloading dependencies
3. **Firewall**: Make sure port 8501 isn't blocked
4. **Permissions**: On macOS/Linux, run `chmod +x safe_launcher.sh`

---

## 🎯 Summary

**Easiest Way**: Run `python3 setup_new_device.py` then `./safe_launcher.sh`

**Web Only**: Run `streamlit run app.py` then open http://localhost:8501

**The app is now running on your new device!** 🚀
