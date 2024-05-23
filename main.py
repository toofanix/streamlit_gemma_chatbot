import streamlit as st
from time import sleep
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import requests

env = Environment(
    loader=FileSystemLoader(os.getcwd()+"/templates"),
    autoescape=select_autoescape()
)

st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #64c0ce;
    color: black;
}
</style>
""", unsafe_allow_html=True)

def chat_response(prompt):
    response = requests.post(
    url="http://127.0.0.1:5000/v1/chat/completions",
    json={
        "model": "google_gemma-1.1-2b-it",
        "messages": [{ "role": "user", "content": prompt}],
        "stream": False
        }
    )
    answer = response.json()['choices'][0]['message']['content']
    return answer

def get_personality_file(value):
    match value:
        case "Default":
            return "default.jinja"
        case "Santa Claus":
            return "santaclaus.jinja"
        case "Scientist":
            return "scientist.jinja"
        case _:
            return "default.jinja"
        
def send_to_llm():
    st.toast("Generating prompt from template")
    personality_template = env.get_template(get_personality_file(personality))
    prompt_template = env.get_template("prompt.jinja")
    prompt = prompt_template.render(
        prompt=prompt_text,
        personality=personality_template.render()
    )
    sleep(1)
    st.toast("Sent Prompt to LLM")
    response = chat_response(prompt)
    sleep(1)
    st.toast("Response received from LLM")
    return response


st.header(":robot_face: Gemma AI Chatbot")

prompt_text = st.text_area('Ask a Question or Start a Conversation: ', '')
col1, col2 = st.columns([3, 1])
col1.text("Choose Personality")
col2.text("Press Enter")

col1, col2 = st.columns([3, 1])

with col1:
    personality = st.selectbox(
    'Choose a personality',
    ('Default', 'Santa Claus', 'Scientist'),
    label_visibility="collapsed"
)

with col2:
    run_llm = st.button("Run LLM", use_container_width=True)

with st.spinner("Generating a Response..."):
    if run_llm:
        st.text_area("Response", send_to_llm(), placeholder="Send your question to LLM and get responses here")
    else:
        st.text_area("Response", "", placeholder="Send your question to LLM and get responses here")

