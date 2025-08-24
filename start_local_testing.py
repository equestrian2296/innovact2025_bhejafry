#!/usr/bin/env python3
"""
Local Testing Startup Script for Neurodiverse Learning Platform
This script helps you start the backend and provides instructions for the frontend.
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def print_banner():
    """Print a beautiful banner"""
    banner = """
    🧠 NEURODIVERSE LEARNING PLATFORM 🧠
    ======================================
    AI-Powered Personalized Learning for Neurodiverse Students
    
    🚀 Starting Local Testing Environment...
    """
    print(banner)

def check_requirements():
    """Check if required files exist"""
    backend_dir = Path("backend")
    frontend_dir = Path("frontend1")
    
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return False
    
    if not frontend_dir.exists():
        print("❌ Frontend1 directory not found!")
        return False
    
    if not (backend_dir / "main.py").exists():
        print("❌ Backend main.py not found!")
        return False
    
    if not (frontend_dir / "index.html").exists():
        print("❌ Frontend index.html not found!")
        return False
    
    print("✅ All required files found!")
    return True

def setup_environment():
    """Setup environment file if needed"""
    backend_dir = Path("backend")
    env_example = backend_dir / "env.example"
    env_file = backend_dir / ".env"
    
    if not env_file.exists():
        if env_example.exists():
            print("📝 Creating .env file from env.example...")
            try:
                import shutil
                shutil.copy(env_example, env_file)
                print("✅ .env file created successfully!")
                print("⚠️  Remember to add your Gemini API key to the .env file if you want enhanced features!")
            except Exception as e:
                print(f"❌ Failed to create .env file: {e}")
        else:
            print("❌ env.example not found! Please create it manually.")
            return False
    else:
        print("✅ .env file already exists!")
    
    return True

def start_backend():
    """Start the backend server"""
    print("\n🔧 Starting Backend Server...")
    print("   Backend will run on: http://localhost:8000")
    print("   API Documentation: http://localhost:8000/docs")
    print("   Press Ctrl+C to stop the backend")
    print("-" * 50)
    
    try:
        # Change to backend directory and start the server
        os.chdir("backend")
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Backend stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Backend failed to start: {e}")
        return False
    except FileNotFoundError:
        print("❌ Python executable not found!")
        return False
    
    return True

def open_frontend():
    """Open the frontend in browser"""
    frontend_path = Path("frontend1/index.html").absolute()
    
    print(f"\n🌐 Opening Frontend...")
    print(f"   Frontend file: {frontend_path}")
    print("   If browser doesn't open automatically, manually open the file above")
    
    try:
        webbrowser.open(f"file://{frontend_path}")
        print("✅ Frontend opened in browser!")
    except Exception as e:
        print(f"❌ Failed to open browser: {e}")
        print(f"   Please manually open: {frontend_path}")

def print_instructions():
    """Print testing instructions"""
    instructions = """
    📋 TESTING INSTRUCTIONS
    =======================
    
    1. 🧪 Test Backend Status:
       - Click "Check Backend Status" in the frontend
       - Verify API is responding and Gemini is available
    
    2. 🎯 Test Learning Items:
       - Select a learning profile (ADHD, Dyslexia, etc.)
       - Enter educational content in the text area
       - Click "Generate Learning Items"
       - Check flashcards, summaries, and MCQs
    
    3. 📖 Test Text Simplification:
       - Enter complex educational text
       - Click "Simplify Text"
       - Compare original vs simplified versions
    
    4. ⚡ Test Micro-Lessons:
       - Enter topic content
       - Click "Create Micro-Lessons"
       - Review bite-sized learning items
    
    5. 🔊 Test Text-to-Speech:
       - Enter text content
       - Click "Generate Audio"
       - Listen to the generated audio file
    
    6. 🧮 Test Math Parsing:
       - Click "Parse Math"
       - Review step-by-step solutions
    
    7. 🚀 Test Complete Pipeline:
       - Enter comprehensive content
       - Click "Complete Pipeline"
       - Test multiple services together
    
    🎉 All tests should work with free services!
    """
    print(instructions)

def main():
    """Main function"""
    print_banner()
    
    # Check requirements
    if not check_requirements():
        print("❌ Setup failed! Please check the file structure.")
        return
    
    # Setup environment
    if not setup_environment():
        print("❌ Environment setup failed!")
        return
    
    # Open frontend instructions
    print("\n" + "="*60)
    print("🌐 FRONTEND SETUP")
    print("="*60)
    print("The frontend is a simple HTML file that can be opened directly in your browser.")
    print("You have two options:")
    print()
    print("Option 1: Direct File Opening (Recommended)")
    print("   - Simply double-click frontend1/index.html")
    print("   - Or right-click and 'Open with' your browser")
    print()
    print("Option 2: Local Server (If you have issues with Option 1)")
    print("   - Open a new terminal/command prompt")
    print("   - Navigate to the frontend1 directory")
    print("   - Run: python -m http.server 3000")
    print("   - Open: http://localhost:3000")
    print()
    
    # Ask user preference
    choice = input("Would you like to open the frontend now? (y/n): ").lower().strip()
    if choice in ['y', 'yes']:
        open_frontend()
    
    # Print instructions
    print_instructions()
    
    # Start backend
    print("\n" + "="*60)
    print("🔧 STARTING BACKEND")
    print("="*60)
    start_backend()

if __name__ == "__main__":
    main()
