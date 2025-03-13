# AlgoUstadh Setup Guide

AlgoUstadh is an interactive platform for learning Computer Science fundamentals, including Data Structures & Algorithms, System Design, and Mathematics. This guide will help you set up the project on your local machine.

## Prerequisites

- Python 3.10 or higher
- Pip (Python package installer)
- Git (for cloning the repository)
- A Groq API key (for AI functionality)

## Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/AlgoUstadh.git
cd AlgoUstadh
```

## Step 2: Create and Activate a Virtual Environment

This isolates the project dependencies from your global Python installation.

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

## Step 3: Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

## Step 4: Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
touch .env
```

Open the `.env` file and add your Groq API key:

```
# API Keys
GROQ_API_KEY=your_groq_api_key_here

# Configuration
DEBUG=False
```

You can get a Groq API key by signing up at [Groq.com](https://console.groq.com/).

## Step 5: Initialize the Database (Optional)

If you want to use a local database instead of the JSON files:

```bash
python init_db.py
```

## Step 6: Running the Application

You can run the application in two ways:

### Option 1: Run the complete application (backend and frontend together)

```bash
python main.py
```

This will start both the Flask backend on port 5000 and the Streamlit frontend on port 8501.

### Option 2: Run backend and frontend separately

Open two terminal windows and run:

Terminal 1 (Backend):
```bash
source venv/bin/activate  # If not already activated
python -m backend.app
```

Terminal 2 (Frontend):
```bash
source venv/bin/activate  # If not already activated
streamlit run frontend/app.py
```

## Step 7: Access the Application

Open your web browser and go to:
- Frontend UI: http://localhost:8501
- Backend API: http://localhost:5000/api

## Data Files

The application uses JSON files in the `data/` directory to store topics and problems:
- `topics.json`: Main categories
- `dsa_topics.json`: Data Structures & Algorithms topics
- `system_design_topics.json`: System Design topics
- `math_topics.json`: Mathematics topics
- `math_problems.json`: Sample math problems

## Troubleshooting

### Missing Data Files

If you encounter errors about missing data files, ensure the following files exist in the `data/` directory:
- `topics.json`
- `dsa_topics.json`
- `system_design_topics.json`
- `math_topics.json`
- `math_problems.json`

### API Connectivity Issues

If the frontend shows generic content instead of real data, the backend API is likely not connecting properly. Ensure:
1. The backend Flask server is running on port 5000
2. The API URL in `frontend/app.py` is correctly set to `http://localhost:5000/api`

### AI Functionality Not Working

If the AI-based tutoring and code evaluation features aren't working:
1. Check that your Groq API key is correctly set in the `.env` file
2. Verify that the `groq` Python package is installed
3. Ensure you have internet connectivity (required for API calls to Groq)

## Project Structure

```
AlgoUstadh/
├── agents/                 # AI tutoring agents
│   ├── evaluators/         # Code evaluation agents
│   └── tutors/             # Topic-specific tutors
├── backend/                # Flask backend API
│   ├── api/                # API routes
│   ├── data/               # JSON data files
│   ├── models/             # Database models
│   └── app.py              # Main backend application
├── data/                   # JSON data files
├── frontend/               # Streamlit frontend
│   └── app.py              # Main frontend application
├── venv/                   # Virtual environment
├── .env                    # Environment variables
├── init_db.py              # Database initialization script
├── main.py                 # Script to run both backend and frontend
└── requirements.txt        # Project dependencies
```

## Contributing

If you'd like to contribute, please fork the repository and create a pull request with your changes. Make sure to test your changes thoroughly before submitting.