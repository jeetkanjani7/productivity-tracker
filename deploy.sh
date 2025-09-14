#!/bin/bash

# Productivity Tracker - Quick Deployment Script
# This script helps you deploy your app to GitHub and Streamlit Cloud

echo "🚀 Productivity Tracker Deployment Helper"
echo "========================================"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial productivity tracker app"
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Check if GitHub remote exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo ""
    echo "🔗 GitHub Repository Setup:"
    echo "1. Go to https://github.com/new"
    echo "2. Create a new repository named 'productivity-tracker'"
    echo "3. Copy the repository URL"
    echo ""
    read -p "Enter your GitHub repository URL: " github_url
    
    if [ ! -z "$github_url" ]; then
        git remote add origin "$github_url"
        git branch -M main
        git push -u origin main
        echo "✅ Pushed to GitHub successfully!"
    else
        echo "❌ No URL provided. You can add it later with:"
        echo "   git remote add origin YOUR_GITHUB_URL"
    fi
else
    echo "✅ GitHub remote already configured"
fi

echo ""
echo "🌐 Streamlit Cloud Deployment:"
echo "1. Go to https://share.streamlit.io/"
echo "2. Sign in with your GitHub account"
echo "3. Click 'New app'"
echo "4. Select your repository: $(git remote get-url origin 2>/dev/null | sed 's/.*\///' | sed 's/\.git$//')"
echo "5. Set main file path to: app.py"
echo "6. Click 'Deploy!'"
echo ""
echo "🔐 Don't forget to add your Supabase credentials in Streamlit Cloud secrets:"
echo "   SUPABASE_URL = your-supabase-url"
echo "   SUPABASE_KEY = your-supabase-anon-key"
echo ""
echo "📱 Once deployed, you can:"
echo "   - Access from any browser (Mac, laptop, phone)"
echo "   - Install as PWA on mobile for app-like experience"
echo "   - Install as desktop app on Mac/Windows"
echo ""
echo "🎉 Your productivity tracker will be accessible from anywhere!"
