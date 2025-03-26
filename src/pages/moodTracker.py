import os
import requests
from io import BytesIO
import json
import streamlit as st
import openai
import azure.cognitiveservices.speech as speechsdk
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
load_dotenv()

# ------------------------- AZURE CONFIGURATION -------------------------
# (Replace the hardcoded values with secure methods later)
AZURE_KEY = os.getenv("AZURE_KEY")
AZURE_TEXT_ENDPOINT = os.getenv("AZURE_TEXT_ENDPOINT")
AZURE_SPEECH_REGION = "eastus"

FACE_API_ENDPOINT = os.getenv("FACE_ENDPOINT")
FACE_API_TOKEN = os.getenv("FACE_API_TOKEN")

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_GPT4_DEPLOYMENT = "gpt-4"
AZURE_GPT4_API_VERSION = "2025-01-01-preview"

# ------------------------- AZURE CLIENTS -------------------------
try:
    text_client = TextAnalyticsClient(
        endpoint=AZURE_TEXT_ENDPOINT,
        credential=AzureKeyCredential(AZURE_KEY)
    )
    openai_client = openai.AzureOpenAI(
    api_key=AZURE_KEY,
    api_version=AZURE_GPT4_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
)
    
except Exception as e:
    st.error(f"⚠ Error initializing Azure clients: {e}")

# ------------------------- STREAMLIT UI -------------------------
st.title("🧠 AI-Powered Mental Health Analyzer")
st.write("Analyze emotional sentiment from text, voice, and images.")

# Variables to store analysis results
sentiment = "Unknown"
speech_sentiment = "Unknown"
gpt4_emotion = "Unknown"

# ------------------------- TEXT SENTIMENT ANALYSIS -------------------------
st.header("📄 Text Sentiment Analysis")
text_input = st.text_area("Enter your thoughts or feelings:")

if st.button("Analyze Text"):
    if text_input.strip():
        try:
            response = text_client.analyze_sentiment([text_input])
            if response and response[0]:
                sentiment = response[0].sentiment
                st.write(f"Sentiment: {sentiment.capitalize()}")
            else:
                st.warning("Unable to analyze sentiment.")
        except Exception as e:
            st.error(f"⚠ Error in text sentiment analysis: {e}")
    else:
        st.warning("Please enter some text.")

# ------------------------- SPEECH SENTIMENT ANALYSIS -------------------------
st.header("🎤 Speech Sentiment Analysis")

languages = ["en-US", "hi-IN", "fr-FR", "es-ES", "de-DE", "it-IT", "pt-PT", "zh-CN", "ja-JP", "ko-KR"]
language_choice = st.selectbox("Select Language", languages)

if st.button("Record & Analyze Speech"):
    try:
        speech_config = speechsdk.SpeechConfig(
            subscription=AZURE_KEY,
            endpoint=AZURE_TEXT_ENDPOINT
        )
        speech_config.speech_recognition_language = language_choice

        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        st.write("🎙 Recording... Please speak now.")
        speech_recognition_result = speech_recognizer.recognize_once_async().get()

        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            recognized_text = speech_recognition_result.text
            st.success(f"Recognized: {recognized_text}")

            # Analyze sentiment of recognized speech
            response = text_client.analyze_sentiment([recognized_text])
            if response and response[0]:
                speech_sentiment = response[0].sentiment
                st.write(f"Speech Sentiment: {speech_sentiment.capitalize()}")
            else:
                st.warning("Unable to analyze speech sentiment.")
        elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
            st.warning(f"No speech recognized: {speech_recognition_result.no_match_details}")
        elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = speech_recognition_result.cancellation_details
            st.error(f"Speech Recognition canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                st.error(f"Error details: {cancellation_details.error_details}")
                st.error("Check speech resource key & region values.")
    except Exception as e:
        st.error(f"⚠ Error in speech analysis: {e}")

# ------------------------- IMAGE EMOTION (VISION + GPT-4) -------------------------
st.header("🔍 Image Emotion Analysis via GPT-4")

image_file = st.file_uploader("📤 Upload an image for analysis:", type=["jpg", "jpeg", "png"])

if image_file is not None:
    # Display the uploaded image
    image_bytes = image_file.read()
    st.image(image_file, caption="📷 Uploaded Image", use_container_width=True)

    # 1. Vision API (v3.2/analyze) to get a description
    vision_api_url = f"{AZURE_TEXT_ENDPOINT}/vision/v3.2/analyze"
    vision_params = {
        "visualFeatures": "Faces,Description",
        "language": "en"
    }
    vision_headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Content-Type": "application/octet-stream"
    }

    try:
        vision_response = requests.post(vision_api_url, headers=vision_headers, params=vision_params, data=image_bytes)
        vision_response.raise_for_status()
        vision_result = vision_response.json()

        st.subheader("📜 Vision API JSON Response:")
        # st.json(vision_result)

        # Extract description from Vision API
        description_text = ""
        if ("description" in vision_result 
            and "captions" in vision_result["description"] 
            and len(vision_result["description"]["captions"]) > 0):
            description_text = vision_result["description"]["captions"][0]["text"]
        
        if not description_text:
            description_text = "No description available."
        st.write("Extracted Description:", description_text)

        # 2. GPT-4 for emotion analysis
        gpt4_url = (
            f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_GPT4_DEPLOYMENT}/chat/completions"
            f"?api-version={AZURE_GPT4_API_VERSION}"
        )
        gpt_headers = {
            "Content-Type": "application/json",
            "api-key": AZURE_KEY
        }
        prompt = (
            f"Analyze this image description and provide the main emotion in one word: {description_text}"
        )
        gpt_data = {
            "messages": [
                {"role": "system", "content": "You are an expert in analyzing emotions in images."},
                {"role": "user", "content": prompt}
            ]
        }

        gpt_response = requests.post(gpt4_url, headers=gpt_headers, json=gpt_data)
        gpt_response.raise_for_status()
        gpt_result = gpt_response.json()

        st.subheader("💬 GPT-4 Emotion Analysis:")
        if "choices" in gpt_result and len(gpt_result["choices"]) > 0:
            gpt4_text = gpt_result["choices"][0]["message"]["content"]
            st.write("GPT-4 Raw Answer:", gpt4_text)

            # A simple approach to parse the single-word emotion from GPT-4's text
            gpt4_text_lower = gpt4_text.lower()

            # Basic keyword matching (improve as needed)
            if any(word in gpt4_text_lower for word in ["happy", "happiness", "joy"]):
                gpt4_emotion = "happiness"
            elif any(word in gpt4_text_lower for word in ["sad", "sadness", "sorrow", "depressed"]):
                gpt4_emotion = "sadness"
            elif any(word in gpt4_text_lower for word in ["anger", "angry"]):
                gpt4_emotion = "anger"
            elif any(word in gpt4_text_lower for word in ["fear", "afraid", "scared"]):
                gpt4_emotion = "fear"
            else:
                gpt4_emotion = "neutral"

            st.success(f"Parsed Emotion: {gpt4_emotion.capitalize()}")
        else:
            st.error("No valid answer from GPT‑4.")
            gpt4_emotion = "neutral"
    except requests.exceptions.RequestException as e:
        st.error(f"🚨 API Request Failed: {e}")
        gpt4_emotion = "neutral"
else:
    # If no image uploaded, default
    gpt4_emotion = "Unknown"

# ------------------------- MENTAL HEALTH ANALYSIS -------------------------
st.header("🩺 Mental Health Prediction & Assistance")
if st.button("Get Mental Health Insights"):
    try:
        prompt = f"""
        Based on the user's inputs:
        - Text Sentiment: {sentiment}
        - Speech Sentiment: {speech_sentiment}
        - Facial Emotion: {gpt4_emotion}

        Based on these inputs, classify their mental health status (Healthy, Mild Stress, Anxiety, Depression), if possible.
        If any of the above sentiment is unknown, just ignore it and predict on the basis of
        known inputs only. Also, provide a short mental health assistance recommendation.
        """

        response = openai_client.chat.completions.create(
            model=AZURE_GPT4_DEPLOYMENT,
            messages=[
                {"role": "system", "content": "You are a mental health AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        if response and response.choices:
            st.write("*Mental Health Prediction:*")
            st.success(response.choices[0].message.content)
        else:
            st.warning("⚠ Failed to get a response from OpenAI.")
    except Exception as e:
        st.error(f"⚠ Error in mental health analysis: {e}")