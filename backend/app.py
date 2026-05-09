import os
from dotenv import load_dotenv

from flask import Flask, request, jsonify
from flask_cors import CORS

from langchain_openai import ChatOpenAI

# =========================
# LOAD ENV
# =========================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# =========================
# APP
# =========================

app = Flask(__name__)
CORS(app)

# =========================
# LLM
# =========================

llm = ChatOpenAI(
    model="llama-3.3-70b-versatile",
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
    temperature=0.7
)

# =========================
# ROUTE
# =========================

@app.route("/generate", methods=["POST"])
def generate():

    data = request.json

    topic = data.get("topic")
    mode = data.get("mode")
    difficulty = data.get("difficulty")
    days = data.get("days", 7)

    topic = data.get("topic")
    mode = data.get("mode")
    difficulty = data.get("difficulty")
    days = data.get("days", 7)

    prompt = f"""
    Generate a {mode} for:

    Topic: {topic}

    Difficulty: {difficulty}

    Study plan duration: {days} days

    IMPORTANT INSTRUCTIONS:

    - If mode is "Test Me":
        STRICTLY generate the paper in this format:

        SECTION A - MCQs (1 mark each)
        SECTION B - Short Answer Questions (2 marks each)
        SECTION C - Long Answer Questions (5 marks each)
        SECTION D - Numerical/Problem Solving Questions if applicable (10 marks each)

        Every question MUST contain marks.
        Format example:
        Q1. What is AI? (2 Marks)
        ALWAYS provide answers after all questions under a separate heading called "Answers".

    - If mode is "Flashcards", format each flashcard properly with spacing.

    - If mode is "Study Plan":
    - STRICTLY create a {days}-day study plan
    - Divide topics day-by-day
    - Do NOT create weekly plans unless days are very large

    - Use proper markdown formatting.
    """

    response = llm.invoke(prompt)

    return jsonify({
        "response": response.content
    })
    
@app.route("/followup", methods=["POST"])
def followup():

    data = request.json

    question = data.get("question", "")
    previous_response = data.get("previous_response", "")

    prompt = f"""
Previous response:
{previous_response}

Follow-up question:
{question}

Answer clearly and properly.
"""

    try:
        response = llm.invoke(prompt)

        return jsonify({
            "response": response.content
        })

    except Exception as e:
        return jsonify({
            "response": f"Error: {str(e)}"
        }), 500
# =========================
# RUN
# =========================

if __name__ == "__main__":
    app.run(debug=True)