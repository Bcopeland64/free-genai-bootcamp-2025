#!/usr/bin/env python3
"""
Megaservice LLM Platform - Main Entry Point
This script launches the Streamlit web interface for the application.
"""

import os
import sys
import subprocess

def main():
    """
    Main entry point for the application.
    Runs the Streamlit frontend.
    """
    frontend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend", "app.py")
    
    try:
        # Run Streamlit
        subprocess.run([
            "streamlit", "run", 
            frontend_path,
            "--server.port=8501",
            "--browser.serverAddress=localhost",
            "--server.headless=true"
        ], check=True)
    except KeyboardInterrupt:
        print("\nExiting Megaservice...")
    except Exception as e:
        print(f"Error running Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()