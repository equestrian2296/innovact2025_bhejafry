#!/usr/bin/env python3
"""
Backend Test Script for Neurodiverse Learning Platform
Tests all endpoints and PDF processing options
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_endpoint(endpoint, method="GET", data=None, description=""):
    """Test a single endpoint"""
    try:
        url = f"{BASE_URL}{endpoint}"
        print(f"\n🧪 Testing: {description}")
        print(f"   URL: {url}")
        
        if method == "GET":
            response = requests.get(url)
        else:
            response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Success: {response.status_code}")
            print(f"   📊 Response: {json.dumps(result, indent=2)[:200]}...")
            return True
        else:
            print(f"   ❌ Failed: {response.status_code}")
            print(f"   📄 Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Connection Error: Backend not running at {BASE_URL}")
        return False
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🧠 Neurodiverse Learning Backend - Test Suite")
    print("=" * 50)
    
    # Test basic connectivity
    print("\n🔧 Testing Basic Connectivity...")
    if not test_endpoint("/", description="Root endpoint"):
        print("❌ Backend is not running. Please start the backend first.")
        return
    
    # Test Gemini stats
    test_endpoint("/gemini-stats", description="Gemini API statistics")
    
    # Test PDF processing modes
    print("\n📄 Testing PDF Processing Modes...")
    test_endpoint("/set-pdf-mode", "POST", {"mode": "text_only"}, "Set text-only mode")
    test_endpoint("/set-pdf-mode", "POST", {"mode": "full_pdf"}, "Set full PDF mode")
    
    # Test text processing
    print("\n📝 Testing Text Processing...")
    sample_text = "Algebra is a branch of mathematics that deals with symbols and the rules for manipulating these symbols. In algebra, we use letters like x, y, z to represent unknown values."
    
    test_endpoint("/process-text", "POST", {"text": sample_text}, "Process text input")
    
    # Test learning items generation
    print("\n🎓 Testing Learning Items Generation...")
    test_endpoint("/generate-learning-items", "POST", {
        "chunk_text": sample_text,
        "learning_profile": "ADHD"
    }, "Generate learning items for ADHD")
    
    # Test text simplification
    print("\n📖 Testing Text Simplification...")
    test_endpoint("/simplify-text", "POST", {
        "original_text": sample_text,
        "target_grade_level": 6
    }, "Simplify text to grade 6 level")
    
    # Test micro-lessons
    print("\n⚡ Testing Micro-Lessons...")
    test_endpoint("/generate-micro-lessons", "POST", {
        "topic_text": sample_text,
        "max_items": 3
    }, "Generate micro-lessons")
    
    # Test TTS
    print("\n🔊 Testing Text-to-Speech...")
    test_endpoint("/generate-audio", "POST", {
        "text": "Hello, this is a test of the text-to-speech system.",
        "voice_type": "FEMALE",
        "learning_profile": "DYSLEXIA"
    }, "Generate audio for dyslexia")
    
    # Test math parsing
    print("\n🧮 Testing Math Parsing...")
    test_endpoint("/parse-math", "POST", {
        "math_expression": "2x + 3 = 7",
        "explanation_level": "BASIC"
    }, "Parse math expression")
    
    # Test topic segmentation
    print("\n📚 Testing Topic Segmentation...")
    test_endpoint("/segment-topics", "POST", {
        "text": sample_text
    }, "Segment topics from text")
    
    # Test personalization
    print("\n👤 Testing Personalization...")
    test_endpoint("/personalize-content", "POST", {
        "content": sample_text,
        "learning_profile": "AUTISM",
        "user_preferences": {"preferred_format": "structured"}
    }, "Personalize content for autism")
    
    # Test roadmap generation
    print("\n🗺️ Testing Roadmap Generation...")
    test_endpoint("/generate-roadmap", "POST", {
        "topics": ["Algebra Basics", "Linear Equations", "Word Problems"],
        "learning_profile": "DYSCALCULIA",
        "study_hours_per_week": 5
    }, "Generate learning roadmap")
    
    # Test complete pipeline
    print("\n🚀 Testing Complete Pipeline...")
    test_endpoint("/process-complete", "POST", {
        "content": sample_text,
        "learning_profile": "NEUROTYPICAL",
        "input_type": "text"
    }, "Complete pipeline processing")
    
    print("\n" + "=" * 50)
    print("🎉 Backend test suite completed!")
    print("📋 Check the results above for any failures.")
    print("💡 If all tests pass, your backend is ready for frontend integration!")

if __name__ == "__main__":
    main()
