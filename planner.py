from datetime import datetime, timedelta
import random
from typing import Dict, List, Any

class StudyPlanner:
    """
    Smart Study Plan Generator that creates personalized study schedules
    based on user inputs and difficulty levels.
    """
    
    def __init__(self):
        self.difficulty_multipliers = {
            "Easy": 1.2,
            "Medium": 1.0,
            "Hard": 0.8
        }
        
        self.topic_templates = {
            "Mathematics": [
                "Algebra Basics", "Linear Equations", "Quadratic Equations", "Geometry Fundamentals",
                "Trigonometry", "Calculus Introduction", "Statistics Basics", "Probability Theory",
                "Advanced Algebra", "Coordinate Geometry", "Differential Calculus", "Integral Calculus"
            ],
            "Physics": [
                "Mechanics Basics", "Newton's Laws", "Work and Energy", "Momentum and Collisions",
                "Rotational Motion", "Gravitation", "Fluid Mechanics", "Thermodynamics",
                "Oscillations", "Waves", "Electrostatics", "Current Electricity"
            ],
            "Chemistry": [
                "Atomic Structure", "Chemical Bonding", "Periodic Table", "Chemical Reactions",
                "Acids and Bases", "Redox Reactions", "Organic Chemistry Basics", "Hydrocarbons",
                "Solutions", "Chemical Kinetics", "Thermodynamics", "Equilibrium"
            ],
            "Biology": [
                "Cell Biology", "Genetics Basics", "Evolution Theory", "Ecology",
                "Human Anatomy", "Physiology", "Plant Biology", "Microbiology",
                "Biochemistry", "Molecular Biology", "Biotechnology", "Environmental Science"
            ],
            "Computer Science": [
                "Programming Basics", "Data Structures", "Algorithms", "Database Management",
                "Web Development", "Machine Learning Basics", "Artificial Intelligence", "Cybersecurity",
                "Software Engineering", "Computer Networks", "Operating Systems", "Cloud Computing"
            ],
            "History": [
                "Ancient Civilizations", "Medieval Period", "Renaissance", "Industrial Revolution",
                "World Wars", "Cold War", "Modern History", "Cultural History",
                "Economic History", "Political History", "Social History", "Military History"
            ],
            "Literature": [
                "Poetry Analysis", "Novel Studies", "Drama and Theatre", "Literary Theory",
                "Creative Writing", "Critical Analysis", "World Literature", "Modern Literature",
                "Classical Literature", "Contemporary Writing", "Literary Movements", "Author Studies"
            ]
        }
    
    def generate_topic_names(self, subject: str, total_topics: int) -> List[str]:
        """
        Generate topic names based on the subject.
        If subject is not in templates, create generic topic names.
        """
        subject_key = subject.title()
        
        # Check if we have templates for this subject
        if subject_key in self.topic_templates:
            available_topics = self.topic_templates[subject_key].copy()
            
            # If we need more topics than available, create variations
            if total_topics > len(available_topics):
                extra_topics = []
                for i in range(total_topics - len(available_topics)):
                    extra_topics.append(f"Advanced Topic {i+1}")
                return available_topics + extra_topics
            else:
                # Randomly select topics from available ones
                return random.sample(available_topics, total_topics)
        else:
            # Generate generic topic names
            return [f"Topic {i+1}: {subject}" for i in range(total_topics)]
    
    def calculate_daily_topics(self, total_topics: int, total_days: int, difficulty: str) -> List[int]:
        """
        Calculate how many topics to study each day based on difficulty.
        Returns a list of topic counts per day.
        """
        multiplier = self.difficulty_multipliers.get(difficulty, 1.0)
        
        # Adjust total effective topics based on difficulty
        effective_topics = int(total_topics * multiplier)
        
        # Base distribution
        base_topics_per_day = effective_topics // total_days
        remainder = effective_topics % total_days
        
        # Create distribution
        daily_topics = [base_topics_per_day] * total_days
        
        # Distribute remainder topics
        for i in range(remainder):
            daily_topics[i] += 1
        
        # Ensure no day has 0 topics
        for i in range(total_days):
            if daily_topics[i] == 0 and total_topics > 0:
                daily_topics[i] = 1
                # Remove from another day
                for j in range(total_days):
                    if daily_topics[j] > 1:
                        daily_topics[j] -= 1
                        break
        
        return daily_topics
    
    def generate_plan(self, subject: str, total_topics: int, exam_date: datetime.date, 
                     hours_per_day: int, difficulty: str) -> Dict[str, Any]:
        """
        Generate a comprehensive study plan.
        """
        # Calculate days until exam
        today = datetime.now().date()
        days_until_exam = (exam_date - today).days
        
        if days_until_exam <= 0:
            raise ValueError("Exam date must be in the future")
        
        # Generate topic names
        topic_names = self.generate_topic_names(subject, total_topics)
        
        # Calculate daily topic distribution
        daily_topic_counts = self.calculate_daily_topics(total_topics, days_until_exam, difficulty)
        
        # Create daily plan
        daily_plan = []
        topic_index = 0
        
        for day in range(1, days_until_exam + 1):
            current_date = today + timedelta(days=day - 1)
            topics_for_day = daily_topic_counts[day - 1]
            
            # Assign topics for this day
            day_topics = []
            for i in range(topics_for_day):
                if topic_index < len(topic_names):
                    day_topics.append(topic_names[topic_index])
                    topic_index += 1
                else:
                    break
            
            # Only add days with topics
            if day_topics:
                daily_plan.append({
                    'day': day,
                    'date': current_date.strftime('%Y-%m-%d'),
                    'topics': day_topics,
                    'topics_count': len(day_topics),
                    'estimated_hours': min(hours_per_day, len(day_topics) * 2),
                    'difficulty': difficulty
                })
        
        # Calculate study statistics
        total_study_hours = sum(day['estimated_hours'] for day in daily_plan)
        avg_topics_per_day = total_topics / len(daily_plan) if daily_plan else 0
        
        # Generate study tips based on difficulty
        study_tips = self.generate_study_tips(difficulty, hours_per_day)
        
        # Create the complete plan
        study_plan = {
            'subject': subject,
            'total_topics': total_topics,
            'exam_date': exam_date.strftime('%Y-%m-%d'),
            'days_until_exam': days_until_exam,
            'hours_per_day': hours_per_day,
            'difficulty': difficulty,
            'daily_plan': daily_plan,
            'total_study_hours': total_study_hours,
            'avg_topics_per_day': round(avg_topics_per_day, 1),
            'study_tips': study_tips,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return study_plan
    
    def generate_study_tips(self, difficulty: str, hours_per_day: int) -> List[str]:
        """
        Generate personalized study tips based on difficulty and available time.
        """
        tips = []
        
        # Difficulty-specific tips
        if difficulty == "Easy":
            tips.extend([
                "Focus on understanding concepts rather than memorization",
                "Use visual aids and diagrams to enhance learning",
                "Practice with real-world examples"
            ])
        elif difficulty == "Medium":
            tips.extend([
                "Break complex topics into smaller, manageable parts",
                "Use the Pomodoro Technique: 25 min study, 5 min break",
                "Review previous topics regularly to reinforce learning"
            ])
        else:  # Hard
            tips.extend([
                "Start with fundamentals before moving to advanced topics",
                "Use active recall techniques instead of passive reading",
                "Take regular breaks to avoid burnout (every 45-60 minutes)"
            ])
        
        # Time-specific tips
        if hours_per_day <= 2:
            tips.append("Prioritize the most important topics first")
        elif hours_per_day <= 4:
            tips.append("Balance between new topics and revision")
        else:
            tips.append("Include practice problems and hands-on activities")
        
        # General tips
        tips.extend([
            "Stay consistent with your study schedule",
            "Get adequate sleep for better retention",
            "Stay hydrated and maintain a healthy diet"
        ])
        
        return tips[:6]  # Return top 6 tips
    
    def adjust_plan_for_progress(self, original_plan: Dict[str, Any], 
                                completed_topics: List[str]) -> Dict[str, Any]:
        """
        Adjust the study plan based on completed topics.
        """
        # This is a placeholder for future enhancement
        # Could be used to dynamically adjust remaining study days
        return original_plan
    
    def calculate_completion_rate(self, total_topics: int, completed_topics: List[str]) -> float:
        """
        Calculate the completion rate as a percentage.
        """
        if total_topics == 0:
            return 0.0
        return (len(completed_topics) / total_topics) * 100
