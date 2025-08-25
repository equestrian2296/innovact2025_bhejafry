import re
from typing import Dict, Any
from models.schemas import LearningProfile
from services.gemini_service import GeminiService

class TextSimplifier:
    def __init__(self):
        # Initialize Gemini service for enhanced text simplification
        self.gemini_service = GeminiService()
        
        # Word replacement dictionary for simplification
        self.word_replacements = {
            'consequently': 'so',
            'furthermore': 'also',
            'nevertheless': 'but',
            'subsequently': 'then',
            'approximately': 'about',
            'utilize': 'use',
            'facilitate': 'help',
            'implement': 'do',
            'methodology': 'method',
            'paradigm': 'model',
            'comprehensive': 'complete',
            'sophisticated': 'complex',
            'elaborate': 'detailed',
            'conceptualize': 'think',
            'articulate': 'say'
        }
        
        # Sentence complexity patterns
        self.complex_patterns = [
            r'although\s+[^,]+,\s*',
            r'despite\s+[^,]+,\s*',
            r'however,\s*',
            r'nevertheless,\s*',
            r'furthermore,\s*',
            r'in\s+addition,\s*',
            r'moreover,\s*'
        ]
    
    def simplify_text(self, original_text: str, target_grade_level: int = 6) -> Dict[str, Any]:
        """
        Task 5: Text Simplification (Dyslexia Support)
        Rewrite text into shorter, simpler sentences for grade 5-6 level
        """
        try:
            # Try Gemini first for better quality simplification
            gemini_simplified = self.gemini_service.simplify_text(original_text, target_grade_level)
            if gemini_simplified and gemini_simplified != original_text:
                simplified_text = gemini_simplified
            else:
                # Fallback to rule-based simplification
                # Step 1: Break down complex sentences
                simplified_sentences = self._break_complex_sentences(original_text)
                
                # Step 2: Replace complex words
                simplified_sentences = self._replace_complex_words(simplified_sentences)
                
                # Step 3: Adjust for target grade level
                simplified_sentences = self._adjust_for_grade_level(simplified_sentences, target_grade_level)
                
                # Step 4: Join sentences back together
                simplified_text = ' '.join(simplified_sentences)
            
            # Step 5: Calculate metrics
            readability_score = self._calculate_readability(simplified_text)
            word_count_reduction = len(original_text.split()) - len(simplified_text.split())
            
            return {
                "original": original_text,
                "simplified": simplified_text,
                "readability_score": readability_score,
                "word_count_reduction": word_count_reduction
            }
            
        except Exception as e:
            raise Exception(f"Text simplification failed: {str(e)}")
    
    def _break_complex_sentences(self, text: str) -> list:
        """Break complex sentences into simpler ones"""
        sentences = re.split(r'[.!?]+', text)
        simplified_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Split on conjunctions
            conjunctions = ['and', 'but', 'or', 'so', 'because', 'although', 'while']
            parts = [sentence]
            
            for conj in conjunctions:
                new_parts = []
                for part in parts:
                    if conj in part.lower():
                        split_parts = re.split(f'\\b{conj}\\b', part, flags=re.IGNORECASE)
                        new_parts.extend(split_parts)
                    else:
                        new_parts.append(part)
                parts = new_parts
            
            # Split on semicolons and colons
            final_parts = []
            for part in parts:
                if ';' in part:
                    final_parts.extend(part.split(';'))
                elif ':' in part and len(part.split(':')) > 2:
                    final_parts.extend(part.split(':'))
                else:
                    final_parts.append(part)
            
            # Clean up parts
            for part in final_parts:
                part = part.strip()
                if len(part) > 10:  # Only keep meaningful parts
                    simplified_sentences.append(part)
        
        return simplified_sentences
    
    def _replace_complex_words(self, sentences: list) -> list:
        """Replace complex words with simpler alternatives"""
        simplified_sentences = []
        
        for sentence in sentences:
            simplified_sentence = sentence
            
            # Replace complex words
            for complex_word, simple_word in self.word_replacements.items():
                pattern = re.compile(r'\b' + re.escape(complex_word) + r'\b', re.IGNORECASE)
                simplified_sentence = pattern.sub(simple_word, simplified_sentence)
            
            # Remove complex phrases
            for pattern in self.complex_patterns:
                simplified_sentence = re.sub(pattern, '', simplified_sentence, flags=re.IGNORECASE)
            
            simplified_sentences.append(simplified_sentence)
        
        return simplified_sentences
    
    def _adjust_for_grade_level(self, sentences: list, target_grade: int) -> list:
        """Adjust text complexity for target grade level"""
        adjusted_sentences = []
        
        for sentence in sentences:
            # Count syllables and words
            word_count = len(sentence.split())
            syllable_count = self._count_syllables(sentence)
            
            # Calculate Flesch-Kincaid grade level
            if word_count > 0:
                grade_level = 0.39 * (word_count / 1) + 11.8 * (syllable_count / word_count) - 15.59
            else:
                grade_level = 0
            
            # If sentence is too complex, simplify further
            if grade_level > target_grade:
                # Break into shorter sentences
                words = sentence.split()
                if len(words) > 15:
                    # Split at natural break points
                    mid_point = len(words) // 2
                    part1 = ' '.join(words[:mid_point])
                    part2 = ' '.join(words[mid_point:])
                    
                    if len(part1.split()) > 5:
                        adjusted_sentences.append(part1)
                    if len(part2.split()) > 5:
                        adjusted_sentences.append(part2)
                else:
                    adjusted_sentences.append(sentence)
            else:
                adjusted_sentences.append(sentence)
        
        return adjusted_sentences
    
    def _count_syllables(self, text: str) -> int:
        """Count syllables in text (simplified method)"""
        text = text.lower()
        count = 0
        vowels = "aeiouy"
        on_vowel = False
        
        for char in text:
            is_vowel = char in vowels
            if is_vowel and not on_vowel:
                count += 1
            on_vowel = is_vowel
        
        # Adjust for common patterns
        if text.endswith("e"):
            count -= 1
        if count == 0:
            count = 1
        
        return count
    
    def _calculate_readability(self, text: str) -> float:
        """Calculate Flesch Reading Ease score"""
        sentences = len(re.split(r'[.!?]+', text))
        words = len(text.split())
        syllables = self._count_syllables(text)
        
        if sentences > 0 and words > 0:
            # Flesch Reading Ease formula
            score = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
            return round(max(0, min(100, score)), 1)
        else:
            return 0.0
