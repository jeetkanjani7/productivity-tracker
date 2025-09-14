#!/usr/bin/env python3
"""
Simple demo version without Supabase authentication
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="Productivity Tracker - Demo",
    page_icon="⏰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Demo data
def get_demo_categories():
    return [
        {"id": 1, "name": "Work", "rate": 50.00, "description": "Professional work activities"},
        {"id": 2, "name": "Personal", "rate": 20.00, "description": "Personal productive activities"},
        {"id": 3, "name": "Personal Development", "rate": 30.00, "description": "Learning and skill development"},
        {"id": 4, "name": "Habit", "rate": 25.00, "description": "Healthy habits like gym, reading"},
        {"id": 5, "name": "Social Media", "rate": -15.00, "description": "Time spent on social media platforms"}
    ]

def get_demo_logs():
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

def main():
    st.title("⏰ Productivity Tracker - Demo Mode")
    st.markdown("**This is a demo version with sample data. No authentication required!**")
    
    # Get demo data
    logs = get_demo_logs()
    categories = get_demo_categories()
    
    # Convert to DataFrame
    df = pd.DataFrame(logs)
    df['date'] = pd.to_datetime(df['date'])
    df['category_name'] = df['categories'].apply(lambda x: x['name'] if x else 'Unknown')
    df['category_rate'] = df['categories'].apply(lambda x: x['rate'] if x else 0)
    
    # Calculate totals
    total_value = df['value'].sum()
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
        savings_goal = 100000
        progress = (total_value / savings_goal) * 100 if savings_goal > 0 else 0
        st.metric("🎯 Goal Progress", f"{progress:.1f}%")
    
    # Progress bar
    st.subheader("🎯 Savings Goal Progress")
    progress_value = min(total_value / savings_goal, 1.0) if savings_goal > 0 else 0
    st.progress(progress_value)
    st.caption(f"${total_value:,.2f} of ${savings_goal:,.2f} ({progress:.1f}%)")
    
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
    
    # Activity logging form (demo)
    st.subheader("📝 Log New Activity (Demo)")
    
    with st.form("activity_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            log_date = st.date_input("Date", value=date.today())
        
        with col2:
            hours = st.number_input("Hours", min_value=0.1, max_value=24.0, step=0.1, value=1.0)
        
        with col3:
            category_options = {cat['name']: cat['id'] for cat in categories}
            selected_category = st.selectbox("Category", list(category_options.keys()))
            category_id = category_options[selected_category]
        
        note = st.text_area("Note (optional)", placeholder="What did you work on?")
        
        submitted = st.form_submit_button("Log Activity")
        
        if submitted:
            st.success("Activity logged successfully! (Demo mode - data not saved)")
    
    # Recent logs table
    st.subheader("📋 Recent Activities")
    
    # Display recent logs
    recent_logs = df.head(20)[['date', 'hours', 'category_name', 'value', 'note']]
    recent_logs.columns = ['Date', 'Hours', 'Category', 'Value ($)', 'Note']
    
    st.dataframe(recent_logs, use_container_width=True)
    
    # Info box
    st.info("""
    **Demo Mode Features:**
    - Sample data from the last 30 days
    - All charts and metrics work
    - Activity logging form (shows success message)
    - No authentication required
    - Perfect for testing the interface
    
    **To use with real data:**
    1. Fix Supabase redirect settings
    2. Disable email verification
    3. Use the main app.py
    """)

if __name__ == "__main__":
    main()
