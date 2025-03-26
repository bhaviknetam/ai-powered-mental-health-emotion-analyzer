import streamlit as st
import openai
import os
from dotenv import load_dotenv
load_dotenv()

# ------------------------- AZURE OPENAI CONFIGURATION -------------------------
AZURE_KEY = os.getenv("AZURE_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_GPT4_DEPLOYMENT = "gpt-4"
AZURE_GPT4_API_VERSION = "2025-01-01-preview"

# ------------------------- SETUP AZURE OPENAI CLIENT -------------------------
openai_client = openai.AzureOpenAI(
    api_key=AZURE_KEY,
    api_version=AZURE_GPT4_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
)

# ------------------------- STREAMLIT UI -------------------------
st.set_page_config(page_title="🩺 AI Medical Assistant", layout="wide")

st.title("🩺 AI Medical Assistant Chatbot")
st.write("💬 Ask about *symptoms, medications, first-aid, or medical advice*.")

# Store chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ------------------------- INPUT HANDLING -------------------------
user_input = st.chat_input("Ask a medical question...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message in chat
    with st.chat_message("user"):
        st.markdown(user_input)

    # ------------------------- GPT-4 RESPONSE -------------------------
    with st.spinner("Analyzing medical data... ⚕"):
        try:
            response = openai_client.chat.completions.create(
                model=AZURE_GPT4_DEPLOYMENT,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a professional medical assistant AI. You provide medical information about symptoms, medications, "
                            "first-aid, and common health conditions. You do NOT engage in non-medical topics. "
                            "For emergencies, you should recommend seeking immediate medical attention."
                        ),
                    },
                    *st.session_state.messages  # Pass chat history
                ]
            )

            if response and response.choices:
                bot_reply = response.choices[0].message.content

                # Add AI response to chat history
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})

                # Display AI response
                with st.chat_message("assistant"):
                    st.markdown(bot_reply)
            else:
                st.warning("⚠ Unable to generate a medical response. Please try again.")
        except Exception as e:
            st.error(f"⚠ Error: {e}")

# ------------------------- FOOTER -------------------------
st.markdown("""
---
⚠ Disclaimer: This AI assistant provides *general medical guidance* but *is not a substitute* for a licensed medical professional.  
If you have a medical emergency, *seek immediate care from a doctor or hospital*.
""")
