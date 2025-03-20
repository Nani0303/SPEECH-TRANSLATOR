import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import tempfile

# Streamlit UI
st.title("Automatic Speech Recognition and Translation")

# Language options
languages = {
    "english": "en",
    "hindi": "hi",
    "telugu": "te",
    "french": "fr",
    "spanish": "es",
    "german": "de"
}

# Language selection for input and output
input_language = st.selectbox("Select Input Language", list(languages.keys()))
output_language = st.selectbox("Select Output Language", list(languages.keys()))

st.write("Click 'Start' to begin speaking. The translation will be processed automatically after speaking.")

# Initialize session state for audio
if 'audio_data' not in st.session_state:
    st.session_state.audio_data = None

recognizer = sr.Recognizer()

if st.button("Start Recording"):
    with sr.Microphone() as source:
        st.write("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio_data = recognizer.listen(source, timeout=10, phrase_time_limit=10)  # Increased duration
        st.write("Processing...")
        try:
            # Recognize speech with the selected input language
            text = recognizer.recognize_google(audio_data, language=languages[input_language])
            st.write(f"Recognized Text ({input_language}): {text}")
            
            # Translate text
            translated_text = GoogleTranslator(source=languages[input_language], target=languages[output_language]).translate(text)
            st.write(f"Translated Text ({output_language}): {translated_text}")
            
            # Convert text to speech
            tts = gTTS(translated_text, lang=languages[output_language])
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_file_name = temp_file.name
            temp_file.close()  # Close the file before using it
            tts.save(temp_file_name)
            
            # Play audio
            st.audio(temp_file_name, format='audio/mp3')
            
        except Exception as e:
            st.error(f"Error: {e}")
        finally:
            if os.path.exists(temp_file_name):
                os.remove(temp_file_name)
