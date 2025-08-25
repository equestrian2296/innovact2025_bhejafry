from typing import Dict, List, Any
from models.schemas import LearningProfile
import random

class RoadmapGenerator:
    def __init__(self):
        # Topic difficulty mappings
        self.topic_difficulties = {
            "basic": 1,
            "intermediate": 2,
            "advanced": 3
        }
        
        # Learning modes for different profiles
        self.profile_modes = {
            LearningProfile.ADHD: [
                "flashcards_with_timer",
                "micro_lessons",
                "interactive_quizzes",
                "visual_summaries"
            ],
            LearningProfile.DYSLEXIA: [
                "simplified_text",
                "text_to_speech",
                "visual_aids",
                "audio_summaries"
            ],
            LearningProfile.AUTISM: [
                "structured_sequence",
                "predictable_format",
                "clear_instructions",
                "visual_schedules"
            ],
            LearningProfile.DYSCALCULIA: [
                "visual_math",
                "step_by_step_explanations",
                "concrete_examples",
                "number_visualizations"
            ],
            LearningProfile.DYSGRAPHIA: [
                "multiple_choice",
                "voice_input",
                "visual_selection",
                "audio_feedback"
            ],
            LearningProfile.NEUROTYPICAL: [
                "mixed_formats",
                "traditional_reading",
                "interactive_elements",
                "standard_assessments"
            ]
        }
        
        # Learning activities for different modes
        self.learning_activities = {
            "flashcards_with_timer": [
                "Review flashcards with 30-second timer",
                "Take 5-minute breaks between sets",
                "Use visual cues for memorization"
            ],
            "micro_lessons": [
                "Complete 5-minute learning sessions",
                "Take short breaks between lessons",
                "Use quick quizzes for reinforcement"
            ],
            "simplified_text": [
                "Read simplified content",
                "Use text-to-speech for difficult passages",
                "Take breaks when reading becomes difficult"
            ],
            "text_to_speech": [
                "Listen to audio versions of content",
                "Follow along with highlighted text",
                "Use audio summaries for review"
            ],
            "structured_sequence": [
                "Follow the exact order of topics",
                "Complete each step before moving on",
                "Use checklists to track progress"
            ],
            "visual_math": [
                "Use number lines and visual counters",
                "Draw diagrams for problem-solving",
                "Use concrete objects for visualization"
            ],
            "step_by_step_explanations": [
                "Follow detailed step-by-step guides",
                "Use visual aids for each step",
                "Practice with similar problems"
            ],
            "multiple_choice": [
                "Answer multiple choice questions",
                "Use voice input for responses",
                "Review explanations for each answer"
            ]
        }
    
    def generate_roadmap(self, topics: List[str], learning_profile: LearningProfile, study_duration_weeks: int = 12) -> Dict[str, Any]:
        """
        Task 9: AI Learning Roadmap
        Generate a structured learning roadmap for neurodiverse students
        """
        try:
            # Assess topic difficulties
            topic_difficulties = self._assess_topic_difficulties(topics)
            
            # Order topics by difficulty
            ordered_topics = self._order_topics_by_difficulty(topics, topic_difficulties)
            
            # Distribute topics across weeks
            weekly_topics = self._distribute_topics_weekly(ordered_topics, study_duration_weeks)
            
            # Generate weekly roadmap
            roadmap = self._generate_weekly_roadmap(weekly_topics, learning_profile, study_duration_weeks)
            
            # Calculate total estimated hours
            total_hours = self._calculate_total_hours(roadmap)
            
            # Determine difficulty progression
            difficulty_progression = self._determine_difficulty_progression(roadmap)
            
            return {
                "roadmap": roadmap,
                "total_estimated_hours": total_hours,
                "difficulty_progression": difficulty_progression
            }
            
        except Exception as e:
            raise Exception(f"Roadmap generation failed: {str(e)}")
    
    def _assess_topic_difficulties(self, topics: List[str]) -> Dict[str, int]:
        """Assess difficulty level of each topic"""
        difficulties = {}
        
        for topic in topics:
            # Simple heuristic based on topic keywords
            topic_lower = topic.lower()
            
            if any(word in topic_lower for word in ['basic', 'introduction', 'fundamental', 'simple']):
                difficulties[topic] = 1
            elif any(word in topic_lower for word in ['advanced', 'complex', 'difficult', 'challenging']):
                difficulties[topic] = 3
            else:
                difficulties[topic] = 2
        
        return difficulties
    
    def _order_topics_by_difficulty(self, topics: List[str], difficulties: Dict[str, int]) -> List[str]:
        """Order topics from easiest to hardest"""
        # Sort topics by difficulty
        sorted_topics = sorted(topics, key=lambda topic: difficulties.get(topic, 2))
        return sorted_topics
    
    def _distribute_topics_weekly(self, ordered_topics: List[str], study_duration_weeks: int) -> List[List[str]]:
        """Distribute topics across weeks"""
        weekly_topics = []
        
        if not ordered_topics:
            return weekly_topics
        
        # Calculate topics per week
        topics_per_week = max(1, len(ordered_topics) // study_duration_weeks)
        
        # Distribute topics
        for i in range(0, len(ordered_topics), topics_per_week):
            week_topics = ordered_topics[i:i + topics_per_week]
            weekly_topics.append(week_topics)
        
        # Ensure we have enough weeks
        while len(weekly_topics) < study_duration_weeks:
            if weekly_topics:
                # Add topics from previous weeks
                weekly_topics.append(weekly_topics[-1][:1])
            else:
                weekly_topics.append(["General Review"])
        
        return weekly_topics[:study_duration_weeks]
    
    def _generate_weekly_roadmap(self, weekly_topics: List[List[str]], learning_profile: LearningProfile, study_duration_weeks: int) -> List[Dict[str, Any]]:
        """Generate detailed weekly roadmap"""
        roadmap = []
        
        for week_num, topics in enumerate(weekly_topics, 1):
            week_roadmap = []
            
            for topic in topics:
                # Determine learning mode for this topic and profile
                mode = self._select_learning_mode(learning_profile, topic)
                
                # Estimate study hours for this topic
                estimated_hours = self._estimate_topic_hours(topic, learning_profile)
                
                # Generate learning activities
                activities = self._generate_learning_activities(mode, topic)
                
                week_roadmap.append({
                    "week_number": week_num,
                    "topic": topic,
                    "mode": mode,
                    "estimated_hours": estimated_hours,
                    "learning_activities": activities
                })
            
            roadmap.extend(week_roadmap)
        
        return roadmap
    
    def _select_learning_mode(self, learning_profile: LearningProfile, topic: str) -> str:
        """Select appropriate learning mode for topic and profile"""
        available_modes = self.profile_modes.get(learning_profile, self.profile_modes[LearningProfile.NEUROTYPICAL])
        
        # Select mode based on topic characteristics
        topic_lower = topic.lower()
        
        if any(word in topic_lower for word in ['math', 'calculation', 'equation']):
            if learning_profile == LearningProfile.DYSCALCULIA:
                return "visual_math"
            else:
                return "step_by_step_explanations"
        elif any(word in topic_lower for word in ['reading', 'text', 'literature']):
            if learning_profile == LearningProfile.DYSLEXIA:
                return "text_to_speech"
            else:
                return "simplified_text"
        elif any(word in topic_lower for word in ['writing', 'essay', 'composition']):
            if learning_profile == LearningProfile.DYSGRAPHIA:
                return "multiple_choice"
            else:
                return "structured_sequence"
        else:
            # Default mode for the profile
            return random.choice(available_modes)
    
    def _estimate_topic_hours(self, topic: str, learning_profile: LearningProfile) -> float:
        """Estimate study hours for a topic based on profile"""
        # Base hours based on topic complexity
        topic_lower = topic.lower()
        
        if any(word in topic_lower for word in ['basic', 'introduction']):
            base_hours = 2.0
        elif any(word in topic_lower for word in ['advanced', 'complex']):
            base_hours = 4.0
        else:
            base_hours = 3.0
        
        # Adjust for learning profile
        profile_multipliers = {
            LearningProfile.ADHD: 1.5,  # ADHD students might need more time
            LearningProfile.DYSLEXIA: 1.3,  # Dyslexic students need more reading time
            LearningProfile.AUTISM: 1.0,  # Standard time for structured learning
            LearningProfile.DYSCALCULIA: 1.4,  # Math takes longer for dyscalculic students
            LearningProfile.DYSGRAPHIA: 1.2,  # Writing tasks take longer
            LearningProfile.NEUROTYPICAL: 1.0  # Standard time
        }
        
        multiplier = profile_multipliers.get(learning_profile, 1.0)
        return round(base_hours * multiplier, 1)
    
    def _generate_learning_activities(self, mode: str, topic: str) -> List[str]:
        """Generate specific learning activities for a mode and topic"""
        base_activities = self.learning_activities.get(mode, [
            "Read the material",
            "Take notes",
            "Complete practice exercises",
            "Review and reflect"
        ])
        
        # Customize activities based on topic
        topic_lower = topic.lower()
        
        if any(word in topic_lower for word in ['math', 'calculation']):
            activities = [
                "Solve practice problems step by step",
                "Use visual aids like number lines",
                "Work with concrete examples",
                "Review solutions and explanations"
            ]
        elif any(word in topic_lower for word in ['reading', 'literature']):
            activities = [
                "Read the text carefully",
                "Take notes on key points",
                "Summarize main ideas",
                "Answer comprehension questions"
            ]
        elif any(word in topic_lower for word in ['writing', 'essay']):
            activities = [
                "Plan your writing structure",
                "Write a first draft",
                "Revise and edit your work",
                "Get feedback and improve"
            ]
        else:
            activities = base_activities
        
        return activities[:4]  # Limit to 4 activities per topic
    
    def _calculate_total_hours(self, roadmap: List[Dict[str, Any]]) -> float:
        """Calculate total estimated study hours"""
        total_hours = sum(week["estimated_hours"] for week in roadmap)
        return round(total_hours, 1)
    
    def _determine_difficulty_progression(self, roadmap: List[Dict[str, Any]]) -> str:
        """Determine the difficulty progression pattern"""
        if not roadmap:
            return "linear"
        
        # Analyze difficulty progression
        difficulties = []
        for week in roadmap:
            topic = week["topic"].lower()
            if any(word in topic for word in ['basic', 'introduction']):
                difficulties.append(1)
            elif any(word in topic for word in ['advanced', 'complex']):
                difficulties.append(3)
            else:
                difficulties.append(2)
        
        # Determine progression pattern
        if len(difficulties) < 2:
            return "linear"
        
        # Check if difficulty increases over time
        increasing = all(difficulties[i] <= difficulties[i+1] for i in range(len(difficulties)-1))
        
        if increasing:
            return "progressive"
        else:
            return "mixed"
    
    def optimize_roadmap_for_profile(self, roadmap: List[Dict[str, Any]], learning_profile: LearningProfile) -> List[Dict[str, Any]]:
        """Optimize roadmap specifically for the learning profile"""
        optimized_roadmap = []
        
        for week in roadmap:
            optimized_week = week.copy()
            
            # Adjust estimated hours based on profile
            if learning_profile == LearningProfile.ADHD:
                # ADHD students might need more frequent breaks
                optimized_week["estimated_hours"] = week["estimated_hours"] * 1.2
                optimized_week["learning_activities"].append("Take 5-minute breaks every 25 minutes")
            
            elif learning_profile == LearningProfile.DYSLEXIA:
                # Dyslexic students might need more time for reading
                optimized_week["estimated_hours"] = week["estimated_hours"] * 1.3
                optimized_week["learning_activities"].append("Use text-to-speech for difficult passages")
            
            elif learning_profile == LearningProfile.AUTISM:
                # Autistic students benefit from clear structure
                optimized_week["learning_activities"].insert(0, "Review the learning schedule for this week")
                optimized_week["learning_activities"].append("Check off completed activities")
            
            optimized_roadmap.append(optimized_week)
        
        return optimized_roadmap
