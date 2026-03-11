"""
Utility functions for AI Study Planner
Contains helper functions for validation, styling, exports, and more.
"""

import streamlit as st
import pandas as pd
import io
from datetime import datetime, timedelta
import random
from typing import Dict, List, Any

def load_css():
    """
    Load custom CSS for responsive design and styling.
    """
    css = """
    /* Responsive Design */
    @media (max-width: 768px) {
        .stColumns {
            flex-direction: column !important;
        }
        
        .stSidebar {
            width: 100% !important;
        }
        
        .main .block-container {
            padding: 1rem !important;
        }
        
        .stForm {
            margin: 0 !important;
        }
        
        .stDataFrame {
            font-size: 12px !important;
        }
    }
    
    @media (max-width: 480px) {
        .stButton > button {
            width: 100% !important;
            margin: 0.25rem 0 !important;
        }
        
        .stSelectbox > div > div {
            font-size: 14px !important;
        }
        
        .stNumberInput > div > div > input {
            font-size: 14px !important;
        }
    }
    
    /* Card Styles */
    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
    }
    
    .card-dark {
        background: #2d2d2d;
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        margin: 1rem 0;
        border-left: 4px solid #4a9eff;
    }
    
    /* Progress Bar Customization */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #1f77b4, #4a9eff);
    }
    
    /* Button Hover Effects */
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(31, 119, 180, 0.3);
        transition: all 0.3s ease;
    }
    
    /* Expander Customization */
    .streamlit-expanderHeader {
        background-color: #f0f2f6;
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Metric Cards */
    div[data-testid="metric-container"] {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    
    /* Dark Mode Styles */
    .dark-mode {
        background-color: #1e1e1e;
        color: white;
    }
    
    .dark-mode .card {
        background: #2d2d2d;
        color: white;
        border-left-color: #4a9eff;
    }
    
    .dark-mode div[data-testid="metric-container"] {
        background-color: #2d2d2d;
        border-color: #4a4a4a;
        color: white;
    }
    
    .dark-mode .streamlit-expanderHeader {
        background-color: #2d2d2d;
        color: white;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-in-out;
    }
    
    /* Custom Checkbox Styles */
    .stCheckbox > div {
        padding: 0.5rem 0;
    }
    
    /* Responsive Tables */
    @media (max-width: 640px) {
        .dataframe {
            font-size: 11px !important;
        }
        
        .dataframe th {
            padding: 4px !important;
        }
        
        .dataframe td {
            padding: 4px !important;
        }
    }
    
    /* Loading Animation */
    .loading-spinner {
        border: 3px solid #f3f3f3;
        border-top: 3px solid #1f77b4;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Success/Error Messages */
    .success-message {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    .error-message {
        background: linear-gradient(135deg, #dc3545, #fd7e14);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: 500;
    }
    
    /* Study Streak Badge */
    .streak-badge {
        background: linear-gradient(135deg, #ff6b6b, #ffd93d);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem 0;
    }
    
    /* Responsive Form Elements */
    @media (max-width: 768px) {
        .stForm > div {
            padding: 0.5rem !important;
        }
        
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stDateInput > div > div > input {
            font-size: 16px !important; /* Prevents zoom on iOS */
        }
    }
    
    /* Chart Container */
    .chart-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .dark-mode .chart-container {
        background: #2d2d2d;
        color: white;
    }
    """
    
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def validate_inputs(subject: str, total_topics: int, exam_date: datetime.date, 
                   hours_per_day: int) -> bool:
    """
    Validate user inputs for the study plan form.
    
    Args:
        subject: Subject name
        total_topics: Number of topics
        exam_date: Exam date
        hours_per_day: Hours available per day
    
    Returns:
        True if all inputs are valid, False otherwise
    """
    if not subject or subject.strip() == "":
        st.error("❌ Please enter a subject name.")
        return False
    
    if total_topics < 1:
        st.error("❌ Total topics must be at least 1.")
        return False
    
    if total_topics > 100:
        st.error("❌ Total topics cannot exceed 100.")
        return False
    
    if exam_date <= datetime.now().date():
        st.error("❌ Exam date must be in the future.")
        return False
    
    if hours_per_day < 1 or hours_per_day > 12:
        st.error("❌ Hours per day must be between 1 and 12.")
        return False
    
    # Check if exam date is too far in the future
    days_until_exam = (exam_date - datetime.now().date()).days
    if days_until_exam > 365:
        st.error("❌ Exam date cannot be more than 365 days from now.")
        return False
    
    return True

def calculate_progress(completed_topics: List[str], total_topics: int) -> Dict[str, Any]:
    """
    Calculate study progress statistics.
    
    Args:
        completed_topics: List of completed topic identifiers
        total_topics: Total number of topics
    
    Returns:
        Dictionary with progress statistics
    """
    if total_topics == 0:
        return {
            'completed': 0,
            'remaining': 0,
            'percentage': 0.0,
            'status': 'No topics'
        }
    
    completed = len(completed_topics)
    remaining = total_topics - completed
    percentage = (completed / total_topics) * 100
    
    if percentage == 0:
        status = 'Not Started'
    elif percentage < 25:
        status = 'Just Beginning'
    elif percentage < 50:
        status = 'Making Progress'
    elif percentage < 75:
        status = 'Halfway There'
    elif percentage < 100:
        status = 'Almost Done'
    else:
        status = 'Completed'
    
    return {
        'completed': completed,
        'remaining': remaining,
        'percentage': round(percentage, 1),
        'status': status
    }

def get_motivational_quote() -> str:
    """
    Get a random motivational quote for studying.
    
    Returns:
        Motivational quote string
    """
    quotes = [
        "The expert in anything was once a beginner.",
        "Success is the sum of small efforts repeated day in and day out.",
        "Don't watch the clock; do what it does. Keep going.",
        "The future depends on what you do today.",
        "Education is the passport to the future.",
        "Learning never exhausts the mind.",
        "The beautiful thing about learning is that nobody can take it away from you.",
        "A little progress each day adds up to big results.",
        "Study hard, dream big.",
        "Your limitation—it's only your imagination.",
        "Great things never come from comfort zones.",
        "Dream it. Wish it. Do it.",
        "Success doesn't just find you. You have to go out and get it.",
        "The harder you work, the luckier you get.",
        "Dream bigger. Do bigger.",
        "Don't stop when you're tired. Stop when you're done.",
        "Wake up with determination. Go to bed with satisfaction.",
        "Do something today that your future self will thank you for.",
        "Little things make big days.",
        "It's going to be hard, but hard does not mean impossible."
    ]
    
    return random.choice(quotes)

def export_to_csv(study_plan: Dict[str, Any]) -> str:
    """
    Export study plan to CSV format.
    
    Args:
        study_plan: Study plan dictionary
    
    Returns:
        CSV string
    """
    output = io.StringIO()
    
    # Write header information
    output.write("AI Study Planner Export\n")
    output.write(f"Subject,{study_plan['subject']}\n")
    output.write(f"Total Topics,{study_plan['total_topics']}\n")
    output.write(f"Exam Date,{study_plan['exam_date']}\n")
    output.write(f"Days Until Exam,{study_plan['days_until_exam']}\n")
    output.write(f"Hours Per Day,{study_plan['hours_per_day']}\n")
    output.write(f"Difficulty,{study_plan['difficulty']}\n")
    output.write(f"Created At,{study_plan['created_at']}\n")
    output.write("\n")
    
    # Write daily plan
    output.write("Daily Study Plan\n")
    output.write("Day,Date,Topics,Topic Count,Estimated Hours\n")
    
    for day_info in study_plan['daily_plan']:
        topics_str = "; ".join(day_info['topics'])
        output.write(f"{day_info['day']},{day_info['date']},\"{topics_str}\",{day_info['topics_count']},{day_info['estimated_hours']}\n")
    
    # Write study tips
    if 'study_tips' in study_plan:
        output.write("\n")
        output.write("Study Tips\n")
        output.write("Tip\n")
        for tip in study_plan['study_tips']:
            output.write(f"\"{tip}\"\n")
    
    return output.getvalue()

def export_to_excel(study_plan: Dict[str, Any]) -> bytes:
    """
    Export study plan to Excel format.
    
    Args:
        study_plan: Study plan dictionary
    
    Returns:
        Excel file bytes
    """
    output = io.BytesIO()
    
    # Create Excel writer
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Summary sheet
        summary_data = {
            'Detail': ['Subject', 'Total Topics', 'Exam Date', 'Days Until Exam', 
                      'Hours Per Day', 'Difficulty', 'Total Study Hours', 
                      'Average Topics Per Day', 'Created At'],
            'Value': [
                study_plan['subject'],
                study_plan['total_topics'],
                study_plan['exam_date'],
                study_plan['days_until_exam'],
                study_plan['hours_per_day'],
                study_plan['difficulty'],
                study_plan.get('total_study_hours', 0),
                study_plan.get('avg_topics_per_day', 0),
                study_plan['created_at']
            ]
        }
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Daily plan sheet
        daily_data = []
        for day_info in study_plan['daily_plan']:
            for topic in day_info['topics']:
                daily_data.append({
                    'Day': day_info['day'],
                    'Date': day_info['date'],
                    'Topic': topic,
                    'Estimated Hours': day_info['estimated_hours'] / len(day_info['topics']),
                    'Difficulty': day_info['difficulty']
                })
        
        if daily_data:
            daily_df = pd.DataFrame(daily_data)
            daily_df.to_excel(writer, sheet_name='Daily Plan', index=False)
        
        # Study tips sheet
        if 'study_tips' in study_plan:
            tips_data = {'Study Tips': study_plan['study_tips']}
            tips_df = pd.DataFrame(tips_data)
            tips_df.to_excel(writer, sheet_name='Study Tips', index=False)
    
    return output.getvalue()

def format_study_time(hours: float) -> str:
    """
    Format study time in human-readable format.
    
    Args:
        hours: Hours as float
    
    Returns:
        Formatted time string
    """
    if hours < 1:
        minutes = int(hours * 60)
        return f"{minutes} minutes"
    elif hours == 1:
        return "1 hour"
    elif hours < 2:
        return f"{hours:.1f} hours"
    else:
        return f"{int(hours)} hours"

def get_difficulty_color(difficulty: str) -> str:
    """
    Get color code for difficulty level.
    
    Args:
        difficulty: Difficulty string
    
    Returns:
        Color hex code
    """
    colors = {
        "Easy": "#28a745",
        "Medium": "#ffc107", 
        "Hard": "#dc3545"
    }
    return colors.get(difficulty, "#6c757d")

def get_progress_color(percentage: float) -> str:
    """
    Get color based on progress percentage.
    
    Args:
        percentage: Progress percentage (0-100)
    
    Returns:
        Color hex code
    """
    if percentage < 25:
        return "#dc3545"  # Red
    elif percentage < 50:
        return "#fd7e14"  # Orange
    elif percentage < 75:
        return "#ffc107"  # Yellow
    elif percentage < 100:
        return "#20c997"  # Teal
    else:
        return "#28a745"  # Green

def create_study_calendar(study_plan: Dict[str, Any]) -> pd.DataFrame:
    """
    Create a calendar view of the study plan.
    
    Args:
        study_plan: Study plan dictionary
    
    Returns:
        DataFrame with calendar data
    """
    calendar_data = []
    
    for day_info in study_plan['daily_plan']:
        calendar_data.append({
            'Date': pd.to_datetime(day_info['date']),
            'Day': day_info['day'],
            'Topics': len(day_info['topics']),
            'Hours': day_info['estimated_hours'],
            'Subject': study_plan['subject']
        })
    
    return pd.DataFrame(calendar_data)

def calculate_study_statistics(study_plan: Dict[str, Any], 
                             completed_topics: List[str]) -> Dict[str, Any]:
    """
    Calculate comprehensive study statistics.
    
    Args:
        study_plan: Study plan dictionary
        completed_topics: List of completed topic identifiers
    
    Returns:
        Dictionary with statistics
    """
    total_topics = study_plan['total_topics']
    completed_count = len(completed_topics)
    
    # Basic progress
    progress_percentage = (completed_count / total_topics * 100) if total_topics > 0 else 0
    
    # Time statistics
    total_hours = study_plan.get('total_study_hours', 0)
    completed_hours = (completed_count / total_topics * total_hours) if total_topics > 0 else 0
    remaining_hours = total_hours - completed_hours
    
    # Daily statistics
    daily_plan = study_plan['daily_plan']
    avg_topics_per_day = study_plan.get('avg_topics_per_day', 0)
    total_days = len(daily_plan)
    
    # Completion rate
    days_passed = min(len(completed_topics) // avg_topics_per_day, total_days) if avg_topics_per_day > 0 else 0
    days_remaining = total_days - days_passed
    
    return {
        'progress_percentage': round(progress_percentage, 1),
        'completed_topics': completed_count,
        'remaining_topics': total_topics - completed_count,
        'total_hours': total_hours,
        'completed_hours': round(completed_hours, 1),
        'remaining_hours': round(remaining_hours, 1),
        'total_days': total_days,
        'days_passed': days_passed,
        'days_remaining': days_remaining,
        'avg_topics_per_day': avg_topics_per_day,
        'study_pace': 'On Track' if progress_percentage >= (days_passed / total_days * 100) else 'Behind Schedule'
    }
