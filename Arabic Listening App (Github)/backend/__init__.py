"""
Arabic Learning Backend Module

Exports core functionality:
- ArabicChat: Interface for Arabic language model
- YouTubeTranscriptDownloader: YouTube content processor
- RAG utilities: Vector storage and retrieval
- Structured data processors
"""

from .chat import ArabicChat
from .get_transcript import YouTubeTranscriptDownloader
from .rag import client, collection  # ChromaDB components
from .structured_data import StructuredDataProcessor

__all__ = [
    'ArabicChat',
    'YouTubeTranscriptDownloader',
    'StructuredDataProcessor',
    'client',
    'collection'
]

__version__ = "1.0.0-arabic"