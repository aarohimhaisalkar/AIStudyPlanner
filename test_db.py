#!/usr/bin/env python3
"""Test database operations"""

from database import db_manager

try:
    print("🧪 Testing database operations...")
    
    # Test creating a user
    print("\n👤 Creating test user...")
    user = db_manager.create_user("testuser", "test@example.com")
    print(f"✅ User created: ID={user.id}, Username={user.username}")
    
    # Test creating a study plan
    print("\n📚 Creating test study plan...")
    plan_data = {
        'subjects': ['Math', 'Science'],
        'daily_hours': 4,
        'exam_date': '2026-06-01',
        'days_until_exam': 30,
        'priority_level': 'High',
        'difficulty_level': 'Intermediate',
        'study_preference': 'Morning',
        'sleep_hours': 8,
        'meal_time': 2,
        'play_time': 1,
        'exercise_time': 0.5,
        'personal_time': 1,
        'screen_time_limit': 2
    }
    
    study_plan = db_manager.save_study_plan(user.id, plan_data, "Test Study Plan")
    print(f"✅ Study plan created: ID={study_plan.id}, Name={study_plan.plan_name}")
    
    # Test updating progress
    print("\n📈 Testing progress update...")
    progress = db_manager.update_progress(user.id, study_plan.id, "task_1", True)
    print(f"✅ Progress updated: Task={progress.task_id}, Completed={progress.completed}")
    
    print("\n🎉 All database operations successful!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
