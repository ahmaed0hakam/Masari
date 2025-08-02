#!/usr/bin/env python3
"""
Setup script for Masari Learning Platform
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def create_virtual_environment():
    """Create a virtual environment"""
    venv_path = Path("venv")
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    return run_command("python3 -m venv venv", "Creating virtual environment")

def install_dependencies():
    """Install project dependencies"""
    # Determine the correct pip command
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/Mac
        pip_cmd = "venv/bin/pip"
    
    return run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies")

def create_directories():
    """Create necessary directories"""
    directories = ['CVs', 'logs', 'instance']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Directories created successfully!")

def setup_environment():
    """Set up environment variables"""
    env_file = Path(".env")
    if not env_file.exists():
        env_content = """# Masari Learning Platform Environment Variables
# Get your free HuggingFace API key from: https://huggingface.co/settings/tokens
HUGGINGFACE_API_KEY=hf_xxx

# Flask configuration
FLASK_APP=run.py
FLASK_ENV=development
"""
        env_file.write_text(env_content)
        print("✅ Environment file created (.env)")
        print("⚠️  Please update HUGGINGFACE_API_KEY in .env file with your API key")
    else:
        print("✅ Environment file already exists")

def main():
    """Main setup function"""
    print("🚀 Setting up Masari Learning Platform...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Setup environment
    setup_environment()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Get a free HuggingFace API key from: https://huggingface.co/settings/tokens")
    print("2. Update the HUGGINGFACE_API_KEY in the .env file")
    print("3. Run: python3 init_db.py")
    print("4. Run: python3 run.py")
    print("5. Open http://localhost:5000 in your browser")
    print("\n📚 For more information, see README.md")

if __name__ == '__main__':
    main() 