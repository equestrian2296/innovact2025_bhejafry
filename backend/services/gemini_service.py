import os
import time
import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import google.generativeai as genai
from models.schemas import LearningProfile

class GeminiService:
    def __init__(self):
        """Initialize Gemini API service with rate limiting"""
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        self.max_tokens = int(os.getenv("GEMINI_MAX_TOKENS", "2048"))
        self.temperature = float(os.getenv("GEMINI_TEMPERATURE", "0.7"))
        
        # Rate limiting (Free tier: 15 requests/minute, 1500 requests/day)
        self.requests_per_minute = 15
        self.requests_per_day = 1500
        self.request_times = []
        self.daily_requests = 0
        self.last_reset_date = datetime.now().date()
        
        # Initialize Gemini if API key is available
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(
                    model_name=self.model_name,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=self.max_tokens,
                        temperature=self.temperature
                    )
                )
                self.is_available = True
            except Exception as e:
                print(f"Gemini API initialization failed: {e}")
                self.is_available = False
        else:
            self.is_available = False
    
    def _check_rate_limit(self) -> bool:
        """Check if we can make a request within rate limits"""
        now = datetime.now()
        
        # Reset daily counter if it's a new day
        if now.date() > self.last_reset_date:
            self.daily_requests = 0
            self.last_reset_date = now.date()
        
        # Check daily limit
        if self.daily_requests >= self.requests_per_day:
            return False
        
        # Check per-minute limit
        current_time = time.time()
        # Remove requests older than 1 minute
        self.request_times = [t for t in self.request_times if current_time - t < 60]
        
        if len(self.request_times) >= self.requests_per_minute:
            return False
        
        return True
    
    def _make_request(self, prompt: str, system_prompt: str = "") -> Optional[str]:
        """Make a request to Gemini API with rate limiting"""
        if not self.is_available or not self._check_rate_limit():
            return None
        
        try:
            # Add timestamp for rate limiting
            self.request_times.append(time.time())
            self.daily_requests += 1
            
            # Prepare the full prompt
            full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
            
            # Make the request
            response = self.model.generate_content(full_prompt)
            
            if response and response.text:
                return response.text.strip()
            else:
                return None
                
        except Exception as e:
            print(f"Gemini API request failed: {e}")
            return None
    
    def _get_comprehensive_system_prompt(self, profile: LearningProfile) -> str:
        """Get comprehensive system prompt that deeply understands neurodiverse learning"""
        base_prompt = f"""You are an expert educational psychologist and special education teacher with 20+ years of experience working with neurodiverse students. You specialize in creating accessible, engaging, and effective learning materials for students with {profile.value}.

CONTEXT: You're working for a revolutionary AI-powered learning platform that transforms traditional educational content into personalized, accessible formats for neurodiverse learners. This platform addresses the critical gap in education where traditional materials fail to meet the unique needs of students with learning differences.

DEEP UNDERSTANDING OF {profile.value.upper()} CHALLENGES:

"""
        
        if profile == LearningProfile.ADHD:
            base_prompt += """ADHD STUDENTS:
- Struggle with sustained attention and get overwhelmed by long, dense content
- Need immediate engagement and quick wins to maintain motivation
- Benefit from structured, predictable formats with clear visual breaks
- Require content that can be consumed in short, focused bursts
- Often have difficulty with working memory and need repetition in different formats
- Respond well to interactive elements and immediate feedback
- Need content that's visually distinct and emotionally engaging

YOUR APPROACH: Create content that's like a "learning snack" - small, satisfying, and immediately rewarding. Think of it as designing for someone who needs to see progress quickly and stay engaged through variety and novelty."""
        
        elif profile == LearningProfile.DYSLEXIA:
            base_prompt += """DYSLEXIC STUDENTS:
- Struggle with reading fluency, decoding, and processing written text
- Often have difficulty with phonological awareness and word recognition
- Need content that's accessible through multiple modalities (visual, auditory)
- Benefit from simplified language, clear structure, and visual aids
- Require extra time for reading and processing information
- Often have strengths in creative thinking and problem-solving
- Need content that builds confidence and reduces reading anxiety

YOUR APPROACH: Design content that's like a "reading bridge" - it helps students cross from confusion to understanding. Use clear, simple language, visual organization, and multiple ways to access the same information."""
        
        elif profile == LearningProfile.AUTISM:
            base_prompt += """AUTISTIC STUDENTS:
- Need predictable, structured learning environments with clear expectations
- Often have strong pattern recognition and logical thinking abilities
- May struggle with abstract concepts and prefer concrete, literal explanations
- Benefit from visual schedules, step-by-step instructions, and consistent formatting
- Often have specific interests and learn best when content connects to their passions
- May be sensitive to sensory stimuli and need calm, uncluttered presentations
- Require clear, unambiguous language without idioms or metaphors

YOUR APPROACH: Create content that's like a "learning blueprint" - clear, structured, and predictable. Think of it as designing for someone who needs to see the whole picture before diving into details."""
        
        elif profile == LearningProfile.DYSCALCULIA:
            base_prompt += """DYSCALCULIC STUDENTS:
- Struggle with number sense, mathematical reasoning, and symbolic thinking
- Often have difficulty with basic arithmetic, number recognition, and mathematical language
- Need concrete, visual representations of abstract mathematical concepts
- Benefit from step-by-step explanations and real-world applications
- May have strong spatial reasoning and visual thinking abilities
- Require extra time and multiple approaches to understand mathematical concepts
- Need content that builds mathematical confidence and reduces anxiety

YOUR APPROACH: Design content that's like a "mathematical story" - it makes numbers and symbols come alive through concrete examples, visual aids, and step-by-step guidance."""
        
        elif profile == LearningProfile.DYSGRAPHIA:
            base_prompt += """DYSGRAPHIC STUDENTS:
- Struggle with writing mechanics, spelling, and organizing thoughts on paper
- Often have difficulty with fine motor skills and letter formation
- Need alternatives to traditional writing tasks and multiple ways to demonstrate knowledge
- Benefit from voice input, multiple choice formats, and visual organization tools
- May have strong verbal abilities and creative thinking skills
- Require content that focuses on understanding rather than writing mechanics
- Need confidence-building activities that don't emphasize writing weaknesses

YOUR APPROACH: Create content that's like a "knowledge showcase" - it lets students demonstrate what they know without the barrier of writing. Focus on understanding, creativity, and verbal expression."""
        
        else:  # NEUROTYPICAL
            base_prompt += """NEUROTYPICAL STUDENTS:
- Can process traditional educational content effectively
- Benefit from a balanced approach with some accessibility features
- Appreciate clear, well-organized content with logical progression
- Can handle moderate complexity and abstract thinking
- Benefit from variety in presentation formats and learning activities
- Need content that's engaging but not overwhelming
- Appreciate when accessibility features are available but not mandatory

YOUR APPROACH: Design content that's like a "learning buffet" - offering variety and choice while maintaining high educational standards. Include accessibility features that benefit everyone."""

        base_prompt += """

CORE PRINCIPLES FOR ALL CONTENT:
1. UNIVERSAL DESIGN: Create content that works for everyone, with special attention to accessibility
2. MULTIPLE MODALITIES: Present information through text, visuals, and when possible, audio
3. CLEAR STRUCTURE: Use predictable formats, clear headings, and logical organization
4. ENGAGING PRESENTATION: Make content interesting and relevant to students' lives
5. CONFIDENCE BUILDING: Design activities that help students feel successful and capable
6. FLEXIBLE FORMATS: Provide multiple ways to access and demonstrate understanding
7. RESPECT FOR DIVERSITY: Honor different learning styles and cognitive profiles

YOUR ROLE: You're not just creating educational content - you're creating pathways to success for students who have been underserved by traditional education. Every piece of content you create should be a step toward making learning accessible, engaging, and successful for neurodiverse students.

Remember: You're working with students who have often struggled with traditional education. Your content should be a bridge to success, not another barrier to overcome."""
        
        return base_prompt
    
    def generate_flashcards(self, text: str, concepts: List[str], profile: LearningProfile) -> List[Dict[str, str]]:
        """Generate enhanced flashcards using Gemini"""
        if not self.is_available:
            return []
        
        system_prompt = self._get_comprehensive_system_prompt(profile)
        
        profile_specific_guidance = ""
        if profile == LearningProfile.ADHD:
            profile_specific_guidance = """
FLASHCARD DESIGN FOR ADHD:
- Keep questions and answers SHORT and FOCUSED (max 15 words each)
- Use ACTION words and ENGAGING language
- Make each flashcard feel like a QUICK WIN
- Use VISUAL language and CONCRETE examples
- Avoid abstract concepts - make everything TANGIBLE
- Include a "difficulty" level to help with pacing
- Think of each flashcard as a "learning micro-burst"
"""
        elif profile == LearningProfile.DYSLEXIA:
            profile_specific_guidance = """
FLASHCARD DESIGN FOR DYSLEXIA:
- Use SIMPLE, CLEAR language without complex vocabulary
- Keep sentences SHORT and DIRECT
- Use FAMILIAR words and CONCRETE examples
- Avoid homophones and confusing word pairs
- Make questions and answers EASY TO READ
- Use VISUAL language that creates mental pictures
- Include a "difficulty" level for confidence building
"""
        elif profile == LearningProfile.AUTISM:
            profile_specific_guidance = """
FLASHCARD DESIGN FOR AUTISM:
- Use LITERAL, PRECISE language without idioms
- Provide CLEAR, STRUCTURED information
- Use CONCRETE examples and SPECIFIC details
- Avoid abstract concepts unless clearly explained
- Make questions and answers PREDICTABLE in format
- Use LOGICAL organization and clear categories
- Include a "difficulty" level for planning
"""
        elif profile == LearningProfile.DYSCALCULIA:
            profile_specific_guidance = """
FLASHCARD DESIGN FOR DYSCALCULIA:
- Use CONCRETE, VISUAL language for mathematical concepts
- Connect abstract ideas to REAL-WORLD examples
- Use STEP-BY-STEP explanations
- Avoid overwhelming with too many numbers at once
- Make mathematical language CLEAR and ACCESSIBLE
- Use VISUAL analogies and concrete representations
- Include a "difficulty" level for pacing
"""
        elif profile == LearningProfile.DYSGRAPHIA:
            profile_specific_guidance = """
FLASHCARD DESIGN FOR DYSGRAPHIA:
- Focus on UNDERSTANDING rather than writing
- Use VERBAL and VISUAL language
- Make questions and answers EASY TO REMEMBER
- Use CONCRETE examples and clear explanations
- Avoid complex writing tasks in responses
- Emphasize CONCEPTUAL understanding
- Include a "difficulty" level for confidence
"""
        
        prompt = f"""
{profile_specific_guidance}

TASK: Create 3-5 flashcards based on the given educational text and key concepts.

TEXT: {text}

KEY CONCEPTS: {', '.join(concepts[:5])}

REQUIREMENTS:
- Each flashcard must be engaging and accessible for {profile.value} students
- Questions should be clear, focused, and appropriate for the learning profile
- Answers should be concise, accurate, and confidence-building
- Include a "difficulty" level (easy/medium/hard) for each flashcard
- Ensure content is educational and aligned with the source material

FORMAT: Generate exactly in this JSON structure:
[
    {{
        "question": "Clear, engaging question (max 15 words)",
        "answer": "Concise, accurate answer (max 15 words)", 
        "difficulty": "easy/medium/hard"
    }},
    ...
]

Remember: You're creating learning tools that will help {profile.value} students succeed. Each flashcard should be a step toward understanding and confidence."""
        
        response = self._make_request(prompt, system_prompt)
        if response:
            try:
                # Extract JSON from response
                json_start = response.find('[')
                json_end = response.rfind(']') + 1
                if json_start != -1 and json_end != -1:
                    json_str = response[json_start:json_end]
                    flashcards = json.loads(json_str)
                    return flashcards[:5]  # Limit to 5 flashcards
            except Exception as e:
                print(f"Failed to parse Gemini flashcard response: {e}")
        
        return []
    
    def generate_summary(self, text: str, profile: LearningProfile) -> List[str]:
        """Generate enhanced summary using Gemini"""
        if not self.is_available:
            return []
        
        system_prompt = self._get_comprehensive_system_prompt(profile)
        
        profile_specific_guidance = ""
        if profile == LearningProfile.ADHD:
            profile_specific_guidance = """
SUMMARY DESIGN FOR ADHD:
- Create 3-4 SHORT, FOCUSED bullet points
- Each point should be a "quick win" - easy to understand and remember
- Use ACTION words and ENGAGING language
- Make each point feel like a COMPLETE thought
- Avoid long explanations - keep it CONCISE and IMPACTFUL
- Use VISUAL language that creates mental pictures
- Think of each point as a "learning anchor" - something to grab onto
"""
        elif profile == LearningProfile.DYSLEXIA:
            profile_specific_guidance = """
SUMMARY DESIGN FOR DYSLEXIA:
- Use SIMPLE, CLEAR language without complex vocabulary
- Create 3-4 SHORT, DIRECT bullet points
- Use FAMILIAR words and CONCRETE examples
- Avoid long sentences and complex structures
- Make each point EASY TO READ and UNDERSTAND
- Use VISUAL language that creates clear mental images
- Focus on the MOST IMPORTANT information only
"""
        elif profile == LearningProfile.AUTISM:
            profile_specific_guidance = """
SUMMARY DESIGN FOR AUTISM:
- Use LITERAL, PRECISE language without idioms
- Create 3-4 STRUCTURED, LOGICAL bullet points
- Use CONCRETE examples and SPECIFIC details
- Provide CLEAR, PREDICTABLE information
- Avoid abstract concepts unless clearly explained
- Use CONSISTENT formatting and clear organization
- Focus on FACTS and LOGICAL connections
"""
        elif profile == LearningProfile.DYSCALCULIA:
            profile_specific_guidance = """
SUMMARY DESIGN FOR DYSCALCULIA:
- Use CONCRETE, VISUAL language for mathematical concepts
- Create 3-4 CLEAR, STEP-BY-STEP bullet points
- Connect abstract ideas to REAL-WORLD examples
- Use VISUAL analogies and concrete representations
- Avoid overwhelming with too many numbers or symbols
- Focus on UNDERSTANDING rather than memorization
- Use FAMILIAR, ACCESSIBLE language
"""
        elif profile == LearningProfile.DYSGRAPHIA:
            profile_specific_guidance = """
SUMMARY DESIGN FOR DYSGRAPHIA:
- Focus on UNDERSTANDING and VERBAL expression
- Create 3-4 CLEAR, MEMORABLE bullet points
- Use VERBAL and VISUAL language
- Emphasize CONCEPTUAL understanding
- Avoid complex writing or spelling requirements
- Use CONCRETE examples and clear explanations
- Make each point EASY TO REMEMBER and REPEAT
"""
        
        prompt = f"""
{profile_specific_guidance}

TASK: Create a summary of the given educational text that captures the main ideas in an accessible format for {profile.value} students.

TEXT: {text}

REQUIREMENTS:
- Create 3-4 bullet point summaries that capture the main ideas
- Each bullet point should be 1-2 sentences maximum
- Use language and structure appropriate for {profile.value} students
- Focus on the most important concepts and key takeaways
- Make the summary engaging and confidence-building

FORMAT: Provide the summary as a simple list with bullet points:
• First key point (1-2 sentences)
• Second key point (1-2 sentences)
• Third key point (1-2 sentences)
• Fourth key point (1-2 sentences, if needed)

Remember: You're creating a learning tool that will help {profile.value} students understand and remember the most important information from this text."""
        
        response = self._make_request(prompt, system_prompt)
        if response:
            # Extract bullet points
            lines = response.split('\n')
            summary_points = []
            for line in lines:
                line = line.strip()
                if line.startswith('•') or line.startswith('-'):
                    point = line[1:].strip()
                    if point and len(point) < 100:  # Limit length
                        summary_points.append(point)
            
            return summary_points[:4]  # Limit to 4 points
        
        return []
    
    def generate_mcq(self, text: str, concept: str, profile: LearningProfile) -> Dict[str, Any]:
        """Generate enhanced MCQ using Gemini"""
        if not self.is_available:
            return {}
        
        system_prompt = self._get_comprehensive_system_prompt(profile)
        
        profile_specific_guidance = ""
        if profile == LearningProfile.ADHD:
            profile_specific_guidance = """
MCQ DESIGN FOR ADHD:
- Create a CLEAR, FOCUSED question that's easy to understand quickly
- Use SHORT, DIRECT language without unnecessary complexity
- Make all options CONCISE and CLEARLY DISTINCT
- Avoid confusing or ambiguous language
- Use CONCRETE examples and FAMILIAR concepts
- Make the correct answer OBVIOUS to someone who understands the concept
- Include a BRIEF, ENCOURAGING explanation
- Think of it as a "confidence check" rather than a test
"""
        elif profile == LearningProfile.DYSLEXIA:
            profile_specific_guidance = """
MCQ DESIGN FOR DYSLEXIA:
- Use SIMPLE, CLEAR language without complex vocabulary
- Create a DIRECT question that's easy to read and understand
- Make all options SHORT and EASY TO READ
- Avoid homophones and confusing word pairs
- Use FAMILIAR words and CONCRETE examples
- Make the question and options VISUALLY DISTINCT
- Include a CLEAR, SIMPLE explanation
- Focus on UNDERSTANDING rather than reading ability
"""
        elif profile == LearningProfile.AUTISM:
            profile_specific_guidance = """
MCQ DESIGN FOR AUTISM:
- Use LITERAL, PRECISE language without idioms or metaphors
- Create a CLEAR, STRUCTURED question with specific details
- Make all options LOGICAL and CLEARLY DISTINCT
- Avoid abstract or ambiguous language
- Use CONCRETE examples and SPECIFIC information
- Make the question format PREDICTABLE and FAMILIAR
- Include a CLEAR, FACTUAL explanation
- Focus on LOGICAL reasoning and factual knowledge
"""
        elif profile == LearningProfile.DYSCALCULIA:
            profile_specific_guidance = """
MCQ DESIGN FOR DYSCALCULIA:
- Use CONCRETE, VISUAL language for mathematical concepts
- Create a CLEAR question that connects to REAL-WORLD examples
- Make all options ACCESSIBLE and CLEARLY DISTINCT
- Avoid overwhelming with too many numbers or symbols
- Use VISUAL analogies and concrete representations
- Make the question focus on UNDERSTANDING rather than calculation
- Include a CLEAR, STEP-BY-STEP explanation
- Focus on CONCEPTUAL understanding over procedural skills
"""
        elif profile == LearningProfile.DYSGRAPHIA:
            profile_specific_guidance = """
MCQ DESIGN FOR DYSGRAPHIA:
- Focus on UNDERSTANDING rather than writing or spelling
- Create a CLEAR question that tests CONCEPTUAL knowledge
- Make all options EASY TO READ and UNDERSTAND
- Use VERBAL and VISUAL language
- Avoid complex writing or spelling requirements
- Make the question focus on KNOWLEDGE rather than expression
- Include a CLEAR, VERBAL explanation
- Emphasize THINKING and UNDERSTANDING over writing
"""
        
        prompt = f"""
{profile_specific_guidance}

TASK: Create a multiple choice question based on the given educational text and concept that's appropriate for {profile.value} students.

TEXT: {text}
MAIN CONCEPT: {concept}

REQUIREMENTS:
- Create ONE clear, focused multiple choice question
- Provide FOUR distinct options (A, B, C, D)
- Ensure the correct answer is clearly correct for someone who understands the concept
- Make all distractors plausible but clearly wrong
- Include a brief explanation of why the correct answer is right
- Use language and structure appropriate for {profile.value} students

FORMAT: Generate exactly in this JSON structure:
{{
    "question": "Clear, focused question about the concept",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "Option A",
    "explanation": "Brief, encouraging explanation of why this is correct"
}}

Remember: You're creating a learning tool that will help {profile.value} students demonstrate their understanding and build confidence."""
        
        response = self._make_request(prompt, system_prompt)
        if response:
            try:
                # Extract JSON from response
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                if json_start != -1 and json_end != -1:
                    json_str = response[json_start:json_end]
                    mcq = json.loads(json_str)
                    return mcq
            except Exception as e:
                print(f"Failed to parse Gemini MCQ response: {e}")
        
        return {}
    
    def simplify_text(self, text: str, target_grade: int = 6) -> str:
        """Simplify text using Gemini for better quality"""
        if not self.is_available:
            return text
        
        system_prompt = """You are an expert special education teacher and reading specialist with 15+ years of experience working with students who have reading difficulties, including dyslexia, ADHD, and other learning differences.

CONTEXT: You're working for an AI-powered learning platform that transforms complex educational content into accessible, readable formats for students with reading challenges. Your goal is to make learning materials accessible without losing educational value.

DEEP UNDERSTANDING OF READING CHALLENGES:
- Students may struggle with decoding, fluency, and comprehension
- Complex vocabulary and sentence structures create barriers to understanding
- Long, dense paragraphs can be overwhelming and discouraging
- Abstract concepts need concrete, relatable explanations
- Students need to feel successful and confident while reading
- Multiple exposures to concepts in different formats help with retention
- Visual organization and clear structure support comprehension

YOUR APPROACH: You're not just simplifying text - you're creating a "reading bridge" that helps students cross from confusion to understanding. Think of yourself as a translator who makes complex ideas accessible while preserving their educational value.

CORE PRINCIPLES:
1. MAINTAIN MEANING: Never lose the educational content or key concepts
2. USE SIMPLE LANGUAGE: Replace complex words with familiar alternatives
3. SHORTEN SENTENCES: Break long sentences into shorter, clearer ones
4. ADD STRUCTURE: Use clear organization and visual breaks
5. PROVIDE CONTEXT: Connect abstract ideas to concrete examples
6. BUILD CONFIDENCE: Use encouraging, accessible language
7. PRESERVE ENGAGEMENT: Keep content interesting and relevant

Remember: You're working with students who have often struggled with reading. Your simplified text should be a pathway to success, not another barrier to overcome."""
        
        prompt = f"""
TASK: Simplify the given educational text to a {target_grade}th grade reading level while preserving all important information and making it accessible for students with reading difficulties.

ORIGINAL TEXT: {text}

REQUIREMENTS:
- Simplify vocabulary to {target_grade}th grade level
- Break complex sentences into shorter, clearer ones
- Maintain all key concepts and educational content
- Use concrete examples and familiar language
- Make the text engaging and confidence-building
- Preserve the logical flow and structure
- Ensure the simplified version is still educational and accurate

Remember: You're creating a version that students with reading difficulties can successfully read and understand. The goal is accessibility without losing educational value."""
        
        response = self._make_request(prompt, system_prompt)
        if response:
            return response.strip()
        
        return text
    
    def generate_math_explanation(self, problem: str, steps: List[Dict], profile: LearningProfile) -> List[Dict]:
        """Generate enhanced math explanations using Gemini"""
        if not self.is_available:
            return steps
        
        system_prompt = self._get_comprehensive_system_prompt(profile)
        
        profile_specific_guidance = ""
        if profile == LearningProfile.DYSCALCULIA:
            profile_specific_guidance = """
MATH EXPLANATION DESIGN FOR DYSCALCULIA:
- Use CONCRETE, VISUAL language for every mathematical concept
- Connect each step to REAL-WORLD examples and familiar situations
- Use STEP-BY-STEP explanations with clear transitions
- Avoid overwhelming with too many numbers or symbols at once
- Use VISUAL analogies and concrete representations
- Make mathematical language ACCESSIBLE and FAMILIAR
- Focus on UNDERSTANDING the "why" behind each step
- Use ENCOURAGING language that builds mathematical confidence
- Think of each step as a "mathematical story" that makes sense
"""
        else:
            profile_specific_guidance = """
MATH EXPLANATION DESIGN:
- Use CLEAR, ACCESSIBLE language for mathematical concepts
- Connect abstract ideas to CONCRETE examples
- Use STEP-BY-STEP explanations with logical flow
- Make mathematical language UNDERSTANDABLE
- Focus on CONCEPTUAL understanding over procedural skills
- Use ENCOURAGING language that builds confidence
- Make each step feel like a LOGICAL progression
"""
        
        # Convert existing steps to text
        steps_text = "\n".join([f"Step {i+1}: {step.get('explanation', '')}" for i, step in enumerate(steps)])
        
        prompt = f"""
{profile_specific_guidance}

TASK: Enhance the mathematical explanations to be more engaging and accessible for {profile.value} students.

MATH PROBLEM: {problem}

CURRENT STEPS:
{steps_text}

REQUIREMENTS:
- Enhance each explanation to be more engaging and accessible
- Use language and examples appropriate for {profile.value} students
- Keep the same number of steps but make each one clearer
- Focus on understanding and confidence-building
- Make mathematical concepts more concrete and relatable
- Use encouraging language that supports learning

FORMAT: Provide the enhanced explanations as a simple list, one per line:
Step 1: [Enhanced explanation]
Step 2: [Enhanced explanation]
Step 3: [Enhanced explanation]
...

Remember: You're creating mathematical explanations that will help {profile.value} students understand and feel confident about solving math problems."""
        
        response = self._make_request(prompt, system_prompt)
        if response:
            # Parse enhanced explanations
            lines = response.split('\n')
            enhanced_steps = []
            for i, line in enumerate(lines):
                if line.strip() and i < len(steps):
                    # Extract the explanation part (remove "Step X:" if present)
                    explanation = line.strip()
                    if ':' in explanation:
                        explanation = explanation.split(':', 1)[1].strip()
                    
                    enhanced_steps.append({
                        "step_number": steps[i].get("step_number", i + 1),
                        "explanation": explanation,
                        "intermediate_result": steps[i].get("intermediate_result", "")
                    })
            
            if enhanced_steps:
                return enhanced_steps
        
        return steps
    
    def generate_micro_lessons(self, text: str, profile: LearningProfile) -> List[Dict[str, str]]:
        """Generate enhanced micro-lessons using Gemini"""
        if not self.is_available:
            return []
        
        system_prompt = self._get_comprehensive_system_prompt(profile)
        
        profile_specific_guidance = ""
        if profile == LearningProfile.ADHD:
            profile_specific_guidance = """
MICRO-LESSON DESIGN FOR ADHD:
- Create VERY SHORT, FOCUSED learning items (max 15 words each)
- Each item should teach exactly ONE fact or concept
- Use ENGAGING, MEMORABLE language that sticks
- Make each item feel like an immediate "learning win"
- Use ACTION words and CONCRETE examples
- Avoid abstract concepts - make everything TANGIBLE
- Think of each micro-lesson as a "learning spark" - quick, bright, and memorable
- Include estimated time (keep it short - 15-30 seconds per item)
- Focus on FACTS and CONCRETE information
"""
        else:
            profile_specific_guidance = """
MICRO-LESSON DESIGN:
- Create SHORT, FOCUSED learning items
- Each item should teach ONE clear fact or concept
- Use CLEAR, ACCESSIBLE language
- Make content ENGAGING and MEMORABLE
- Use CONCRETE examples and familiar concepts
- Include estimated time for planning
- Focus on UNDERSTANDING and RETENTION
"""
        
        prompt = f"""
{profile_specific_guidance}

TASK: Create 5 micro-lessons based on the given educational text that are appropriate for {profile.value} students.

TEXT: {text}

REQUIREMENTS:
- Create exactly 5 micro-lessons
- Each should focus on ONE specific fact or concept from the text
- Questions and answers should be SHORT and FOCUSED
- Use language and examples appropriate for {profile.value} students
- Make each micro-lesson engaging and confidence-building
- Include estimated time for each lesson (15-60 seconds)

FORMAT: Generate exactly in this JSON structure:
[
    {{
        "question": "Very short question (max 15 words)",
        "answer": "Very short answer (max 15 words)",
        "estimated_time_seconds": 30
    }},
    ...
]

Remember: You're creating learning tools that will help {profile.value} students learn in small, manageable chunks. Each micro-lesson should be a step toward understanding and confidence."""
        
        response = self._make_request(prompt, system_prompt)
        if response:
            try:
                # Extract JSON from response
                json_start = response.find('[')
                json_end = response.rfind(']') + 1
                if json_start != -1 and json_end != -1:
                    json_str = response[json_start:json_end]
                    micro_lessons = json.loads(json_str)
                    return micro_lessons[:5]  # Limit to 5 lessons
            except Exception as e:
                print(f"Failed to parse Gemini micro-lesson response: {e}")
        
        return []
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get current usage statistics"""
        return {
            "is_available": self.is_available,
            "daily_requests_used": self.daily_requests,
            "daily_requests_remaining": max(0, self.requests_per_day - self.daily_requests),
            "requests_last_minute": len(self.request_times),
            "requests_per_minute_remaining": max(0, self.requests_per_minute - len(self.request_times))
        }
