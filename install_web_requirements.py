#!/usr/bin/env python3
"""
Script to install additional requirements for the web dashboard upload functionality.
"""

import subprocess
import sys
import os

def install_requirements():
    """Install the additional requirements for the web upload functionality."""
    try:
        # Get the path to the requirements file
        requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
        
        # Install the requirements
        print("Installing additional requirements for web upload functionality...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_path])
        print("Additional requirements installed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    install_requirements()