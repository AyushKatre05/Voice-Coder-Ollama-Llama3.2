import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
import tempfile
import ollama  # Ensure you have the Ollama API installed

# Initialize session state for code
if "code" not in st.session_state:
    st.session_state.code = ""

# Function for text-to-speech (feedback)
def speak(text):
    tts = gTTS(text)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        os.system(f"start {fp.name}")

# Function for speech recognition
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        with st.spinner("Listening..."):
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio)
                return text
            except sr.UnknownValueError:
                return "Sorry, I didn't catch that."
            except sr.RequestError:
                return "API unavailable"

# Function to get code from Ollama based on user input
def get_code_from_ollama(command):
    # Send the voice command to Ollama to generate code
    response = ollama.chat(
        model='llama3.2:latest',  # Ensure you're using the correct Ollama model
        messages=[{'role': 'user', 'content': command}]
    )
    return response['message']['content']

# Styling the app for a better look
st.markdown("""
    <style>
        .main {
            background-color: #f0f2f6;
            padding: 20px;
            border-radius: 10px;
        }
        .btn {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
        }
        .btn-clear {
            background-color: #f44336;
        }
        .code-area {
            background-color: #1e1e1e;
            color: #d4d4d4;
            font-family: Consolas, monaco, monospace;
            padding: 15px;
            border-radius: 5px;
        }
        .stButton>button {
            padding: 12px;
            font-size: 18px;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("Voice to Code Generator")
st.subheader("Speak your programming commands, and I will generate the code for you!")
st.markdown("---")

# Voice input button to trigger listening and code generation
col1, col2 = st.columns([4, 1])

with col1:
    if st.button("🎤 Start Listening", key="start"):
        spoken_text = listen()  # Capture the spoken text
        st.session_state.code += f"\n{spoken_text}"

        # Use Ollama to generate code from the spoken command
        code = get_code_from_ollama(spoken_text)
        st.session_state.code += f"\n{code}"

        # Provide feedback via speech
        speak(f"Command processed: {spoken_text}")
        speak("Code generated")

# Clear Button with custom styling applied through CSS
with col2:
    if st.button("Clear Code", key="clear", help="Clear the generated code"):
        st.session_state.code = ""  # Clear code in session state

# Display the generated code in a text area
st.text_area("🧠 Your Generated Code", value=st.session_state.code, key="code", height=300, max_chars=1500, help="This is your generated code")
