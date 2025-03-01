# Megaservice LLM Platform - Installation Guide

This guide provides step-by-step instructions for setting up and running the Megaservice LLM Platform.

## Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose (for running Ollama)
- Git (optional, for cloning the repository)

## Step 1: Setting Up Ollama

The Megaservice LLM Platform requires Ollama to be running as a backend service.

1. Start by installing Docker if you haven't already:
   ```bash
   # For Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install docker.io docker-compose
   ```

2. Start the Ollama server using Docker:
   ```bash
   HOST_IP=$(hostname -I | awk '{print $1}') NO_PROXY=localhost LLM_ENDPOINT_PORT=9000 LLM_MODEL_ID="llama3.2:1b" docker compose up -d
   ```

   If you want to use a different model, you can change the `LLM_MODEL_ID` value. Available models can be found at the [Ollama Library](https://ollama.com/library).

3. Verify that the Ollama service is running:
   ```bash
   curl http://localhost:8008/api/tags
   ```

## Step 2: Installing the Megaservice LLM Platform

1. Clone or download the Megaservice application.

2. Navigate to the project directory:
   ```bash
   cd megaservice
   ```

3. Set up a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

4. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

5. Configure the application by creating a `.env` file:
   ```bash
   echo "OLLAMA_API_URL=http://localhost:8008/api" > .env
   echo "DEFAULT_MODEL=llama3.2:1b" >> .env
   ```

   If your Ollama server is running on a different host or port, adjust the `OLLAMA_API_URL` value accordingly.

## Step 3: Running the Application

1. Make sure the virtual environment is activated:
   ```bash
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

2. Launch the application:
   ```bash
   python app.py
   ```

   Alternatively, you can run the Streamlit app directly:
   ```bash
   streamlit run frontend/app.py
   ```

3. The application should now be accessible in your web browser at http://localhost:8501

## Troubleshooting

If you encounter issues when running the application, here are some common problems and solutions:

### Connection Error with Ollama API

If the application displays an error about not being able to connect to the Ollama API:

1. Verify that the Ollama server is running:
   ```bash
   curl http://localhost:8008/api/tags
   ```

2. Check that the `OLLAMA_API_URL` in the `.env` file is correct.

3. Ensure there are no firewall rules blocking the connection.

### Model Not Found

If you encounter errors related to missing models:

1. Use the Model Management tab in the application to download the desired model.

2. Alternatively, you can download a model directly through the Ollama API:
   ```bash
   curl http://localhost:8008/api/pull -d '{"model": "llama3.2:1b"}'
   ```

## Additional Configuration

### Custom Models

To use custom models with Ollama, refer to the [Ollama documentation](https://github.com/ollama/ollama/blob/main/docs/modelfile.md) on creating and using Modelfiles.

### Environment Variables

The application supports the following environment variables:

- `OLLAMA_API_URL`: The URL of the Ollama API (default: http://localhost:8008/api)
- `DEFAULT_MODEL`: The default model to use for text generation (default: llama3.2:1b)

These can be set in the `.env` file or passed as environment variables when running the application.