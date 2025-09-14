#!/usr/bin/env python3
"""
Productivity Tracker - New Device Setup Script
This script helps set up the Productivity Tracker on a new device
"""

import subprocess
import sys
import os

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    
    packages = [
        "streamlit>=1.49.0",
        "plotly>=6.0.0", 
        "python-dotenv>=1.0.0",
        "supabase>=2.0.0",
        "pywebview>=4.0.0",
        "psutil>=5.9.0"
    ]
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            return False
    
    return True

def test_installation():
    """Test if all dependencies are working"""
    print("🧪 Testing installation...")
    
    try:
        import streamlit
        print(f"✅ Streamlit {streamlit.__version__}")
    except ImportError:
        print("❌ Streamlit not found")
        return False
    
    try:
        import plotly
        print("✅ Plotly")
    except ImportError:
        print("❌ Plotly not found")
        return False
    
    try:
        import supabase
        print("✅ Supabase")
    except ImportError:
        print("❌ Supabase not found")
        return False
    
    try:
        import webview
        print("✅ PyWebView")
    except ImportError:
        print("❌ PyWebView not found")
        return False
    
    try:
        import psutil
        print("✅ Psutil")
    except ImportError:
        print("❌ Psutil not found")
        return False
    
    return True

def create_env_template():
    """Create a template .env file"""
    env_content = """# Productivity Tracker Environment Variables
# Copy this file and fill in your actual values

# Supabase Configuration (optional - app works in demo mode without these)
SUPABASE_URL=your-supabase-url-here
SUPABASE_KEY=your-supabase-anon-key-here

# Example:
# SUPABASE_URL=https://your-project.supabase.co
# SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
"""
    
    if not os.path.exists('.env'):
        with open('.env.example', 'w') as f:
            f.write(env_content)
        print("✅ Created .env.example file")
        print("💡 Copy .env.example to .env and add your Supabase credentials")
    else:
        print("✅ .env file already exists")

def main():
    print("🚀 Productivity Tracker - New Device Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return
    
    # Test installation
    if not test_installation():
        print("❌ Installation test failed")
        return
    
    # Create environment template
    create_env_template()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Copy .env.example to .env and add your Supabase credentials (optional)")
    print("2. Run the app: python3 desktop_app.py")
    print("3. Or use the safe launcher: ./safe_launcher.sh")
    print("4. Or run web version: streamlit run app.py")
    print("\n🌐 The app will be available at: http://localhost:8501")

if __name__ == "__main__":
    main()
