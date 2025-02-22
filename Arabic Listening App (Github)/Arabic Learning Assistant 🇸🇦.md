# Arabic Learning Assistant 🇸🇦

The **Arabic Learning Assistant** is a Streamlit-based web application designed to help users learn Arabic through interactive features like chat-based learning, YouTube transcript processing, and structured data analysis. It leverages free-tier frameworks like Hugging Face Transformers and ChromaDB for natural language processing and vector storage.

------

## Features ✨

- **Interactive Chat**: Chat with an Arabic GPT model to learn grammar, vocabulary, and cultural aspects.
- **YouTube Transcript Processing**: Download and analyze Arabic YouTube video transcripts.
- **Structured Data Extraction**: Extract and structure dialogue from transcripts for further analysis.
- **RAG System**: Use Retrieval-Augmented Generation (RAG) to provide context-aware responses.
- **Interactive Learning**: Practice Arabic through dialogues, quizzes, and listening exercises.

------

## Tech Stack 🫠

- **Frontend**: Streamlit
- **Backend**: Python
- **NLP**: Hugging Face Transformers (`aragpt2-base`)
- **Vector Storage**: ChromaDB
- **YouTube Transcripts**: `youtube-transcript-api`

------

## Installation 🚀

### Prerequisites

- Python 3.9+
- Stable internet connection

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/arabic-learning-assistant.git
   cd arabic-learning-assistant
   ```

2. Set up a virtual environment:

   ```bash
   python -m venv venv
   ```

   - Activate the environment:
     - **Linux/Mac**: `source venv/bin/activate`
     - **Windows**: `venv\Scripts\activate`

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create necessary directories:

   ```bash
   mkdir -p transcripts structured_data
   ```

5. Running the Application 🖥️

   - Start the Streamlit app:

     ```bash
     streamlit run main.py
     ```

   - Open your browser and navigate to `http://localhost:8501`.

------

## Usage Guide 📚

### 1. Chat with Arabic GPT

- Ask questions about Arabic grammar, vocabulary, or culture.
- Example questions:
  - "How do I say 'Where is the train station?' in Arabic?"
  - "Explain the difference between 'ال' and 'أل'."

### 2. Raw Transcript Processing

- Paste a YouTube URL with Arabic content.
- Download and view the transcript.
- Analyze transcript statistics (e.g., total characters, Arabic characters).

### 3. Structured Data

- Extract dialogues and structure transcript data.
- Save structured data as CSV or JSON for further analysis.

### 4. RAG Implementation

- Query the RAG system for context-aware responses.
- Example query: "What is the capital of Saudi Arabia?"

### 5. Interactive Learning

- Practice Arabic through dialogues, quizzes, and listening exercises.
- Receive feedback on your answers.

------

## Project Structure 👤

```
arabic-learning-assistant/
├── backend/
│   ├── __init__.py
│   ├── chat.py
│   ├── get_transcript.py
│   ├── rag.py
│   └── structured_data.py
├── frontend/
│   ├── __init__.py
│   └── interactive.py
├── transcripts/
├── structured_data/
├── main.py
├── requirements.txt
└── README.md
```

------

## Troubleshooting 🪖

### Common Issues

- **Transcript download fails:**

  - Verify the YouTube video has captions.
  - Try a different YouTube URL.

- **Slow model responses:**

  - Reduce the `max_length` parameter in `backend/chat.py`.

- **ChromaDB errors:**

  - Upgrade ChromaDB:

    ```bash
    pip install --upgrade chromadb
    ```

  - Reset the vector store:

    ```bash
    rm -rf chroma-data
    ```

- **Missing dependencies:**

  - Reinstall requirements:

    ```bash
    pip install -r requirements.txt
    ```

------

## Deployment ☁️

### Streamlit Cloud

1. Create an account at Streamlit Cloud.
2. Connect your GitHub repository.
3. Set Python version to 3.9.
4. Deploy!

------

## Acknowledgments 🙏

- Andrew Brown (GenAI Bootcamp Teacher)
- Hugging Face for the Arabic GPT model.
- Streamlit for the web framework.
- ChromaDB for vector storage.
