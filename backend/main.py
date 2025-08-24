from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from dotenv import load_dotenv

from services.pdf_processor import PDFProcessor
from services.semantic_segmentation import SemanticSegmentation
from services.learning_generator import LearningGenerator
from services.tts_service import TTSService
from services.text_simplifier import TextSimplifier
from services.adhd_micro_lessons import ADHDMicroLessons
from services.math_parser import MathParser
from services.personalization import PersonalizationService
from services.roadmap_generator import RoadmapGenerator
from services.gemini_service import GeminiService
from models.schemas import *

load_dotenv()

app = FastAPI(
    title="Neurodiverse Learning Backend",
    description="ML-powered backend for personalized learning for neurodiverse students",
    version="1.0.0"
)

# CORS middleware - Fixed for fetch issues
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
pdf_processor = PDFProcessor()
semantic_segmentation = SemanticSegmentation()
learning_generator = LearningGenerator()
tts_service = TTSService()
text_simplifier = TextSimplifier()
adhd_micro_lessons = ADHDMicroLessons()
math_parser = MathParser()
personalization_service = PersonalizationService()
roadmap_generator = RoadmapGenerator()
gemini_service = GeminiService()

@app.get("/")
async def root():
    return {"message": "Neurodiverse Learning Backend API"}

@app.get("/gemini-stats")
async def get_gemini_stats():
    """Get Gemini API usage statistics"""
    try:
        stats = gemini_service.get_usage_stats()
        return {
            "gemini_available": stats["is_available"],
            "daily_requests_used": stats["daily_requests_used"],
            "daily_requests_remaining": max(0, stats["requests_per_day"] - stats["daily_requests_used"]),
            "requests_last_minute": stats["requests_last_minute"],
            "requests_per_minute_remaining": max(0, stats["requests_per_minute"] - stats["requests_last_minute"]),
            "rate_limit_info": {
                "free_tier_limit": f"{stats['requests_per_minute']} requests/minute, {stats['requests_per_day']} requests/day",
                "model": gemini_service.model_name
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/set-pdf-mode")
async def set_pdf_mode(request: dict):
    """Set PDF processing mode"""
    try:
        mode = request.get("mode", "text_only")
        pdf_processor.set_processing_mode(mode)
        return {"message": f"PDF processing mode set to: {mode}", "mode": mode}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/upload-pdf", response_model=PDFExtractionResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """Task 1: PDF Ingestion & OCR"""
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="File must be a PDF")
        
        # Save uploaded file temporarily
        temp_path = f"temp/{file.filename}"
        os.makedirs("temp", exist_ok=True)
        
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process PDF
        result = pdf_processor.process_pdf(temp_path)
        
        # Clean up
        os.remove(temp_path)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-text", response_model=PDFExtractionResponse)
async def process_text(request: dict):
    """Process plain text input (alternative to PDF)"""
    try:
        text = request.get("text", "")
        if not text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        result = pdf_processor.process_text_input(text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/segment-topics", response_model=TopicSegmentationResponse)
async def segment_topics(request: TopicSegmentationRequest):
    """Task 2: Semantic Segmentation & Topic Detection"""
    try:
        result = semantic_segmentation.segment_topics(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-learning-items", response_model=LearningItemsResponse)
async def generate_learning_items(request: LearningItemsRequest):
    """Task 3: Learning Item Generation (Flashcards, Summaries, MCQs)"""
    try:
        result = learning_generator.generate_learning_items(
            request.chunk_text, 
            request.learning_profile
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-audio", response_model=TTSResponse)
async def generate_audio(request: TTSRequest):
    """Task 4: Text-to-Speech (TTS)"""
    try:
        result = tts_service.generate_audio(
            request.text,
            request.voice_type,
            request.learning_profile
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/simplify-text", response_model=TextSimplificationResponse)
async def simplify_text(request: TextSimplificationRequest):
    """Task 5: Text Simplification (Dyslexia Support)"""
    try:
        result = text_simplifier.simplify_text(
            request.original_text,
            request.target_grade_level
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-micro-lessons", response_model=MicroLessonsResponse)
async def generate_micro_lessons(request: MicroLessonsRequest):
    """Task 6: ADHD Micro-lessons"""
    try:
        result = adhd_micro_lessons.generate_micro_lessons(
            request.topic_text,
            request.max_items
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/parse-math", response_model=MathParsingResponse)
async def parse_math(request: MathParsingRequest):
    """Task 7: Math Parsing & Dyscalculia Support"""
    try:
        result = math_parser.parse_math_expression(
            request.math_expression,
            request.explanation_level
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/personalize-content", response_model=PersonalizationResponse)
async def personalize_content(request: PersonalizationRequest):
    """Task 8: Personalization by Profile"""
    try:
        result = personalization_service.personalize_content(
            request.content,
            request.learning_profile,
            request.user_preferences
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-roadmap", response_model=RoadmapResponse)
async def generate_roadmap(request: RoadmapRequest):
    """Task 9: AI Learning Roadmap"""
    try:
        result = roadmap_generator.generate_roadmap(
            request.topics,
            request.learning_profile,
            request.study_hours_per_week
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process-complete", response_model=CompletePipelineResponse)
async def process_complete(request: CompletePipelineRequest):
    """Complete pipeline processing"""
    try:
        # Step 1: Process input (PDF or text)
        if request.input_type == "pdf":
            # This would require file upload handling
            raise HTTPException(status_code=400, detail="PDF upload not supported in complete pipeline yet")
        else:
            # Process text input
            extracted_data = pdf_processor.process_text_input(request.content)
        
        # Step 2: Segment topics
        topics = semantic_segmentation.segment_topics(extracted_data["extracted_text"])
        
        # Step 3: Generate learning items for first topic
        if topics["topics"]:
            first_topic = topics["topics"][0]
            learning_items = learning_generator.generate_learning_items(
                first_topic["chunks"][0]["text"],
                request.learning_profile
            )
        else:
            learning_items = learning_generator.generate_learning_items(
                extracted_data["extracted_text"][:500],
                request.learning_profile
            )
        
        # Step 4: Simplify text
        simplified = text_simplifier.simplify_text(
            extracted_data["extracted_text"][:1000],
            6
        )
        
        # Step 5: Generate micro-lessons
        micro_lessons = adhd_micro_lessons.generate_micro_lessons(
            extracted_data["extracted_text"][:500],
            5
        )
        
        # Step 6: Generate roadmap
        roadmap = roadmap_generator.generate_roadmap(
            [topic["topic"] for topic in topics["topics"][:5]],
            request.learning_profile,
            5
        )
        
        return CompletePipelineResponse(
            extracted_data=extracted_data,
            topics=topics,
            learning_items=learning_items,
            simplified_text=simplified,
            micro_lessons=micro_lessons,
            roadmap=roadmap
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Error handlers for better fetch compatibility
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc), "error": "Internal server error"}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error": "HTTP error"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
