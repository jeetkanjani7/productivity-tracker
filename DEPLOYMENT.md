# Productivity Tracker - Streamlit Cloud Deployment

## Quick Deploy to Streamlit Cloud

1. **Go to**: https://share.streamlit.io/
2. **Sign in** with your GitHub account
3. **Click "New app"**
4. **Repository**: Your GitHub repo URL
5. **Branch**: main
6. **Main file path**: app.py
7. **Click "Deploy!"**

## Environment Variables Setup

In Streamlit Cloud dashboard, add these secrets:

```
SUPABASE_URL = "your-supabase-url"
SUPABASE_KEY = "your-supabase-anon-key"
```

## Access Your App

Once deployed, you'll get a URL like:
`https://your-app-name.streamlit.app`

This URL works on:
- ✅ Mac (Safari/Chrome)
- ✅ Work laptop (any browser)
- ✅ Phone (PWA installable)

## PWA Installation

On mobile:
1. Open the app URL
2. Look for "Add to Home Screen" prompt
3. Or manually: Share → Add to Home Screen

On desktop:
1. Look for install icon in address bar
2. Click to install as desktop app
