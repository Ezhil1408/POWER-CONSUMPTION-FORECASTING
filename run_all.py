#!/usr/bin/env python3
"""
Script to run all services for the Power Consumption Forecasting project in a single command.
"""

import subprocess
import sys
import os
import time

def print_status(message):
    """Print status messages with a consistent format."""
    print(f"[INFO] {message}")

def run_spark_app():
    """Run the main Spark application."""
    try:
        print_status("Starting Spark application...")
        # Get the current directory (project root)
        project_root = os.getcwd()
        spark_process = subprocess.Popen([
            sys.executable, 
            os.path.join(project_root, "forecasting_app.py"), 
            "--power-csv", 
            os.path.join(project_root, "power_consumption_2015_2024_no_building.csv"), 
            "--keep-ui"
        ])
        print_status("Spark application started successfully")
        return spark_process
    except Exception as e:
        print_status(f"Error starting Spark application: {e}")
        return None

def run_upload_handler():
    """Run the upload handler."""
    try:
        print_status("Starting upload handler...")
        # Get the current directory (project root)
        project_root = os.getcwd()
        upload_process = subprocess.Popen([
            sys.executable, 
            os.path.join(project_root, "web_dashboard", "upload_handler.py")
        ])
        print_status("Upload handler started successfully")
        return upload_process
    except Exception as e:
        print_status(f"Error starting upload handler: {e}")
        return None

def run_web_server():
    """Run the web server."""
    try:
        print_status("Starting web server...")
        # Get the web_dashboard directory
        project_root = os.getcwd()
        web_dashboard_dir = os.path.join(project_root, "web_dashboard")
        web_process = subprocess.Popen([
            sys.executable, 
            "-m", 
            "http.server", 
            "8000"
        ], cwd=web_dashboard_dir)
        print_status("Web server started successfully on http://localhost:8000")
        return web_process
    except Exception as e:
        print_status(f"Error starting web server: {e}")
        return None

def main():
    """Main function to run all services."""
    print_status("Starting Power Consumption Forecasting project...")
    print_status("This may take a moment to initialize...")
    
    # Start all services
    spark_process = run_spark_app()
    time.sleep(2)  # Give Spark a moment to start
    
    upload_process = run_upload_handler()
    time.sleep(2)  # Give upload handler a moment to start
    
    web_process = run_web_server()
    
    # Print access information
    print("\n" + "="*50)
    print("PROJECT READY!")
    print("="*50)
    print("Access the web dashboard at: http://localhost:8000")
    print("Spark UI available at: http://localhost:4040 or http://localhost:4041")
    print("Upload handler API at: http://localhost:5000")
    print("\nLogin credentials:")
    print("  Username: admin")
    print("  Password: password")
    print("\nPress Ctrl+C to stop all services")
    print("="*50 + "\n")
    
    try:
        # Wait for all processes
        if spark_process:
            spark_process.wait()
        if upload_process:
            upload_process.wait()
        if web_process:
            web_process.wait()
    except KeyboardInterrupt:
        print_status("Stopping all services...")
        if spark_process:
            spark_process.terminate()
        if upload_process:
            upload_process.terminate()
        if web_process:
            web_process.terminate()
        print_status("All services stopped")

if __name__ == "__main__":
    main()