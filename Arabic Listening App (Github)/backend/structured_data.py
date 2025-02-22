import pandas as pd
import json
from typing import List, Dict
import re

class StructuredDataProcessor:
    def __init__(self):
        self.metadata_fields = {
            "language": "ar",
            "source": "youtube",
            "processed": False
        }

    def transcript_to_dataframe(self, transcript: List[Dict]) -> pd.DataFrame:
        """Convert raw transcript to structured DataFrame"""
        df = pd.DataFrame(transcript)
        df["duration"] = df["duration"].round(2)
        df["word_count"] = df["text"].apply(lambda x: len(x.split()))
        return df

    def extract_linguistic_features(self, text: str) -> Dict:
        """Extract Arabic language features from text"""
        return {
            "arabic_chars_count": len(re.findall(r'[\u0600-\u06FF]', text)),
            "unique_verbs": len(set(re.findall(r'\b\w+َ\w+', text))),  # Simple verb pattern match
            "question_count": text.count("؟"),
            "avg_sentence_length": len(text.split()) / max(1, text.count("."))
        }

    def generate_metadata(self, transcript: List[Dict], video_id: str) -> Dict:
        """Generate structured metadata from transcript"""
        full_text = " ".join([entry["text"] for entry in transcript])
        
        return {
            "video_id": video_id,
            **self.metadata_fields,
            **self.extract_linguistic_features(full_text),
            "total_duration": transcript[-1]["start"] + transcript[-1]["duration"],
            "total_words": len(full_text.split())
        }

    def save_as_csv(self, df: pd.DataFrame, filename: str) -> None:
        """Save structured data to CSV"""
        df.to_csv(f"./structured_data/{filename}.csv", index=False, encoding='utf-8-sig')

    def save_as_json(self, data: Dict, filename: str) -> None:
        """Save structured data to JSON"""
        with open(f"./structured_data/{filename}.json", "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

def process_transcript(transcript: List[Dict], video_id: str) -> None:
    """Main processing function"""
    processor = StructuredDataProcessor()
    
    # Convert to DataFrame
    df = processor.transcript_to_dataframe(transcript)
    
    # Generate metadata
    metadata = processor.generate_metadata(transcript, video_id)
    
    # Save structured data
    processor.save_as_csv(df, video_id)
    processor.save_as_json(metadata, video_id)
    
    print(f"Structured data saved for {video_id}")