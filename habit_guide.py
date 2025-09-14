#!/usr/bin/env python3
"""
Habit Value Calculator and Guide
This script helps you assign monetary values to different habits
"""

import streamlit as st

def show_habit_value_guide():
    """Show a comprehensive guide for assigning monetary values to habits"""
    
    st.title("💰 Habit Value Assignment Guide")
    st.markdown("Learn how to assign meaningful monetary values to your habits and activities.")
    
    # Habit categories with suggested values
    habit_categories = {
        "💼 Professional Development": {
            "Learning new skills": 50,
            "Reading industry books": 40,
            "Taking online courses": 45,
            "Attending conferences": 60,
            "Networking events": 35,
            "Mentoring others": 30,
            "Writing articles/blog posts": 25,
            "Building side projects": 40
        },
        "🏃 Health & Fitness": {
            "Exercise/Gym": 30,
            "Running/Jogging": 25,
            "Yoga/Meditation": 20,
            "Swimming": 25,
            "Cycling": 20,
            "Hiking": 15,
            "Team sports": 20,
            "Martial arts": 25,
            "Dancing": 15
        },
        "📚 Personal Growth": {
            "Reading books": 20,
            "Journaling": 15,
            "Learning languages": 25,
            "Playing musical instruments": 20,
            "Art/Creative projects": 15,
            "Volunteering": 10,
            "Travel/Exploration": 15,
            "Cooking new recipes": 10
        },
        "💸 Time Wasters (Negative Values)": {
            "Social media scrolling": -15,
            "Watching TV/movies": -10,
            "Gaming": -20,
            "Online shopping": -25,
            "Gossiping": -5,
            "Procrastination": -30,
            "Excessive news consumption": -10,
            "Mindless web browsing": -15
        },
        "🏠 Life Management": {
            "Cleaning/organizing": 15,
            "Meal prep": 20,
            "Garden maintenance": 10,
            "Home repairs": 25,
            "Financial planning": 40,
            "Family time": 30,
            "Pet care": 15,
            "Errands/shopping": 10
        }
    }
    
    # Display categories
    for category, habits in habit_categories.items():
        st.subheader(category)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            for habit, value in habits.items():
                if value > 0:
                    st.write(f"• **{habit}**: +${value}/hour")
                else:
                    st.write(f"• **{habit}**: ${value}/hour")
        
        with col2:
            st.info(f"**Total habits**: {len(habits)}")
    
    st.markdown("---")
    
    # Value calculation guide
    st.subheader("🎯 How to Calculate Habit Values")
    
    st.markdown("""
    ### **Positive Value Habits** (Money Earned):
    
    1. **Professional Value**: How much would you pay someone to do this?
    2. **Future Earnings**: Skills that increase your earning potential
    3. **Health Savings**: Activities that prevent future medical costs
    4. **Time Saved**: Habits that save you time (time = money)
    5. **Quality of Life**: Activities that improve your well-being
    
    ### **Negative Value Habits** (Money Lost):
    
    1. **Opportunity Cost**: What else could you be doing?
    2. **Health Costs**: Activities that harm your health
    3. **Financial Impact**: Habits that cost money directly
    4. **Productivity Loss**: Time that could be spent earning
    5. **Stress/Anxiety**: Activities that increase negative emotions
    
    ### **Example Calculations**:
    
    - **Learning Python**: +$50/hour (could lead to $100k+ salary increase)
    - **Exercise**: +$30/hour (prevents $50k+ in future medical costs)
    - **Social Media**: -$15/hour (wastes time that could earn money)
    - **Gaming**: -$20/hour (high opportunity cost)
    """)
    
    # Interactive calculator
    st.subheader("🧮 Habit Value Calculator")
    
    with st.form("habit_calculator"):
        col1, col2 = st.columns(2)
        
        with col1:
            habit_name = st.text_input("Habit Name", placeholder="e.g., Reading, Gaming, Exercise")
            hours_per_week = st.number_input("Hours per Week", min_value=0.1, max_value=168.0, step=0.5, value=5.0)
        
        with col2:
            suggested_rate = st.number_input("Suggested Rate ($/hour)", value=0.0, step=1.0, format="%.2f")
            habit_type = st.selectbox("Habit Type", ["Positive (Earns Money)", "Negative (Costs Money)"])
        
        if st.form_submit_button("Calculate Value"):
            if habit_name and suggested_rate != 0:
                weekly_value = hours_per_week * suggested_rate
                monthly_value = weekly_value * 4.33  # Average weeks per month
                yearly_value = weekly_value * 52
                
                st.success(f"**{habit_name} Value Analysis:**")
                st.write(f"• **Weekly**: ${weekly_value:.2f}")
                st.write(f"• **Monthly**: ${monthly_value:.2f}")
                st.write(f"• **Yearly**: ${yearly_value:.2f}")
                
                if habit_type == "Positive (Earns Money)":
                    st.info(f"💚 This habit adds ${yearly_value:.2f} to your productivity pot each year!")
                else:
                    st.warning(f"💸 This habit costs you ${abs(yearly_value):.2f} each year!")

if __name__ == "__main__":
    show_habit_value_guide()
