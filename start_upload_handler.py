#!/usr/bin/env python3
"""
Script to start the upload handler for the PowerForecast web dashboard.
"""

import subprocess
import sys
import os

def start_upload_handler():
    """Start the upload handler server."""
    try:
        # Get the path to the upload handler script
        handler_path = os.path.join(os.path.dirname(__file__), 'web_dashboard', 'upload_handler.py')
        
        # Start the upload handler
        print("Starting upload handler server...")
        print("Server will be available at http://localhost:5000")
        print("Press Ctrl+C to stop the server")
        
        subprocess.check_call([sys.executable, handler_path])
        
    except subprocess.CalledProcessError as e:
        print(f"Error starting upload handler: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    start_upload_handler()