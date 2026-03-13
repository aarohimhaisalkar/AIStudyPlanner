import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import calendar

def create_analytics_charts(study_plan):
    """
    Create comprehensive analytics charts for the study plan
    
    Args:
        study_plan (dict): Study plan data
        
    Returns:
        dict: Dictionary containing all chart figures
    """
    
    charts = {}
    
    try:
        # Study distribution pie chart
        charts['study_distribution'] = create_study_distribution_chart(study_plan)
        
        # Time analysis chart
        charts['time_analysis'] = create_time_analysis_chart(study_plan)
        
        # Subject performance chart
        charts['subject_performance'] = create_subject_performance_chart(study_plan)
        
        # Goal tracking chart
        charts['goal_tracking'] = create_goal_tracking_chart(study_plan)
        
        # Weekly progress chart
        charts['weekly_progress'] = create_weekly_progress_chart(study_plan)
        
        # Study intensity heatmap
        charts['study_heatmap'] = create_study_heatmap(study_plan)
        
    except Exception as e:
        print(f"Error creating charts: {str(e)}")
        # Return empty charts if there's an error
        charts = {}
    
    return charts

def create_study_distribution_chart(study_plan):
    """
    Create a pie chart showing study time distribution across subjects
    
    Args:
        study_plan (dict): Study plan data
        
    Returns:
        plotly.graph_objects.Figure: Pie chart figure
    """
    
    subjects = study_plan.get('subjects', [])
    daily_hours = study_plan.get('daily_hours', 4)
    
    if not subjects:
        # Create empty chart
        fig = go.Figure()
        fig.add_annotation(
            text="No subjects available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig
    
    # Calculate hours per subject
    hours_per_subject = daily_hours / len(subjects)
    
    # Create data for pie chart
    subject_data = {
        'Subject': subjects,
        'Hours': [hours_per_subject] * len(subjects),
        'Percentage': [100 / len(subjects)] * len(subjects)
    }
    
    df = pd.DataFrame(subject_data)
    
    # Create pie chart
    fig = px.pie(
        df,
        values='Hours',
        names='Subject',
        title='📚 Daily Study Time Distribution',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Hours: %{value:.1f}<br>Percentage: %{percent}<extra></extra>'
    )
    
    fig.update_layout(
        font=dict(size=12),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.01
        )
    )
    
    return fig

def create_time_analysis_chart(study_plan):
    """
    Create a bar chart showing time analysis for different activities
    
    Args:
        study_plan (dict): Study plan data
        
    Returns:
        plotly.graph_objects.Figure: Bar chart figure
    """
    
    daily_hours = study_plan.get('daily_hours', 4)
    include_breaks = study_plan.get('include_breaks', True)
    include_revision = study_plan.get('include_revision', True)
    include_tests = study_plan.get('include_tests', False)
    
    # Calculate time allocation
    activities = {}
    
    # Main study time
    activities['Main Study'] = daily_hours * 0.7  # 70% for main study
    
    # Revision time
    if include_revision:
        activities['Revision'] = daily_hours * 0.15  # 15% for revision
    else:
        activities['Revision'] = 0
    
    # Break time
    if include_breaks:
        activities['Breaks'] = daily_hours * 0.1  # 10% for breaks
    else:
        activities['Breaks'] = 0
    
    # Practice tests
    if include_tests:
        activities['Practice Tests'] = daily_hours * 0.05  # 5% for tests
    else:
        activities['Practice Tests'] = 0
    
    # Create DataFrame
    df = pd.DataFrame(list(activities.items()), columns=['Activity', 'Hours'])
    
    # Create bar chart
    fig = px.bar(
        df,
        x='Activity',
        y='Hours',
        title='⏰ Daily Time Allocation',
        color='Hours',
        color_continuous_scale='Blues'
    )
    
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Hours: %{y:.1f}<extra></extra>'
    )
    
    fig.update_layout(
        xaxis_title="Activities",
        yaxis_title="Hours",
        showlegend=False
    )
    
    return fig

def create_subject_performance_chart(study_plan):
    """
    Create a chart showing subject performance based on completion rates
    
    Args:
        study_plan (dict): Study plan data
        
    Returns:
        plotly.graph_objects.Figure: Performance chart
    """
    
    daily_tasks = study_plan.get('daily_tasks', [])
    
    if not daily_tasks:
        # Create empty chart
        fig = go.Figure()
        fig.add_annotation(
            text="No task data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig
    
    # Calculate completion rates by subject
    subject_stats = {}
    
    for task in daily_tasks:
        subject = task.get('subject', 'Unknown')
        if subject not in subject_stats:
            subject_stats[subject] = {'total': 0, 'completed': 0}
        
        subject_stats[subject]['total'] += 1
        if task.get('completed', False):
            subject_stats[subject]['completed'] += 1
    
    # Create performance data
    performance_data = []
    for subject, stats in subject_stats.items():
        completion_rate = (stats['completed'] / stats['total'] * 100) if stats['total'] > 0 else 0
        performance_data.append({
            'Subject': subject,
            'Completion Rate': completion_rate,
            'Completed Tasks': stats['completed'],
            'Total Tasks': stats['total']
        })
    
    df = pd.DataFrame(performance_data)
    
    # Create bar chart
    fig = px.bar(
        df,
        x='Subject',
        y='Completion Rate',
        title='📈 Subject Performance (Completion Rate)',
        color='Completion Rate',
        color_continuous_scale='RdYlGn',
        range_y=[0, 100]
    )
    
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Completion Rate: %{y:.1f}%<br>Completed: %{customdata[0]} / %{customdata[1]}<extra></extra>',
        customdata=df[['Completed Tasks', 'Total Tasks']].values
    )
    
    fig.update_layout(
        xaxis_title="Subjects",
        yaxis_title="Completion Rate (%)"
    )
    
    # Add target line
    fig.add_hline(
        y=80,
        line_dash="dash",
        line_color="red",
        annotation_text="Target: 80%"
    )
    
    return fig

def create_goal_tracking_chart(study_plan):
    """
    Create a progress tracking chart towards study goals
    
    Args:
        study_plan (dict): Study plan data
        
    Returns:
        plotly.graph_objects.Figure: Goal tracking chart
    """
    
    daily_tasks = study_plan.get('daily_tasks', [])
    days_until_exam = study_plan.get('days_until_exam', 30)
    
    if not daily_tasks:
        # Create empty chart
        fig = go.Figure()
        fig.add_annotation(
            text="No goal data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig
    
    # Calculate current progress
    completed_tasks = sum(1 for task in daily_tasks if task.get('completed', False))
    total_tasks = len(daily_tasks)
    current_progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    # Create progress timeline
    days_passed = max(0, 30 - days_until_exam)  # Assuming 30 days total study period
    expected_progress = (days_passed / 30 * 100) if days_until_exam > 0 else 100
    
    # Create gauge chart for current progress
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = current_progress,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Study Progress"},
        delta = {'reference': expected_progress},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 25], 'color': "lightgray"},
                {'range': [25, 50], 'color': "gray"},
                {'range': [50, 75], 'color': "lightblue"},
                {'range': [75, 100], 'color': "blue"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        title='🎯 Overall Study Goal Progress',
        height=400
    )
    
    return fig

def create_weekly_progress_chart(study_plan):
    """
    Create a weekly progress chart
    
    Args:
        study_plan (dict): Study plan data
        
    Returns:
        plotly.graph_objects.Figure: Weekly progress chart
    """
    
    # Generate sample weekly data
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    
    # Simulate progress data (in real app, this would come from actual user data)
    progress_data = []
    for i, day in enumerate(days):
        # Simulate increasing progress throughout the week
        base_progress = 20 + (i * 10)
        daily_progress = min(100, base_progress + np.random.randint(-5, 15))
        progress_data.append(daily_progress)
    
    # Create line chart
    fig = px.line(
        x=days,
        y=progress_data,
        title='📅 Weekly Study Progress',
        markers=True
    )
    
    fig.update_traces(
        line=dict(color='blue', width=3),
        marker=dict(size=8, color='blue')
    )
    
    fig.update_layout(
        xaxis_title="Day of Week",
        yaxis_title="Progress (%)",
        yaxis=dict(range=[0, 100])
    )
    
    # Add target line
    fig.add_hline(
        y=80,
        line_dash="dash",
        line_color="green",
        annotation_text="Weekly Target: 80%"
    )
    
    return fig

def create_study_heatmap(study_plan):
    """
    Create a study intensity heatmap
    
    Args:
        study_plan (dict): Study plan data
        
    Returns:
        plotly.graph_objects.Figure: Heatmap figure
    """
    
    subjects = study_plan.get('subjects', [])
    daily_hours = study_plan.get('daily_hours', 4)
    
    if not subjects:
        # Create empty chart
        fig = go.Figure()
        fig.add_annotation(
            text="No subject data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig
    
    # Create time slots
    time_slots = []
    for hour in range(9, 22):  # 9 AM to 9 PM
        time_slots.append(f"{hour:02d}:00")
    
    # Create intensity data (simulate study intensity throughout the day)
    intensity_data = []
    for subject in subjects:
        subject_intensity = []
        for i, time_slot in enumerate(time_slots):
            # Simulate higher intensity during preferred study times
            if 10 <= i <= 15:  # Peak study hours
                intensity = np.random.randint(7, 10)
            elif 16 <= i <= 18:  # Afternoon dip
                intensity = np.random.randint(3, 6)
            else:  # Evening study
                intensity = np.random.randint(5, 8)
            subject_intensity.append(intensity)
        intensity_data.append(subject_intensity)
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=intensity_data,
        x=time_slots,
        y=subjects,
        colorscale='Blues',
        showscale=True,
        hovertemplate='<b>%{y}</b><br>Time: %{x}<br>Intensity: %{z}<extra></extra>'
    ))
    
    fig.update_layout(
        title='🔥 Study Intensity Heatmap',
        xaxis_title="Time of Day",
        yaxis_title="Subjects"
    )
    
    return fig

def create_study_streak_chart(user_data):
    """
    Create a study streak visualization
    
    Args:
        user_data (dict): User's historical data
        
    Returns:
        plotly.graph_objects.Figure: Streak chart
    """
    
    # Generate sample streak data
    dates = []
    streak_values = []
    current_streak = 0
    
    for i in range(30):  # Last 30 days
        date = datetime.now() - timedelta(days=29-i)
        dates.append(date.strftime('%m/%d'))
        
        # Simulate streak data (in real app, this would come from actual user data)
        if i < 25 or i in [26, 27, 29]:  # Simulate some missed days
            current_streak += 1
        else:
            current_streak = 0
        
        streak_values.append(current_streak)
    
    # Create line chart
    fig = px.line(
        x=dates,
        y=streak_values,
        title='🔥 Study Streak (Last 30 Days)',
        markers=True
    )
    
    fig.update_traces(
        line=dict(color='orange', width=3),
        marker=dict(size=6, color='orange')
    )
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Consecutive Study Days"
    )
    
    return fig

def create_productivity_analysis_chart(study_plan):
    """
    Create a productivity analysis chart
    
    Args:
        study_plan (dict): Study plan data
        
    Returns:
        plotly.graph_objects.Figure: Productivity chart
    """
    
    daily_tasks = study_plan.get('daily_tasks', [])
    
    if not daily_tasks:
        return None
    
    # Calculate productivity metrics
    total_tasks = len(daily_tasks)
    completed_tasks = sum(1 for task in daily_tasks if task.get('completed', False))
    
    # Create productivity categories
    productivity_data = {
        'Category': ['Completed', 'In Progress', 'Not Started'],
        'Count': [
            completed_tasks,
            sum(1 for task in daily_tasks if not task.get('completed', False)),
            0  # Assuming all tasks are either completed or not started
        ]
    }
    
    df = pd.DataFrame(productivity_data)
    
    # Create donut chart
    fig = px.pie(
        df,
        values='Count',
        names='Category',
        title='⚡ Task Status Distribution',
        hole=0.4
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Tasks: %{value}<br>Percentage: %{percent}<extra></extra>'
    )
    
    return fig

def calculate_study_metrics(study_plan):
    """
    Calculate various study metrics
    
    Args:
        study_plan (dict): Study plan data
        
    Returns:
        dict: Calculated metrics
    """
    
    daily_tasks = study_plan.get('daily_tasks', [])
    daily_hours = study_plan.get('daily_hours', 4)
    days_until_exam = study_plan.get('days_until_exam', 30)
    subjects = study_plan.get('subjects', [])
    
    # Basic metrics
    total_tasks = len(daily_tasks)
    completed_tasks = sum(1 for task in daily_tasks if task.get('completed', False))
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    # Time metrics
    total_study_hours = daily_hours * days_until_exam
    hours_per_subject = daily_hours / len(subjects) if subjects else 0
    
    # Subject metrics
    subject_completion = {}
    for task in daily_tasks:
        subject = task.get('subject', 'Unknown')
        if subject not in subject_completion:
            subject_completion[subject] = {'total': 0, 'completed': 0}
        subject_completion[subject]['total'] += 1
        if task.get('completed', False):
            subject_completion[subject]['completed'] += 1
    
    # Calculate average completion rate per subject
    avg_subject_completion = 0
    if subject_completion:
        completion_rates = [
            (data['completed'] / data['total'] * 100) 
            for data in subject_completion.values() 
            if data['total'] > 0
        ]
        avg_subject_completion = sum(completion_rates) / len(completion_rates) if completion_rates else 0
    
    metrics = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'completion_rate': completion_rate,
        'total_study_hours': total_study_hours,
        'hours_per_subject': hours_per_subject,
        'subject_count': len(subjects),
        'avg_subject_completion': avg_subject_completion,
        'daily_hours': daily_hours,
        'days_until_exam': days_until_exam
    }
    
    return metrics

def get_study_insights(metrics):
    """
    Generate insights based on study metrics
    
    Args:
        metrics (dict): Calculated study metrics
        
    Returns:
        list: List of insights
    """
    
    insights = []
    
    # Completion rate insights
    completion_rate = metrics.get('completion_rate', 0)
    if completion_rate >= 80:
        insights.append("🎉 Excellent progress! You're on track to achieve your goals.")
    elif completion_rate >= 60:
        insights.append("👍 Good progress! Keep up the consistent effort.")
    elif completion_rate >= 40:
        insights.append("📈 You're making progress. Consider increasing study consistency.")
    else:
        insights.append("⚠️ Progress is low. Let's create a more achievable study schedule.")
    
    # Time management insights
    daily_hours = metrics.get('daily_hours', 0)
    if daily_hours >= 6:
        insights.append("⏰ High study load! Remember to take regular breaks.")
    elif daily_hours <= 2:
        insights.append("📚 Consider increasing daily study hours for better coverage.")
    
    # Subject insights
    subject_count = metrics.get('subject_count', 0)
    if subject_count >= 5:
        insights.append("🎯 Many subjects! Focus on prioritizing high-importance topics.")
    elif subject_count <= 2:
        insights.append("🔍 Focused study approach. Dive deep into each subject.")
    
    return insights

def export_study_plan_csv(study_plan):
    """
    Export study plan to CSV format
    
    Args:
        study_plan (dict): Study plan data
        
    Returns:
        str: CSV string or error message
    """
    try:
        if not study_plan:
            return "Error: No study plan data available"
        
        # Create CSV data
        csv_data = []
        
        # Add daily tasks
        if 'daily_tasks' in study_plan:
            for task in study_plan['daily_tasks']:
                csv_data.append({
                    'Type': 'Task',
                    'Subject': task.get('subject', 'N/A'),
                    'Description': task.get('description', 'N/A'),
                    'Duration': task.get('duration', 0),
                    'Priority': task.get('priority', 'N/A'),
                    'Status': 'Completed' if task.get('completed', False) else 'Pending'
                })
        
        # Add daily activities
        if 'daily_schedule' in study_plan:
            for activity in study_plan['daily_schedule']:
                csv_data.append({
                    'Type': 'Activity',
                    'Time': activity.get('time', 'N/A'),
                    'Activity': activity.get('activity', 'N/A'),
                    'Category': activity.get('category', 'N/A'),
                    'Subject': activity.get('subject', 'N/A'),
                    'Description': activity.get('description', 'N/A')
                })
        
        # Add study tips
        if 'study_tips' in study_plan:
            for i, tip in enumerate(study_plan['study_tips'], 1):
                csv_data.append({
                    'Type': 'Tip',
                    'Number': f'Tip {i}',
                    'Content': tip
                })
        
        # Convert to DataFrame
        df = pd.DataFrame(csv_data)
        
        # Convert to CSV string
        return df.to_csv(index=False)
        
    except Exception as e:
        return f"Error exporting study plan: {str(e)}"
