import streamlit as st

# Set page configuration
st.set_page_config(page_title="About Us - MindEase", layout="wide")

st.title("📌 About MindEase")
st.write("""
MindEase is our capstone project developed under the *Microsoft Hackathon* initiative. 
It is an AI-powered wellness assistant designed to help users track their mood and provide a responsive medical chatbot for mental well-being.
""")

st.subheader("👨‍💻 Meet the Team")

# List of team members with names and roll numbers
team_members = [
    {"name": "Sonalika Chandra", "roll": "2201CS68"},
    {"name": "Bhavik Netam", "roll": "2201CS84"},
    {"name": "Uday Shrotriya", "roll": "2201CS87"},
    {"name": "Saumya Sinha", "roll": "2201CS65"},
    {"name": "Sahil Kumar", "roll": "2201CS60"},
]

# Display team members in a two-column grid layout
for i in range(0, len(team_members), 2):
    cols = st.columns(2 if i + 1 < len(team_members) else 1)
    
    for j in range(2):
        if i + j < len(team_members):
            with cols[j]:
                member = team_members[i + j]
                st.markdown(f"""
                    <p style="font-weight: bold; color: #ffffff; text-align: center; font-size: 20px;">{member['name']}</p>
                    <p style="color: #1E90FF; font-size: 18px; text-align: center; font-weight: bold;">{member['roll']}</p>
                """, unsafe_allow_html=True)