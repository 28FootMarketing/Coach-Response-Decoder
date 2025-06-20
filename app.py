import streamlit as st
import openai
import os

# ✅ Load API key from secrets or .env
try:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    from dotenv import load_dotenv
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ Confirm if key loaded properly
if not openai.api_key:
    st.error("❌ API key not loaded. Check your .env file or Streamlit Secrets setup.")
else:
    st.success("✅ OpenAI API key loaded successfully!")

# ✅ Set page config for mobile friendliness
st.set_page_config(page_title="Coach Response Decoder", layout="centered")

# ✅ Function to decode coach message using OpenAI
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

# ✅ Streamlit interface
st.title("📩 Coach Response Decoder")
st.markdown("Upload or paste a coach's message to get analysis of interest level and a recommended reply.")

# Text area input
coach_message = st.text_area("✍️ Paste the coach's message here:", height=180)

# File upload option
uploaded_file = st.file_uploader("📄 Or upload a .txt file", type=["txt"])
if uploaded_file:
    file_text = uploaded_file.read().decode("utf-8")
    st.text_area("📃 Coach Message from File", file_text, height=180, key="file_input")
    coach_message = file_text  # Prioritize uploaded text

# Decode button
if st.button("🎯 Decode Coach Message"):
    if coach_message.strip():
        with st.spinner("Analyzing..."):
            result = decode_coach_message(coach_message)
        st.markdown("### 🧠 Analysis Result:")
        st.markdown(result)
    else:
        st.warning("Please provide a message before decoding.")
