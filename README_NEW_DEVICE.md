# 🚀 Productivity Tracker - Quick Setup for New Device

## ⚡ Quick Start (3 Commands)

```bash
# 1. Get the files (choose one method below)
git clone https://github.com/YOUR_USERNAME/productivity-tracker.git
# OR copy the files manually to your new device

# 2. Navigate to the project folder
cd productivity-tracker

# 3. Run the setup script
python3 setup_new_device.py
```

## 🎯 That's it! 

The setup script will:
- ✅ Check your Python version
- ✅ Install all required dependencies
- ✅ Test the installation
- ✅ Create configuration templates

## 🚀 Running the App

After setup, you have 3 options:

### Option 1: Desktop App (Recommended)
```bash
./safe_launcher.sh
```

### Option 2: Web Version (Simplest)
```bash
streamlit run app.py
```
Then open: http://localhost:8501

### Option 3: Direct Desktop Launch
```bash
python3 desktop_app.py
```

## 📱 Access the App

- **Desktop Window**: Opens automatically
- **Browser**: http://localhost:8501
- **Mobile**: Same URL from your phone (same network)

## 🔧 Troubleshooting

### If something goes wrong:
```bash
# Clean up and try again
python3 cleanup_processes.py
python3 setup_new_device.py
```

### If you see "module not found":
```bash
# Reinstall dependencies
pip3 install -r requirements.txt
```

### If the desktop window is white:
- Open your browser to http://localhost:8501
- The web version works perfectly

## 📋 What You Need

- **Python 3.8+** (most systems have this)
- **Internet connection** (for downloading dependencies)
- **5 minutes** (for setup)

## 🌟 Features

- 📊 Productivity tracking dashboard
- ⏰ Time logging
- 🎯 Habit management
- 💰 Value calculation
- 📈 Progress charts
- 🔄 Cross-device sync (with Supabase)

## 💡 Pro Tips

1. **Demo Mode**: Works without any setup - just run the app!
2. **Cloud Sync**: Add Supabase credentials to `.env` file for data sync
3. **Mobile Access**: Use the same URL from your phone
4. **Bookmark**: Save http://localhost:8501 as a bookmark

---

**🎉 Ready to boost your productivity!**
