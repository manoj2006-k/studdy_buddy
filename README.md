# AI Study Buddy

AI Study Buddy is a Streamlit web app that helps students summarize notes, explain concepts, and generate quiz questions from uploaded PDF or TXT files.

Live deployment: https://studdybuddy-fv2sqcwtzphg8vrth447bz.streamlit.app/

## Features

- Upload PDF or TXT files
- Summarize the main points of uploaded content
- Explain a concept in simple language
- Generate study questions and answers
- Works with a fallback response if the AI model is unavailable

## Tech Stack

- Python
- Streamlit
- Transformers
- PyPDF2 / pypdf
- Torch
- Pandas / NumPy

## Project Structure

- study_buddy.py - Main Streamlit application
- requirements.txt - Python dependencies

## Installation

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Locally

```bash
streamlit run study_buddy.py
```

Then open the local URL shown in the terminal.

## Deployment

This project is ready for deployment on Streamlit Cloud.

### Streamlit Cloud Setup

- Choose the repository
- Set the main file to study_buddy.py
- Use requirements.txt for dependencies
- Deploy the app

## Notes

The app tries to load a transformer-based text-generation model, but it also includes a fallback response so it can still provide helpful output even when the model is unavailable.

## License

No license has been specified yet.
