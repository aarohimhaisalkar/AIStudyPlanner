"""
Enhanced AI Study Planner with PostgreSQL Database Integration
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import json
import os

# Import our modules
from planner import generate_study_plan, init_openai_client
from utils import save_user_data, load_user_data
from analytics import create_analytics_charts, export_study_plan_csv
from database import db_manager, init_database

# Initialize OpenAI client
init_openai_client()

# Initialize database only once
database_initialized = False

def ensure_database():
    global database_initialized
    if not database_initialized:
        try:
            init_database()
            database_initialized = True
        except Exception as e:
            st.error(f"❌ Database connection failed: {e}")
            st.info("🔧 Please check your DATABASE_URL in .env file")

# Page configuration
st.set_page_config(
    page_title="AI Study Planner - Enhanced",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def load_css():
    """Load custom CSS styles"""
    st.markdown("""
    <style>
    /* Custom styles for the application */
    .main {
        padding-top: 2rem;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
    }
    .task-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .feature-card {
        background: linear-gradient(135deg, #e6fffa 0%, #f0fff4 100%);
        border-left: 4px solid #4299e1;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        color: #1a202c;
        border: 1px solid #bee3f8;
    }
    .tip-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        color: #1a202c;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .completed-task {
        background: #c6f6d5;
        color: #1a202c;
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.25rem 0;
        text-decoration: line-through;
    }
    .footer {
        text-align: center;
        padding: 2rem;
        color: #718096;
        border-top: 1px solid #e2e8f0;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
        border-left: 4px solid #4299e1;
    }
    .progress-card {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .study-schedule {
        background: linear-gradient(135deg, #edf2f7 0%, #e2e8f0 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Home"
    
    if 'user_data' not in st.session_state:
        st.session_state.user_data = load_user_data()
    
    if 'study_plan' not in st.session_state:
        st.session_state.study_plan = None
    
    
    if 'task_completion' not in st.session_state:
        st.session_state.task_completion = {}

# Navigation handlers
def handle_navigation(page):
    """Handle page navigation"""
    st.session_state.current_page = page
    st.rerun()

def handle_task_completion(task_id, completed):
    """Handle task completion updates"""
    # Update in session state only (no login required)
    st.session_state.task_completion[task_id] = completed

# Sidebar navigation
def sidebar_navigation():
    """Enhanced sidebar navigation"""
    
    # Navigation
    st.sidebar.markdown("---")
    st.sidebar.title("🧭 Navigation")
    
    pages = [
        ("🏠 Home", "Home"),
        ("📝 Generate Study Plan", "Generate Study Plan"),
        ("📊 Dashboard", "Dashboard"),
        ("📈 Progress Tracker", "Progress Tracker"),
        ("📊 Analytics", "Analytics")
    ]
    
    for page_name, page_key in pages:
        if st.sidebar.button(page_name, key=f"nav_{page_key}", width='stretch'):
            handle_navigation(page_key)

# Home page
def home_page():
    """Enhanced home page"""
    st.title("🎓 AI Study Planner - Enhanced")
    st.markdown("### 🌟 Your Intelligent Study Companion with Database Integration")
    
    # Feature highlights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card" style="background: linear-gradient(135deg, #e6fffa 0%, #f0fff4 100%); color: #1a202c; border: 1px solid #bee3f8;">
            <h4 style="color: #1a202c;">🧠 AI-Powered Planning</h4>
            <p style="color: #1a202c;">Get personalized study plans powered by advanced AI technology that considers your learning style and schedule.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card" style="background: linear-gradient(135deg, #e6fffa 0%, #f0fff4 100%); color: #1a202c; border: 1px solid #bee3f8;">
            <h4 style="color: #1a202c;">🗄️ Database Storage</h4>
            <p style="color: #1a202c;">Your study plans and progress are securely stored in PostgreSQL database with automatic backups.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card" style="background: linear-gradient(135deg, #e6fffa 0%, #f0fff4 100%); color: #1a202c; border: 1px solid #bee3f8;">
            <h4 style="color: #1a202c;">📊 Progress Analytics</h4>
            <p style="color: #1a202c;">Track your study progress with detailed analytics and visualizations.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick start section
    st.markdown("---")
    st.subheader("🚀 Quick Start")
    
    st.success("👋 Ready to create your personalized study plan!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📝 Create New Study Plan", key="quick_start", width='stretch'):
            handle_navigation("Generate Study Plan")
    
    with col2:
        if st.session_state.study_plan:
            if st.button("📊 View Dashboard", key="view_dashboard", width='stretch'):
                handle_navigation("Dashboard")
        else:
            st.info("📋 No study plan yet. Create one to get started!")

# Generate study plan page (enhanced with database)
def generate_study_plan_page():
    """Enhanced study plan generation with database storage"""
    st.title("📝 Generate Your Study Plan")
    st.markdown("Fill in your details to create a personalized study schedule.")
    
    with st.form("study_plan_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📚 Academic Details")
            subjects = st.text_area(
                "Subjects (one per line)",
                placeholder="Mathematics\nPhysics\nChemistry\nBiology",
                help="Enter each subject on a new line"
            )
            
            exam_date = st.date_input(
                "Exam Date / Deadline",
                min_value=datetime.now().date(),
                help="When is your exam or deadline?"
            )
            
            priority_level = st.selectbox(
                "Priority Level",
                ["Low", "Medium", "High", "Urgent"],
                help="How important is this exam for you?"
            )
        
        with col2:
            st.subheader("⏰ Study Schedule")
            daily_hours = st.slider(
                "Daily Study Hours",
                min_value=1.0,
                max_value=12.0,
                value=4.0,
                step=0.5,
                help="How many hours can you study per day?"
            )
            
            difficulty_level = st.selectbox(
                "Difficulty Level",
                ["Beginner", "Intermediate", "Advanced", "Expert"],
                help="How difficult are these subjects for you?"
            )
            
            study_preference = st.selectbox(
                "Study Preference",
                ["Morning", "Afternoon", "Evening", "Flexible"],
                help="When do you prefer to study?"
            )
        
        # Daily Activities Section
        st.subheader("🌅 Daily Activities Schedule")
        col1, col2 = st.columns(2)
        
        with col1:
            sleep_hours = st.slider(
                "😴 Sleep Hours",
                min_value=4.0,
                max_value=12.0,
                value=8.0,
                step=0.5,
                help="Recommended: 7-9 hours for optimal learning"
            )
            
            meal_time = st.slider(
                "🍽️ Meal Time (per day)",
                min_value=1.0,
                max_value=4.0,
                value=2.0,
                step=0.5,
                help="Hours for breakfast, lunch, dinner"
            )
            
            play_time = st.slider(
                "🎮 Leisure/Play Time",
                min_value=0.0,
                max_value=4.0,
                value=1.0,
                step=0.5,
                help="Time for hobbies, games, relaxation"
            )
        
        with col2:
            exercise_time = st.slider(
                "🏃 Exercise Time",
                min_value=0.0,
                max_value=2.0,
                value=0.5,
                step=0.5,
                help="Physical activity for better focus"
            )
            
            personal_time = st.slider(
                "🧘 Personal Time",
                min_value=0.0,
                max_value=3.0,
                value=1.0,
                step=0.5,
                help="Time for hobbies, reading, meditation"
            )
            
            screen_time_limit = st.slider(
                "📱 Screen Time Limit (non-study)",
                min_value=0.0,
                max_value=4.0,
                value=2.0,
                step=0.5,
                help="Limit recreational screen time"
            )
        
        # Additional preferences
        st.subheader("🎯 Additional Preferences")
        col1, col2 = st.columns(2)
        
        with col1:
            include_breaks = st.checkbox("Include regular breaks", value=True)
            include_revision = st.checkbox("Include revision sessions", value=True)
        
        with col2:
            include_tests = st.checkbox("Include practice tests", value=False)
            flexible_schedule = st.checkbox("Flexible scheduling", value=True)
        
        # Submit button
        submit_button = st.form_submit_button("🚀 Generate Study Plan", width='stretch')
        
        if submit_button:
            if not subjects.strip():
                st.error("Please enter at least one subject.")
                return
            
            # Process subjects
            subject_list = [s.strip() for s in subjects.split('\n') if s.strip()]
            
            # Calculate days until exam
            days_until = (exam_date - datetime.now().date()).days
            
            if days_until <= 0:
                st.error("Exam date must be in future!")
                return
            
            # Show loading spinner
            with st.spinner("🤖 Generating your personalized study plan..."):
                try:
                    # Generate study plan
                    plan_data = {
                        'subjects': subject_list,
                        'daily_hours': daily_hours,
                        'exam_date': exam_date.strftime('%Y-%m-%d'),
                        'days_until_exam': days_until,
                        'priority_level': priority_level,
                        'difficulty_level': difficulty_level,
                        'study_preference': study_preference,
                        'include_breaks': include_breaks,
                        'include_revision': include_revision,
                        'include_tests': include_tests,
                        'flexible_schedule': flexible_schedule,
                        # Daily Activities
                        'sleep_hours': sleep_hours,
                        'meal_time': meal_time,
                        'play_time': play_time,
                        'exercise_time': exercise_time,
                        'personal_time': personal_time,
                        'screen_time_limit': screen_time_limit
                    }
                    
                    study_plan = generate_study_plan(plan_data)
                    
                    if study_plan:
                        # Save to session state
                        st.session_state.study_plan = study_plan
                        st.success("✅ Study plan created!")
                        
                        st.success("🎉 Study plan generated successfully!")
                        st.balloons()
                        
                        # Show preview
                        st.subheader("📋 Study Plan Preview")
                        
                        # Display key metrics
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Total Study Days", days_until)
                        with col2:
                            st.metric("Daily Hours", daily_hours)
                        with col3:
                            st.metric("Total Subjects", len(subject_list))
                        with col4:
                            st.metric("Total Tasks", len(subject_list))
                        
                        # Show first few tasks
                        if 'daily_tasks' in study_plan:
                            st.subheader("📅 Sample Daily Tasks")
                            tasks_df = pd.DataFrame(study_plan['daily_tasks'][:5])
                            st.dataframe(tasks_df, width='stretch')
                
                except Exception as e:
                    st.error(f"Error generating study plan: {str(e)}")
                    st.info("Please check your OpenAI API key configuration and try again.")
    
    # Button outside form
    if st.session_state.study_plan:
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 View Full Dashboard", key="view_dashboard", width='stretch'):
                handle_navigation("Dashboard")
        
        with col2:
            if st.button("💾 Save Changes", key="save_changes", width='stretch'):
                if st.session_state.study_plan:
                    user_id = "anonymous"
                    plan_id = st.session_state.study_plan.get('id')
                    
                    if plan_id:
                        # Update existing plan
                        db_manager.save_study_plan(user_id, st.session_state.study_plan)
                        st.success("✅ Changes saved to database!")
                    else:
                        st.info("Create a new plan to save to database")

# Dashboard page (enhanced with database)
def dashboard_page():
    """Enhanced dashboard with database integration"""
    st.title("📊 Study Dashboard")
    
    if not st.session_state.study_plan:
        st.warning("No study plan available. Please generate a study plan first.")
        if st.button("Generate Study Plan", key="dashboard_generate"):
            handle_navigation("Generate Study Plan")
        return
    
    plan = st.session_state.study_plan
    
    # Overview metrics
    st.subheader("📈 Plan Overview")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Study Hours/Day", plan.get('daily_hours', 0))
    with col2:
        st.metric("Days Until Exam", plan.get('days_until_exam', 0))
    with col3:
        st.metric("Subjects", len(plan.get('subjects', [])))
    with col4:
        completed = sum(1 for task in plan.get('daily_tasks', []) if task.get('completed', False))
        total = len(plan.get('daily_tasks', []))
        st.metric("Progress", f"{completed}/{total}")
    with col5:
        sleep_hours = plan.get('sleep_hours', 8)
        st.metric("Sleep Hours", f"{sleep_hours}h")
    
    st.markdown("---")
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📅 Complete Daily Schedule", "📚 Study Tasks", "🌅 Daily Activities", "💡 AI Tips"])
    
    with tab1:
        st.subheader("🌅 Complete Daily Schedule")
        
        # Show complete hourly schedule
        if 'daily_schedule' in plan and plan['daily_schedule']:
            for activity in plan['daily_schedule']:
                category = activity.get('category', 'General')
                emoji = {
                    'Study': '📚',
                    'Meal': '🍽️',
                    'Health': '🏃',
                    'Personal': '🧘',
                    'Leisure': '🎮'
                }.get(category, '📌')
                
                st.markdown(f"""
                <div class="task-card">
                    <h4>{emoji} {activity.get('time', 'N/A')} - {activity.get('activity', 'N/A')}</h4>
                    <p><strong>Category:</strong> {category}</p>
                    <p><strong>Description:</strong> {activity.get('description', 'N/A')}</p>
                    {f'<p><strong>Subject:</strong> {activity.get("subject", "N/A")}</p>' if activity.get('subject') else ''}
                    {f'<p><strong>Topic:</strong> {activity.get("topic", "N/A")}</p>' if activity.get('topic') else ''}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No complete schedule available. Generate a study plan to see your full daily schedule.")
        
        # Show daily summary
        st.markdown("---")
        st.subheader("📊 Daily Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("😴 Sleep", f"{plan.get('sleep_hours', 8)}h")
        with col2:
            st.metric("🍽️ Meals", f"{plan.get('meal_time', 2)}h")
        with col3:
            st.metric("🎮 Play Time", f"{plan.get('play_time', 1)}h")
        with col4:
            st.metric("🏃 Exercise", f"{plan.get('exercise_time', 0.5)}h")
    
    with tab2:
        st.subheader("📚 Study Tasks")
        
        # Progress tracker at top - show for everyone
        daily_tasks = plan.get('daily_tasks', [])
        completed_count = 0
        for i, task in enumerate(daily_tasks):
            task_key = f"task_{i}"
            if st.session_state.task_completion.get(task_key, False):
                completed_count += 1
        total_count = len(daily_tasks)
        progress_percentage = (completed_count / total_count * 100) if total_count > 0 else 0
        
        # Progress tracker display
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("✅ Completed", completed_count)
        with col2:
            st.metric("📋 Total Tasks", total_count)
        with col3:
            st.metric("📊 Progress", f"{progress_percentage:.1f}%")
        
        # Progress bar
        st.progress(progress_percentage / 100)
        st.markdown("---")
        
        if daily_tasks:
            # Create schedule dataframe
            tasks_df = pd.DataFrame(daily_tasks)
            
            # Display tasks with checkboxes
            for i, task in tasks_df.iterrows():
                task_key = f"task_{i}"
                
                col1, col2, col3, col4 = st.columns([0.1, 0.4, 0.3, 0.2])
                
                with col1:
                    completed = st.checkbox(
                        "",
                        value=st.session_state.task_completion.get(task_key, task.get('completed', False)),
                        key=task_key
                    )
                    # Update completion status
                    handle_task_completion(task_key, completed)
                
                with col2:
                    st.write(f"**{task.get('subject', 'N/A')}**")
                
                with col3:
                    st.write(f"⏰ {task.get('time', 'N/A')}")
                
                with col4:
                    st.write(f"📖 {task.get('duration', 'N/A')}h")
                
                if task.get('description'):
                    st.write(f"📝 {task['description']}")
                
                st.markdown("---")
        
        # Save updated progress - available for everyone without login
        if st.button("💾 Save Progress", key="save_progress"):
            # Save all task completions to session state (no database required)
            saved_count = 0
            for i, task in enumerate(daily_tasks):
                task_key = f"task_{i}"
                completed = st.session_state.task_completion.get(task_key, task.get('completed', False))
                
                # Update task completion in session state
                if task_key in st.session_state.task_completion:
                    saved_count += 1
            
            if saved_count > 0:
                st.success(f"✅ {saved_count} tasks progress saved!")
                st.balloons()
            else:
                st.info("No changes to save.")
        else:
            st.info("No study tasks scheduled.")
    
    with tab3:
        st.subheader("🌅 Daily Activities")
        
        # Show daily activities breakdown
        activities = {
            '😴 Sleep': plan.get('sleep_hours', 8),
            '🍽️ Meals': plan.get('meal_time', 2),
            '🎮 Play Time': plan.get('play_time', 1),
            '🏃 Exercise': plan.get('exercise_time', 0.5),
            '🧘 Personal Time': plan.get('personal_time', 1),
            '📱 Screen Time': plan.get('screen_time_limit', 2)
        }
        
        # Create activity chart
        activities_df = pd.DataFrame(list(activities.items()), columns=['Activity', 'Hours'])
        
        # Pie chart
        fig = px.pie(
            activities_df,
            values='Hours',
            names='Activity',
            title="Daily Activities Distribution",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig, width='stretch')
        
        # Activity details
        st.markdown("### 📋 Activity Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="feature-card" style="background: linear-gradient(135deg, #e6fffa 0%, #f0fff4 100%); color: #1a202c; border: 1px solid #bee3f8;">
                <h4 style="color: #1a202c;">😴 Sleep Schedule</h4>
                <p style="color: #1a202c;">Recommended 7-9 hours for optimal brain function and memory consolidation.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card" style="background: linear-gradient(135deg, #e6fffa 0%, #f0fff4 100%); color: #1a202c; border: 1px solid #bee3f8;">
                <h4 style="color: #1a202c;">🍽️ Meal Times</h4>
                <p style="color: #1a202c;">Regular meals maintain energy levels and concentration for studying.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card" style="background: linear-gradient(135deg, #e6fffa 0%, #f0fff4 100%); color: #1a202c; border: 1px solid #bee3f8;">
                <h4 style="color: #1a202c;">🏃 Physical Activity</h4>
                <p style="color: #1a202c;">Exercise improves blood flow to the brain and enhances cognitive function.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class="feature-card" style="background: linear-gradient(135deg, #e6fffa 0%, #f0fff4 100%); color: #1a202c; border: 1px solid #bee3f8;">
                <h4 style="color: #1a202c;">🧘 Personal Time</h4>
                <p style="color: #1a202c;">Hobbies and relaxation prevent burnout and maintain mental health.</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.subheader("💡 AI Study Tips")
        
        if 'study_tips' in plan and plan['study_tips']:
            for i, tip in enumerate(plan['study_tips'], 1):
                st.markdown(f"""
                <div class="tip-card">
                    <h4>💡 Tip {i}</h4>
                    <p>{tip}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No study tips available.")
    
    # Export options
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        csv_data = export_study_plan_csv(plan)
        if csv_data and csv_data != "Error exporting study plan":
            st.download_button(
                label="📥 Download Study Plan (CSV)",
                data=csv_data,
                file_name=f"study_plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                width='stretch'
            )
        else:
            st.error("❌ Unable to generate CSV file")
    
    with col2:
        if st.button("🔄 Regenerate Plan", key="regenerate"):
            handle_navigation("Generate Study Plan")

# Progress tracker page (no login required)
def progress_tracker_page():
    """Progress tracking page (no login required)"""
    st.title("📈 Progress Tracker")
    
    if not st.session_state.study_plan:
        st.warning("No study plan available. Please generate a study plan first.")
        if st.button("Generate Study Plan", key="progress_generate"):
            handle_navigation("Generate Study Plan")
        return
    
    plan = st.session_state.study_plan
    
    # Calculate progress from session state
    daily_tasks = plan.get('daily_tasks', [])
    completed_count = 0
    for i, task in enumerate(daily_tasks):
        task_key = f"task_{i}"
        if st.session_state.task_completion.get(task_key, False):
            completed_count += 1
    total_count = len(daily_tasks)
    completion_percentage = (completed_count / total_count * 100) if total_count > 0 else 0
    
    # Calculate progress
    st.subheader("📊 Overall Progress")
    
    # Progress bar
    st.progress(completion_percentage / 100)
    st.write(f"**{completed_count} of {total_count} tasks completed ({completion_percentage:.1f}%)**")
    
    # Progress metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Completed Tasks", completed_count)
    with col2:
        st.metric("Remaining Tasks", total_count - completed_count)
    with col3:
        st.metric("Study Streak", "5 days")  # This could be calculated from user data
    
    st.markdown("---")
    
    # Task completion by subject
    if 'daily_tasks' in plan and plan['daily_tasks']:
        st.subheader("📚 Progress by Subject")
        
        # Group tasks by subject
        subject_progress = {}
        for task in plan['daily_tasks']:
            subject = task.get('subject', 'Unknown')
            if subject not in subject_progress:
                subject_progress[subject] = {'total': 0, 'completed': 0}
            subject_progress[subject]['total'] += 1
            if task.get('completed', False):
                subject_progress[subject]['completed'] += 1
        
        # Create progress data
        progress_data = []
        for subject, data in subject_progress.items():
            percentage = (data['completed'] / data['total'] * 100) if data['total'] > 0 else 0
            progress_data.append({
                'Subject': subject,
                'Completed': data['completed'],
                'Total': data['total'],
                'Progress %': percentage
            })
        
        progress_df = pd.DataFrame(progress_data)
        
        # Bar chart
        fig = px.bar(
            progress_df,
            x='Subject',
            y='Progress %',
            title="Progress by Subject",
            color='Subject'
        )
        st.plotly_chart(fig, width='stretch')
        
        # Progress table
        st.dataframe(progress_df, width='stretch')
    
    st.markdown("---")
    
    # Recent activity
    st.subheader("🕐 Recent Activity")
    
    # Show progress from session state (no database required)
    if daily_tasks:
        # Show recently completed tasks
        completed_tasks = []
        for i, task in enumerate(daily_tasks):
            task_key = f"task_{i}"
            if st.session_state.task_completion.get(task_key, False):
                completed_tasks.append(task)
        
        if completed_tasks:
            # Show completed tasks
            for task in completed_tasks[:5]:  # Show last 5
                st.markdown(f"""
                <div class="completed-task">
                    ✅ **{task.get('subject', 'Task')}** - {task.get('description', 'Completed')}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📝 No tasks completed yet. Start checking off tasks to see your progress!")
    else:
        st.info("📝 No tasks available in your study plan.")

# Analytics page (same as original)
def analytics_page():
    """Analytics and visualization page"""
    st.title("📊 Study Analytics")
    
    if not st.session_state.study_plan:
        st.warning("No study plan available. Please generate a study plan first.")
        return
    
    # Create analytics charts
    charts = create_analytics_charts(st.session_state.study_plan)
    
    if charts:
        # Display charts in tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 Study Distribution", 
            "⏰ Time Analysis", 
            "📚 Subject Performance", 
            "🎯 Goal Tracking"
        ])
        
        with tab1:
            if 'study_distribution' in charts:
                st.plotly_chart(charts['study_distribution'], width='stretch')
        
        with tab2:
            if 'time_analysis' in charts:
                st.plotly_chart(charts['time_analysis'], width='stretch')
        
        with tab3:
            if 'subject_performance' in charts:
                st.plotly_chart(charts['subject_performance'], width='stretch')
        
        with tab4:
            if 'goal_tracking' in charts:
                st.plotly_chart(charts['goal_tracking'], width='stretch')
    else:
        st.info("Analytics data not available. Complete more tasks to see detailed analytics.")
    
    # Study statistics
    st.markdown("---")
    st.subheader("📋 Study Statistics")
    
    plan = st.session_state.study_plan
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_study_hours = plan.get('daily_hours', 0) * plan.get('days_until_exam', 0)
        st.metric("Total Study Hours", total_study_hours)
    
    with col2:
        avg_session_length = plan.get('daily_hours', 0) / max(len(plan.get('subjects', [])), 1)
        st.metric("Avg Session Length", f"{avg_session_length:.1f}h")
    
    with col3:
        subjects_count = len(plan.get('subjects', []))
        st.metric("Total Subjects", subjects_count)
    
    with col4:
        tasks_per_day = len(plan.get('daily_tasks', [])) / max(plan.get('days_until_exam', 1), 1)
        st.metric("Tasks per Day", f"{tasks_per_day:.1f}")

# Main application logic
def main():
    """Main application with database integration"""
    # Initialize database only once
    ensure_database()
    
    # Load CSS
    load_css()
    
    # Initialize session state
    init_session_state()
    
    # Sidebar navigation
    sidebar_navigation()
    
    # Page content based on selection
    if st.session_state.current_page == "Home":
        home_page()
    elif st.session_state.current_page == "Generate Study Plan":
        generate_study_plan_page()
    elif st.session_state.current_page == "Dashboard":
        dashboard_page()
    elif st.session_state.current_page == "Progress Tracker":
        progress_tracker_page()
    elif st.session_state.current_page == "Analytics":
        analytics_page()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p>Made with ❤️ by AI Study Planner | Powered by OpenAI, Streamlit & PostgreSQL</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
