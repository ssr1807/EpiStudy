import os
from dotenv import load_dotenv

from flask import Flask, request, jsonify
from flask_cors import CORS

from langchain_groq import ChatGroq

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
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
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
    You are an AI study assistant.

    Topic: {topic}
    Mode: {mode}
    Difficulty: {difficulty}
    Study plan duration: {days} days

    IMPORTANT:
    You must ONLY generate content for the selected mode.

    If mode is "Summary":
    - Generate only a concise summary
    - Do NOT create study plans
    - Do NOT create flashcards
    - Do NOT create tests

    If mode is "Flashcards":
    - Generate only flashcards
    - Format:
    Q:
    A:
    - Do NOT create study plans
    - Do NOT mention Day 1, Day 2, etc.

    If mode is "Test Me":
    - Generate:
    1. MCQs
    2. Short answer questions
    3. Long answer questions
    4. Numerical/problem-solving questions if applicable
    5. Mention marks for every question
    6. Put all answers under:
    ## ANSWERS
    - Do NOT create study plans

    If mode is "Study Plan":
    - STRICTLY create a {days}-day study plan
    - Divide content day-by-day
    - ONLY this mode can mention Day 1, Day 2 etc.

    Use proper markdown formatting.
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