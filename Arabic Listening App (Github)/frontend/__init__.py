"""
Arabic Learning Frontend Module

Contains Streamlit UI components and:
- Interactive learning interfaces
- Visualization utilities
- State management
"""

from .interactive import (  # Assuming you have UI components
    render_chat_interface,
    render_transcript_viewer,
    generate_practice_scenarios
)

__all__ = [
    'render_chat_interface',
    'render_transcript_viewer',
    'generate_practice_scenarios'
]

__version__ = "1.0.0-ui"