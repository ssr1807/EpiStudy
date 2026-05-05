from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import gradio as gr

llm = ChatOpenAI(
    model="meta-llama/Meta-Llama-3.1-8B-Instruct",
    base_url="http://localhost:3000/v1",
    api_key="dummy",
    temperature=0.7
)

def summarize(topic):
    prompt = ChatPromptTemplate.from_template(
        "Summarize the topic '{topic}' in simple, clear language in 5-7 sentences."
    )
    chain = prompt | llm
    return chain.invoke({"topic": topic}).content

def generate_flashcards(topic):
    prompt = ChatPromptTemplate.from_template(
        "Create 5 flashcards for the topic '{topic}'. Format each as:\nQ: question\nA: answer\n"
    )
    chain = prompt | llm
    return chain.invoke({"topic": topic}).content

def generate_quiz(topic):
    prompt = ChatPromptTemplate.from_template(
        "Create 3 multiple choice questions about '{topic}'. Format each as:\nQ: question\na) option\nb) option\nc) option\nd) option\nAnswer: correct option\n"
    )
    chain = prompt | llm
    return chain.invoke({"topic": topic}).content

def explain_simple(topic):
    prompt = ChatPromptTemplate.from_template(
        "Explain '{topic}' as if I am a 10 year old. Use simple words and a fun analogy."
    )
    chain = prompt | llm
    return chain.invoke({"topic": topic}).content

def study_buddy(topic, mode):
    if mode == "Summary":
        return summarize(topic)
    elif mode == "Flashcards":
        return generate_flashcards(topic)
    elif mode == "Quiz":
        return generate_quiz(topic)
    elif mode == "Explain Simply":
        return explain_simple(topic)

app = gr.Interface(
    fn=study_buddy,
    inputs=[
        gr.Textbox(label="Enter a topic", placeholder="e.g. Photosynthesis, Newton's Laws..."),
        gr.Radio(["Summary", "Flashcards", "Quiz", "Explain Simply"], label="What do you want?")
    ],
    outputs=gr.Textbox(label="EpiStudy Response", lines=20),
    title="📚 EpiStudy",
    description="Your AI-powered study assistant running on AMD MI300X with Llama 3.1 8B"
)

app.launch(server_name="0.0.0.0", server_port=7860, share=True)
