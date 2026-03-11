"""
AI Helper Module for OpenAI Integration
Optional module that provides AI-powered study recommendations and tips.
"""

import os
from typing import List, Dict, Any
import json

class AIHelper:
    """
    AI Helper class for generating personalized study recommendations
    using OpenAI API. This is an optional feature.
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize AI Helper with OpenAI API key.
        
        Args:
            api_key: OpenAI API key. If None, will try to get from environment.
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.client = None
        
        if self.api_key:
            try:
                import openai
                self.client = openai.OpenAI(api_key=self.api_key)
            except ImportError:
                print("OpenAI library not installed. Install with: pip install openai")
                self.client = None
        else:
            print("OpenAI API key not provided. AI features will be disabled.")
    
    def is_available(self) -> bool:
        """Check if AI features are available."""
        return self.client is not None
    
    def generate_study_tips(self, subject: str, difficulty: str, 
                           hours_per_day: int, learning_style: str = "visual") -> List[str]:
        """
        Generate personalized study tips using AI.
        
        Args:
            subject: Subject name
            difficulty: Difficulty level (Easy, Medium, Hard)
            hours_per_day: Available study hours per day
            learning_style: Learning style (visual, auditory, kinesthetic, reading)
        
        Returns:
            List of personalized study tips
        """
        if not self.is_available():
            return self._get_fallback_tips(subject, difficulty, hours_per_day)
        
        try:
            prompt = f"""
            Generate 5 personalized study tips for a student studying {subject} at {difficulty} difficulty level.
            The student has {hours_per_day} hours per day to study and prefers {learning_style} learning style.
            
            Make the tips:
            - Practical and actionable
            - Specific to the subject and difficulty
            - Tailored to the available time
            - Suitable for the learning style
            
            Return only the tips, one per line, without numbering.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert study advisor providing personalized learning recommendations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            tips = response.choices[0].message.content.strip().split('\n')
            return [tip.strip() for tip in tips if tip.strip()]
        
        except Exception as e:
            print(f"Error generating AI tips: {e}")
            return self._get_fallback_tips(subject, difficulty, hours_per_day)
    
    def generate_motivation_message(self, subject: str, progress_percentage: float) -> str:
        """
        Generate a motivational message based on progress.
        
        Args:
            subject: Subject being studied
            progress_percentage: Current progress (0-100)
        
        Returns:
            Motivational message
        """
        if not self.is_available():
            return self._get_fallback_motivation(progress_percentage)
        
        try:
            prompt = f"""
            Generate a short, motivational message for a student studying {subject}.
            The student has completed {progress_percentage:.1f}% of their study plan.
            
            Make it:
            - Encouraging and positive
            - Under 50 words
            - Specific to their progress level
            - Inspiring but not cheesy
            
            Return only the message, no extra text.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a motivational coach helping students stay focused on their goals."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Error generating motivation: {e}")
            return self._get_fallback_motivation(progress_percentage)
    
    def generate_break_recommendations(self, study_duration: int, difficulty: str) -> List[str]:
        """
        Generate break recommendations based on study duration and difficulty.
        
        Args:
            study_duration: Study duration in minutes
            difficulty: Difficulty level
        
        Returns:
            List of break activity recommendations
        """
        if not self.is_available():
            return self._get_fallback_breaks(study_duration, difficulty)
        
        try:
            prompt = f"""
            Generate 4 break activity recommendations for a student who has been studying for {study_duration} minutes.
            The subject difficulty is {difficulty}.
            
            Make the recommendations:
            - Quick (2-5 minutes each)
            - Refreshing and mentally restorative
            - Suitable for a study environment
            - Varied (physical, mental, visual, etc.)
            
            Return only the activities, one per line, without numbering.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a productivity expert specializing in study break optimization."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            breaks = response.choices[0].message.content.strip().split('\n')
            return [break_item.strip() for break_item in breaks if break_item.strip()]
        
        except Exception as e:
            print(f"Error generating break recommendations: {e}")
            return self._get_fallback_breaks(study_duration, difficulty)
    
    def _get_fallback_tips(self, subject: str, difficulty: str, hours_per_day: int) -> List[str]:
        """Fallback study tips when AI is not available."""
        tips = []
        
        if difficulty == "Easy":
            tips = [
                "Use visual aids and diagrams to understand concepts better",
                "Practice with real-world examples to make learning relevant",
                "Teach the concepts to someone else to reinforce your understanding"
            ]
        elif difficulty == "Medium":
            tips = [
                "Break complex topics into smaller, manageable chunks",
                "Use the Pomodoro Technique: 25 minutes focused study, 5 minutes break",
                "Create summary notes for each topic to review later"
            ]
        else:  # Hard
            tips = [
                "Start with fundamentals before tackling advanced concepts",
                "Use active recall techniques instead of passive reading",
                "Take regular breaks every 45-60 minutes to maintain focus"
            ]
        
        # Time-based tips
        if hours_per_day <= 2:
            tips.append("Focus on the most important topics first")
        elif hours_per_day >= 6:
            tips.append("Include practice problems and hands-on activities")
        
        return tips[:5]
    
    def _get_fallback_motivation(self, progress_percentage: float) -> str:
        """Fallback motivation messages when AI is not available."""
        if progress_percentage < 25:
            return "Great start! Every journey begins with a single step. Keep going! 💪"
        elif progress_percentage < 50:
            return "You're making solid progress! Stay consistent and you'll reach your goal! 🎯"
        elif progress_percentage < 75:
            return "Excellent work! You're more than halfway there. Finish strong! 🚀"
        elif progress_percentage < 100:
            return "Almost there! The finish line is in sight. Push through! 🏁"
        else:
            return "Congratulations! You've completed your study plan! 🎉"
    
    def _get_fallback_breaks(self, study_duration: int, difficulty: str) -> List[str]:
        """Fallback break recommendations when AI is not available."""
        breaks = [
            "Stand up and stretch for 2 minutes",
            "Drink a glass of water and walk around",
            "Do some quick eye exercises (look far, then near)",
            "Take 10 deep breaths to refresh your mind"
        ]
        
        if study_duration > 60:
            breaks.insert(0, "Take a 5-minute walk to get fresh air")
        
        if difficulty == "Hard":
            breaks.append("Listen to one calming song to reset your focus")
        
        return breaks[:4]
    
    def generate_weekly_summary(self, completed_topics: List[str], 
                              total_topics: int, subject: str) -> str:
        """
        Generate a weekly study summary.
        
        Args:
            completed_topics: List of completed topics
            total_topics: Total number of topics
            subject: Subject name
        
        Returns:
            Weekly summary message
        """
        if not self.is_available():
            return self._get_fallback_summary(completed_topics, total_topics, subject)
        
        try:
            progress = (len(completed_topics) / total_topics * 100) if total_topics > 0 else 0
            
            prompt = f"""
            Generate a brief weekly study summary for a student studying {subject}.
            This week, they completed {len(completed_topics)} out of {total_topics} topics ({progress:.1f}%).
            
            Make it:
            - Positive and encouraging
            - Highlight achievements
            - Suggest focus areas for next week
            - Under 75 words
            
            Return only the summary, no extra text.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a study progress analyst providing weekly summaries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=120,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Error generating weekly summary: {e}")
            return self._get_fallback_summary(completed_topics, total_topics, subject)
    
    def _get_fallback_summary(self, completed_topics: List[str], 
                            total_topics: int, subject: str) -> str:
        """Fallback weekly summary when AI is not available."""
        progress = (len(completed_topics) / total_topics * 100) if total_topics > 0 else 0
        
        if progress >= 80:
            return f"Fantastic week! You've mastered {len(completed_topics)} topics in {subject}. You're on track for exam success! 🌟"
        elif progress >= 50:
            return f"Good progress this week! You've completed {len(completed_topics)} topics in {subject}. Keep up the consistent effort! 📚"
        elif progress >= 25:
            return f"Steady progress! You've covered {len(completed_topics)} topics in {subject}. Focus on consistency next week! 📈"
        else:
            return f"You've completed {len(completed_topics)} topics in {subject}. Try to increase study time next week for better progress! 💪"
