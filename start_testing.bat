@echo off
echo.
echo 🧠 NEURODIVERSE LEARNING PLATFORM 🧠
echo ======================================
echo AI-Powered Personalized Learning for Neurodiverse Students
echo.
echo 🚀 Starting Local Testing Environment...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH!
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if backend directory exists
if not exist "backend" (
    echo ❌ Backend directory not found!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

REM Check if frontend1 directory exists
if not exist "frontend1" (
    echo ❌ Frontend1 directory not found!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

echo ✅ All directories found!

REM Setup environment file
if not exist "backend\.env" (
    if exist "backend\env.example" (
        echo 📝 Creating .env file from env.example...
        copy "backend\env.example" "backend\.env" >nul
        echo ✅ .env file created successfully!
        echo ⚠️  Remember to add your Gemini API key to the .env file if you want enhanced features!
    ) else (
        echo ❌ env.example not found!
        pause
        exit /b 1
    )
) else (
    echo ✅ .env file already exists!
)

echo.
echo 🌐 FRONTEND SETUP
echo =================
echo The frontend is a simple HTML file that can be opened directly in your browser.
echo.
echo Option 1: Direct File Opening (Recommended)
echo    - Simply double-click frontend1\index.html
echo    - Or right-click and 'Open with' your browser
echo.
echo Option 2: Local Server (If you have issues with Option 1)
echo    - Open a new command prompt
echo    - Navigate to the frontend1 directory
echo    - Run: python -m http.server 3000
echo    - Open: http://localhost:3000
echo.

set /p choice="Would you like to open the frontend now? (y/n): "
if /i "%choice%"=="y" (
    echo 🌐 Opening Frontend...
    start "" "frontend1\index.html"
    echo ✅ Frontend opened in browser!
)

echo.
echo 📋 TESTING INSTRUCTIONS
echo =======================
echo.
echo 1. 🧪 Test Backend Status:
echo    - Click "Check Backend Status" in the frontend
echo    - Verify API is responding and Gemini is available
echo.
echo 2. 🎯 Test Learning Items:
echo    - Select a learning profile (ADHD, Dyslexia, etc.)
echo    - Enter educational content in the text area
echo    - Click "Generate Learning Items"
echo    - Check flashcards, summaries, and MCQs
echo.
echo 3. 📖 Test Text Simplification:
echo    - Enter complex educational text
echo    - Click "Simplify Text"
echo    - Compare original vs simplified versions
echo.
echo 4. ⚡ Test Micro-Lessons:
echo    - Enter topic content
echo    - Click "Create Micro-Lessons"
echo    - Review bite-sized learning items
echo.
echo 5. 🔊 Test Text-to-Speech:
echo    - Enter text content
echo    - Click "Generate Audio"
echo    - Listen to the generated audio file
echo.
echo 6. 🧮 Test Math Parsing:
echo    - Click "Parse Math"
echo    - Review step-by-step solutions
echo.
echo 7. 🚀 Test Complete Pipeline:
echo    - Enter comprehensive content
echo    - Click "Complete Pipeline"
echo    - Test multiple services together
echo.
echo 🎉 All tests should work with free services!
echo.

echo 🔧 STARTING BACKEND
echo ===================
echo Backend will run on: http://localhost:8000
echo API Documentation: http://localhost:8000/docs
echo Press Ctrl+C to stop the backend
echo.

cd backend
python main.py

echo.
echo 🛑 Backend stopped.
pause
