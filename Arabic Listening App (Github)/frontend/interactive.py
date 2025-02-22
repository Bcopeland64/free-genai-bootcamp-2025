import streamlit as st
from get_transcript import YouTubeTranscriptDownloader
from chat import ArabicChat
from rag import client
import structured_data  # Our new data processing module
import os

# Initialize components
transcript_downloader = YouTubeTranscriptDownloader(languages=["ar"])
chat_model = ArabicChat()

# Streamlit UI
st.title("🇸🇦 Arabic Language Learning Assistant")

# Sidebar for YouTube processing
with st.sidebar:
    st.header("YouTube Processing")
    youtube_url = st.text_input("Enter YouTube URL (Arabic content):")
    
    if st.button("Process Transcript"):
        if youtube_url:
            with st.spinner("Downloading transcript..."):
                transcript = transcript_downloader.get_transcript(youtube_url)
                video_id = transcript_downloader.extract_video_id(youtube_url)
                
                if transcript:
                    # Save and structure data
                    structured_data.process_transcript(transcript, video_id)
                    
                    # Add to ChromaDB
                    with open(f"./transcripts/{video_id}.txt", "r") as f:
                        text = f.read()
                        client.get_collection("arabic-listening").add(
                            documents=[text],
                            metadatas=[{"source": youtube_url}],
                            ids=[video_id]
                        )
                    st.success("Transcript processed and stored!")
                else:
                    st.error("Failed to download transcript")

# Main chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about Arabic content:"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = chat_model.generate_response(prompt)
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})