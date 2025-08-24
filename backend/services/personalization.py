from typing import Dict, List, Any
from models.schemas import LearningProfile, UserPreferences

class PersonalizationService:
    def __init__(self):
        # Profile-specific adaptation rules
        self.profile_rules = {
            LearningProfile.ADHD: {
                "content_length": "short",
                "format_preferences": ["flashcards", "timers", "interactive"],
                "accessibility_features": ["timer", "break_reminders", "focus_mode"],
                "time_multiplier": 1.5
            },
            LearningProfile.DYSLEXIA: {
                "content_length": "medium",
                "format_preferences": ["simplified_text", "tts", "visual_aids"],
                "accessibility_features": ["dyslexic_font", "line_spacing", "color_overlay"],
                "time_multiplier": 1.3
            },
            LearningProfile.AUTISM: {
                "content_length": "structured",
                "format_preferences": ["predictable_order", "clear_structure", "visual_schedules"],
                "accessibility_features": ["predictable_interface", "reduced_stimuli", "clear_instructions"],
                "time_multiplier": 1.0
            },
            LearningProfile.DYSCALCULIA: {
                "content_length": "step_by_step",
                "format_preferences": ["visual_math", "step_explanations", "concrete_examples"],
                "accessibility_features": ["number_line", "visual_counters", "math_tools"],
                "time_multiplier": 1.4
            },
            LearningProfile.DYSGRAPHIA: {
                "content_length": "minimal_writing",
                "format_preferences": ["multiple_choice", "voice_input", "visual_selection"],
                "accessibility_features": ["voice_to_text", "prediction_text", "spell_check"],
                "time_multiplier": 1.2
            },
            LearningProfile.NEUROTYPICAL: {
                "content_length": "standard",
                "format_preferences": ["mixed_formats", "traditional", "interactive"],
                "accessibility_features": ["standard_interface"],
                "time_multiplier": 1.0
            }
        }
    
    def personalize_content(self, content: Any, learning_profile: LearningProfile, preferences: UserPreferences) -> Dict[str, Any]:
        """
        Task 8: Personalization by Profile
        Adapt content based on neurodiverse learning profiles
        """
        try:
            # Get profile-specific rules
            profile_rules = self.profile_rules.get(learning_profile, self.profile_rules[LearningProfile.NEUROTYPICAL])
            
            # Apply personalization based on profile
            adapted_content = self._adapt_content_for_profile(content, learning_profile, profile_rules)
            
            # Apply user preferences
            adapted_content = self._apply_user_preferences(adapted_content, preferences)
            
            # Determine recommended format
            recommended_format = self._determine_recommended_format(learning_profile, preferences)
            
            # Generate accessibility features
            accessibility_features = self._generate_accessibility_features(learning_profile, preferences)
            
            # Calculate estimated completion time
            completion_time = self._calculate_completion_time(content, learning_profile, preferences)
            
            # Generate profile-specific recommendations
            recommendations = self._generate_profile_recommendations(learning_profile, preferences)
            
            return {
                "personalized_content": {
                    "adapted_content": adapted_content,
                    "recommended_format": recommended_format,
                    "accessibility_features": accessibility_features,
                    "estimated_completion_time": completion_time
                },
                "profile_specific_recommendations": recommendations
            }
            
        except Exception as e:
            raise Exception(f"Content personalization failed: {str(e)}")
    
    def _adapt_content_for_profile(self, content: Any, profile: LearningProfile, profile_rules: Dict) -> Any:
        """Adapt content based on learning profile"""
        if isinstance(content, list):
            return [self._adapt_single_item(item, profile, profile_rules) for item in content]
        else:
            return self._adapt_single_item(content, profile, profile_rules)
    
    def _adapt_single_item(self, item: Any, profile: LearningProfile, profile_rules: Dict) -> Any:
        """Adapt a single content item for the learning profile"""
        if isinstance(item, dict):
            adapted_item = {}
            
            for key, value in item.items():
                if key == "flashcards" and profile == LearningProfile.ADHD:
                    # ADHD: Shorter, more focused flashcards
                    adapted_item[key] = self._adapt_flashcards_for_adhd(value)
                elif key == "summary" and profile == LearningProfile.DYSLEXIA:
                    # Dyslexia: Simplified summaries
                    adapted_item[key] = self._adapt_summary_for_dyslexia(value)
                elif key == "mcq" and profile == LearningProfile.DYSGRAPHIA:
                    # Dysgraphia: Shorter MCQ options
                    adapted_item[key] = self._adapt_mcq_for_dysgraphia(value)
                else:
                    adapted_item[key] = value
            
            return adapted_item
        else:
            return item
    
    def _adapt_flashcards_for_adhd(self, flashcards: List[Dict]) -> List[Dict]:
        """Adapt flashcards specifically for ADHD learners"""
        adapted_flashcards = []
        
        for flashcard in flashcards:
            # Make questions more direct
            question = flashcard.get("question", "")
            if question.startswith("What is"):
                question = question.replace("What is", "Define")
            
            # Make answers shorter
            answer = flashcard.get("answer", "")
            if len(answer) > 30:
                words = answer.split()
                if len(words) > 6:
                    answer = ' '.join(words[:6]) + '...'
            
            adapted_flashcards.append({
                "question": question,
                "answer": answer,
                "difficulty": flashcard.get("difficulty", "medium"),
                "estimated_time": 30  # 30 seconds per flashcard for ADHD
            })
        
        return adapted_flashcards
    
    def _adapt_summary_for_dyslexia(self, summary: List[str]) -> List[str]:
        """Adapt summary specifically for dyslexic learners"""
        adapted_summary = []
        
        for point in summary:
            # Simplify language
            simplified = self._simplify_for_dyslexia(point)
            
            # Limit length
            if len(simplified) > 25:
                words = simplified.split()
                if len(words) > 5:
                    simplified = ' '.join(words[:5]) + '...'
            
            adapted_summary.append(simplified)
        
        return adapted_summary
    
    def _adapt_mcq_for_dysgraphia(self, mcq: Dict) -> Dict:
        """Adapt MCQ specifically for dysgraphic learners"""
        adapted_mcq = mcq.copy()
        
        # Shorten options
        options = mcq.get("options", [])
        shortened_options = []
        
        for option in options:
            if len(option) > 25:
                words = option.split()
                if len(words) > 4:
                    shortened = ' '.join(words[:4]) + '...'
                else:
                    shortened = option[:25] + '...'
            else:
                shortened = option
            
            shortened_options.append(shortened)
        
        adapted_mcq["options"] = shortened_options
        return adapted_mcq
    
    def _simplify_for_dyslexia(self, text: str) -> str:
        """Simplify text for dyslexic readers"""
        # Replace complex words with simpler alternatives
        replacements = {
            'consequently': 'so',
            'furthermore': 'also',
            'nevertheless': 'but',
            'subsequently': 'then',
            'approximately': 'about'
        }
        
        simplified = text
        for complex_word, simple_word in replacements.items():
            simplified = simplified.replace(complex_word, simple_word)
        
        return simplified
    
    def _apply_user_preferences(self, content: Any, preferences: UserPreferences) -> Any:
        """Apply user-specific preferences to content"""
        # This would apply user preferences like content length, audio settings, etc.
        # For now, return content as-is
        return content
    
    def _determine_recommended_format(self, profile: LearningProfile, preferences: UserPreferences) -> str:
        """Determine the recommended format for the learning profile"""
        if profile == LearningProfile.ADHD:
            return "flashcards_with_timer"
        elif profile == LearningProfile.DYSLEXIA:
            return "simplified_text_with_tts"
        elif profile == LearningProfile.AUTISM:
            return "structured_sequence"
        elif profile == LearningProfile.DYSCALCULIA:
            return "visual_step_by_step"
        elif profile == LearningProfile.DYSGRAPHIA:
            return "multiple_choice_voice"
        else:
            return "standard_format"
    
    def _generate_accessibility_features(self, profile: LearningProfile, preferences: UserPreferences) -> List[str]:
        """Generate list of accessibility features for the profile"""
        base_features = []
        
        if profile == LearningProfile.ADHD:
            base_features = ["timer", "break_reminders", "focus_mode", "progress_tracker"]
        elif profile == LearningProfile.DYSLEXIA:
            base_features = ["dyslexic_font", "line_spacing", "color_overlay", "text_to_speech"]
        elif profile == LearningProfile.AUTISM:
            base_features = ["predictable_interface", "reduced_stimuli", "clear_instructions", "visual_schedule"]
        elif profile == LearningProfile.DYSCALCULIA:
            base_features = ["number_line", "visual_counters", "math_tools", "step_by_step_guide"]
        elif profile == LearningProfile.DYSGRAPHIA:
            base_features = ["voice_to_text", "prediction_text", "spell_check", "voice_input"]
        else:
            base_features = ["standard_interface"]
        
        # Add user preference-based features
        if preferences.audio_enabled:
            base_features.append("audio_support")
        if preferences.visual_aids:
            base_features.append("visual_aids")
        if preferences.interactive_elements:
            base_features.append("interactive_elements")
        
        return base_features
    
    def _calculate_completion_time(self, content: Any, profile: LearningProfile, preferences: UserPreferences) -> int:
        """Calculate estimated completion time in minutes"""
        # Get base time multiplier for profile
        profile_rules = self.profile_rules.get(profile, self.profile_rules[LearningProfile.NEUROTYPICAL])
        time_multiplier = profile_rules["time_multiplier"]
        
        # Estimate base time based on content
        base_time = self._estimate_base_time(content)
        
        # Apply profile multiplier
        adjusted_time = int(base_time * time_multiplier)
        
        # Apply user preference adjustments
        if preferences.preferred_content_length == "short":
            adjusted_time = int(adjusted_time * 0.8)
        elif preferences.preferred_content_length == "long":
            adjusted_time = int(adjusted_time * 1.2)
        
        return max(1, adjusted_time)  # Minimum 1 minute
    
    def _estimate_base_time(self, content: Any) -> int:
        """Estimate base completion time for content"""
        if isinstance(content, list):
            total_time = 0
            for item in content:
                total_time += self._estimate_base_time(item)
            return total_time
        elif isinstance(content, dict):
            # Estimate based on content type
            if "flashcards" in content:
                return len(content["flashcards"]) * 2  # 2 minutes per flashcard
            elif "summary" in content:
                return len(content["summary"]) * 1  # 1 minute per summary point
            elif "mcq" in content:
                return 3  # 3 minutes for MCQ
            else:
                return 5  # Default 5 minutes
        else:
            return 5  # Default 5 minutes
    
    def _generate_profile_recommendations(self, profile: LearningProfile, preferences: UserPreferences) -> List[str]:
        """Generate profile-specific learning recommendations"""
        recommendations = []
        
        if profile == LearningProfile.ADHD:
            recommendations = [
                "Take frequent short breaks (5 minutes every 25 minutes)",
                "Use a timer to stay focused",
                "Study in a quiet, distraction-free environment",
                "Break large tasks into smaller, manageable chunks",
                "Use visual aids and color coding"
            ]
        elif profile == LearningProfile.DYSLEXIA:
            recommendations = [
                "Use text-to-speech for reading",
                "Take breaks when reading becomes difficult",
                "Use a ruler or bookmark to track lines",
                "Try different background colors for text",
                "Read aloud or listen to audio versions"
            ]
        elif profile == LearningProfile.AUTISM:
            recommendations = [
                "Follow a predictable study schedule",
                "Use clear, literal instructions",
                "Minimize sensory distractions",
                "Use visual schedules and checklists",
                "Take breaks when feeling overwhelmed"
            ]
        elif profile == LearningProfile.DYSCALCULIA:
            recommendations = [
                "Use visual aids like number lines",
                "Break math problems into smaller steps",
                "Use concrete objects to visualize numbers",
                "Practice with real-world examples",
                "Allow extra time for calculations"
            ]
        elif profile == LearningProfile.DYSGRAPHIA:
            recommendations = [
                "Use voice-to-text software",
                "Type instead of writing by hand",
                "Use spell-check and grammar tools",
                "Take breaks during writing tasks",
                "Use templates and outlines"
            ]
        else:
            recommendations = [
                "Study in a comfortable environment",
                "Take regular breaks",
                "Use a variety of learning methods",
                "Review material regularly",
                "Ask for help when needed"
            ]
        
        return recommendations
