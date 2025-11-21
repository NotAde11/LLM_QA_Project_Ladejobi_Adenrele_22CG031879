#!/usr/bin/env python3
"""
CLI Application for Question-and-Answering using LLM API
"""

import os
import re
import string
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

def preprocess_question(question):
    """
    Apply basic preprocessing to the question:
    - Lowercasing
    - Tokenization
    - Punctuation removal
    """
    # Store original for comparison
    original = question
    
    # Lowercase
    processed = question.lower()
    
    # Remove punctuation
    processed = processed.translate(str.maketrans('', '', string.punctuation))
    
    # Tokenization (split into words)
    tokens = processed.split()
    
    # Rejoin tokens
    processed_text = ' '.join(tokens)
    
    return {
        'original': original,
        'processed': processed_text,
        'tokens': tokens
    }

def query_llm_api(question):
    """
    Send question to LLM API and get response
    Using OpenAI API (can be easily swapped with Groq, Cohere, etc.)
    """
    api_key = os.getenv('OPENAI_API_KEY') or os.getenv('GROQ_API_KEY')
    api_type = os.getenv('API_TYPE', 'openai')  # openai or groq
    
    if not api_key:
        return "Error: API key not found. Please set OPENAI_API_KEY or GROQ_API_KEY in .env file"
    
    try:
        if api_type == 'groq':
            # Groq API
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "llama3-8b-8192",
                "messages": [
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 1024
            }
        else:
            # OpenAI API
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "user",
                        "content": question
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 1024
            }
        
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        data = response.json()
        answer = data['choices'][0]['message']['content']
        return answer
        
    except requests.exceptions.RequestException as e:
        return f"Error querying API: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    """
    Main CLI loop
    """
    print("=" * 60)
    print("LLM Question-and-Answering System (CLI)")
    print("=" * 60)
    print("\nType 'quit' or 'exit' to end the session\n")
    
    while True:
        # Get user input
        question = input("Enter your question: ").strip()
        
        if not question:
            print("Please enter a valid question.\n")
            continue
        
        if question.lower() in ['quit', 'exit']:
            print("\nGoodbye!")
            break
        
        # Preprocess the question
        print("\n--- Preprocessing ---")
        preprocessed = preprocess_question(question)
        print(f"Original: {preprocessed['original']}")
        print(f"Processed: {preprocessed['processed']}")
        print(f"Tokens: {preprocessed['tokens']}")
        
        # Query LLM API
        print("\n--- Querying LLM API ---")
        answer = query_llm_api(preprocessed['original'])
        
        # Display answer
        print("\n--- Answer ---")
        print(answer)
        print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    main()
