import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from planner import StudyPlanner
from utils import (
    load_css, validate_inputs, calculate_progress,
    get_motivational_quote, export_to_csv, export_to_excel
)
import json

# Initialize session state
if 'study_plan' not in st.session_state:
    st.session_state.study_plan = None
if 'completed_topics' not in st.session_state:
    st.session_state.completed_topics = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'study_streak' not in st.session_state:
    st.session_state.study_streak = 0

# Load custom CSS
load_css()

def main():
    st.set_page_config(
        page_title="AI Study Planner",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="auto"
    )
    
    # Dark mode toggle in sidebar
    with st.sidebar:
        st.title("🎯 Settings")
        dark_mode = st.checkbox("🌙 Dark Mode", value=st.session_state.dark_mode)
        st.session_state.dark_mode = dark_mode
        
        if dark_mode:
            st.markdown("""
            <style>
                .stApp {
                    background-color: #1e1e1e;
                    color: white;
                }
            </style>
            """, unsafe_allow_html=True)
    
    # Main header
    st.title("📚 AI Study Planner")
    st.markdown("---")
    
    # Motivational quote
    quote = get_motivational_quote()
    st.info(f"💡 *{quote}*")
    
    # Study streak display
    if st.session_state.study_streak > 0:
        st.success(f"🔥 Study Streak: {st.session_state.study_streak} days!")
    
    # Create columns for responsive layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Create Study Plan")
        
        # Input form
        with st.form("study_plan_form"):
            subject = st.text_input("Subject Name*", placeholder="e.g., Mathematics, Physics")
            
            col_a, col_b = st.columns(2)
            with col_a:
                total_topics = st.number_input("Total Topics*", min_value=1, max_value=100, value=5)
            with col_b:
                difficulty = st.selectbox("Difficulty Level*", ["Easy", "Medium", "Hard"])
            
            exam_date = st.date_input(
                "Exam Date*",
                min_value=datetime.now().date(),
                max_value=datetime.now().date() + timedelta(days=365)
            )
            
            hours_per_day = st.slider("Hours Available Per Day*", 1, 12, 3)
            
            submitted = st.form_submit_button("🚀 Generate Study Plan")
            
            if submitted:
                if validate_inputs(subject, total_topics, exam_date, hours_per_day):
                    # Generate study plan
                    planner = StudyPlanner()
                    study_plan = planner.generate_plan(
                        subject=subject,
                        total_topics=total_topics,
                        exam_date=exam_date,
                        hours_per_day=hours_per_day,
                        difficulty=difficulty
                    )
                    
                    st.session_state.study_plan = study_plan
                    st.session_state.completed_topics = []
                    st.success("✅ Study plan generated successfully!")
                    st.rerun()
                else:
                    st.error("❌ Please fill in all required fields correctly.")
    
    with col2:
        st.subheader("📊 Study Progress")
        
        if st.session_state.study_plan:
            plan_data = st.session_state.study_plan
            
            # Progress metrics
            total_days = len(plan_data['daily_plan'])
            completed_count = len(st.session_state.completed_topics)
            total_topics_count = plan_data['total_topics']
            progress_percentage = (completed_count / total_topics_count) * 100 if total_topics_count > 0 else 0
            
            # Display progress cards
            col_progress1, col_progress2, col_progress3 = st.columns(3)
            
            with col_progress1:
                st.metric("📅 Total Days", total_days)
            
            with col_progress2:
                st.metric("✅ Completed Topics", f"{completed_count}/{total_topics_count}")
            
            with col_progress3:
                st.metric("📈 Progress", f"{progress_percentage:.1f}%")
            
            # Progress bar
            st.progress(progress_percentage / 100)
            
            # Progress chart
            if plan_data['daily_plan']:
                df_progress = pd.DataFrame(plan_data['daily_plan'])
                fig = px.bar(
                    df_progress,
                    x='day',
                    y='topics_count',
                    title="Daily Topic Distribution",
                    labels={'day': 'Day', 'topics_count': 'Number of Topics'},
                    color='topics_count',
                    color_continuous_scale='viridis'
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # Display study plan if generated
    if st.session_state.study_plan:
        st.markdown("---")
        st.subheader("📋 Your Study Plan")
        
        plan_data = st.session_state.study_plan
        
        # Plan summary
        col_summary1, col_summary2, col_summary3, col_summary4 = st.columns(4)
        
        with col_summary1:
            st.info(f"📚 **Subject**: {plan_data['subject']}")
        
        with col_summary2:
            st.info(f"📅 **Days Until Exam**: {plan_data['days_until_exam']}")
        
        with col_summary3:
            st.info(f"⏰ **Hours/Day**: {plan_data['hours_per_day']}")
        
        with col_summary4:
            st.info(f"🎯 **Difficulty**: {plan_data['difficulty']}")
        
        # Daily plan with checkboxes
        st.subheader("📅 Daily Schedule")
        
        for day_info in plan_data['daily_plan']:
            with st.expander(f"Day {day_info['day']} - {day_info['date']} ({day_info['topics_count']} topics)"):
                for i, topic in enumerate(day_info['topics']):
                    topic_key = f"day_{day_info['day']}_topic_{i}"
                    is_completed = topic_key in st.session_state.completed_topics
                    
                    col_topic, col_checkbox = st.columns([4, 1])
                    
                    with col_topic:
                        if is_completed:
                            st.markdown(f"~~✅ {topic}~~")
                        else:
                            st.markdown(f"📌 {topic}")
                    
                    with col_checkbox:
                        if st.checkbox("Done", key=topic_key, value=is_completed):
                            if topic_key not in st.session_state.completed_topics:
                                st.session_state.completed_topics.append(topic_key)
                                # Update streak
                                if len(st.session_state.completed_topics) % 3 == 0:
                                    st.session_state.study_streak += 1
                        else:
                            if topic_key in st.session_state.completed_topics:
                                st.session_state.completed_topics.remove(topic_key)
        
        # Export options
        st.markdown("---")
        st.subheader("💾 Export Study Plan")
        
        col_export1, col_export2 = st.columns(2)
        
        with col_export1:
            if st.button("📄 Download as CSV"):
                csv_data = export_to_csv(plan_data)
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name=f"study_plan_{plan_data['subject']}_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        
        with col_export2:
            if st.button("📊 Download as Excel"):
                excel_data = export_to_excel(plan_data)
                st.download_button(
                    label="Download Excel",
                    data=excel_data,
                    file_name=f"study_plan_{plan_data['subject']}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        
        # Reset button
        if st.button("🔄 Create New Plan"):
            st.session_state.study_plan = None
            st.session_state.completed_topics = []
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; padding: 20px;'>"
        "Made with ❤️ using Streamlit | AI Study Planner © 2024"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
