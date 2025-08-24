# Neurodiverse Learning Backend

A comprehensive ML-powered backend system designed to support neurodiverse students (ADHD, Autism, Dyslexia, Dysgraphia, Dyscalculia) by providing personalized learning experiences.

## 🎯 Core Problem We're Solving

Neurodiverse students struggle with traditional course material because it is often:
- **Long, dense, and overwhelming** (ADHD)
- **Written with complex structures and vocabulary** (Dyslexia, Dysgraphia)
- **Sequential without personalization** (Autism)
- **Heavy on abstract math without step-by-step guidance** (Dyscalculia)

## 🚀 Features

### Task 1: PDF Ingestion & OCR
- Accept PDF uploads (digital and scanned)
- Extract text, headings, tables, math expressions, and images
- OCR processing for scanned documents
- Math expression recognition and processing

### Task 2: Semantic Segmentation & Topic Detection
- Break large text into digestible topics
- Automatic topic labeling using BERTopic
- HDBSCAN clustering for topic grouping
- Confidence scoring for segmentation quality

### Task 3: Learning Item Generation
- Generate flashcards, summaries, and MCQs
- Profile-specific content adaptation
- Enforce constraints for neurodiverse learners
- Estimated study time calculations

### Task 4: Text-to-Speech (TTS)
- Audio generation for dyslexic students
- Multiple voice types (male, female, child)
- Optimized for different learning profiles
- Audio file management and streaming

### Task 5: Text Simplification
- Rewrite complex text into simpler language
- Grade-level appropriate content (5-6 level)
- Readability scoring
- Word count reduction tracking

### Task 6: ADHD Micro-lessons
- Generate 1-fact flashcards
- Strict word limits for attention management
- Small study sets (5 items max)
- Quick engagement activities

### Task 7: Math Parsing & Dyscalculia Support
- Step-by-step math problem solving
- SymPy integration for symbolic computation
- Plain English explanations
- Visual math tools and number lines

### Task 8: Personalization by Profile
- Profile-specific content adaptation
- Accessibility features per learning profile
- User preference integration
- Completion time estimation

### Task 9: AI Learning Roadmap
- Structured learning paths
- Difficulty progression
- Weekly topic distribution
- Profile-specific learning modes

## 🛠️ Technology Stack

- **FastAPI**: Modern, fast web framework
- **PyMuPDF**: PDF processing and text extraction
- **Tesseract OCR**: Image-to-text conversion
- **OpenCV**: Computer vision for math processing (free alternative to Mathpix)
- **NLTK**: Natural language processing (free alternative to OpenAI)
- **Google Gemini API**: Enhanced content generation (free tier - 15 req/min, 1500 req/day)
- **SentenceTransformers**: Semantic embeddings
- **HDBSCAN**: Topic clustering
- **SymPy**: Mathematical computation
- **Coqui TTS**: Text-to-speech generation
- **All services are now FREE** - No paid API keys required!

## 📦 Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd innovact2025_bhejafry/backend
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Create .env file
cp env.example .env

# Optional: Google Gemini API for enhanced content generation
# Get your free API key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# No other API keys needed! The system uses free alternatives:
# - NLTK for text processing (replaces OpenAI)
# - OpenCV for math processing (replaces Mathpix)
# - Coqui TTS for text-to-speech (already free)
```

4. **Install Tesseract OCR**
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract

# Windows
# Download from https://github.com/UB-Mannheim/tesseract/wiki
```

## 🚀 Running the Application

1. **Start the server**
```bash
python main.py
```

2. **Access the API**
- API Documentation: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## 📚 API Endpoints

### Core Processing
- `POST /upload-pdf` - Upload and process PDF documents
- `POST /segment-topics` - Segment text into topics
- `POST /generate-learning-items` - Generate learning materials
- `POST /process-complete` - Complete end-to-end processing

### System Information
- `GET /gemini-stats` - Get Gemini API usage statistics

### Specialized Services
- `POST /generate-tts` - Text-to-speech generation
- `POST /simplify-text` - Text simplification for dyslexia
- `POST /generate-micro-lessons` - ADHD micro-lessons
- `POST /parse-math` - Math problem solving
- `POST /personalize-content` - Content personalization
- `POST /generate-roadmap` - Learning roadmap generation

## 🧪 Testing

Run the test script to verify all services:
```bash
python test_services.py
```

## 🎯 Learning Profiles Supported

### ADHD
- Short, focused content
- Timer-based learning
- Micro-lessons and quick wins
- Visual aids and color coding

### Dyslexia
- Simplified text and vocabulary
- Text-to-speech support
- Dyslexic-friendly fonts
- Audio alternatives

### Autism
- Structured, predictable sequences
- Clear, literal instructions
- Visual schedules
- Reduced sensory stimuli

### Dyscalculia
- Visual math tools
- Step-by-step explanations
- Concrete examples
- Number line visualizations

### Dysgraphia
- Voice input options
- Multiple choice formats
- Spell-check and prediction
- Minimal writing requirements

### Neurotypical
- Standard learning formats
- Mixed content types
- Traditional assessments
- Balanced approach

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: OpenAI API key for content generation
- `MATHPIX_APP_ID`: Mathpix app ID for math OCR
- `MATHPIX_APP_KEY`: Mathpix app key for math OCR

### Service Configuration
Each service can be configured through its respective class:
- PDF processing parameters
- TTS voice settings
- Math solving complexity levels
- Personalization rules

## 📊 Performance Considerations

- **PDF Processing**: Large PDFs may take 30-60 seconds
- **TTS Generation**: Audio files generated on-demand
- **Math Solving**: Complex equations may take 5-10 seconds
- **Topic Segmentation**: Depends on text length and complexity

## 🔒 Security

- File upload validation
- API key management
- Input sanitization
- Error handling without information leakage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- FastAPI community for the excellent web framework
- PyMuPDF for robust PDF processing
- SentenceTransformers for semantic understanding
- SymPy for mathematical computation
- Coqui TTS for open-source text-to-speech

## 📞 Support

For questions or support, please open an issue in the repository or contact the development team.
