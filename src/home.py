import streamlit as st

# Set page configuration
st.set_page_config(page_title="MindEase 🌿 - Wellness Assistant", layout="wide")

# Custom CSS for Light-Themed Navbar and Styling
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

        * {
            font-family: 'Poppins', sans-serif;
        }

        .navbar {
            background-color: #ffffff;
            padding: 15px;
            border-radius: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05);
        }

        .navbar a {
            color: #2D5F5D;
            text-decoration: none;
            margin: 0 15px;
            font-weight: 500;
            font-size: 18px;
        }

        .navbar a:hover {
            text-decoration: underline;
            color: #1E403F;
        }

        .title {
            font-size: 40px;
            font-weight: 600;
            text-align: center;
            color: #2D5F5D;
            margin-top: 30px;
        }

        .subtitle {
            font-size: 20px;
            text-align: center;
            color: #555;
            margin-bottom: 20px;
        }

        .quote-box {
            background-color: #EAF6F6;
            padding: 15px;
            border-radius: 12px;
            text-align: center;
            font-size: 18px;
            font-weight: 500;
            color: #2D5F5D;
            margin: 20px auto;
            max-width: 500px;
        }

        .options-box {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 30px;
        }

        .option-button {
            background-color: #2D5F5D;
            color: white;
            padding: 12px 25px;
            border-radius: 8px;
            font-size: 18px;
            font-weight: 500;
            text-decoration: none;
            transition: background 0.3s ease-in-out;
        }

        .option-button:hover {
            background-color: #1E403F;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Navbar
st.markdown(
    """
    <div class="navbar">
        <h3 style="margin: 0; color: #2D5F5D;">MindEase 🌿</h3>
        <div>
            <a href="#">Home</a>
            <a href="#">About</a>
            <a href="#">Contact</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Title and Subtitle
st.markdown('<h1 class="title">🌟 Welcome to MindEase - Your AI Wellness Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">🌼 A positive mind leads to a positive life.</p>', unsafe_allow_html=True)

# Quote Box
st.markdown('<div class="quote-box">“Happiness depends upon ourselves.” - Aristotle</div>', unsafe_allow_html=True)

# Navigation Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("🧠 Mood Tracker"):
        st.switch_page("pages/moodTracker.py")

with col2:
    if st.button("💬 AI Medical Chatbot"):
        st.switch_page("pages/chatbot.py")