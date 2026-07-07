"""
LucentCV - Streamlit Application
"""

import os
import streamlit as st
from google import genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from agents import run_full_analysis, run_interview_generator, run_interview_evaluator
from services.supabase_service import (
    save_analysis,
    get_history,
    save_interview_questions,
    get_interview_questions,
    save_interview_answers
)

from components.hero import render_hero
from components.cards import empty_state
from components.loading import animated_loading
from components.results import render_results_dashboard
from components.interview import render_interview_questions, render_interview_feedback
from components.history import render_history_card
from components.icons import get_icon

st.set_page_config(page_title="LucentCV", layout="wide", initial_sidebar_state="collapsed")

# Inject Custom CSS
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# API Initialization
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    st.error("GEMINI_API_KEY environment variable not found. Please export it and restart.")
    st.stop()
client = genai.Client(api_key=API_KEY)

# Session State Initialization
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "last_analysis_id" not in st.session_state:
    st.session_state.last_analysis_id = None
if "interview_questions" not in st.session_state:
    st.session_state.interview_questions = None
if "interview_answers" not in st.session_state:
    st.session_state.interview_answers = {}
if "interview_feedback" not in st.session_state:
    st.session_state.interview_feedback = None
if "viewing_history_id" not in st.session_state:
    st.session_state.viewing_history_id = None

# Hero Section
render_hero()

# Main Tabs (No emojis)
tab_analiz, tab_mulakat, tab_gecmis = st.tabs([
    "New Analysis", 
    "Interview", 
    "History"
])

with tab_analiz:
    # If viewing a historical analysis from the history tab, show a "Back" button
    if st.session_state.viewing_history_id and st.session_state.last_result:
        if st.button("New Analysis"):
            st.session_state.viewing_history_id = None
            st.session_state.last_result = None
            st.session_state.last_analysis_id = None
            st.rerun()
            
        render_results_dashboard(st.session_state.last_result)
        
    elif st.session_state.last_result:
        # Just finished a new analysis
        if st.button("New Analysis"):
            st.session_state.last_result = None
            st.session_state.last_analysis_id = None
            st.rerun()
            
        render_results_dashboard(st.session_state.last_result)
        
    else:
        # Empty Form
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<div style='display: flex; align-items: center; gap: 8px; margin-bottom: 8px;'><span style='color: #4F46E5;'>{get_icon('file_text', size=20)}</span><h3 style='margin: 0 !important; font-size: 17px !important;'>Resume</h3></div>", unsafe_allow_html=True)
            cv_text = st.text_area("Resume", height=350, placeholder="Paste your resume here...", label_visibility="collapsed")
        with col2:
            st.markdown(f"<div style='display: flex; align-items: center; gap: 8px; margin-bottom: 8px;'><span style='color: #4F46E5;'>{get_icon('briefcase', size=20)}</span><h3 style='margin: 0 !important; font-size: 17px !important;'>Job Description</h3></div>", unsafe_allow_html=True)
            job_text = st.text_area("Job Description", height=350, placeholder="Paste the job description here...", label_visibility="collapsed")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        button_disabled = not cv_text.strip() or not job_text.strip()
        
        if st.button("Analyze Resume", type="primary", use_container_width=True, disabled=button_disabled):
            result = animated_loading(run_full_analysis, client, cv_text, job_text)
            
            analysis_id = save_analysis(cv_text, job_text, result)
            
            st.session_state.last_result = result
            st.session_state.last_analysis_id = analysis_id
            st.session_state.interview_questions = None
            st.session_state.interview_answers = {}
            st.session_state.interview_feedback = None
            
            st.rerun()

with tab_mulakat:
    if st.session_state.last_result is None:
        empty_state(get_icon("target", size=48), "Run a resume analysis first to generate tailored interview questions.")
    else:
        result = st.session_state.last_result
        cv_analysis = result.get("cv_analysis", {})
        job_analysis = result.get("job_analysis", {})
        match_result = result.get("match_result", {})

        if st.session_state.interview_questions is None:
            existing_questions = get_interview_questions(st.session_state.last_analysis_id) if st.session_state.last_analysis_id else []
            
            if existing_questions:
                mapped_questions = []
                for q in existing_questions:
                    mapped_questions.append({
                        "id": q["order_index"] + 1,
                        "question": q["question"],
                        "focus_area": q["category"],
                        "question_type": q["category"],
                        "difficulty": q.get("difficulty", "Medium")
                    })
                st.session_state.interview_questions = mapped_questions
                st.rerun()
            else:
                empty_state(get_icon("lightbulb", size=48), "No interview questions generated yet.")
                st.write("")
                if st.button("Generate Interview Questions", type="primary", use_container_width=True):
                    with st.spinner("Generating questions..."):
                        q_result = run_interview_generator(client, cv_analysis, job_analysis, match_result)
                        questions = q_result.get("questions", [])
                        if st.session_state.last_analysis_id:
                            save_interview_questions(st.session_state.last_analysis_id, questions)
                    st.session_state.interview_questions = questions
                    st.rerun()
        else:
            if st.session_state.interview_feedback:
                render_interview_feedback(st.session_state.interview_feedback)
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Regenerate Questions"):
                    st.session_state.interview_questions = None
                    st.session_state.interview_answers = {}
                    st.session_state.interview_feedback = None
                    st.rerun()
            else:
                st.markdown("<p style='color: #6B7280; font-size: 17px; margin-bottom: 24px;'>Answer each question below and click evaluate when you're finished.</p>", unsafe_allow_html=True)
                
                with st.form("interview_form", border=False):
                    updated_answers = render_interview_questions(st.session_state.interview_questions, st.session_state.interview_answers)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    submitted = st.form_submit_button("Finish Interview & Evaluate", type="primary", use_container_width=True)
                    
                if submitted:
                    st.session_state.interview_answers = updated_answers
                    with st.spinner("Evaluating your answers..."):
                        feedback = run_interview_evaluator(
                            client, st.session_state.interview_questions, st.session_state.interview_answers
                        )
                    
                    if st.session_state.last_analysis_id:
                        db_questions = get_interview_questions(st.session_state.last_analysis_id)
                        q_map = {q["order_index"] + 1: q["id"] for q in db_questions}
                        
                        answers_to_save = []
                        for q in st.session_state.interview_questions:
                            qid = q.get("id")
                            db_id = q_map.get(qid)
                            if db_id:
                                q_score = 0
                                q_fb = ""
                                for pf in feedback.get("per_question_feedback", []):
                                    if pf.get("question_id") == qid:
                                        q_score = pf.get("score", 0)
                                        q_fb = pf.get("feedback", "")
                                        break
                                answers_to_save.append({
                                    "question_id": db_id,
                                    "answer": st.session_state.interview_answers.get(qid, ""),
                                    "score": q_score,
                                    "feedback": q_fb
                                })
                        if answers_to_save:
                            save_interview_answers(answers_to_save)

                    st.session_state.interview_feedback = feedback
                    st.rerun()

with tab_gecmis:
    if st.session_state.get("viewing_history_in_tab"):
        if st.button("← Back to History"):
            st.session_state.viewing_history_in_tab = False
            st.rerun()
            
        if st.session_state.last_result:
            render_results_dashboard(st.session_state.last_result)
    else:
        history = get_history()
        
        if not history:
            empty_state(get_icon("clock", size=48), "No historical analyses found.")
        else:
            st.markdown(f"<div style='display: flex; align-items: center; gap: 8px; margin-bottom: 24px;'><span style='color: #111827;'>{get_icon('clock', size=28)}</span><h2 style='margin: 0 !important;'>History</h2></div>", unsafe_allow_html=True)
            
            cols = st.columns(2)
            for i, entry in enumerate(history):
                col_idx = i % 2
                with cols[col_idx]:
                    if render_history_card(entry):
                        st.session_state.viewing_history_id = entry["id"]
                        st.session_state.last_result = entry["result"]
                        st.session_state.last_analysis_id = entry["id"]
                        st.session_state.interview_questions = None
                        st.session_state.interview_answers = {}
                        st.session_state.interview_feedback = None
                        st.session_state.viewing_history_in_tab = True
                        st.rerun()
