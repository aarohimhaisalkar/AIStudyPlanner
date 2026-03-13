import json
import os
import csv
import io
from datetime import datetime, timedelta
import random
import hashlib

# Data storage file
USER_DATA_FILE = "user_data.json"

def load_user_data():
    """
    Load user data from JSON file
    
    Returns:
        dict: User data dictionary
    """
    
    try:
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, 'r') as f:
                return json.load(f)
        else:
            # Return default user data structure
            return create_default_user_data()
    except Exception as e:
        print(f"Error loading user data: {str(e)}")
        return create_default_user_data()

def save_user_data(user_data):
    """
    Save user data to JSON file
    
    Args:
        user_data (dict): User data to save
    """
    
    try:
        with open(USER_DATA_FILE, 'w') as f:
            json.dump(user_data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving user data: {str(e)}")
        return False

def create_default_user_data():
    """
    Create default user data structure
    
    Returns:
        dict: Default user data
    """
    
    return {
        "user_id": generate_user_id(),
        "created_at": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat(),
        "study_plans": [],
        "current_study_plan": None,
        "study_history": [],
        "preferences": {
            "theme": "light",
            "notifications": True,
            "reminder_time": "09:00",
            "study_preference": "Flexible"
        },
        "statistics": {
            "total_study_hours": 0,
            "total_tasks_completed": 0,
            "study_streak": 0,
            "longest_streak": 0,
            "subjects_studied": []
        }
    }

def generate_user_id():
    """
    Generate a unique user ID
    
    Returns:
        str: Unique user ID
    """
    
    timestamp = str(datetime.now().timestamp())
    random_num = str(random.randint(1000, 9999))
    return hashlib.md5((timestamp + random_num).encode()).hexdigest()[:12]

def get_motivational_quote():
    """
    Get a random motivational quote
    
    Returns:
        str: Motivational quote
    """
    
    quotes = [
        "The expert in anything was once a beginner. - Helen Hayes",
        "Success is the sum of small efforts repeated day in and day out. - Robert Collier",
        "Your future is created by what you do today, not tomorrow. - Robert T. Kiyosaki",
        "Education is the passport to the future, for tomorrow belongs to those who prepare for it today. - Malcolm X",
        "Believe you can and you're halfway there. - Theodore Roosevelt",
        "The beautiful thing about learning is that nobody can take it away from you. - B.B. King",
        "A person who never made a mistake never tried anything new. - Albert Einstein",
        "The capacity to learn is a gift; the ability to learn is a skill; the willingness to learn is a choice. - Brian Herbert",
        "Learning never exhausts the mind. - Leonardo da Vinci",
        "The more that you read, the more things you will know. - Dr. Seuss",
        "Education is not preparation for life; education is life itself. - John Dewey",
        "Live as if you were to die tomorrow. Learn as if you were to live forever. - Mahatma Gandhi",
        "The mind is not a vessel to be filled, but a fire to be kindled. - Plutarch",
        "Education's purpose is to replace an empty mind with an open one. - Malcolm Forbes",
        "The only person who is educated is the one who has learned how to learn and change. - Carl Rogers"
    ]
    
    return random.choice(quotes)

def export_study_plan_csv(study_plan):
    """
    Export study plan to CSV format
    
    Args:
        study_plan (dict): Study plan data
        
    Returns:
        str: CSV data as string
    """
    
    try:
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Subject', 'Task Description', 'Duration (hours)', 'Priority', 'Status', 'Time'])
        
        # Write tasks
        daily_tasks = study_plan.get('daily_tasks', [])
        for task in daily_tasks:
            status = 'Completed' if task.get('completed', False) else 'Pending'
            writer.writerow([
                task.get('subject', 'N/A'),
                task.get('description', 'N/A'),
                task.get('duration', 0),
                task.get('priority', 'Medium'),
                status,
                task.get('time', 'N/A')
            ])
        
        # Add study tips section
        writer.writerow([])
        writer.writerow(['Study Tips'])
        study_tips = study_plan.get('study_tips', [])
        for tip in study_tips:
            writer.writerow(['', tip])
        
        # Add metadata
        writer.writerow([])
        writer.writerow(['Study Plan Metadata'])
        writer.writerow(['Daily Hours', study_plan.get('daily_hours', 0)])
        writer.writerow(['Days Until Exam', study_plan.get('days_until_exam', 0)])
        writer.writerow(['Priority Level', study_plan.get('priority_level', 'Medium')])
        writer.writerow(['Difficulty Level', study_plan.get('difficulty_level', 'Intermediate')])
        writer.writerow(['Generated Date', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        
        return output.getvalue()
        
    except Exception as e:
        print(f"Error exporting CSV: {str(e)}")
        return "Error exporting study plan"

def calculate_study_progress(user_data):
    """
    Calculate overall study progress
    
    Args:
        user_data (dict): User data
        
    Returns:
        float: Progress percentage
    """
    
    try:
        current_plan = user_data.get('current_study_plan') or user_data.get('study_plan')
        
        if not current_plan:
            return 0.0
        
        daily_tasks = current_plan.get('daily_tasks', [])
        if not daily_tasks:
            return 0.0
        
        completed_tasks = sum(1 for task in daily_tasks if task.get('completed', False))
        total_tasks = len(daily_tasks)
        
        progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0.0
        return round(progress, 1)
        
    except Exception as e:
        print(f"Error calculating progress: {str(e)}")
        return 0.0

def format_duration(hours):
    """
    Format duration in hours to human-readable format
    
    Args:
        hours (float): Duration in hours
        
    Returns:
        str: Formatted duration
    """
    
    if hours >= 1:
        return f"{hours:.1f}h"
    else:
        minutes = int(hours * 60)
        return f"{minutes}m"

def get_priority_color(priority):
    """
    Get color for priority level
    
    Args:
        priority (str): Priority level
        
    Returns:
        str: Color code
    """
    
    priority_colors = {
        'Low': '#28a745',      # Green
        'Medium': '#ffc107',   # Yellow
        'High': '#fd7e14',     # Orange
        'Urgent': '#dc3545'    # Red
    }
    
    return priority_colors.get(priority, '#6c757d')  # Default gray

def validate_date_format(date_string):
    """
    Validate and parse date string
    
    Args:
        date_string (str): Date string to validate
        
    Returns:
        tuple: (is_valid, datetime_object or None)
    """
    
    try:
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        return True, date_obj
    except ValueError:
        try:
            # Try other common formats
            date_obj = datetime.strptime(date_string, '%Y/%m/%d')
            return True, date_obj
        except ValueError:
            return False, None

def calculate_study_statistics(user_data):
    """
    Calculate comprehensive study statistics
    
    Args:
        user_data (dict): User data
        
    Returns:
        dict: Study statistics
    """
    
    stats = {
        'total_tasks': 0,
        'completed_tasks': 0,
        'completion_rate': 0,
        'total_study_hours': 0,
        'subjects_count': 0,
        'study_streak': 0,
        'avg_daily_hours': 0
    }
    
    try:
        current_plan = user_data.get('current_study_plan') or user_data.get('study_plan')
        
        if current_plan:
            # Task statistics
            daily_tasks = current_plan.get('daily_tasks', [])
            stats['total_tasks'] = len(daily_tasks)
            stats['completed_tasks'] = sum(1 for task in daily_tasks if task.get('completed', False))
            stats['completion_rate'] = (stats['completed_tasks'] / stats['total_tasks'] * 100) if stats['total_tasks'] > 0 else 0
            
            # Time statistics
            daily_hours = current_plan.get('daily_hours', 0)
            days_until_exam = current_plan.get('days_until_exam', 0)
            stats['total_study_hours'] = daily_hours * days_until_exam
            stats['avg_daily_hours'] = daily_hours
            
            # Subject statistics
            subjects = current_plan.get('subjects', [])
            stats['subjects_count'] = len(subjects)
        
        # Study streak (simplified calculation)
        stats['study_streak'] = user_data.get('statistics', {}).get('study_streak', 0)
        
    except Exception as e:
        print(f"Error calculating statistics: {str(e)}")
    
    return stats

def create_study_reminder(user_data):
    """
    Create a study reminder message
    
    Args:
        user_data (dict): User data
        
    Returns:
        str: Reminder message
    """
    
    try:
        current_plan = user_data.get('current_study_plan') or user_data.get('study_plan')
        
        if not current_plan:
            return "No active study plan. Generate a study plan to get started!"
        
        # Get pending tasks
        daily_tasks = current_plan.get('daily_tasks', [])
        pending_tasks = [task for task in daily_tasks if not task.get('completed', False)]
        
        if not pending_tasks:
            return "🎉 Great job! All tasks for today are completed!"
        
        # Count tasks by subject
        subject_counts = {}
        for task in pending_tasks:
            subject = task.get('subject', 'Unknown')
            subject_counts[subject] = subject_counts.get(subject, 0) + 1
        
        # Create reminder message
        reminder = f"⏰ Study Reminder!\n\nYou have {len(pending_tasks)} tasks pending:\n"
        
        for subject, count in subject_counts.items():
            reminder += f"• {subject}: {count} task(s)\n"
        
        reminder += f"\nKeep up the great work! 💪"
        
        return reminder
        
    except Exception as e:
        print(f"Error creating reminder: {str(e)}")
        return "Error creating study reminder"

def backup_user_data(user_data):
    """
    Create a backup of user data
    
    Args:
        user_data (dict): User data to backup
        
    Returns:
        bool: Success status
    """
    
    try:
        # Create backup filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"user_data_backup_{timestamp}.json"
        
        # Save backup
        with open(backup_filename, 'w') as f:
            json.dump(user_data, f, indent=2)
        
        return True
        
    except Exception as e:
        print(f"Error creating backup: {str(e)}")
        return False

def restore_user_data(backup_filename):
    """
    Restore user data from backup
    
    Args:
        backup_filename (str): Backup file name
        
    Returns:
        dict: Restored user data or None if failed
    """
    
    try:
        if os.path.exists(backup_filename):
            with open(backup_filename, 'r') as f:
                return json.load(f)
        else:
            return None
            
    except Exception as e:
        print(f"Error restoring backup: {str(e)}")
        return None

def clean_old_backups(days_old=7):
    """
    Clean old backup files
    
    Args:
        days_old (int): Number of days to keep backups
    """
    
    try:
        current_time = datetime.now()
        
        for filename in os.listdir('.'):
            if filename.startswith('user_data_backup_') and filename.endswith('.json'):
                # Extract timestamp from filename
                timestamp_str = filename.replace('user_data_backup_', '').replace('.json', '')
                file_time = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                
                # Calculate age in days
                age_days = (current_time - file_time).days
                
                if age_days > days_old:
                    os.remove(filename)
                    print(f"Removed old backup: {filename}")
                    
    except Exception as e:
        print(f"Error cleaning backups: {str(e)}")

def get_study_recommendations(user_data):
    """
    Get personalized study recommendations
    
    Args:
        user_data (dict): User data
        
    Returns:
        list: List of recommendations
    """
    
    recommendations = []
    
    try:
        current_plan = user_data.get('current_study_plan') or user_data.get('study_plan')
        
        if not current_plan:
            recommendations.append("Start by generating a personalized study plan!")
            return recommendations
        
        # Analyze completion rates
        stats = calculate_study_statistics(user_data)
        completion_rate = stats['completion_rate']
        
        if completion_rate < 30:
            recommendations.append("Consider reducing daily study goals to build consistency")
        elif completion_rate > 90:
            recommendations.append("Excellent progress! You might be ready for advanced topics")
        
        # Analyze study hours
        daily_hours = stats['avg_daily_hours']
        if daily_hours > 6:
            recommendations.append("High study load detected! Remember to take regular breaks")
        elif daily_hours < 2:
            recommendations.append("Consider increasing daily study hours for better coverage")
        
        # Subject-specific recommendations
        daily_tasks = current_plan.get('daily_tasks', [])
        subject_progress = {}
        
        for task in daily_tasks:
            subject = task.get('subject', 'Unknown')
            if subject not in subject_progress:
                subject_progress[subject] = {'total': 0, 'completed': 0}
            subject_progress[subject]['total'] += 1
            if task.get('completed', False):
                subject_progress[subject]['completed'] += 1
        
        for subject, progress in subject_progress.items():
            rate = progress['completed'] / progress['total'] if progress['total'] > 0 else 0
            if rate < 0.3:
                recommendations.append(f"Focus more on {subject} - it needs more attention")
        
        # General recommendations
        if completion_rate > 50:
            recommendations.append("Great progress! Keep maintaining your study routine")
        
    except Exception as e:
        print(f"Error generating recommendations: {str(e)}")
        recommendations.append("Continue with your current study plan")
    
    return recommendations

def format_time_remaining(exam_date):
    """
    Format time remaining until exam
    
    Args:
        exam_date (str): Exam date in YYYY-MM-DD format
        
    Returns:
        str: Formatted time remaining
    """
    
    try:
        exam_datetime = datetime.strptime(exam_date, '%Y-%m-%d')
        current_datetime = datetime.now()
        
        if exam_datetime <= current_datetime:
            return "Exam date has passed"
        
        delta = exam_datetime - current_datetime
        days = delta.days
        
        if days == 0:
            return "Exam is today!"
        elif days == 1:
            return "Exam is tomorrow!"
        elif days <= 7:
            return f"{days} days until exam"
        elif days <= 30:
            weeks = days // 7
            remaining_days = days % 7
            if remaining_days > 0:
                return f"{weeks} week{'' if weeks == 1 else 's'}, {remaining_days} days until exam"
            else:
                return f"{weeks} week{'' if weeks == 1 else 's'} until exam"
        else:
            months = days // 30
            remaining_days = days % 30
            if remaining_days > 0:
                return f"{months} month{'' if months == 1 else 's'}, {remaining_days} days until exam"
            else:
                return f"{months} month{'' if months == 1 else 's'} until exam"
                
    except Exception as e:
        print(f"Error formatting time remaining: {str(e)}")
        return "Invalid date format"

def create_study_summary(user_data):
    """
    Create a comprehensive study summary
    
    Args:
        user_data (dict): User data
        
    Returns:
        dict: Study summary
    """
    
    summary = {
        'overview': {},
        'progress': {},
        'recommendations': [],
        'next_steps': []
    }
    
    try:
        current_plan = user_data.get('current_study_plan') or user_data.get('study_plan')
        
        if current_plan:
            # Overview
            summary['overview'] = {
                'subjects': current_plan.get('subjects', []),
                'daily_hours': current_plan.get('daily_hours', 0),
                'days_until_exam': current_plan.get('days_until_exam', 0),
                'priority_level': current_plan.get('priority_level', 'Medium'),
                'difficulty_level': current_plan.get('difficulty_level', 'Intermediate')
            }
            
            # Progress
            stats = calculate_study_statistics(user_data)
            summary['progress'] = stats
            
            # Recommendations
            summary['recommendations'] = get_study_recommendations(user_data)
            
            # Next steps
            daily_tasks = current_plan.get('daily_tasks', [])
            pending_tasks = [task for task in daily_tasks if not task.get('completed', False)]
            
            if pending_tasks:
                summary['next_steps'] = pending_tasks[:3]  # Top 3 pending tasks
            else:
                summary['next_steps'] = ["All tasks completed! Great job!"]
        
    except Exception as e:
        print(f"Error creating summary: {str(e)}")
    
    return summary
