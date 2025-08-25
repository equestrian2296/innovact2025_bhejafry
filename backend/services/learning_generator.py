import os
from typing import Dict, List, Any
import random
import re
from models.schemas import LearningProfile
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from services.gemini_service import GeminiService

class LearningGenerator:
    def __init__(self):
        # Initialize NLTK components for free text processing
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
        except:
            pass  # Continue even if NLTK download fails
        
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Initialize Gemini service for enhanced content generation
        self.gemini_service = GeminiService()
        
        # Enhanced template-based generation (free alternative to OpenAI)
        self.flashcard_templates = [
            "What is {concept}?",
            "Define {concept}.",
            "What does {concept} mean?",
            "Explain {concept} in simple terms.",
            "What is the main idea of {concept}?"
        ]
        
        self.answer_templates = [
            "{concept} is {definition}.",
            "{concept} refers to {definition}.",
            "{concept} means {definition}.",
            "{definition} is what {concept} is.",
            "The concept of {concept} involves {definition}."
        ]
        
        self.mcq_templates = [
            "Which of the following best describes {concept}?",
            "What is the correct definition of {concept}?",
            "Which option correctly explains {concept}?",
            "What does {concept} refer to?",
            "Which statement about {concept} is true?"
        ]
    
    def generate_items(self, chunk_text: str, learning_profile: LearningProfile) -> Dict[str, Any]:
        """
        Task 3: Learning Item Generation (Flashcards, Summaries, MCQs)
        Generate alternative formats for neurodiverse learners
        """
        try:
            # Extract key concepts from the text
            key_concepts = self._extract_key_concepts(chunk_text)
            
            # Generate flashcards (try Gemini first, fallback to templates)
            gemini_flashcards = self.gemini_service.generate_flashcards(chunk_text, key_concepts, learning_profile)
            if gemini_flashcards:
                flashcards = gemini_flashcards
            else:
                flashcards = self._generate_flashcards(chunk_text, key_concepts, learning_profile)
            
            # Generate summary (try Gemini first, fallback to templates)
            gemini_summary = self.gemini_service.generate_summary(chunk_text, learning_profile)
            if gemini_summary:
                summary = gemini_summary
            else:
                summary = self._generate_summary(chunk_text, learning_profile)
            
            # Generate MCQ (try Gemini first, fallback to templates)
            if key_concepts:
                gemini_mcq = self.gemini_service.generate_mcq(chunk_text, key_concepts[0], learning_profile)
                if gemini_mcq:
                    mcq = gemini_mcq
                else:
                    mcq = self._generate_mcq(chunk_text, key_concepts, learning_profile)
            else:
                mcq = self._generate_mcq(chunk_text, key_concepts, learning_profile)
            
            # Calculate estimated study time
            estimated_time = self._calculate_study_time(flashcards, summary, mcq, learning_profile)
            
            return {
                "flashcards": flashcards,
                "summary": summary,
                "mcq": mcq,
                "estimated_study_time_minutes": estimated_time
            }
            
        except Exception as e:
            raise Exception(f"Learning item generation failed: {str(e)}")
    
    def _extract_key_concepts(self, text: str) -> List[str]:
        """Extract key concepts from text using NLTK and advanced NLP"""
        concepts = []
        
        try:
            # Tokenize and tag parts of speech
            sentences = sent_tokenize(text)
            for sentence in sentences[:10]:  # Process first 10 sentences
                words = word_tokenize(sentence)
                pos_tags = nltk.pos_tag(words)
                
                # Extract nouns and noun phrases (potential concepts)
                noun_phrases = []
                current_phrase = []
                
                for word, pos in pos_tags:
                    if pos.startswith('NN'):  # Noun
                        current_phrase.append(word)
                    elif current_phrase:
                        if len(current_phrase) > 0:
                            noun_phrases.append(' '.join(current_phrase))
                        current_phrase = []
                
                if current_phrase:
                    noun_phrases.append(' '.join(current_phrase))
                
                concepts.extend(noun_phrases)
                
        except Exception as e:
            # Fallback to regex-based extraction
            pass
        
        # Extract capitalized phrases (potential concepts)
        capitalized_phrases = re.findall(r'\b[A-Z][a-zA-Z\s]*(?:\s+[A-Z][a-zA-Z\s]*)*\b', text)
        concepts.extend([phrase.strip() for phrase in capitalized_phrases if len(phrase.strip()) > 2])
        
        # Extract phrases in quotes
        quoted_phrases = re.findall(r'"([^"]+)"', text)
        concepts.extend(quoted_phrases)
        
        # Extract phrases after definition words
        definition_patterns = [
            r'(?:is|are|refers to|means|defined as|called|known as)\s+([^.!?]+)',
            r'([^.!?]+)\s+(?:is|are|refers to|means|defined as)'
        ]
        
        for pattern in definition_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            concepts.extend([match.strip() for match in matches if len(match.strip()) > 5])
        
        # Clean and filter concepts
        cleaned_concepts = []
        for concept in concepts:
            # Remove stop words and clean
            words = word_tokenize(concept.lower())
            filtered_words = [word for word in words if word not in self.stop_words and len(word) > 2]
            if filtered_words:
                cleaned_concept = ' '.join(filtered_words).title()
                if len(cleaned_concept.split()) <= 5 and len(cleaned_concept) > 3:
                    cleaned_concepts.append(cleaned_concept)
        
        # Remove duplicates and return top concepts
        unique_concepts = list(set(cleaned_concepts))
        return unique_concepts[:10]  # Limit to top 10 concepts
    
    def _generate_flashcards(self, text: str, concepts: List[str], profile: LearningProfile) -> List[Dict[str, str]]:
        """Generate flashcards based on learning profile"""
        flashcards = []
        
        if profile == LearningProfile.ADHD:
            # ADHD: Short, focused flashcards
            max_flashcards = 5
            max_question_length = 50
            max_answer_length = 30
        elif profile == LearningProfile.DYSLEXIA:
            # Dyslexia: Simple language, clear structure
            max_flashcards = 4
            max_question_length = 40
            max_answer_length = 25
        else:
            # Default: Balanced approach
            max_flashcards = 6
            max_question_length = 60
            max_answer_length = 40
        
        # Generate flashcards for key concepts
        for concept in concepts[:max_flashcards]:
            if len(concept) < 3:
                continue
                
            # Find definition in text
            definition = self._find_definition(text, concept)
            
            if not definition:
                definition = f"a key concept related to {concept.lower()}"
            
            # Generate question and answer
            question_template = random.choice(self.flashcard_templates)
            answer_template = random.choice(self.answer_templates)
            
            question = question_template.format(concept=concept)
            answer = answer_template.format(concept=concept, definition=definition)
            
            # Truncate if too long
            if len(question) > max_question_length:
                question = question[:max_question_length-3] + "..."
            if len(answer) > max_answer_length:
                answer = answer[:max_answer_length-3] + "..."
            
            flashcards.append({
                "question": question,
                "answer": answer,
                "difficulty": self._assess_difficulty(concept, definition)
            })
        
        # If not enough concepts, create general flashcards
        while len(flashcards) < max_flashcards:
            general_question = self._generate_general_question(text, profile)
            general_answer = self._generate_general_answer(text, profile)
            
            flashcards.append({
                "question": general_question,
                "answer": general_answer,
                "difficulty": "medium"
            })
        
        return flashcards
    
    def _generate_summary(self, text: str, profile: LearningProfile) -> List[str]:
        """Generate summary points based on learning profile"""
        # Split text into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        if profile == LearningProfile.ADHD:
            # ADHD: Very short, bullet-point style
            max_points = 3
            max_length = 20
        elif profile == LearningProfile.DYSLEXIA:
            # Dyslexia: Simple, clear sentences
            max_points = 3
            max_length = 25
        else:
            # Default: Standard summary
            max_points = 4
            max_length = 30
        
        # Select key sentences
        key_sentences = self._select_key_sentences(sentences, max_points)
        
        # Simplify sentences based on profile
        summary_points = []
        for sentence in key_sentences:
            simplified = self._simplify_sentence(sentence, profile)
            if len(simplified) > max_length:
                simplified = simplified[:max_length-3] + "..."
            summary_points.append(simplified)
        
        return summary_points
    
    def _generate_mcq(self, text: str, concepts: List[str], profile: LearningProfile) -> Dict[str, Any]:
        """Generate multiple choice question"""
        if not concepts:
            # Generate a general MCQ
            question = "What is the main topic of this text?"
            correct_answer = "The main topic"
            distractors = ["A different topic", "Another concept", "Something else"]
        else:
            # Use first concept for MCQ
            concept = concepts[0]
            definition = self._find_definition(text, concept)
            
            if not definition:
                definition = f"a key concept in this text"
            
            question_template = random.choice(self.mcq_templates)
            question = question_template.format(concept=concept)
            correct_answer = definition
            
            # Generate distractors
            distractors = self._generate_distractors(concept, text, profile)
        
        # Ensure options are not too long for neurodiverse learners
        max_option_length = 30 if profile in [LearningProfile.ADHD, LearningProfile.DYSLEXIA] else 40
        
        if len(correct_answer) > max_option_length:
            correct_answer = correct_answer[:max_option_length-3] + "..."
        
        distractors = [d[:max_option_length-3] + "..." if len(d) > max_option_length else d for d in distractors]
        
        # Shuffle options
        options = [correct_answer] + distractors
        random.shuffle(options)
        
        return {
            "question": question,
            "options": options,
            "correct_answer": correct_answer,
            "explanation": f"The correct answer is '{correct_answer}' because it best describes the concept."
        }
    
    def _find_definition(self, text: str, concept: str) -> str:
        """Find definition of a concept in text"""
        # Look for definition patterns
        patterns = [
            rf'{re.escape(concept)}\s+(?:is|are|refers to|means|defined as)\s+([^.!?]+)',
            rf'([^.!?]+)\s+(?:is|are|refers to|means|defined as)\s+{re.escape(concept)}'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                return matches[0].strip()
        
        return ""
    
    def _generate_distractors(self, concept: str, text: str, profile: LearningProfile) -> List[str]:
        """Generate plausible distractors for MCQ"""
        # Extract other concepts as potential distractors
        other_concepts = self._extract_key_concepts(text)
        other_concepts = [c for c in other_concepts if c.lower() != concept.lower()]
        
        distractors = []
        
        # Use other concepts as distractors
        for other_concept in other_concepts[:2]:
            distractors.append(f"a different concept: {other_concept}")
        
        # Add generic distractors
        generic_distractors = [
            "something completely different",
            "an unrelated topic",
            "a different subject"
        ]
        
        distractors.extend(generic_distractors)
        
        return distractors[:3]  # Return exactly 3 distractors
    
    def _select_key_sentences(self, sentences: List[str], max_points: int) -> List[str]:
        """Select key sentences for summary"""
        # Simple heuristic: longer sentences with key words
        scored_sentences = []
        
        for sentence in sentences:
            score = len(sentence.split())  # Longer sentences get higher score
            
            # Bonus for sentences with key words
            key_words = ['important', 'key', 'main', 'primary', 'essential', 'crucial']
            for word in key_words:
                if word.lower() in sentence.lower():
                    score += 10
            
            scored_sentences.append((score, sentence))
        
        # Sort by score and take top sentences
        scored_sentences.sort(reverse=True)
        return [sentence for score, sentence in scored_sentences[:max_points]]
    
    def _simplify_sentence(self, sentence: str, profile: LearningProfile) -> str:
        """Simplify sentence based on learning profile"""
        if profile == LearningProfile.DYSLEXIA:
            # Remove complex punctuation and long words
            sentence = re.sub(r'[;:]', ',', sentence)
            sentence = re.sub(r'--', '-', sentence)
            
            # Replace long words with shorter alternatives
            word_replacements = {
                'consequently': 'so',
                'furthermore': 'also',
                'nevertheless': 'but',
                'subsequently': 'then',
                'approximately': 'about'
            }
            
            for long_word, short_word in word_replacements.items():
                sentence = sentence.replace(long_word, short_word)
        
        return sentence.strip()
    
    def _generate_general_question(self, text: str, profile: LearningProfile) -> str:
        """Generate a general question about the text"""
        if profile == LearningProfile.ADHD:
            return "What is the main point?"
        elif profile == LearningProfile.DYSLEXIA:
            return "What is this about?"
        else:
            return "What is the main topic discussed?"
    
    def _generate_general_answer(self, text: str, profile: LearningProfile) -> str:
        """Generate a general answer about the text"""
        # Extract first meaningful sentence
        sentences = re.split(r'[.!?]+', text)
        for sentence in sentences:
            if len(sentence.strip()) > 10:
                return sentence.strip()[:30] + "..."
        
        return "The main topic of the text"
    
    def _assess_difficulty(self, concept: str, definition: str) -> str:
        """Assess difficulty level of a concept"""
        # Simple heuristic based on word length and complexity
        concept_words = len(concept.split())
        definition_words = len(definition.split())
        
        if concept_words > 3 or definition_words > 15:
            return "hard"
        elif concept_words > 2 or definition_words > 10:
            return "medium"
        else:
            return "easy"
    
    def _calculate_study_time(self, flashcards: List, summary: List, mcq: Dict, profile: LearningProfile) -> int:
        """Calculate estimated study time in minutes"""
        base_time = 0
        
        # Time for flashcards
        flashcard_time = len(flashcards) * 2  # 2 minutes per flashcard
        
        # Time for summary
        summary_time = len(summary) * 1  # 1 minute per summary point
        
        # Time for MCQ
        mcq_time = 3  # 3 minutes for MCQ
        
        total_time = flashcard_time + summary_time + mcq_time
        
        # Adjust based on learning profile
        if profile == LearningProfile.ADHD:
            # ADHD students might need more time due to attention challenges
            total_time = int(total_time * 1.5)
        elif profile == LearningProfile.DYSLEXIA:
            # Dyslexic students might need more time for reading
            total_time = int(total_time * 1.3)
        
        return max(5, min(60, total_time))  # Between 5 and 60 minutes
