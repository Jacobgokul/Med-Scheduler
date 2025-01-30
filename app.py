import os
import requests
import streamlit as st
from dotenv import load_dotenv
import speech_recognition as sr
import pyttsx3
from main import memory

load_dotenv()  # Load API key from .env
openai_key = os.getenv("OPENAI_API_KEY")

API_URL = "http://127.0.0.1:8000/chat"  # FastAPI Backend

st.title("🩺 AI Appointment Scheduler")
st.write("Chat with our assistant to book a hospital appointment.")

menu_option = st.sidebar.selectbox("Choose Input Method", ["Text to Book", "Voice to Book"])

if st.button("New Chat", key="new_chat"):
    st.session_state.messages = []
    memory.clear()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Voice-to-Text Functionality
def voice_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        st.write(f"User said: {text}")
        return text
    except sr.UnknownValueError:
        st.write("Sorry, I could not understand the audio.")
        return ""
    except sr.RequestError:
        st.write("Could not request results from the speech recognition service.")
        return ""

#Text-to-VOice Functionality 
def text_to_voice(text):
    engine = pyttsx3.init(driverName="espeak")
    engine.setProperty("rate", 150)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[29].id)
    engine.say(text)
    engine.runAndWait()


if menu_option == "Text to Book":
    user_input = st.chat_input("Type your appointment request...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        headers = {"Content-Type": "application/json"}
        payload = {"user_message": user_input}

        try:
            response = requests.post(API_URL, params=payload, headers=headers)
            if response.status_code == 200:
                bot_reply = response.json().get("response", "I couldn't understand your request.")
            else:
                bot_reply = "Error: AI service unavailable."
        except requests.exceptions.RequestException:
            bot_reply = "Error: Could not connect to AI service."

        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        with st.chat_message("assistant"):
            st.markdown(bot_reply)


if menu_option == "Voice to Book":
    if st.button("Click to Speak"):
        user_input = voice_to_text()

        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            headers = {"Content-Type": "application/json"}
            payload = {"user_message": user_input}

            try:
                response = requests.post(API_URL, params=payload, headers=headers)
                if response.status_code == 200:
                    bot_reply = response.json().get("response", "I couldn't understand your request.")
                else:
                    bot_reply = "Error: AI service unavailable."
            except requests.exceptions.RequestException:
                bot_reply = "Error: Could not connect to AI service."

            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            with st.chat_message("assistant"):
                st.markdown(bot_reply)

            # Convert the bot's reply to speech
            text_to_voice(bot_reply)
