#!/usr/bin/env python3

import requests
import json

def main():
    """
    Simple test to see if Gemma model works.
    """
    api_url = "http://localhost:8008/api/generate"
    
    payload = {
        "model": "gemma:2b",
        "prompt": "Summarize the key principles of machine learning in 3 short paragraphs.",
        "temperature": 0.7,
        "max_tokens": 500,
        "stream": False
    }
    
    try:
        response = requests.post(api_url, json=payload)
        
        if response.status_code == 200:
            print("Success!")
            try:
                print("Response:", response.json().get("response", "No response field"))
            except json.JSONDecodeError:
                print("Couldn't parse JSON. Raw response:", response.text[:500])
        else:
            print(f"Error: {response.status_code}")
            print(f"Message: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    main()