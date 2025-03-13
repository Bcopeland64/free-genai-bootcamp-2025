import os
import subprocess
import threading
import time
import webbrowser

def start_backend():
    """Start the Flask backend server"""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run(["python3", "-m", "backend.app"])

def start_frontend():
    """Start the Streamlit frontend"""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run(["streamlit", "run", "frontend/app.py"])

def open_browser():
    """Open the browser after a short delay"""
    time.sleep(3)  # Give servers time to start
    webbrowser.open_new("http://localhost:8501")  # Streamlit default port

if __name__ == "__main__":
    print("Starting AlgoMentor - Interactive DSA Learning Platform")
    print("...")
    
    # Start backend in a separate thread
    backend_thread = threading.Thread(target=start_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Start frontend (this will block until frontend is closed)
    start_frontend()