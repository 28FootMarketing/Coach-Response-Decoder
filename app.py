import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load API key securely from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set mobile-friendly page layout
st.set_page_config(page_title="Coach Response Decoder", layout="centered")

def decode_coach_message(message):
    prompt = f'''
    You are a Coach Response Decoder. Analyze the message below and reply in this format:

    🔍 Interest Level: [High / Moderate / Low / Not Interested]
    🗣️ Tone: [Brief tone description]
    🎯 Intent Summary: [Short summary of coach’s intent]
    ✅ Recommended Reply: [Custom-crafted reply message]

    Message:
    "{message}"
    '''
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert recruiting analyst."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"⚠️ Error during analysis: {str(e)}"

# Streamlit UI
st.title("📩 Coach Response Decoder")
st.markdown("Upload or paste a coach's message below to get instant analysis and a reply strategy.")

# Text input
coach_message = st.text_area("✍️ Paste the coach's message here:", height=180)

# File upload option
uploaded_file = st.file_uploader("📄 Or upload a .txt file", type=["txt"])
if uploaded_file:
    file_text = uploaded_file.read().decode("utf-8")
    st.text_area("📃 Coach Message from File", file_text, height=180, key="file_input")
    coach_message = file_text  # prioritize uploaded file

# Decode button
if st.button("🎯 Decode Coach Message"):
    if coach_message.strip():
        with st.spinner("Analyzing..."):
            result = decode_coach_message(coach_message)
        st.markdown("### 🧠 Analysis Result:")
        st.markdown(result)
    else:
        st.warning("Please provide a message before decoding.")
