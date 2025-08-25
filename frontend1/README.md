# Frontend1 - ML Backend Testing Interface

A simple, beautiful HTML frontend for testing the neurodiverse learning ML backend capabilities locally.

## 🚀 Quick Start

1. **Start the Backend**
   ```bash
   cd backend
   python main.py
   ```
   The backend will run on `http://localhost:8000`

2. **Open the Frontend**
   - Simply open `index.html` in your web browser
   - Or serve it with a local server:
     ```bash
     # Using Python
     python -m http.server 3000
     
     # Using Node.js
     npx serve .
     
     # Using PHP
     php -S localhost:3000
     ```

3. **Test the ML Services**
   - Click "Check Backend Status" to verify connection
   - Select a learning profile (ADHD, Dyslexia, etc.)
   - Enter educational content in the text area
   - Use the test buttons to try different ML services

## 🧪 Available Tests

### Core ML Services
- **Generate Learning Items** - Creates flashcards, summaries, and MCQs
- **Simplify Text** - Rewrites content for better readability
- **Create Micro-Lessons** - Generates ADHD-friendly bite-sized content
- **Generate Audio** - Converts text to speech
- **Parse Math** - Solves equations with step-by-step explanations
- **Complete Pipeline** - Tests multiple services together

### System Information
- **Backend Status** - API health check
- **Gemini API Stats** - Usage and rate limiting information

## 🎨 Features

- **Responsive Design** - Works on desktop and mobile
- **Real-time Status Updates** - Shows processing state
- **Interactive Results** - Clickable MCQ options with feedback
- **Beautiful UI** - Modern gradient design with smooth animations
- **Error Handling** - Clear error messages and fallbacks

## 🔧 Configuration

The frontend connects to the backend at `http://localhost:8000` by default. To change this:

1. Open `index.html`
2. Find the line: `const API_BASE = 'http://localhost:8000';`
3. Change the URL to match your backend

## 📱 Learning Profiles Supported

- **ADHD** - Attention Deficit Hyperactivity Disorder
- **Dyslexia** - Reading and Language Processing
- **Autism** - Structured Learning and Predictability
- **Dyscalculia** - Mathematical Processing
- **Dysgraphia** - Writing and Expression
- **Neurotypical** - Standard Learning

## 🎯 Example Content

Try this sample text for testing:

```
Algebra is a branch of mathematics that deals with symbols and the rules for manipulating these symbols. In algebra, we use letters like x, y, z to represent unknown values. Variables are letters that represent numbers whose values we don't know or want to represent. Constants are numbers that have fixed values, like 2, 3, 7. Expressions are combinations of variables and constants, like 2x + 3.
```

## 🔍 Troubleshooting

### Backend Not Responding
- Ensure the backend is running on port 8000
- Check that CORS is enabled in the backend
- Verify the API endpoints are working

### Gemini API Issues
- Check the Gemini API key in your `.env` file
- Monitor rate limits (15 requests/minute, 1500/day)
- The system will fallback to rule-based methods if Gemini is unavailable

### Audio Generation
- Audio files are stored in the backend's `audio_files` directory
- Ensure the directory exists and is writable

## 🚀 Next Steps

This frontend is designed for testing and demonstration. For production:

1. **Enhance UI/UX** - Add more interactive features
2. **User Management** - Add login/signup functionality
3. **Progress Tracking** - Save user progress and preferences
4. **Content Management** - Upload and manage educational materials
5. **Analytics** - Track learning progress and engagement

## 📄 License

This is part of the Neurodiverse Learning Platform project.
