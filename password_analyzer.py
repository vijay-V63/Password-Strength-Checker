import streamlit as st
import re
import google.generativeai as genai

import os
import cred as key

PAGE_TITLE = "PASSWORD STRENGTH CHECKER"
PAGE_ICON = "🔒"
LAYOUT = "centered"
MODEL_NAME = "gemini-2.0-flash"

#API_KEY_ENV_VAR = "GOOGLE_API_KEY"
#API_KEY = os.getenv(API_KEY_ENV_VAR)

API_KEY=key.API_KEY

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout=LAYOUT)

if not API_KEY:
    st.error(f"API Key not found. Set {API_KEY} as an environment variable.")
    st.stop()

genai.configure(api_key=API_KEY)

def check_password_strength(password):
    strength = "Weak"
    feedback = []
    
    # General rule-based checks
    if len(password) < 8:
        feedback.append("Increase password length to at least 8 characters.")
    if not re.search(r"[A-Z]", password):
        feedback.append("Include at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        feedback.append("Include at least one lowercase letter.")
    if not re.search(r"[0-9]", password):
        feedback.append("Include at least one number.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        feedback.append("Include at least one special character (!@#$%^&* etc.).")
    
    # Assign strength level based on general checks
    if len(feedback) == 0:
        strength = "Strong"
    elif len(feedback) <= 2:
        strength = "Moderate"
    
    return strength, feedback

def analyze_with_gemini(password):
    model = genai.GenerativeModel(MODEL_NAME)
    prompt = (
        f"Analyze the security of the following password: '{password}'. "
        "Provide a detailed analysis covering its strength, potential vulnerabilities, and how easily it can be cracked. "
        "Consider factors like length, presence of uppercase and lowercase letters, numbers, special characters, and predictability. "
        "Also, suggest actionable improvements to make it stronger while maintaining user-friendliness. "
        "Ensure that the feedback is clear, concise, and easy to understand for a non-technical user."
    )
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.title("🔐 Password Strength Checker")
password = st.text_input("Enter your password:", type="password")

if password:
    strength, feedback = check_password_strength(password)
    st.subheader(f"General Analysis: {strength}")
    if feedback:
        st.write("🔹 Suggestions:")
        for item in feedback:
            st.write(f"- {item}")
    
    st.subheader("AI-Powered Analysis:")
    ai_feedback = analyze_with_gemini(password)
    st.write(ai_feedback)
    
    if strength == "Strong":
        st.success("✅ Your password is strong!")
    elif strength == "Moderate":
        st.warning("⚠️ Your password is okay but could be improved.")
    else:
        st.error("❌ Your password is weak! Consider improving it.")
st.markdown("---")
st.markdown("<h3 style='text-align: center; color: orange;'>Developed by Vijay Vadapalli 🤠</h3>",unsafe_allow_html=True)
st.markdown(
    "<h2 style='text-align: center;'>Contact me: "
    "<a href='mailto:ramkrishvan06@gmail.com' style='color: blue;'>ramkrishvan06@gmail.com</a></h2>",
    unsafe_allow_html=True
)
