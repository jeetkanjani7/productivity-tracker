import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import os
from dotenv import load_dotenv
from supabase import create_client, Client
import json

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Productivity Tracker",
    page_icon="⏰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Supabase client
@st.cache_resource
def init_supabase():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key or url == "demo_mode" or key == "demo_mode":
        st.warning("🚧 **Demo Mode**: Supabase credentials not configured. This is a demo version with sample data.")
        return None
    
    return create_client(url, key)

supabase: Client = init_supabase()

# Demo mode functions
def get_demo_categories():
    return [
        {"id": 1, "name": "Work", "rate": 50.00, "description": "Professional work activities"},
        {"id": 2, "name": "Personal", "rate": 20.00, "description": "Personal productive activities"},
        {"id": 3, "name": "Personal Development", "rate": 30.00, "description": "Learning and skill development"},
        {"id": 4, "name": "Habit", "rate": 25.00, "description": "Healthy habits like gym, reading"},
        {"id": 5, "name": "Social Media", "rate": -15.00, "description": "Time spent on social media platforms"}
    ]

def get_demo_logs():
    import random
    from datetime import datetime, timedelta
    
    categories = get_demo_categories()
    logs = []
    
    # Generate sample data for the last 30 days
    for i in range(30):
        date = datetime.now() - timedelta(days=i)
        category = random.choice(categories)
        hours = round(random.uniform(0.5, 8.0), 1)
        value = hours * category['rate']
        
        logs.append({
            "id": i + 1,
            "date": date.strftime("%Y-%m-%d"),
            "hours": hours,
            "value": value,
            "note": f"Sample activity {i+1}",
            "categories": category
        })
    
    return logs

# Authentication functions
def sign_up(email: str, password: str):
    if supabase is None:
        # Demo mode - simulate successful signup
        user_obj = type('obj', (object,), {'id': 'demo_user', 'email': email})()
        return type('obj', (object,), {'user': user_obj})()
    
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "email_redirect_to": "http://localhost:8501"
            }
        })
        if response and response.user:
            # Store session info for immediate login
            st.session_state.user = response.user
            st.session_state.authenticated = True
            st.session_state.user_email = email
            st.session_state.user_id = response.user.id
            st.success("Account created successfully! You are now signed in.")
            return response
        else:
            st.error("Failed to create account. Please try again.")
            return None
    except Exception as e:
        error_msg = str(e)
        if "already registered" in error_msg.lower():
            st.error("This email is already registered. Please sign in instead.")
        else:
            st.error(f"Sign up error: {error_msg}")
        return None

def sign_in(email: str, password: str):
    if supabase is None:
        # Demo mode - simulate successful signin
        user_obj = type('obj', (object,), {'id': 'demo_user', 'email': email})()
        return type('obj', (object,), {'user': user_obj})()
    
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        if response and response.user:
            # Store session info
            st.session_state.user = response.user
            st.session_state.authenticated = True
            st.session_state.user_email = email
            st.session_state.user_id = response.user.id
            st.success("Signed in successfully!")
            return response
        else:
            st.error("Failed to sign in. Please check your credentials.")
            return None
    except Exception as e:
        error_msg = str(e)
        if "invalid" in error_msg.lower() or "credentials" in error_msg.lower():
            st.error("Invalid email or password. Please try again.")
        elif "email not confirmed" in error_msg.lower():
            st.error("Please check your email and click the verification link before signing in.")
        else:
            st.error(f"Sign in error: {error_msg}")
        return None

def sign_out():
    try:
        if supabase is not None:
            supabase.auth.sign_out()
        # Clear all session data
        st.session_state.user = None
        st.session_state.authenticated = False
        st.session_state.user_email = None
        st.session_state.user_id = None
        st.rerun()
    except Exception as e:
        st.error(f"Sign out error: {str(e)}")

def check_auth_status():
    """Check if user is still authenticated"""
    if supabase is None:
        return st.session_state.get('user') is not None
    
    # Always try to get current session first
    try:
        session = supabase.auth.get_session()
        if session and session.user:
            # Update session state with current user
            st.session_state.user = session.user
            st.session_state.authenticated = True
            st.session_state.user_email = session.user.email
            st.session_state.user_id = session.user.id
            return True
        else:
            # No valid session, clear state
            st.session_state.user = None
            st.session_state.authenticated = False
            st.session_state.user_email = None
            st.session_state.user_id = None
            return False
    except Exception as e:
        # If there's an error, check if we have cached user info
        if st.session_state.get('user') and st.session_state.get('authenticated'):
            # Keep the cached user for now
            return True
        else:
            # Clear state
            st.session_state.user = None
            st.session_state.authenticated = False
            st.session_state.user_email = None
            st.session_state.user_id = None
            return False

# Habit management functions
def get_habits():
    """Get all habits/categories with their monetary values"""
    if supabase is None:
        return get_demo_categories()
    
    try:
        response = supabase.table("categories").select("*").order("name").execute()
        return response.data
    except Exception as e:
        st.error(f"Error fetching habits: {str(e)}")
        return []

def add_habit(name: str, rate: float, description: str = ""):
    """Add a new habit/category"""
    if supabase is None:
        st.success("Habit added! (Demo mode - not saved)")
        return True
    
    try:
        response = supabase.table("categories").insert({
            "name": name,
            "rate": rate,
            "description": description
        }).execute()
        return response.data is not None
    except Exception as e:
        st.error(f"Error adding habit: {str(e)}")
        return False

def update_habit(habit_id: int, name: str, rate: float, description: str = ""):
    """Update an existing habit"""
    if supabase is None:
        st.success("Habit updated! (Demo mode - not saved)")
        return True
    
    try:
        response = supabase.table("categories").update({
            "name": name,
            "rate": rate,
            "description": description
        }).eq("id", habit_id).execute()
        return response.data is not None
    except Exception as e:
        st.error(f"Error updating habit: {str(e)}")
        return False

def delete_habit(habit_id: int):
    """Delete a habit"""
    if supabase is None:
        st.success("Habit deleted! (Demo mode - not saved)")
        return True
    
    try:
        response = supabase.table("categories").delete().eq("id", habit_id).execute()
        return response.data is not None
    except Exception as e:
        st.error(f"Error deleting habit: {str(e)}")
        return False

def update_log(log_id: int, date_val: date, hours: float, category_id: int, note: str = ""):
    """Update an existing log entry"""
    if supabase is None:
        st.success("Log updated! (Demo mode - not saved)")
        return True
    
    try:
        # Get category rate to calculate value
        category_response = supabase.table("categories").select("rate").eq("id", category_id).execute()
        if not category_response.data:
            st.error("Category not found")
            return False
        
        rate = category_response.data[0]['rate']
        value = hours * rate
        
        response = supabase.table("logs").update({
            "date": date_val.isoformat(),
            "hours": hours,
            "category_id": category_id,
            "note": note,
            "value": value
        }).eq("id", log_id).execute()
        return response.data is not None
    except Exception as e:
        st.error(f"Error updating log: {str(e)}")
        return False

def delete_log(log_id: int):
    """Delete a log entry"""
    if supabase is None:
        st.success("Log deleted! (Demo mode - not saved)")
        return True
    
    try:
        response = supabase.table("logs").delete().eq("id", log_id).execute()
        return response.data is not None
    except Exception as e:
        st.error(f"Error deleting log: {str(e)}")
        return False

def get_user_logs(user_id: str, limit: int = 100):
    if supabase is None:
        return get_demo_logs()
    
    try:
        response = supabase.table("logs").select("*, categories(*)").eq("user_id", user_id).order("date", desc=True).limit(limit).execute()
        return response.data
    except Exception as e:
        st.error(f"Error fetching logs: {str(e)}")
        return []

def insert_log(user_id: str, date_val: date, hours: float, category_id: int, note: str = ""):
    if supabase is None:
        # Demo mode - just show success message
        st.success("Activity logged successfully! (Demo mode - data not saved)")
        return [{"id": 1, "user_id": user_id, "date": date_val.isoformat(), "hours": hours, "category_id": category_id, "note": note}]
    
    try:
        # Get category rate to calculate value
        category_response = supabase.table("categories").select("rate").eq("id", category_id).execute()
        if not category_response.data:
            st.error("Category not found")
            return None
        
        rate = category_response.data[0]['rate']
        value = hours * rate
        
        response = supabase.table("logs").insert({
            "user_id": user_id,
            "date": date_val.isoformat(),
            "hours": hours,
            "category_id": category_id,
            "note": note,
            "value": value
        }).execute()
        return response.data
    except Exception as e:
        st.error(f"Error inserting log: {str(e)}")
        return None

def get_user_settings(user_id: str):
    if supabase is None:
        return {"savings_goal": 100000.00, "currency": "USD", "goal_date": "2025-12-31"}
    
    try:
        response = supabase.table("settings").select("*").eq("user_id", user_id).execute()
        if response.data:
            return response.data[0]
        else:
            # Create default settings
            default_settings = {
                "user_id": user_id,
                "savings_goal": 100000.00,
                "currency": "USD",
                "goal_date": "2025-12-31"
            }
            supabase.table("settings").insert(default_settings).execute()
            return default_settings
    except Exception as e:
        st.error(f"Error fetching settings: {str(e)}")
        return {"savings_goal": 100000.00, "currency": "USD", "goal_date": "2025-12-31"}

def update_settings(user_id: str, savings_goal: float, currency: str = "USD", goal_date: str = None):
    if supabase is None:
        # Demo mode - just show success message
        settings_data = {"user_id": user_id, "savings_goal": savings_goal, "currency": currency}
        if goal_date:
            settings_data["goal_date"] = goal_date
        st.success("Settings updated! (Demo mode - data not saved)")
        return [settings_data]
    
    try:
        # First, check if settings exist for this user
        existing_response = supabase.table("settings").select("*").eq("user_id", user_id).execute()
        
        settings_data = {
            "savings_goal": savings_goal,
            "currency": currency
        }
        if goal_date:
            settings_data["goal_date"] = goal_date
            
        if existing_response.data:
            # Update existing settings
            response = supabase.table("settings").update(settings_data).eq("user_id", user_id).execute()
        else:
            # Insert new settings
            settings_data["user_id"] = user_id
            response = supabase.table("settings").insert(settings_data).execute()
            
        return response.data
    except Exception as e:
        st.error(f"Error updating settings: {str(e)}")
        return None

# Initialize session state
if "user" not in st.session_state:
    st.session_state.user = None
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Authentication UI
def show_auth():
    st.title("⏰ Productivity Tracker")
    st.markdown("Track your hours and see your productivity value grow!")
    
    tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
    
    with tab1:
        st.subheader("Sign In")
        email = st.text_input("Email", key="signin_email")
        password = st.text_input("Password", type="password", key="signin_password")
        
        if st.button("Sign In"):
            if email and password:
                response = sign_in(email, password)
                if response and response.user:
                    st.rerun()
            else:
                st.error("Please enter both email and password")
    
    with tab2:
        st.subheader("Sign Up")
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm")
        
        if st.button("Sign Up"):
            if email and password and confirm_password:
                if password == confirm_password:
                    response = sign_up(email, password)
                    if response and response.user:
                        st.rerun()
                else:
                    st.error("Passwords do not match")
            else:
                st.error("Please fill in all fields")

# Activity logging form
def show_activity_form(user_id: str, habits: list):
    """Show the activity logging form"""
    st.subheader("📝 Log New Activity")
    
    # Form inputs outside of form for real-time calculation
    col1, col2, col3 = st.columns(3)
    
    with col1:
        log_date = st.date_input("Date", value=date.today(), key="log_date")
    
    with col2:
        hours = st.number_input("Hours", min_value=0.1, max_value=24.0, step=0.1, value=1.0, key="log_hours")
    
    with col3:
        habit_options = {habit['name']: habit['id'] for habit in habits}
        selected_habit = st.selectbox("Habit/Activity", list(habit_options.keys()), key="log_habit")
        habit_id = habit_options.get(selected_habit) if selected_habit else None
        
        # Show the rate for the selected habit
        selected_habit_data = next((h for h in habits if h['id'] == habit_id), None)
        if selected_habit_data:
            rate = selected_habit_data['rate']
            rate_text = f"${rate:.2f}/hour"
            if rate > 0:
                st.success(f"💰 {rate_text}")
            else:
                st.error(f"💸 {rate_text}")
    
    # Real-time value calculation (outside form)
    if selected_habit_data and habit_id:
        calculated_value = hours * selected_habit_data['rate']
        value_emoji = "💰" if calculated_value > 0 else "💸"
        
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if calculated_value > 0:
                st.success(f"**{value_emoji} Total Value: ${calculated_value:.2f}**")
            else:
                st.error(f"**{value_emoji} Total Value: ${calculated_value:.2f}**")
    elif selected_habit:
        st.markdown("---")
        st.info("Select a habit/activity to see the value calculation")
    
    note = st.text_area("Note (optional)", placeholder="What did you work on?", key="log_note")
    
    # Submit button
    if st.button("Log Activity", key="log_submit"):
        if habit_id is None:
            st.error("Please select a habit/activity first!")
        else:
            result = insert_log(user_id, log_date, hours, habit_id, note)
            if result:
                st.success("Activity logged successfully!")
                st.rerun()

# Main app UI
def show_main_app():
    user = st.session_state.user
    
    # Get data first (needed for sidebar calculations)
    logs = get_user_logs(user.id)
    habits = get_habits()
    settings = get_user_settings(user.id)
    savings_goal = float(settings.get("savings_goal", 100000))
    
    # Sidebar
    with st.sidebar:
        st.title("⏰ Productivity Tracker")
        st.write(f"Welcome, {user.email}!")
        
        if st.button("Sign Out"):
            sign_out()
        
        st.markdown("---")
        
        # Settings
        st.subheader("Settings")
        
        savings_goal = st.number_input(
            "Savings Goal", 
            value=savings_goal,
            min_value=0.0,
            step=1000.0,
            format="%.2f"
        )
        
        currency = st.selectbox("Currency", ["USD", "EUR", "GBP", "CAD"], 
                              index=["USD", "EUR", "GBP", "CAD"].index(settings.get("currency", "USD")))
        
        if st.button("Update Settings"):
            update_settings(user.id, savings_goal, currency)
            st.success("Settings updated!")
        
        st.markdown("---")
        
        # Goal Timeline Calculator
        st.subheader("🎯 Goal Timeline Calculator")
        
        with st.expander("📅 Set Custom Goal Date"):
            # Get current goal date from settings or use default
            current_goal_date_str = settings.get("goal_date")
            if current_goal_date_str:
                try:
                    current_goal_date = datetime.strptime(current_goal_date_str, "%Y-%m-%d").date()
                except:
                    current_goal_date = date(2025, 12, 31)
            else:
                current_goal_date = date(2025, 12, 31)
            
            # Debug info
            st.caption(f"Current saved goal date: {current_goal_date_str or 'Not set'}")
            
            goal_date_input = st.date_input(
                "Target Goal Date", 
                value=current_goal_date,
                help="When do you want to reach your savings goal?"
            )
            
            # Auto-save goal date when changed
            if goal_date_input != current_goal_date:
                if st.button("💾 Save Goal Date"):
                    result = update_settings(user.id, savings_goal, settings.get("currency", "USD"), goal_date_input.isoformat())
                    if result:
                        st.success("Goal date updated!")
                        st.rerun()
                    else:
                        st.error("Failed to update goal date")
                else:
                    st.info("⚠️ Goal date changed - click 'Save Goal Date' to update")
            
            # Calculate required daily earnings for custom date
            days_to_custom_goal = (goal_date_input - date.today()).days
            if days_to_custom_goal > 0:
                # Calculate remaining amount here
                remaining_amount_sidebar = savings_goal
                if logs:
                    df_temp = pd.DataFrame(logs)
                    total_value_temp = df_temp['value'].sum()
                    remaining_amount_sidebar = savings_goal - total_value_temp
                
                required_daily = remaining_amount_sidebar / days_to_custom_goal
                st.info(f"**Required daily earnings**: ${required_daily:.2f}")
                
                # Calculate current daily average for comparison
                current_daily_avg_sidebar = 0
                if logs:
                    df_temp = pd.DataFrame(logs)
                    df_temp['date'] = pd.to_datetime(df_temp['date'])
                    days_with_data = (df_temp['date'].max() - df_temp['date'].min()).days + 1
                    current_daily_avg_sidebar = df_temp['value'].sum() / max(days_with_data, 1)
                
                # Show comparison with current pace
                if current_daily_avg_sidebar > 0:
                    pace_ratio = required_daily / current_daily_avg_sidebar
                    if pace_ratio > 1:
                        st.warning(f"You need to increase your pace by {pace_ratio:.1f}x")
                    else:
                        st.success(f"You're on track! Current pace is {1/pace_ratio:.1f}x faster than needed")
        
        st.markdown("---")
        
        # Habit Management
        st.subheader("🎯 Habit Management")
        
        # Link to habit guide
        st.info("💡 **Need help assigning values?** Check out our [Habit Value Guide](http://localhost:8503)")
        
        # Show current habits
        habits = get_habits()
        if habits:
            st.write("**Current Habits:**")
            for habit in habits:
                rate_color = "green" if habit['rate'] > 0 else "red"
                st.write(f"• **{habit['name']}**: ${habit['rate']:.2f}/hour")
                if habit.get('description'):
                    st.caption(f"  _{habit['description']}_")
        
        # Add new habit form
        with st.expander("➕ Add New Habit"):
            with st.form("add_habit_form"):
                habit_name = st.text_input("Habit Name", placeholder="e.g., Exercise, Reading, Gaming")
                habit_rate = st.number_input("Hourly Rate ($)", value=0.0, step=1.0, format="%.2f")
                habit_desc = st.text_area("Description (optional)", placeholder="What is this habit about?")
                
                if st.form_submit_button("Add Habit"):
                    if habit_name and habit_rate != 0:
                        if add_habit(habit_name, habit_rate, habit_desc):
                            st.rerun()
                    else:
                        st.error("Please enter habit name and rate")
        
        # Edit existing habits
        with st.expander("✏️ Edit Habits"):
            for habit in habits:
                with st.form(f"edit_habit_{habit['id']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        new_name = st.text_input("Name", value=habit['name'], key=f"name_{habit['id']}")
                        new_rate = st.number_input("Rate ($)", value=float(habit['rate']), step=1.0, format="%.2f", key=f"rate_{habit['id']}")
                    with col2:
                        new_desc = st.text_area("Description", value=habit.get('description', ''), key=f"desc_{habit['id']}")
                        if st.form_submit_button("Update"):
                            if update_habit(habit['id'], new_name, new_rate, new_desc):
                                st.rerun()
                        if st.form_submit_button("Delete", type="secondary"):
                            if delete_habit(habit['id']):
                                st.rerun()
    
    # Calculate key metrics for sidebar
    total_value = 0
    current_daily_avg = 0
    remaining_amount = savings_goal
    
    if logs:
        # Convert to DataFrame for calculations
        df = pd.DataFrame(logs)
        df['date'] = pd.to_datetime(df['date'])
        total_value = df['value'].sum()
        remaining_amount = savings_goal - total_value
        
        # Calculate current daily average
        days_with_data = (df['date'].max() - df['date'].min()).days + 1
        current_daily_avg = total_value / max(days_with_data, 1)
    
    # Main content
    st.title("📊 Dashboard")
    
    if not logs:
        st.info("No logs found. Start logging your activities!")
        # Still show the activity logging form even if no logs exist
        show_activity_form(user.id, habits)
        return
    
    # Convert to DataFrame (reuse the one we already created)
    df['category_name'] = df['categories'].apply(lambda x: x['name'] if x else 'Unknown')
    df['category_rate'] = df['categories'].apply(lambda x: x['rate'] if x else 0)
    
    # Calculate totals (reuse the ones we already calculated)
    total_hours = df['hours'].sum()
    
    # Main metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Total Pot", f"${total_value:,.2f}")
    
    with col2:
        st.metric("⏱️ Total Hours", f"{total_hours:.1f}")
    
    with col3:
        avg_rate = total_value / total_hours if total_hours > 0 else 0
        st.metric("📈 Avg Rate", f"${avg_rate:.2f}/hr")
    
    with col4:
        progress = (total_value / savings_goal) * 100 if savings_goal > 0 else 0
        st.metric("🎯 Goal Progress", f"{progress:.1f}%")
    
    # Daily earnings and timeline metrics
    st.markdown("---")
    st.subheader("📅 Goal Timeline & Daily Targets")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate daily earnings needed using saved goal date
    remaining_amount = savings_goal - total_value
    
    # Get goal date from settings
    goal_date_str = settings.get("goal_date")
    if goal_date_str:
        try:
            goal_date_from_settings = datetime.strptime(goal_date_str, "%Y-%m-%d").date()
        except:
            goal_date_from_settings = date(2025, 12, 31)
    else:
        goal_date_from_settings = date(2025, 12, 31)
    
    days_remaining = (goal_date_from_settings - date.today()).days
    daily_target = remaining_amount / max(days_remaining, 1) if days_remaining > 0 else 0
    
    # Calculate current daily average
    if logs:
        days_with_data = (df['date'].max() - df['date'].min()).days + 1
        current_daily_avg = total_value / max(days_with_data, 1)
    else:
        current_daily_avg = 0
    
    # Calculate days remaining until target goal date
    days_to_goal = days_remaining  # This is the days until your target goal date
    
    # Calculate projected goal date based on current pace (for reference)
    if current_daily_avg > 0:
        projected_days_to_goal = remaining_amount / current_daily_avg
        projected_goal_date = date.today() + timedelta(days=int(projected_days_to_goal))
    else:
        projected_days_to_goal = float('inf')
        projected_goal_date = None
    
    with col1:
        st.metric(
            "📊 Daily Target", 
            f"${daily_target:.2f}",
            help=f"Amount needed daily to reach goal by {goal_date_from_settings.strftime('%Y-%m-%d')}"
        )
    
    with col2:
        st.metric(
            "📈 Current Daily Avg", 
            f"${current_daily_avg:.2f}",
            help="Your current daily earning average"
        )
    
    with col3:
        if days_to_goal > 0:
            st.metric(
                "⏰ Days to Goal", 
                f"{int(days_to_goal)}",
                help=f"Days remaining until your target goal date ({goal_date_from_settings.strftime('%Y-%m-%d')})"
            )
        else:
            st.metric("⏰ Days to Goal", "Goal Date Passed", help="Your target goal date has already passed")
    
    with col4:
        st.metric(
            "🎯 Target Goal Date", 
            goal_date_from_settings.strftime("%b %d, %Y"),
            help="Your target date to reach the savings goal"
        )
    
    # Show projected vs target comparison
    if projected_goal_date and current_daily_avg > 0:
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"**🎯 Your Target Goal Date**: {goal_date_from_settings.strftime('%b %d, %Y')}")
        
        with col2:
            if projected_goal_date < goal_date_from_settings:
                st.success(f"**📈 Projected Goal Date**: {projected_goal_date.strftime('%b %d, %Y')} (Ahead of target!)")
            else:
                st.warning(f"**📈 Projected Goal Date**: {projected_goal_date.strftime('%b %d, %Y')} (Behind target)")
    
    # Progress bar
    st.subheader("🎯 Savings Goal Progress")
    progress_value = min(total_value / savings_goal, 1.0) if savings_goal > 0 else 0
    st.progress(progress_value)
    st.caption(f"${total_value:,.2f} of ${savings_goal:,.2f} ({progress:.1f}%)")
    
    # Weekly and Monthly breakdown
    st.markdown("---")
    st.subheader("📊 Earning Breakdown")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "📅 Daily Target", 
            f"${daily_target:.2f}",
            help="Amount needed daily to reach goal by end of year"
        )
    
    with col2:
        weekly_target = daily_target * 7
        st.metric(
            "📅 Weekly Target", 
            f"${weekly_target:.2f}",
            help="Amount needed weekly to reach goal by end of year"
        )
    
    with col3:
        monthly_target = daily_target * 30
        st.metric(
            "📅 Monthly Target", 
            f"${monthly_target:.2f}",
            help="Amount needed monthly to reach goal by end of year"
        )
    
    # Motivation message
    if remaining_amount > 0:
        if current_daily_avg >= daily_target:
            st.success("🎉 **You're on track to reach your goal!** Keep up the great work!")
        elif current_daily_avg > 0:
            st.warning(f"📈 **You need to increase your daily earnings by ${daily_target - current_daily_avg:.2f}** to reach your goal on time.")
        else:
            st.info("🚀 **Start logging your activities** to begin tracking your progress toward your goal!")
    else:
        st.balloons()
        st.success("🎊 **Congratulations! You've reached your savings goal!** 🎊")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Total Pot Over Time")
        
        # Calculate cumulative sum
        df_sorted = df.sort_values('date')
        df_sorted['cumulative_value'] = df_sorted['value'].cumsum()
        
        fig_line = px.line(df_sorted, x='date', y='cumulative_value', 
                          title="Cumulative Value Over Time")
        fig_line.update_layout(xaxis_title="Date", yaxis_title="Total Value ($)")
        st.plotly_chart(fig_line, use_container_width=True)
    
    with col2:
        st.subheader("🥧 Value by Category")
        
        category_totals = df.groupby('category_name')['value'].sum().reset_index()
        fig_pie = px.pie(category_totals, values='value', names='category_name',
                        title="Value Distribution by Category")
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Show activity logging form
    show_activity_form(user.id, habits)
    
    # Recent logs table with edit functionality
    st.subheader("📋 Recent Activities")
    
    # Display recent logs with edit/delete options
    recent_logs = df.head(20)
    
    # Create a more interactive display
    for idx, log in recent_logs.iterrows():
        with st.expander(f"📅 {log['date'].strftime('%Y-%m-%d')} - {log['category_name']} ({log['hours']}h - ${log['value']:.2f})"):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"**Hours**: {log['hours']}")
                st.write(f"**Category**: {log['category_name']}")
                st.write(f"**Value**: ${log['value']:.2f}")
                if log['note']:
                    st.write(f"**Note**: {log['note']}")
            
            with col2:
                if st.button("✏️ Edit", key=f"edit_{log['id']}"):
                    st.session_state[f"editing_{log['id']}"] = True
            
            with col3:
                if st.button("🗑️ Delete", key=f"delete_{log['id']}"):
                    if delete_log(log['id']):
                        st.rerun()
        
        # Edit form (appears when edit button is clicked)
        if st.session_state.get(f"editing_{log['id']}", False):
            st.write("**Edit Activity:**")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                edit_date = st.date_input("Date", value=log['date'].date(), key=f"edit_date_{log['id']}")
            
            with col2:
                edit_hours = st.number_input("Hours", min_value=0.1, max_value=24.0, step=0.1, 
                                          value=float(log['hours']), key=f"edit_hours_{log['id']}")
            
            with col3:
                habit_options = {habit['name']: habit['id'] for habit in habits}
                current_category = log['category_name']
                edit_category = st.selectbox("Category", list(habit_options.keys()), 
                                           index=list(habit_options.keys()).index(current_category) if current_category in habit_options else 0,
                                           key=f"edit_category_{log['id']}")
                edit_category_id = habit_options[edit_category]
                
                # Show rate for selected category
                selected_habit_data = next((h for h in habits if h['id'] == edit_category_id), None)
                if selected_habit_data:
                    rate = selected_habit_data['rate']
                    rate_text = f"${rate:.2f}/hour"
                    if rate > 0:
                        st.success(f"💰 {rate_text}")
                    else:
                        st.error(f"💸 {rate_text}")
            
            # Real-time value calculation for edit form
            if selected_habit_data:
                calculated_value = edit_hours * selected_habit_data['rate']
                value_emoji = "💰" if calculated_value > 0 else "💸"
                
                st.markdown("---")
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if calculated_value > 0:
                        st.success(f"**{value_emoji} New Total Value: ${calculated_value:.2f}**")
                    else:
                        st.error(f"**{value_emoji} New Total Value: ${calculated_value:.2f}**")
            
            edit_note = st.text_area("Note", value=log['note'] if log['note'] else "", 
                                   key=f"edit_note_{log['id']}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save Changes", key=f"save_{log['id']}"):
                    if update_log(log['id'], edit_date, edit_hours, edit_category_id, edit_note):
                        st.session_state[f"editing_{log['id']}"] = False
                        st.rerun()
            
            with col2:
                if st.button("❌ Cancel", key=f"cancel_{log['id']}"):
                    st.session_state[f"editing_{log['id']}"] = False
                    st.rerun()
    
    # Quick stats for recent activities
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📊 Total Activities", len(recent_logs))
    
    with col2:
        avg_hours = recent_logs['hours'].mean()
        st.metric("⏱️ Avg Hours/Activity", f"{avg_hours:.1f}")
    
    with col3:
        avg_value = recent_logs['value'].mean()
        st.metric("💰 Avg Value/Activity", f"${avg_value:.2f}")
    
    # Bulk actions
    st.markdown("---")
    st.subheader("🔧 Bulk Actions")
    
    with st.expander("📊 Quick Edit Multiple Activities"):
        st.write("Select activities to edit in bulk:")
        
        # Create checkboxes for each activity
        selected_logs = []
        habit_options = {habit['name']: habit['id'] for habit in habits}
        
        for idx, log in recent_logs.iterrows():
            if st.checkbox(f"{log['date'].strftime('%Y-%m-%d')} - {log['category_name']} ({log['hours']}h)", 
                          key=f"bulk_select_{log['id']}"):
                selected_logs.append(log)
        
        if selected_logs:
            st.write(f"**Selected {len(selected_logs)} activities**")
            
            with st.form("bulk_edit_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    bulk_hours_adjustment = st.number_input("Hours Adjustment", value=0.0, step=0.1, 
                                                          help="Add/subtract hours from selected activities")
                    bulk_category_change = st.selectbox("Change Category", ["Keep Current"] + list(habit_options.keys()))
                
                with col2:
                    bulk_note_addition = st.text_area("Add Note", placeholder="Add this note to all selected activities")
                    bulk_action = st.selectbox("Action", ["Adjust Hours", "Change Category", "Add Note", "Delete Selected"])
                
                if st.form_submit_button("🚀 Apply Bulk Changes"):
                    success_count = 0
                    for log in selected_logs:
                        try:
                            if bulk_action == "Adjust Hours":
                                new_hours = max(0.1, float(log['hours']) + bulk_hours_adjustment)
                                if update_log(log['id'], log['date'].date(), new_hours, log['category_id'], log['note']):
                                    success_count += 1
                            elif bulk_action == "Change Category" and bulk_category_change != "Keep Current":
                                new_category_id = habit_options[bulk_category_change]
                                if update_log(log['id'], log['date'].date(), float(log['hours']), new_category_id, log['note']):
                                    success_count += 1
                            elif bulk_action == "Add Note" and bulk_note_addition:
                                new_note = f"{log['note']} {bulk_note_addition}".strip() if log['note'] else bulk_note_addition
                                if update_log(log['id'], log['date'].date(), float(log['hours']), log['category_id'], new_note):
                                    success_count += 1
                            elif bulk_action == "Delete Selected":
                                if delete_log(log['id']):
                                    success_count += 1
                        except Exception as e:
                            st.error(f"Error updating activity {log['id']}: {str(e)}")
                    
                    st.success(f"Successfully updated {success_count} out of {len(selected_logs)} activities!")
                    st.rerun()

# PWA Service Worker
def add_pwa_meta():
    st.markdown("""
    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="#1f77b4">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="default">
    <meta name="apple-mobile-web-app-title" content="Productivity Tracker">
    """, unsafe_allow_html=True)

# Main app logic
def main():
    add_pwa_meta()
    
    # Check authentication status on every page load
    if not check_auth_status():
        show_auth()
    else:
        show_main_app()

if __name__ == "__main__":
    main()
