"""
PostgreSQL Database Configuration and Management for AI Study Planner
"""

import os
import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.sql import func

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///study_planner.db")

# Create database engine with SQLite-specific settings
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get database session
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    preferences = Column(Text)  # JSON string for user preferences
    
    # Relationship with study plans
    study_plans = relationship("StudyPlan", back_populates="user")

class StudyPlan(Base):
    __tablename__ = "study_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_name = Column(String(100), nullable=False)
    subjects = Column(Text, nullable=False)  # JSON string
    daily_hours = Column(Float, nullable=False)
    exam_date = Column(String(20), nullable=False)
    days_until_exam = Column(Integer, nullable=False)
    priority_level = Column(String(20), nullable=False)
    difficulty_level = Column(String(20), nullable=False)
    study_preference = Column(String(20), nullable=False)
    
    # Daily Activities
    sleep_hours = Column(Float, nullable=False)
    meal_time = Column(Float, nullable=False)
    play_time = Column(Float, nullable=False)
    exercise_time = Column(Float, nullable=False)
    personal_time = Column(Float, nullable=False)
    screen_time_limit = Column(Float, nullable=False)
    
    # Additional preferences
    include_breaks = Column(Boolean, default=True)
    include_revision = Column(Boolean, default=True)
    include_tests = Column(Boolean, default=False)
    flexible_schedule = Column(Boolean, default=True)
    
    # Plan data (full JSON response from AI)
    plan_data = Column(Text, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationship with user
    user = relationship("User", back_populates="study_plans")
    
    # Relationship with progress
    progress_entries = relationship("Progress", back_populates="study_plan")

class Progress(Base):
    __tablename__ = "progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("study_plans.id"), nullable=False)
    task_id = Column(String(100), nullable=False)  # Task identifier
    task_description = Column(Text, nullable=False)
    completed = Column(Boolean, default=False)
    completion_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    study_plan = relationship("StudyPlan", back_populates="progress_entries")

# Database Operations
class DatabaseManager:
    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal
    
    def create_tables(self):
        """Create all database tables"""
        Base.metadata.create_all(bind=self.engine)
        print("✅ Database tables created successfully!")
    
    def get_session(self) -> Session:
        """Get a new database session"""
        return self.SessionLocal()
    
    # User Operations
    def create_user(self, username: str, email: str, preferences: Optional[Dict] = None) -> User:
        """Create a new user"""
        session = self.get_session()
        try:
            user = User(
                username=username,
                email=email,
                preferences=json.dumps(preferences) if preferences else "{}"
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        session = self.get_session()
        try:
            user = session.query(User).filter(User.username == username).first()
            if user:
                # Detach the user from session to prevent errors after session closes
                session.expunge(user)
            return user
        finally:
            session.close()
    
    # Study Plan Operations
    def save_study_plan(self, user_id: int, plan_data: Dict, plan_name: str = "My Study Plan") -> StudyPlan:
        """Save a study plan for a user"""
        session = self.get_session()
        try:
            study_plan = StudyPlan(
                user_id=user_id,
                plan_name=plan_name,
                subjects=json.dumps(plan_data.get('subjects', [])),
                daily_hours=plan_data.get('daily_hours', 4),
                exam_date=plan_data.get('exam_date', ''),
                days_until_exam=plan_data.get('days_until_exam', 30),
                priority_level=plan_data.get('priority_level', 'Medium'),
                difficulty_level=plan_data.get('difficulty_level', 'Intermediate'),
                study_preference=plan_data.get('study_preference', 'Flexible'),
                
                # Daily activities
                sleep_hours=plan_data.get('sleep_hours', 8),
                meal_time=plan_data.get('meal_time', 2),
                play_time=plan_data.get('play_time', 1),
                exercise_time=plan_data.get('exercise_time', 0.5),
                personal_time=plan_data.get('personal_time', 1),
                screen_time_limit=plan_data.get('screen_time_limit', 2),
                
                # Additional preferences
                include_breaks=plan_data.get('include_breaks', True),
                include_revision=plan_data.get('include_revision', True),
                include_tests=plan_data.get('include_tests', False),
                flexible_schedule=plan_data.get('flexible_schedule', True),
                
                # Full plan data
                plan_data=json.dumps(plan_data)
            )
            session.add(study_plan)
            session.commit()
            session.refresh(study_plan)
            return study_plan
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_user_study_plans(self, user_id: int) -> List[StudyPlan]:
        """Get all study plans for a user"""
        session = self.get_session()
        try:
            return session.query(StudyPlan).filter(StudyPlan.user_id == user_id).all()
        finally:
            session.close()
    
    def get_latest_study_plan(self, user_id: int) -> Optional[StudyPlan]:
        """Get the latest study plan for a user"""
        session = self.get_session()
        try:
            return session.query(StudyPlan).filter(StudyPlan.user_id == user_id).order_by(StudyPlan.created_at.desc()).first()
        finally:
            session.close()
    
    def update_progress(self, user_id: int, plan_id: int, task_id: str, completed: bool) -> Progress:
        """Update task completion status"""
        session = self.get_session()
        try:
            # Check if progress entry exists
            progress = session.query(Progress).filter(
                Progress.user_id == user_id,
                Progress.plan_id == plan_id,
                Progress.task_id == task_id
            ).first()
            
            if progress:
                progress.completed = completed
                if completed:
                    progress.completion_date = datetime.now()
                else:
                    progress.completion_date = None
            else:
                # Create new progress entry
                progress = Progress(
                    user_id=user_id,
                    plan_id=plan_id,
                    task_id=task_id,
                    completed=completed,
                    completion_date=datetime.now() if completed else None
                )
                session.add(progress)
            
            session.commit()
            return progress
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_user_progress(self, user_id: int, plan_id: int) -> List[Progress]:
        """Get all progress for a user's study plan"""
        session = self.get_session()
        try:
            return session.query(Progress).filter(
                Progress.user_id == user_id,
                Progress.plan_id == plan_id
            ).all()
        finally:
            session.close()
    
    def get_progress_stats(self, user_id: int, plan_id: int) -> Dict[str, Any]:
        """Get progress statistics for a study plan"""
        session = self.get_session()
        try:
            total_tasks = session.query(Progress).filter(
                Progress.user_id == user_id,
                Progress.plan_id == plan_id
            ).count()
            
            completed_tasks = session.query(Progress).filter(
                Progress.user_id == user_id,
                Progress.plan_id == plan_id,
                Progress.completed == True
            ).count()
            
            return {
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'completion_percentage': (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            }
        finally:
            session.close()

# Initialize database manager
db_manager = DatabaseManager()

# Initialize database on import
def init_database():
    """Initialize database tables"""
    try:
        db_manager.create_tables()
        print("🗄️ PostgreSQL database initialized successfully!")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        print("🔧 Please check your DATABASE_URL in .env file")
        raise e
