I want you to build me a full-stack productivity app with the following requirements:

### Goal
- Track the number of hours I work (and other activities).
- Each activity belongs to a category with a monetary value (positive or negative).
- Show my total “pot of money” that grows or shrinks based on logged activities.
- Accessible from my work laptop, personal laptop, and phone (via browser or PWA install).

### Tech Stack
- **Frontend/UI**: Streamlit (Python).
- **Backend/Database**: Supabase (Postgres).
- **Auth**: Supabase authentication (email login is fine).
- **Deploy**: Deployable to Streamlit Cloud or similar.
- Make the Streamlit app **PWA-ready** so I can “install” it as an app on desktop and phone.

### Features
1. **Activity Logging**
   - Input form: date, hours worked, category (dropdown), optional note.
   - Categories should be configurable (e.g., in a JSON file or Supabase table) with rates:
     - Work = +50/hour
     - Personal = +20/hour
     - Personal Development = +30/hour
     - Habit (e.g., gym) = +25/hour
     - Social Media = –15/hour
   - Calculate value = hours × rate.
   - Store log in Supabase.

2. **CLI Logging (optional)**
   - Small Python script (separate file) that lets me run:
     ```bash
     python log_hours.py --hours 2 --category work --note "Deep work"
     ```
   - This script should insert directly into the Supabase table so logs appear in the dashboard instantly.

3. **Dashboard**
   - Big counter showing total pot.
   - Table of recent logs.
   - Line chart of total pot over time.
   - Pie chart / bar chart of time & money by category.
   - Progress bar toward a 2-year savings goal (configurable).

4. **Config**
   - Categories and rates should be easy to edit.
   - Savings goal should be easy to change.

### Deliverables
- Streamlit app code.
- Supabase schema (tables for `categories`, `logs`).
- CLI logging script.
- Deployment instructions (Streamlit Cloud + Supabase setup).
- Add minimal PWA manifest/service worker so app can be “installed”.

Make the code clean, modular, and production-ready.