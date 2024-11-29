import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Streamlit page configuration
st.set_page_config(
    page_title="GeminiBot",
    page_icon="🤖",
    layout="wide",
)

# Google API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
gen_ai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Generative Model
model = gen_ai.GenerativeModel('gemini-pro')

def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize session state for chat
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Sidebar: Reset Chat Button
with st.sidebar:
    st.title("Chat Settings")
    if st.button("Reset Chat"):
        st.session_state.chat_session = model.start_chat(history=[])
        st.experimental_rerun()

# Header Section
st.markdown(
    """
    <div style="text-align: center; padding: 10px; background-color: #f8f9fa; border-radius: 10px;">
        <h1>🤖 GeminiBot</h1>
        <p style="color: #6c757d;">Ask anything, and Gemini is here to help!</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Chat Display Section
st.divider()
st.write("### Chat History")
chat_container = st.container()

with chat_container:
    for message in st.session_state.chat_session.history:
        role = translate_role_for_streamlit(message.role)
        if role == "user":
            st.markdown(
                f"""
                <div style="text-align: right; margin: 10px;">
                    <div style="display: inline-block; background-color: #007bff; color: white; padding: 10px; border-radius: 10px; max-width: 60%;">
                        {message.parts[0].text}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div style="text-align: left; margin: 10px;">
                    <div style="display: inline-block; background-color: #e9ecef; color: black; padding: 10px; border-radius: 10px; max-width: 60%;">
                        {message.parts[0].text}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# User Input Section
st.divider()
st.write("### Send a Message")
user_prompt = st.text_input("Type your message...")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    gemini_response = st.session_state.chat_session.send_message(user_prompt)
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)

    # Update chat session with the assistant's response
    st.session_state.chat_session.history.append({"role": "assistant", "parts": [{"text": gemini_response.text}]})

# Footer Section
st.markdown(
    """
    <footer style="text-align: center; padding: 10px; margin-top: 20px; background-color: #f8f9fa; border-radius: 10px;">
    </footer>
    """,
    unsafe_allow_html=True,
)
