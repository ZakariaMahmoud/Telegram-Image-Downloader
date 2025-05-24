#!/usr/bin/env python3

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ All packages installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("✗ Failed to install packages")
        return False

def setup_env_file():
    """Setup environment file"""
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if env_file.exists():
        print("✓ .env file already exists")
        return True
    
    if env_example.exists():
        try:
            with open(env_example, 'r') as f:
                content = f.read()
            
            with open(env_file, 'w') as f:
                f.write(content)
            
            print("✓ Created .env file from template")
            print("⚠ Please edit .env file with your Telegram credentials")
            return True
        except Exception as e:
            print(f"✗ Failed to create .env file: {e}")
            return False
    else:
        print("✗ .env.example file not found")
        return False

def main():
    print("Telegram Image Downloader Setup")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✓ Python {sys.version.split()[0]} detected")
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Setup env file
    if not setup_env_file():
        sys.exit(1)
    
    print("\n" + "=" * 40)
    print("Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file with your Telegram API credentials")
    print("2. Run: python telegram_downloader.py")
    print("3. Run: python image_search.py --image your_image.jpg")

if __name__ == "__main__":
    main()
