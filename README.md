# AI Resume + Cover Letter Generator

A lightweight Streamlit app that generates a tailored resume and cover letter from a candidate profile and job description.

## Features
- Generate resume + cover letter in one click
- OpenAI-powered generation (`OPENAI_API_KEY`) or local deterministic fallback mode
- Adjustable tone and model
- Download generated output as Markdown

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
streamlit run app.py
```

Then open the local URL shown by Streamlit (usually `http://localhost:8501`).

## Environment
If you want AI generation through OpenAI, set:
```bash
export OPENAI_API_KEY="your_api_key_here"
```

If no key is set, disable the API toggle in the sidebar to use the built-in fallback generator.
