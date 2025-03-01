import os
import sys
import streamlit as st
import time

# Add the parent directory to the path to import our apps
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from apps import TextGenerator, ModelManager, check_ollama_connection

# Set page configuration
st.set_page_config(
    page_title="Megaservice LLM Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a modern design
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #ffffff;
        border-radius: 8px;
        padding: 10px 16px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4F8BF9;
        color: white;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        font-weight: 600;
    }
    .css-1cpxqw2, .css-1fcdlhc {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 24px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    .stTextInput > div > div > input {
        border-radius: 8px;
    }
    .stSlider > div > div {
        border-radius: 8px;
    }
    .output-container {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        min-height: 200px;
        margin-top: 16px;
    }
    h1, h2, h3 {
        color: #1E3A8A;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🤖 Megaservice LLM Platform")
st.markdown("A modern interface for interacting with Ollama LLM models")

# Check Ollama connection
connection_status = check_ollama_connection()
if not connection_status:
    st.error("⚠️ Unable to connect to Ollama API. Please make sure the Ollama server is running.")
    st.info("Hint: You may need to start the Ollama server using Docker. Check the installation guide for details.")
    st.stop()

# Initialize session state
if 'text_generator' not in st.session_state:
    st.session_state.text_generator = TextGenerator()
if 'model_manager' not in st.session_state:
    st.session_state.model_manager = ModelManager()
if 'generated_text' not in st.session_state:
    st.session_state.generated_text = ""
if 'selected_model' not in st.session_state:
    st.session_state.selected_model = st.session_state.text_generator.model_name
if 'available_models' not in st.session_state:
    st.session_state.available_models = st.session_state.model_manager.get_models()

# Function to update the list of available models
def update_models():
    with st.spinner("Updating model list..."):
        st.session_state.available_models = st.session_state.model_manager.get_models()

# Function to download a model
def download_model():
    model_name = st.session_state.model_to_download
    if model_name:
        with st.spinner(f"Downloading model {model_name}. This might take a while..."):
            success, message = st.session_state.model_manager.download_model(model_name)
            if success:
                st.success(message)
                update_models()
            else:
                st.error(message)

# Function to generate text
def generate_text():
    prompt = st.session_state.prompt
    temperature = st.session_state.temperature
    max_tokens = st.session_state.max_tokens
    
    if not prompt:
        st.error("Please enter a prompt first.")
        return
    
    with st.spinner("Generating text..."):
        try:
            response = st.session_state.text_generator.generate(
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens
            )
            st.session_state.generated_text = response
        except Exception as e:
            st.error(f"Error generating text: {str(e)}")

# Function to change the model
def change_model():
    new_model = st.session_state.model_selector
    st.session_state.text_generator.set_model(new_model)
    st.session_state.selected_model = new_model
    st.success(f"Model changed to {new_model}")

# Create tabs for different functionalities
tab1, tab2 = st.tabs(["Text Generation", "Model Management"])

# Tab 1: Text Generation
with tab1:
    st.header("Text Generation")
    
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("### Prompt")
            st.text_area("Enter your prompt here:", key="prompt", height=150, 
                        placeholder="What would you like the AI to generate? For example: 'Write a short story about a robot learning to feel emotions.'")
        
        with col2:
            st.markdown("### Parameters")
            
            # Model selector
            model_options = [m["name"] for m in st.session_state.available_models] if st.session_state.available_models else [st.session_state.selected_model]
            st.selectbox("Model:", model_options, key="model_selector", 
                        index=model_options.index(st.session_state.selected_model) if st.session_state.selected_model in model_options else 0,
                        on_change=change_model)
            
            # Temperature slider
            st.slider("Temperature:", min_value=0.1, max_value=1.0, value=0.7, step=0.1, key="temperature",
                     help="Higher values make output more random, lower values more deterministic")
            
            # Max tokens slider
            st.slider("Max Tokens:", min_value=100, max_value=4000, value=2000, step=100, key="max_tokens",
                     help="Maximum number of tokens to generate")
    
    # Generate button
    if st.button("Generate Text", key="generate_button", use_container_width=True):
        generate_text()
    
    # Output container
    st.markdown("### Generated Output")
    output_container = st.container()
    with output_container:
        if st.session_state.generated_text:
            st.markdown(f'<div class="output-container">{st.session_state.generated_text}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="output-container"><i>Generated text will appear here</i></div>', unsafe_allow_html=True)

# Tab 2: Model Management
with tab2:
    st.header("Model Management")
    
    # Refresh button for model list
    if st.button("Refresh Model List", key="refresh_button"):
        update_models()
    
    # Display available models
    st.markdown("### Available Models")
    if st.session_state.available_models:
        model_df = [{"Name": model["name"], "Size": f"{model.get('size', 'Unknown')} MB", "Modified": model.get("modified", "Unknown")} 
                   for model in st.session_state.available_models]
        st.table(model_df)
    else:
        st.info("No models found. You may need to download a model first.")
    
    # Download new model
    st.markdown("### Download New Model")
    st.text_input("Enter model name (e.g., llama3.2:1b):", key="model_to_download", 
                placeholder="Enter model identifier from Ollama library")
    
    # Download button
    if st.button("Download Model", key="download_button"):
        download_model()
    
    st.markdown("Visit the [Ollama Library](https://ollama.com/library) to find available models.")

# Footer
st.markdown("---")
st.markdown("Megaservice LLM Platform • Built with Streamlit and Ollama")