import openai
import os
from datetime import datetime, timedelta
import json
import random
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key and validate it
api_key = os.getenv("OPENAI_API_KEY")
if not api_key or api_key == "your_openai_api_key_here":
    print("⚠️ Warning: Invalid OpenAI API key. Please update your .env file.")
    print("📝 Instructions:")
    print("1. Get your API key from: https://platform.openai.com/account/api-keys")
    print("2. Edit the .env file")
    print("3. Replace 'your_openai_api_key_here' with your actual API key")
    client = None
else:
    # Set OpenAI API key from environment variable
    client = openai.OpenAI(api_key=api_key)

def init_openai_client():
    """Initialize OpenAI client - called from app_db.py"""
    # This function exists for compatibility with app_db.py imports
    pass

def generate_mock_study_plan(user_input):
    """Generate a mock study plan for testing when API is unavailable"""
    subjects = user_input.get('subjects', ['Mathematics'])
    daily_hours = user_input.get('daily_hours', 4)
    days_until = user_input.get('days_until_exam', 30)
    
    # Daily activities
    sleep_hours = user_input.get('sleep_hours', 8)
    meal_time = user_input.get('meal_time', 2)
    play_time = user_input.get('play_time', 1)
    exercise_time = user_input.get('exercise_time', 0.5)
    personal_time = user_input.get('personal_time', 1)
    
    result = {
        'daily_schedule': [
            {
                'time': '06:00 - 06:30',
                'activity': 'Wake up & Morning Routine',
                'category': 'Personal',
                'description': 'Start the day fresh'
            },
            {
                'time': '06:30 - 07:00',
                'activity': 'Exercise',
                'category': 'Health',
                'description': 'Physical activity for energy'
            },
            {
                'time': '07:00 - 08:00',
                'activity': 'Breakfast',
                'category': 'Meal',
                'description': 'Healthy breakfast to fuel the brain'
            },
            {
                'time': '09:00 - 10:30',
                'subject': subjects[0] if subjects else 'Mathematics',
                'topic': 'Study Session 1',
                'activity': 'Study new concepts',
                'category': 'Study'
            },
            {
                'time': '12:30 - 13:30',
                'activity': 'Lunch',
                'category': 'Meal',
                'description': 'Midday meal break'
            },
            {
                'time': '14:00 - 16:00',
                'subject': subjects[1] if len(subjects) > 1 else subjects[0],
                'topic': 'Study Session 2',
                'activity': 'Practice problems',
                'category': 'Study'
            },
            {
                'time': '16:00 - 17:00',
                'activity': 'Leisure Time',
                'category': 'Leisure',
                'description': 'Relax and recharge'
            },
            {
                'time': '19:00 - 20:00',
                'activity': 'Dinner',
                'category': 'Meal',
                'description': 'Evening meal'
            },
            {
                'time': '20:00 - 21:00',
                'activity': 'Personal Time',
                'category': 'Personal',
                'description': 'Hobbies and relaxation'
            },
            {
                'time': '22:00 - 06:00',
                'activity': 'Sleep',
                'category': 'Personal',
                'description': f'Rest for {sleep_hours} hours'
            }
        ],
        'daily_tasks': [],
        'study_tips': [
            "Use the Pomodoro technique for better focus",
            "Schedule study sessions during your peak energy hours",
            "Take regular breaks to maintain concentration",
            f"Get {sleep_hours} hours of sleep for optimal learning"
        ],
        'break_schedule': [
            {
                'time': '10:30 - 10:45',
                'activity': 'Short break and stretch'
            },
            {
                'time': '15:30 - 15:45',
                'activity': 'Quick walk and refresh'
            }
        ],
        'subjects': subjects,
        'daily_hours': daily_hours,
        'days_until_exam': days_until,
        'sleep_hours': sleep_hours,
        'meal_time': meal_time,
        'play_time': play_time,
        'exercise_time': exercise_time,
        'personal_time': personal_time
    }
    
    # Generate tasks for each subject
    hours_per_subject = daily_hours / max(len(subjects), 1)
    current_time = 9.0
    
    for i, subject in enumerate(subjects):
        task = {
            'subject': subject,
            'description': f'Complete {subject} exercises and review concepts',
            'duration': round(hours_per_subject, 1),
            'priority': 'High' if i == 0 else 'Medium',
            'completed': False,
            'category': 'Study',
            'time': f"{int(current_time):02d}:00 - {int(current_time + hours_per_subject):02d}:00"
        }
        result['daily_tasks'].append(task)
        current_time += hours_per_subject
    
    return result

def generate_study_plan(user_input):
    """
    Generate a personalized study plan using OpenAI API
    
    Args:
        user_input (dict): Dictionary containing user preferences and constraints
        
    Returns:
        dict: Generated study plan with daily tasks and recommendations
    """
    
    # If no API client available, use mock mode
    if not client:
        print("🧪 Using mock mode - API client not available")
        return generate_mock_study_plan(user_input)
    
    # Validate OpenAI API key
    if not client:
        raise ValueError("OpenAI API key not configured. Please update your .env file with a valid API key.")
    
    # Construct the prompt for AI
    prompt = create_study_plan_prompt(user_input)
    
    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert study planner and educational consultant. Create comprehensive, realistic study plans that balance academic goals with student wellbeing."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        # Parse the response
        plan_text = response.choices[0].message.content
        
        # Try to parse as JSON
        try:
            study_plan = json.loads(plan_text)
            return study_plan
        except json.JSONDecodeError:
            # If JSON parsing fails, create a basic plan
            print("⚠️ JSON parsing failed, creating basic plan")
            return generate_mock_study_plan(user_input)
            
    except Exception as e:
        # Handle API errors gracefully
        error_message = str(e)
        if "429" in error_message or "quota" in error_message.lower():
            print("🚫 API quota exceeded, using mock mode")
            return generate_mock_study_plan(user_input)
        elif "401" in error_message or "invalid_api_key" in error_message.lower():
            print("❌ Invalid API key, using mock mode")
            return generate_mock_study_plan(user_input)
        else:
            print(f"⚠️ API error: {e}, using mock mode")
            return generate_mock_study_plan(user_input)

def create_study_plan_prompt(user_input):
    """
    Create a detailed prompt for the AI based on user input
    
    Args:
        user_input (dict): User preferences and constraints
        
    Returns:
        str: Formatted prompt for OpenAI API
    """
    
    subjects = user_input.get('subjects', [])
    daily_hours = user_input.get('daily_hours', 4)
    exam_date = user_input.get('exam_date', '')
    days_until = user_input.get('days_until_exam', 30)
    priority = user_input.get('priority_level', 'Medium')
    difficulty = user_input.get('difficulty_level', 'Intermediate')
    preference = user_input.get('study_preference', 'Flexible')
    include_breaks = user_input.get('include_breaks', True)
    include_revision = user_input.get('include_revision', True)
    include_tests = user_input.get('include_tests', False)
    flexible = user_input.get('flexible_schedule', True)
    
    # Daily Activities
    sleep_hours = user_input.get('sleep_hours', 8)
    meal_time = user_input.get('meal_time', 2)
    play_time = user_input.get('play_time', 1)
    exercise_time = user_input.get('exercise_time', 0.5)
    personal_time = user_input.get('personal_time', 1)
    screen_time_limit = user_input.get('screen_time_limit', 2)
    
    # Calculate total daily hours
    total_activity_hours = sleep_hours + meal_time + play_time + exercise_time + personal_time + daily_hours
    remaining_hours = 24 - total_activity_hours
    
    prompt = f"""
Create a comprehensive DAILY LIFESTYLE AND STUDY PLAN for a student with the following details:

ACADEMIC DETAILS:
SUBJECTS: {', '.join(subjects)}
DAILY STUDY HOURS: {daily_hours} hours
EXAM DATE: {exam_date}
DAYS UNTIL EXAM: {days_until} days
PRIORITY LEVEL: {priority}
DIFFICULTY LEVEL: {difficulty}
STUDY PREFERENCE: {preference}

DAILY ACTIVITIES:
SLEEP HOURS: {sleep_hours} hours
MEAL TIME: {meal_time} hours
PLAY/LEISURE TIME: {play_time} hours
EXERCISE TIME: {exercise_time} hours
PERSONAL TIME: {personal_time} hours
SCREEN TIME LIMIT: {screen_time_limit} hours
TOTAL SCHEDULED HOURS: {total_activity_hours} hours
FREE TIME: {remaining_hours:.1f} hours

STUDY OPTIONS:
INCLUDE BREAKS: {include_breaks}
INCLUDE REVISION SESSIONS: {include_revision}
INCLUDE PRACTICE TESTS: {include_tests}
FLEXIBLE SCHEDULING: {flexible}

Please provide a COMPLETE DAILY SCHEDULE that includes:
1. HOURLY TIMELINE from morning to night
2. STUDY SESSIONS with subjects and topics
3. MEAL TIMES (breakfast, lunch, dinner)
4. SLEEP SCHEDULE
5. EXERCISE/PHYSICAL ACTIVITY
6. LEISURE/PLAY TIME
7. PERSONAL TIME for hobbies/relaxation
8. SCREEN TIME management
9. Study tips and strategies
10. Break recommendations
6. Practice test schedule (if requested)

Format your response as JSON with the following structure:
{{
    "daily_schedule": [
        {{
            "time": "06:00 - 06:30",
            "activity": "Wake up & Morning Routine",
            "category": "Personal",
            "description": "Start the day fresh"
        }},
        {{
            "time": "06:30 - 07:00",
            "activity": "Exercise",
            "category": "Health",
            "description": "Physical activity for energy"
        }},
        {{
            "time": "07:00 - 08:00",
            "activity": "Breakfast",
            "category": "Meal",
            "description": "Healthy breakfast to fuel the brain"
        }},
        {{
            "time": "09:00 - 10:30",
            "subject": "Mathematics",
            "topic": "Calculus - Derivatives",
            "activity": "Study new concepts",
            "category": "Study"
        }}
    ],
    "daily_tasks": [
        {{
            "subject": "Mathematics",
            "description": "Complete calculus exercises",
            "duration": 1.5,
            "priority": "High",
            "completed": false,
            "category": "Study"
        }}
    ],
    "daily_activities": {{
        "sleep_schedule": {{
            "bedtime": "22:00",
            "wake_time": "06:00",
            "total_hours": {sleep_hours}
        }},
        "meal_times": [
            {{
                "meal": "Breakfast",
                "time": "07:00 - 08:00",
                "duration": 1
            }},
            {{
                "meal": "Lunch", 
                "time": "12:30 - 13:30",
                "duration": 1
            }},
            {{
                "meal": "Dinner",
                "time": "19:00 - 20:00", 
                "duration": 1
            }}
        ],
        "exercise": {{
            "time": "06:30 - 07:00",
            "duration": {exercise_time},
            "type": "Morning workout"
        }},
        "leisure_time": {{
            "time": "16:00 - 17:00",
            "duration": {play_time},
            "activities": ["Games", "Hobbies", "Relaxation"]
        }},
        "personal_time": {{
            "time": "20:00 - 21:00",
            "duration": {personal_time},
            "activities": ["Reading", "Meditation", "Hobbies"]
        }}
    }},
    "study_tips": [
        "Use the Pomodoro technique for better focus",
        "Schedule study sessions during your peak energy hours",
        "Take regular breaks to maintain concentration"
    ],
    "break_schedule": [
        {{
            "time": "10:30 - 10:45",
            "activity": "Short break and stretch"
        }}
    ],
    "revision_topics": [
        {{
            "subject": "Mathematics",
            "topics": ["Algebra", "Geometry"],
            "schedule": "Every Sunday"
        }}
    ],
    "practice_tests": [
        {{
            "subject": "Mathematics",
            "date": "2024-01-15",
            "topics": ["Calculus", "Algebra"]
        }}
    ]
}}

Make the plan realistic, achievable, and motivational. Consider the student's preferences and constraints.
"""
    
    return prompt

def parse_ai_response(ai_response, user_input):
    """
    Parse the AI response into a structured study plan
    
    Args:
        ai_response (str): Raw response from OpenAI API
        user_input (dict): Original user input
        
    Returns:
        dict: Parsed study plan
    """
    
    try:
        # Try to parse as JSON first
        if ai_response.strip().startswith('{'):
            study_plan = json.loads(ai_response)
        else:
            # Extract JSON from the response if it's embedded
            start_idx = ai_response.find('{')
            end_idx = ai_response.rfind('}') + 1
            if start_idx != -1 and end_idx != -1:
                json_str = ai_response[start_idx:end_idx]
                study_plan = json.loads(json_str)
            else:
                # Fallback: create basic structure from text
                study_plan = create_plan_from_text(ai_response, user_input)
    
    except json.JSONDecodeError:
        # If JSON parsing fails, create a basic plan
        study_plan = create_fallback_study_plan(user_input)
    
    # Ensure all required fields exist
    study_plan = ensure_plan_structure(study_plan, user_input)
    
    return study_plan

def create_fallback_study_plan(user_input):
    """
    Create a basic study plan when AI generation fails
    
    Args:
        user_input (dict): User preferences and constraints
        
    Returns:
        dict: Basic study plan
    """
    
    subjects = user_input.get('subjects', [])
    daily_hours = user_input.get('daily_hours', 4)
    days_until = user_input.get('days_until_exam', 30)
    
    # Calculate hours per subject
    hours_per_subject = daily_hours / max(len(subjects), 1)
    
    # Generate basic daily tasks
    daily_tasks = []
    current_time = 9.0  # Start at 9 AM
    
    for subject in subjects:
        task = {
            "subject": subject,
            "description": f"Study {subject} concepts and practice problems",
            "duration": round(hours_per_subject, 1),
            "priority": user_input.get('priority_level', 'Medium'),
            "completed": False,
            "time": f"{int(current_time):02d}:00 - {int(current_time + hours_per_subject):02d}:00"
        }
        daily_tasks.append(task)
        current_time += hours_per_subject
    
    # Basic study tips
    study_tips = [
        "Take regular breaks every 45-60 minutes",
        "Review your notes at the end of each study session",
        "Practice active recall instead of passive reading",
        "Stay hydrated and maintain good posture",
        "Use flashcards for key concepts"
    ]
    
    study_plan = {
        "daily_tasks": daily_tasks,
        "study_tips": study_tips,
        "subjects": subjects,
        "daily_hours": daily_hours,
        "days_until_exam": days_until,
        "priority_level": user_input.get('priority_level', 'Medium'),
        "difficulty_level": user_input.get('difficulty_level', 'Intermediate')
    }
    
    return study_plan

def create_plan_from_text(ai_response, user_input):
    """
    Create a study plan from text response when JSON parsing fails
    
    Args:
        ai_response (str): Text response from AI
        user_input (dict): User input data
        
    Returns:
        dict: Structured study plan
    """
    
    subjects = user_input.get('subjects', [])
    daily_hours = user_input.get('daily_hours', 4)
    
    # Extract tasks from text (basic implementation)
    daily_tasks = []
    for subject in subjects:
        task = {
            "subject": subject,
            "description": f"Study {subject} as per AI recommendations",
            "duration": daily_hours / len(subjects),
            "priority": user_input.get('priority_level', 'Medium'),
            "completed": False
        }
        daily_tasks.append(task)
    
    # Extract tips from text
    study_tips = [
        "Follow the AI-generated recommendations",
        "Maintain consistent study schedule",
        "Review regularly for better retention"
    ]
    
    return {
        "daily_tasks": daily_tasks,
        "study_tips": study_tips,
        "subjects": subjects,
        "daily_hours": daily_hours
    }

def ensure_plan_structure(study_plan, user_input):
    """
    Ensure the study plan has all required fields
    
    Args:
        study_plan (dict): Current study plan
        user_input (dict): User input data
        
    Returns:
        dict: Complete study plan
    """
    
    # Required fields with defaults
    required_fields = {
        "daily_tasks": [],
        "study_tips": [],
        "subjects": user_input.get('subjects', []),
        "daily_hours": user_input.get('daily_hours', 4),
        "days_until_exam": user_input.get('days_until_exam', 30),
        "priority_level": user_input.get('priority_level', 'Medium'),
        "difficulty_level": user_input.get('difficulty_level', 'Intermediate'),
        "break_schedule": [],
        "revision_topics": [],
        "practice_tests": []
    }
    
    # Add missing fields
    for field, default_value in required_fields.items():
        if field not in study_plan:
            study_plan[field] = default_value
    
    # Ensure tasks have required fields
    for task in study_plan.get('daily_tasks', []):
        if 'completed' not in task:
            task['completed'] = False
        if 'priority' not in task:
            task['priority'] = user_input.get('priority_level', 'Medium')
        if 'duration' not in task:
            task['duration'] = 1.0
    
    return study_plan

def enhance_study_plan(study_plan, user_input):
    """
    Add additional features to the study plan
    
    Args:
        study_plan (dict): Current study plan
        user_input (dict): User input data
        
    Returns:
        dict: Enhanced study plan
    """
    
    # Add motivational quotes
    motivational_quotes = [
        "Success is the sum of small efforts repeated day in and day out.",
        "The expert in anything was once a beginner.",
        "Your future is created by what you do today, not tomorrow.",
        "Education is the passport to the future.",
        "Believe you can and you're halfway there."
    ]
    
    if 'motivational_quotes' not in study_plan:
        study_plan['motivational_quotes'] = random.sample(motivational_quotes, 3)
    
    # Add productivity tips
    productivity_tips = [
        "Use the Pomodoro Technique: 25 minutes of focused study followed by a 5-minute break.",
        "Create a dedicated study space free from distractions.",
        "Set specific, measurable goals for each study session.",
        "Review material within 24 hours for better retention.",
        "Teach concepts to others to reinforce your understanding."
    ]
    
    if 'productivity_tips' not in study_plan:
        study_plan['productivity_tips'] = productivity_tips
    
    # Add weekly schedule if not present
    if 'weekly_schedule' not in study_plan:
        study_plan['weekly_schedule'] = generate_weekly_schedule(study_plan, user_input)
    
    # Add milestones
    if 'milestones' not in study_plan:
        study_plan['milestones'] = generate_milestones(study_plan, user_input)
    
    return study_plan

def generate_weekly_schedule(study_plan, user_input):
    """
    Generate a weekly study schedule
    
    Args:
        study_plan (dict): Current study plan
        user_input (dict): User input data
        
    Returns:
        list: Weekly schedule
    """
    
    subjects = study_plan.get('subjects', [])
    daily_hours = study_plan.get('daily_hours', 4)
    
    weekly_schedule = []
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    for day in days:
        day_schedule = {
            'day': day,
            'tasks': [],
            'total_hours': daily_hours
        }
        
        # Distribute subjects throughout the week
        for i, subject in enumerate(subjects):
            if i < len(subjects):
                task = {
                    'subject': subject,
                    'duration': daily_hours / len(subjects),
                    'time': f"{9 + i * 2}:00 - {9 + i * 2 + 2}:00"
                }
                day_schedule['tasks'].append(task)
        
        weekly_schedule.append(day_schedule)
    
    return weekly_schedule

def generate_milestones(study_plan, user_input):
    """
    Generate study milestones
    
    Args:
        study_plan (dict): Current study plan
        user_input (dict): User input data
        
    Returns:
        list: Study milestones
    """
    
    days_until = user_input.get('days_until_exam', 30)
    subjects = study_plan.get('subjects', [])
    
    milestones = []
    
    # Create milestones at 25%, 50%, 75%, and 100% completion
    milestone_points = [0.25, 0.5, 0.75, 1.0]
    
    for point in milestone_points:
        days_to_milestone = int(days_until * point)
        milestone = {
            'name': f"{int(point * 100)}% Study Complete",
            'target_date': f"Day {days_to_milestone}",
            'description': f"Complete {int(point * 100)}% of study material",
            'subjects_covered': subjects[:int(len(subjects) * point)]
        }
        milestones.append(milestone)
    
    return milestones

def validate_study_plan(study_plan):
    """
    Validate the generated study plan
    
    Args:
        study_plan (dict): Study plan to validate
        
    Returns:
        tuple: (is_valid, error_message)
    """
    
    required_fields = ['daily_tasks', 'subjects', 'daily_hours']
    
    for field in required_fields:
        if field not in study_plan:
            return False, f"Missing required field: {field}"
    
    if not study_plan['daily_tasks']:
        return False, "No daily tasks generated"
    
    if not study_plan['subjects']:
        return False, "No subjects specified"
    
    if study_plan['daily_hours'] <= 0:
        return False, "Daily hours must be greater than 0"
    
    return True, "Study plan is valid"

def get_study_recommendations(study_plan, user_progress):
    """
    Get personalized study recommendations based on progress
    
    Args:
        study_plan (dict): Current study plan
        user_progress (dict): User's progress data
        
    Returns:
        list: Personalized recommendations
    """
    
    recommendations = []
    
    # Analyze completion rates
    completed_tasks = sum(1 for task in study_plan.get('daily_tasks', []) if task.get('completed', False))
    total_tasks = len(study_plan.get('daily_tasks', []))
    completion_rate = completed_tasks / total_tasks if total_tasks > 0 else 0
    
    if completion_rate < 0.5:
        recommendations.append("Consider reducing daily study hours to maintain consistency")
    elif completion_rate > 0.9:
        recommendations.append("Great progress! You might be ready for advanced topics")
    
    # Subject-specific recommendations
    subject_progress = {}
    for task in study_plan.get('daily_tasks', []):
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
        elif rate > 0.8:
            recommendations.append(f"Excellent progress in {subject}! Consider advanced topics")
    
    return recommendations
