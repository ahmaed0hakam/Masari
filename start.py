#!/usr/bin/env python3
"""
Comprehensive start script for Masari Learning Platform
"""

import os
import sys
import subprocess
from pathlib import Path

def check_environment():
    """Check if the environment is properly set up"""
    print("🔍 Checking environment...")
    
    # Check if virtual environment exists
    venv_path = Path("venv")
    if not venv_path.exists():
        print("❌ Virtual environment not found!")
        print("Please run: python setup.py")
        return False
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found. Creating default...")
        create_env_file()
    
    # Check if database exists
    db_path = Path("instance/database.db")
    if not db_path.exists():
        print("⚠️  Database not found. Initializing...")
        init_database()
    
    print("✅ Environment check completed!")
    return True

def create_env_file():
    """Create a default .env file"""
    env_content = """# Masari Learning Platform Environment Variables
# Get your free HuggingFace API key from: https://huggingface.co/settings/tokens
HUGGINGFACE_API_KEY=hf_xxx

# Flask configuration
FLASK_APP=run.py
FLASK_ENV=development
"""
    Path(".env").write_text(env_content)
    print("✅ Created .env file")
    print("⚠️  Please update HUGGINGFACE_API_KEY with your API key")

def init_database():
    """Initialize the database"""
    try:
        result = subprocess.run([sys.executable, "init_db.py"], 
                              capture_output=True, text=True, check=True)
        print("✅ Database initialized successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Database initialization failed: {e}")
        return False
    return True

def run_application():
    """Run the Flask application"""
    print("🚀 Starting Masari Learning Platform...")
    
    # Set environment variables
    os.environ['FLASK_APP'] = 'run.py'
    os.environ['FLASK_ENV'] = 'development'
    
    try:
        # Run the application
        subprocess.run([sys.executable, "run.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Application failed to start: {e}")
        return False
    
    return True

def main():
    """Main function"""
    print("🎓 Masari Learning Platform")
    print("=" * 40)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Run the application
    if not run_application():
        sys.exit(1)

if __name__ == '__main__':
    main() 