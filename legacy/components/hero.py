import streamlit as st
from components.icons import get_icon

def render_hero():
    sparkles_icon = get_icon("sparkles", color="#4F46E5", size=48)
    st.markdown(
        f"""
<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 32px 24px; background: #ffffff; border-radius: 16px; border: 1px solid #E5E7EB; margin-bottom: 32px;">
    <div style="margin-bottom: 16px;">{sparkles_icon}</div>
    <h1 style="font-size: 48px; font-weight: 800; color: #111827; margin: 0 0 8px 0; letter-spacing: -0.02em;">LucentCV</h1>
    <h3 style="font-size: 22px; font-weight: 600; color: #4F46E5; margin: 0 0 16px 0;">
        AI Resume Intelligence
    </h3>
    <p style="color: #6B7280; font-size: 17px; max-width: 600px; margin: 0 auto; text-align: center;">
        Analyze your resume against any job description using Gemini AI. 
        Identify missing skills, get tailored recommendations, and practice with AI-generated interview questions.
    </p>
</div>
        """,
        unsafe_allow_html=True
    )
