from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from enum import Enum

class LearningProfile(str, Enum):
    ADHD = "ADHD"
    DYSLEXIA = "DYSLEXIA"
    AUTISM = "AUTISM"
    DYSCALCULIA = "DYSCALCULIA"
    DYSGRAPHIA = "DYSGRAPHIA"
    NEUROTYPICAL = "NEUROTYPICAL"

class VoiceType(str, Enum):
    MALE = "male"
    FEMALE = "female"
    CHILD = "child"

class ExplanationLevel(str, Enum):
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    DETAILED = "detailed"

# PDF Processing Schemas
class PDFExtractionResponse(BaseModel):
    page: int
    heading: str
    paragraphs: List[str]
    equations: List[str]
    images: List[str]
    extracted_text: str
    confidence_score: float

# Topic Segmentation Schemas
class TopicSegmentationRequest(BaseModel):
    extracted_text: str

class TopicChunk(BaseModel):
    id: int
    text: str
    confidence: float

class Topic(BaseModel):
    topic_name: str
    chunks: List[TopicChunk]
    confidence_score: float

class TopicSegmentationResponse(BaseModel):
    topics: List[Topic]
    total_chunks: int

# Learning Items Schemas
class LearningItemsRequest(BaseModel):
    chunk_text: str
    learning_profile: LearningProfile

class Flashcard(BaseModel):
    question: str
    answer: str
    difficulty: str

class MCQ(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    explanation: str

class LearningItemsResponse(BaseModel):
    flashcards: List[Flashcard]
    summary: List[str]
    mcq: MCQ
    estimated_study_time_minutes: int

# TTS Schemas
class TTSRequest(BaseModel):
    text: str
    voice_type: VoiceType = VoiceType.FEMALE

class TTSResponse(BaseModel):
    audio_url: str
    duration_seconds: float
    word_count: int

# Text Simplification Schemas
class TextSimplificationRequest(BaseModel):
    original_text: str
    target_grade_level: int = Field(ge=1, le=12)

class TextSimplificationResponse(BaseModel):
    original: str
    simplified: str
    readability_score: float
    word_count_reduction: int

# ADHD Micro-lessons Schemas
class MicroLessonsRequest(BaseModel):
    topic_text: str
    max_items: int = Field(default=10, ge=1, le=50)

class MicroLesson(BaseModel):
    question: str
    answer: str
    estimated_time_seconds: int

class MicroLessonsResponse(BaseModel):
    micro_lessons: List[MicroLesson]
    total_estimated_time_minutes: int

# Math Parsing Schemas
class MathParsingRequest(BaseModel):
    math_expression: str
    explanation_level: ExplanationLevel = ExplanationLevel.INTERMEDIATE

class MathStep(BaseModel):
    step_number: int
    explanation: str
    intermediate_result: str

class MathParsingResponse(BaseModel):
    problem: str
    steps: List[MathStep]
    final_answer: str
    difficulty_level: str

# Personalization Schemas
class UserPreferences(BaseModel):
    preferred_content_length: str = "medium"  # short, medium, long
    audio_enabled: bool = True
    visual_aids: bool = True
    interactive_elements: bool = True
    repetition_frequency: str = "normal"  # low, normal, high

class PersonalizationRequest(BaseModel):
    content: Any
    learning_profile: LearningProfile
    preferences: UserPreferences

class PersonalizedContent(BaseModel):
    adapted_content: Any
    recommended_format: str
    accessibility_features: List[str]
    estimated_completion_time: int

class PersonalizationResponse(BaseModel):
    personalized_content: PersonalizedContent
    profile_specific_recommendations: List[str]

# Roadmap Schemas
class RoadmapRequest(BaseModel):
    topics: List[str]
    learning_profile: LearningProfile
    study_duration_weeks: int = Field(ge=1, le=52)

class RoadmapWeek(BaseModel):
    week_number: int
    topic: str
    mode: str
    estimated_hours: float
    learning_activities: List[str]

class RoadmapResponse(BaseModel):
    roadmap: List[RoadmapWeek]
    total_estimated_hours: float
    difficulty_progression: str

# Complete Processing Schemas
class CompleteProcessingRequest(BaseModel):
    pdf_path: str
    learning_profile: LearningProfile
    preferences: UserPreferences
    study_duration_weeks: int = 12

class CompleteProcessingResponse(BaseModel):
    pdf_extraction: PDFExtractionResponse
    topic_segmentation: TopicSegmentationResponse
    learning_items: List[Dict[str, Any]]
    personalized_content: PersonalizationResponse
    roadmap: RoadmapResponse
