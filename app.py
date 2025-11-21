#!/usr/bin/env python3
"""
Flask Web Application for Question-and-Answering using LLM API
"""

from flask import Flask, render_template, request, jsonify
import os
import string
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)

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
    """
    api_key = os.getenv('OPENAI_API_KEY') or os.getenv('GROQ_API_KEY')
    api_type = os.getenv('API_TYPE', 'openai')  # openai or groq
    
    if not api_key:
        return {
            'success': False,
            'error': 'API key not configured. Please set OPENAI_API_KEY or GROQ_API_KEY environment variable.'
        }
    
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
        
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        answer = data['choices'][0]['message']['content']
        
        return {
            'success': True,
            'answer': answer
        }
        
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': f'API request failed: {str(e)}'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Error: {str(e)}'
        }

@app.route('/')
def index():
    """
    Render the main page
    """
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    """
    Handle question submission and return answer
    """
    try:
        data = request.get_json()
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({
                'success': False,
                'error': 'Please enter a valid question'
            })
        
        # Preprocess the question
        preprocessed = preprocess_question(question)
        
        # Query LLM API
        api_response = query_llm_api(preprocessed['original'])
        
        if not api_response['success']:
            return jsonify(api_response)
        
        # Return full response
        return jsonify({
            'success': True,
            'original_question': preprocessed['original'],
            'processed_question': preprocessed['processed'],
            'tokens': preprocessed['tokens'],
            'answer': api_response['answer']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
