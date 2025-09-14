# ⏰ Productivity Tracker

A full-stack productivity app that tracks your hours and activities, assigns monetary values to different habits, and helps you build your "pot of money" towards your savings goal.

## 🌟 Features

- **📊 Activity Logging**: Track hours spent on different activities
- **💰 Monetary Values**: Assign hourly rates to habits (positive for productive, negative for time-wasters)
- **🎯 Goal Tracking**: Set savings goals with timeline calculations
- **📱 Cross-Device Access**: Works on Mac, laptop, and phone
- **📈 Analytics**: Charts showing your progress and earning patterns
- **✏️ Edit Activities**: Update or delete logged activities
- **🔐 Secure**: User authentication and data protection via Supabase

## 🚀 Quick Deploy (5 Minutes)

### Option 1: Streamlit Cloud (Recommended)

1. **Run the deployment script**:
   ```bash
   ./deploy.sh
   ```

2. **Or manually**:
   - Create GitHub repository
   - Push your code
   - Go to [Streamlit Cloud](https://share.streamlit.io/)
   - Deploy with your GitHub repo

3. **Add environment variables** in Streamlit Cloud:
   ```
   SUPABASE_URL = your-supabase-url
   SUPABASE_KEY = your-supabase-anon-key
   ```

### Option 2: Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp env_example.txt .env
# Edit .env with your Supabase credentials

# Run the app
streamlit run app.py
```

## 📱 Cross-Device Access

Once deployed, access your app from:

- **Mac**: Open in Safari/Chrome
- **Work Laptop**: Any browser
- **Phone**: Install as PWA for app-like experience

### PWA Installation:
- **iPhone**: Safari → Share → Add to Home Screen
- **Android**: Chrome → Add to Home Screen
- **Desktop**: Look for install icon in address bar

## 🛠️ Setup Instructions

### 1. Supabase Setup
1. Create account at [supabase.com](https://supabase.com)
2. Create new project
3. Run the SQL schema: `supabase_schema.sql`
4. Get your URL and anon key from Settings → API

### 2. Environment Variables
Create `.env` file:
```
SUPABASE_URL=your-project-url
SUPABASE_KEY=your-anon-key
```

### 3. Database Migration (if needed)
Run `add_goal_date_migration.sql` in Supabase SQL editor to add goal date functionality.

## 📊 Usage

1. **Sign up** with your email
2. **Add habits** with hourly rates (positive for productive, negative for time-wasters)
3. **Log activities** and watch your "pot of money" grow
4. **Set goals** and track your progress
5. **View analytics** to understand your productivity patterns

## 🔧 CLI Usage

Log activities from command line:
```bash
python log_hours.py
```

## 📁 Project Structure

```
Productivity_app/
├── app.py                 # Main Streamlit application
├── demo_app.py           # Demo version (no auth required)
├── habit_guide.py        # Habit value assignment guide
├── log_hours.py          # CLI for logging hours
├── requirements.txt      # Python dependencies
├── manifest.json         # PWA configuration
├── sw.js                 # Service worker for offline capability
├── supabase_schema.sql   # Database schema
└── deploy.sh             # Deployment helper script
```

## 🌐 Deployment Options

- **Streamlit Cloud**: Free, easy deployment
- **Railway**: Alternative cloud platform
- **Self-hosted**: Docker, VPS, or local server
- **GitHub Pages**: Static hosting (limited functionality)

## 🔐 Security

- User authentication via Supabase Auth
- Row-level security for data protection
- HTTPS encryption for all connections
- No sensitive data stored locally

## 📱 PWA Features

- **Offline capability** with service worker
- **App-like experience** when installed
- **Push notifications** (future feature)
- **Responsive design** for all screen sizes

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

MIT License - feel free to use and modify!

## 🆘 Support

- Check the [deployment guide](CROSS_DEVICE_DEPLOYMENT.md)
- Review [setup instructions](DEPLOYMENT.md)
- Open an issue for bugs or feature requests

---

**Start tracking your productivity and building your savings pot today!** 🎯
