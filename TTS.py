import streamlit as st
import os
import time
import PyPDF2
from gtts import gTTS

try:
    os.mkdir("temp")
except:
    pass

st.title("Text to Speech")

def text_to_speech(language, text):
    try:
        tts = gTTS(text, lang=language, slow=False)
        my_file_name = text[:20] if len(text) > 20 else "audio"
        tts.save(f"temp/{my_file_name}.mp3")
        return my_file_name
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def read_text_from_pdf(file):
    pdfReader = PyPDF2.PdfReader(file)
    text = ""
    for page_num in range(len(pdfReader.pages)):
        page = pdfReader.pages[page_num]
        text += page.extract_text()
    return text

text = st.text_input("Masukkan Kalimat : ")
language = st.selectbox("Pilih Bahasa : ", ("English", "Indonesian"))
lang_code = "en" if language == "English" else "id"

uploaded_file = st.file_uploader("Pilih PDF File : ", type="pdf")

def process_text(text):
    result = text_to_speech(lang_code, text)
    if result:
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown(f"## Your audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        if display_output_text:
            st.markdown(f"## Output text:")
            st.write(f"{text}")

display_output_text = st.checkbox("Tampilkan Teks Dari PDF ")

if st.button("Convert"):
    if uploaded_file is not None:
        text = read_text_from_pdf(uploaded_file)
        time.sleep(1)
    if text:
        process_text(text)
    else:
        st.error("Please enter text or upload a PDF file.")
