# Megaservice LLM Platform

A modern interface for interacting with Ollama LLM models.

## Features

- Text generation using Ollama models
- Model management (download, selection)
- User-friendly web interface built with Streamlit
- Docker support for easy deployment

## Installation

### Prerequisites

- Python 3.8+
- Docker (optional)

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/megaservice.git
   cd megaservice
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. If using Docker, start the Ollama service:
   ```
   docker-compose up -d
   ```

4. Pull a model:
   ```
   python pull_model.py
   ```

## Usage

Run the application:
```
python app.py
```

Access the web interface at http://localhost:8501

## Models

The application works with [Ollama](https://ollama.com/) models. By default, it uses Gemma 2B, but you can switch to other models in the interface.

## License

MIT
