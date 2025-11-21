# LLM Question & Answer System

A complete Question-and-Answering system that connects to Large Language Model APIs, featuring both a CLI application and a Flask web interface.

## Features

- **CLI Application**: Command-line interface for asking questions
- **Web GUI**: Beautiful Flask web application with modern UI
- **Text Preprocessing**: Automatic lowercasing, tokenization, and punctuation removal
- **LLM Integration**: Supports OpenAI and Groq APIs
- **Real-time Responses**: Fast API integration with loading states
- **Responsive Design**: Mobile-friendly web interface

## Project Structure

```
LLM_QA_Project/
├── LLM_QA_CLI.py                    # CLI application
├── app.py                           # Flask web application
├── requirements.txt                 # Python dependencies
├── LLM_QA_hosted_webGUI_link.txt   # Deployment information
├── templates/
│   └── index.html                   # Web interface template
├── static/
│   └── style.css                    # Styling
└── README.md                        # This file
```

## Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd LLM_QA_Project
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file in the project root:

```env
API_TYPE=openai
OPENAI_API_KEY=your_api_key_here
```

Or for Groq (free alternative):

```env
API_TYPE=groq
GROQ_API_KEY=your_groq_api_key_here
```

## Usage

### CLI Application

Run the command-line interface:

```bash
python LLM_QA_CLI.py
```

### Web Application

Run the Flask web server:

```bash
python app.py
```

Then open your browser to `http://localhost:5000`

## API Key Setup

### Option 1: OpenAI (Paid)
1. Visit https://platform.openai.com/
2. Create an account and add payment method
3. Generate an API key
4. Set `API_TYPE=openai` and `OPENAI_API_KEY=your_key`

### Option 2: Groq (Free)
1. Visit https://console.groq.com/
2. Sign up for free
3. Generate an API key
4. Set `API_TYPE=groq` and `GROQ_API_KEY=your_key`

## Deployment

### Deploy to Render.com

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. **Create Render Web Service**
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app`
     - Add environment variables (API keys)

3. **Set Environment Variables on Render**
   - Add `API_TYPE`, `OPENAI_API_KEY`, or `GROQ_API_KEY`

4. **Deploy and get your live URL**

## Technologies Used

- **Backend**: Flask, Python
- **Frontend**: HTML, CSS, JavaScript
- **APIs**: OpenAI GPT / Groq LLaMA
- **Deployment**: Render.com
- **Dependencies**: requests, python-dotenv, gunicorn

## Course Information

**Course**: CSC415 / CSC331 - Artificial Intelligence  
**Project**: Project 2 - NLP Question-and-Answering System

## License

This project is for educational purposes as part of CSC415/CSC331 coursework.

