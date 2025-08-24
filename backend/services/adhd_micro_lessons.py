import re
from typing import Dict, List, Any
import random
from services.gemini_service import GeminiService

class ADHDMicroLessons:
    def __init__(self):
        # Initialize Gemini service for enhanced micro-lessons
        self.gemini_service = GeminiService()
        
        # Fact extraction patterns
        self.fact_patterns = [
            r'(\w+)\s+is\s+([^.!?]+)',
            r'(\w+)\s+are\s+([^.!?]+)',
            r'(\w+)\s+means\s+([^.!?]+)',
            r'(\w+)\s+refers\s+to\s+([^.!?]+)',
            r'(\w+)\s+=\s+([^.!?]+)',
            r'(\d+)\s+([^.!?]+)',
            r'([A-Z][a-z]+)\s+([^.!?]+)'
        ]
        
        # Question templates for micro-lessons
        self.question_templates = [
            "What is {}?",
            "Define {}.",
            "What does {} mean?",
            "What is the value of {}?",
            "What is {} equal to?",
            "What is the definition of {}?"
        ]
    
    def generate_micro_lessons(self, topic_text: str, max_items: int = 10) -> Dict[str, Any]:
        """
        Task 6: ADHD Micro-lessons
        Generate 1-fact flashcards from topics for ADHD students
        """
        try:
            # Try Gemini first for enhanced micro-lessons
            gemini_micro_lessons = self.gemini_service.generate_micro_lessons(topic_text, LearningProfile.ADHD)
            if gemini_micro_lessons:
                micro_lessons = gemini_micro_lessons
            else:
                # Fallback to rule-based extraction
                # Extract facts from text
                facts = self._extract_facts(topic_text)
                
                # Generate micro-lessons from facts
                micro_lessons = self._create_micro_lessons(facts, max_items)
            
            # Calculate total estimated time
            total_time = self._calculate_total_time(micro_lessons)
            
            return {
                "micro_lessons": micro_lessons,
                "total_estimated_time_minutes": total_time
            }
            
        except Exception as e:
            raise Exception(f"Micro-lesson generation failed: {str(e)}")
    
    def _extract_facts(self, text: str) -> List[Dict[str, str]]:
        """Extract facts from text using pattern matching"""
        facts = []
        
        # Split text into sentences
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 10:
                continue
            
            # Try different fact patterns
            for pattern in self.fact_patterns:
                matches = re.findall(pattern, sentence, re.IGNORECASE)
                for match in matches:
                    if len(match) == 2:
                        concept, definition = match
                        concept = concept.strip()
                        definition = definition.strip()
                        
                        # Filter out very short or very long facts
                        if (len(concept) > 2 and len(concept) < 50 and 
                            len(definition) > 5 and len(definition) < 100):
                            facts.append({
                                "concept": concept,
                                "definition": definition,
                                "sentence": sentence
                            })
        
        # Remove duplicates
        unique_facts = []
        seen_concepts = set()
        for fact in facts:
            if fact["concept"].lower() not in seen_concepts:
                unique_facts.append(fact)
                seen_concepts.add(fact["concept"].lower())
        
        return unique_facts
    
    def _create_micro_lessons(self, facts: List[Dict[str, str]], max_items: int) -> List[Dict[str, Any]]:
        """Create micro-lessons from extracted facts"""
        micro_lessons = []
        
        for fact in facts[:max_items]:
            # Generate question
            question_template = random.choice(self.question_templates)
            question = question_template.format(fact["concept"])
            
            # Generate answer (keep it short for ADHD)
            answer = self._simplify_answer(fact["definition"])
            
            # Estimate time (ADHD students need quick wins)
            estimated_time = self._estimate_lesson_time(question, answer)
            
            micro_lessons.append({
                "question": question,
                "answer": answer,
                "estimated_time_seconds": estimated_time
            })
        
        # If not enough facts, create general micro-lessons
        while len(micro_lessons) < max_items:
            general_lesson = self._create_general_micro_lesson()
            micro_lessons.append(general_lesson)
        
        return micro_lessons
    
    def _simplify_answer(self, definition: str) -> str:
        """Simplify answer for ADHD learners"""
        # Remove complex punctuation
        simplified = re.sub(r'[;:]', ',', definition)
        
        # Limit length
        if len(simplified) > 30:
            # Try to cut at word boundary
            words = simplified.split()
            if len(words) > 6:
                simplified = ' '.join(words[:6]) + '...'
            else:
                simplified = simplified[:30] + '...'
        
        return simplified.strip()
    
    def _estimate_lesson_time(self, question: str, answer: str) -> int:
        """Estimate time needed for a micro-lesson (in seconds)"""
        # Base time for reading question and answer
        base_time = 10
        
        # Add time based on length
        question_words = len(question.split())
        answer_words = len(answer.split())
        
        # ADHD students might need more time to process
        reading_time = (question_words + answer_words) * 2
        
        # Time to think and respond
        thinking_time = 5
        
        total_time = base_time + reading_time + thinking_time
        
        # Cap at reasonable limits for ADHD
        return min(60, max(10, total_time))
    
    def _create_general_micro_lesson(self) -> Dict[str, Any]:
        """Create a general micro-lesson when specific facts aren't available"""
        general_questions = [
            "What is the main topic?",
            "What is the key point?",
            "What is the main idea?",
            "What is this about?"
        ]
        
        general_answers = [
            "The main topic of the text.",
            "The key point being discussed.",
            "The main idea presented.",
            "The subject being explained."
        ]
        
        question = random.choice(general_questions)
        answer = random.choice(general_answers)
        
        return {
            "question": question,
            "answer": answer,
            "estimated_time_seconds": 15
        }
    
    def _calculate_total_time(self, micro_lessons: List[Dict[str, Any]]) -> int:
        """Calculate total estimated time in minutes"""
        total_seconds = sum(lesson["estimated_time_seconds"] for lesson in micro_lessons)
        return max(1, total_seconds // 60)  # Convert to minutes, minimum 1 minute
    
    def create_study_sets(self, micro_lessons: List[Dict[str, Any]], set_size: int = 5) -> List[List[Dict[str, Any]]]:
        """Group micro-lessons into small study sets"""
        study_sets = []
        
        for i in range(0, len(micro_lessons), set_size):
            study_set = micro_lessons[i:i + set_size]
            study_sets.append(study_set)
        
        return study_sets
    
    def optimize_for_adhd(self, micro_lessons: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Optimize micro-lessons specifically for ADHD learners"""
        optimized_lessons = []
        
        for lesson in micro_lessons:
            # Make questions more direct
            question = lesson["question"]
            if question.startswith("What is"):
                question = question.replace("What is", "Define")
            
            # Make answers even shorter
            answer = lesson["answer"]
            if len(answer) > 25:
                words = answer.split()
                if len(words) > 4:
                    answer = ' '.join(words[:4]) + '...'
            
            # Reduce estimated time for quick wins
            estimated_time = max(5, lesson["estimated_time_seconds"] - 5)
            
            optimized_lessons.append({
                "question": question,
                "answer": answer,
                "estimated_time_seconds": estimated_time
            })
        
        return optimized_lessons
