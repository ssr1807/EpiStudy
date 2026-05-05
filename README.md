# 📚 EpiStudy

An AI-powered study assistant built on AMD MI300X GPU using Llama 3.1 8B and vLLM.

## Features
- **Summary** — Get a concise summary of any topic
- **Flashcards** — Generate 5 flashcards for quick revision
- **Quiz** — Test yourself with multiple choice questions
- **Explain Simply** — Get a simple, beginner-friendly explanation

## Tech Stack
- AMD MI300X GPU
- vLLM 0.17.1 with ROCm 7.2
- Llama 3.1 8B Instruct
- LangChain
- Gradio

## How to Run
1. Start vLLM server on port 3000
2. Run `python app.py`
3. Open the Gradio URL in your browser
