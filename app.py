import os
import tempfile
from dotenv import load_dotenv

import gradio as gr
from langchain_openai import ChatOpenAI

# =========================
# LOAD ENV
# =========================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# =========================
# LLM SETUP
# =========================

llm = ChatOpenAI(
    model="llama-3.3-70b-versatile",
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
    temperature=0.7
)

# =========================
# CUSTOM CSS
# =========================

custom_css = """
body {
    font-family: 'Times New Roman', serif;
}

.gradio-container {
    background: #020b22 !important;
    color: white !important;
}

textarea, input, button {
    font-family: 'Times New Roman', serif !important;
}
"""

# =========================
# MEMORY
# =========================

last_topic = ""
last_mode = ""

# =========================
# MAIN GENERATION
# =========================

def generate_response(topic, mode, difficulty, days, marks):

    global last_topic, last_mode

    last_topic = topic
    last_mode = mode

    if not topic.strip():
        return "Please enter a topic."

    prompts = {

        "Summary":
        f"""
        Give a detailed summary of {topic}.

        Difficulty: {difficulty}
        """,

        "Flashcards":
        f"""
        Create 5 flashcards for {topic}.

        STRICT FORMAT:
        Q1: Question
        A1: Answer

        Q2: Question
        A2: Answer
        """,

        "Explain Simply":
        f"""
        Explain {topic} in a very simple beginner-friendly way.

        Use:
        - analogies
        - examples
        - easy explanations
        """,

        "Study Plan":
        f"""
        Create a {days}-day study plan for {topic}.

        Include:
        - daily goals
        - revision
        - practice
        """,

        "Test Me":
        f"""
        Create a {marks}-mark test on {topic}.

        RULES:
        - MCQs with A/B/C/D
        - Short answers
        - Long answers
        - NO answers
        """
    }

    response = llm.invoke(prompts[mode])

    return response.content

# =========================
# SHOW ANSWERS
# =========================

def show_answers(topic, difficulty, marks):

    prompt = f"""
    Give ONLY answers for the previously generated
    {marks}-mark test on:

    {topic}

    Difficulty: {difficulty}

    Include:
    - MCQ correct options
    - short answers
    - long answers
    """

    response = llm.invoke(prompt)

    return response.content

# =========================
# FOLLOW-UP
# =========================

def follow_up(question):

    global last_topic, last_mode

    if not question.strip():
        return "Ask a follow-up question."

    prompt = f"""
    Previous topic: {last_topic}
    Previous mode: {last_mode}

    User follow-up:
    {question}
    """

    response = llm.invoke(prompt)

    return response.content

# =========================
# VISIBILITY SYSTEM
# =========================

def update_visibility(mode):

    if mode == "Study Plan":

        return (
            gr.update(visible=True),   # days
            gr.update(visible=False),  # marks
            gr.update(visible=False),  # answers
            "",                        # clear input
            ""                         # clear output
        )

    elif mode == "Test Me":

        return (
            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(visible=True),
            "",
            ""
        )

    else:

        return (
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            "",
            ""
        )
# =========================
# DOWNLOAD FUNCTIONS
# =========================

def download_main_response(text):

    if not text:
        return None

    temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".txt",
        mode="w",
        encoding="utf-8"
    )

    temp.write(text)
    temp.close()

    return temp.name


def download_followup_response(text):

    if not text:
        return None

    temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".txt",
        mode="w",
        encoding="utf-8"
    )

    temp.write(text)
    temp.close()

    return temp.name
# =========================
# UI
# =========================

with gr.Blocks(theme=gr.themes.Soft(), css=custom_css) as app:

    gr.Markdown(
        """
        # 📚 EpiStudy
        ### AI-Powered Smart Study Assistant
        """
    )

    with gr.Row():

        # LEFT PANEL
        with gr.Column(scale=1):

            topic = gr.Textbox(
                label="Enter Topic",
                placeholder="Example: Wave Optics"
            )

            mode = gr.Dropdown(
                choices=[
                    "Summary",
                    "Flashcards",
                    "Explain Simply",
                    "Study Plan",
                    "Test Me"
                ],
                value="Summary",
                label="Select Mode"
            )

            difficulty = gr.Dropdown(
                choices=["Easy", "Medium", "Hard"],
                value="Medium",
                label="Difficulty"
            )

            # DAYS
            days = gr.Slider(
                minimum=1,
                maximum=30,
                value=7,
                step=1,
                label="Number of Days",
                visible=False
            )

            # MARKS
            marks = gr.Slider(
                minimum=5,
                maximum=100,
                value=20,
                step=5,
                label="Marks",
                visible=False
            )

            generate_btn = gr.Button("Generate")

            # SHOW ANSWERS
            answers_btn = gr.Button(
                "Show Answers",
                visible=False
            )

        # RIGHT PANEL
        with gr.Column(scale=2):

            output = gr.Textbox(
                label="Output",
                lines=20,
                interactive=False
            )

            with gr.Row():

                 download_main_btn = gr.Button("Download Response")

            main_download_file = gr.File(
                label="Download File",
)

            gr.Markdown("## Follow-Up Questions")

            follow_input = gr.Textbox(
                placeholder="Ask a follow-up question..."
            )

            follow_btn = gr.Button("Ask")

            follow_output = gr.Textbox(
                label="Follow-Up Response",
                lines=10,
                interactive=False
)

            with gr.Row():

                download_follow_btn = gr.Button("Download Follow-Up")

            follow_download_file = gr.File(
                label="Follow-Up File",
)

    # =========================
    # BUTTON ACTIONS
    # =========================

    generate_btn.click(
        fn=generate_response,
        inputs=[topic, mode, difficulty, days, marks],
        outputs=output
    )

    answers_btn.click(
        fn=show_answers,
        inputs=[topic, difficulty, marks],
        outputs=output
    )

    follow_btn.click(
        fn=follow_up,
        inputs=follow_input,
        outputs=follow_output
    )
    download_main_btn.click(
        fn=download_main_response,
        inputs=output,
        outputs=main_download_file
    )

    download_follow_btn.click(
        fn=download_followup_response,
        inputs=follow_output,
        outputs=follow_download_file
    )

    # =========================
    # MODE CHANGE
    # =========================

    mode.change(
        fn=update_visibility,
        inputs=mode,
        outputs=[
            days,
            marks,
            answers_btn,
            follow_input,
            follow_output
        ]
    )

# =========================
# LAUNCH
# =========================

app.launch()