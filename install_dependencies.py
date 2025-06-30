#!/usr/bin/env python3
"""
SignSafe Dependency Installer
Simple script to install all required dependencies for SignSafe
"""

import subprocess
import sys
import os
from pathlib import Path

def install_package(package):
    """Install a single package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ Installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install {package}: {e}")
        return False

def check_pip():
    """Check if pip is available."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"])
        return True
    except subprocess.CalledProcessError:
        print("✗ pip not found. Please install pip first.")
        return False

def main():
    """Main installer function."""
    print("SignSafe Dependency Installer")
    print("=" * 35)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Python 3.8 or higher is required")
        return False
    
    print(f"✓ Using Python {sys.version}")
    
    # Check pip
    if not check_pip():
        return False
    
    # Required packages
    packages = [
        "streamlit>=1.46.1",
        "google-generativeai>=0.8.5",
        "google-genai>=1.23.0",
        "pillow>=11.2.1",
        "pypdf2>=3.0.1",
        "pytesseract>=0.3.13",
        "python-dotenv>=1.1.1",
        "requests>=2.32.4",
        "watchdog>=6.0.0"
    ]
    
    print(f"\nInstalling {len(packages)} packages...")
    print("-" * 35)
    
    failed_packages = []
    for package in packages:
        if not install_package(package):
            failed_packages.append(package)
    
    # Create uploads directory
    uploads_dir = Path("uploads")
    uploads_dir.mkdir(exist_ok=True)
    print(f"✓ Created uploads directory: {uploads_dir.absolute()}")
    
    # Create config template if it doesn't exist
    config_file = Path("config.py")
    config_template = Path("config.template.py")
    
    if not config_file.exists():
        print("✓ Found config.template.py - copy to config.py and update with your API keys")
    
    print("\n" + "=" * 50)
    
    if failed_packages:
        print("Installation completed with errors:")
        for package in failed_packages:
            print(f"  ✗ {package}")
        print("\nYou can try installing failed packages manually:")
        print(f"  pip install {' '.join(failed_packages)}")
    else:
        print("All dependencies installed successfully!")
    
    print("\nNext steps:")
    print("1. Copy config.template.py to config.py and update with your API keys")
    print("2. Run the application: streamlit run app.py")
    print("\nThe app will be available at: http://localhost:8501")
    
    return len(failed_packages) == 0

if __name__ == "__main__":
    success = main()
    if not success:
        print("\nSome packages failed to install. Check the errors above.")
        sys.exit(1)
    else:
        print("\nReady to run SignSafe!")