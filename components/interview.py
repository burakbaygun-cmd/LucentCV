import streamlit as st
from components.badges import render_difficulty_badge
from components.icons import get_icon

def render_interview_questions(questions, answers_dict):
    """
    Renders interview questions nicely inside bordered containers.
    Returns the updated answers dictionary.
    """
    updated_answers = {}
    
    for q in questions:
        st.markdown(
            f"""
<div class="custom-card" style="padding: 24px; margin-bottom: 24px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        {render_difficulty_badge(q.get("difficulty", "Medium"))}
        <span style="color: #6B7280; font-size: 14px; font-weight: 500;">Category: {q.get("focus_area", q.get("category", "General"))}</span>
    </div>
    <h3 style="margin-top: 0;">Question {q.get('id')}</h3>
    <p style="font-size: 17px; color: #111827; margin-bottom: 16px;">{q.get('question')}</p>
</div>
            """,
            unsafe_allow_html=True
        )
        
        # The text area must be outside the markdown HTML wrapper because Streamlit widgets can't be embedded inside arbitrary HTML.
        # However, we can wrap the widget using st.container with our styling if needed, but standard is fine.
        
        answer = st.text_area(
            "Your Answer",
            key=f"answer_{q.get('id')}",
            value=answers_dict.get(q.get('id'), ""),
            height=140,
            placeholder="Type your answer here...",
            label_visibility="collapsed"
        )
        updated_answers[q.get('id')] = answer
        st.markdown("<div style='margin-bottom: 32px;'></div>", unsafe_allow_html=True)
            
    return updated_answers

def render_interview_feedback(feedback):
    """
    Renders the interview evaluation feedback in a structured layout.
    """
    score = feedback.get('overall_score', 0)
    
    st.markdown(f"<div style='display: flex; align-items: center; gap: 8px; margin-bottom: 24px;'><span style='color: #4F46E5;'>{get_icon('target', size=32)}</span><h2 style='margin: 0 !important;'>Interview Evaluation Report</h2></div>", unsafe_allow_html=True)
    
    from components.badges import get_score_color
    color_class = get_score_color(score)
    st.markdown(
        f"""
<div class="custom-card" style="text-align: center; padding: 48px 24px; margin-bottom: 32px;">
    <h3 style="margin: 0 0 16px 0; color: #6B7280; font-weight: 500;">Overall Interview Score</h3>
    <div style="font-size: 64px; font-weight: 800; color: var(--{color_class}-color, #4F46E5);">{score}<span style="font-size: 32px; color: #9CA3AF;"> / 100</span></div>
</div>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div style='display: flex; align-items: center; gap: 8px; margin-bottom: 16px;'><span style='color: #10B981;'>{get_icon('check_circle', size=24)}</span><h3 style='margin: 0 !important;'>Strengths</h3></div>", unsafe_allow_html=True)
        strengths_html = "<ul style='color: #4B5563; font-size: 17px;'>" + "".join([f"<li style='margin-bottom: 8px;'>{s}</li>" for s in feedback.get("strengths", [])]) + "</ul>"
        from components.cards import render_html_card
        render_html_card(strengths_html)
            
    with col2:
        st.markdown(f"<div style='display: flex; align-items: center; gap: 8px; margin-bottom: 16px;'><span style='color: #F59E0B;'>{get_icon('alert_circle', size=24)}</span><h3 style='margin: 0 !important;'>Areas to Improve</h3></div>", unsafe_allow_html=True)
        improve_html = "<ul style='color: #4B5563; font-size: 17px;'>" + "".join([f"<li style='margin-bottom: 8px;'>{a}</li>" for a in feedback.get("areas_to_improve", [])]) + "</ul>"
        render_html_card(improve_html)
            
    st.markdown("<h3 style='margin-top: 32px; margin-bottom: 24px;'>Detailed Feedback</h3>", unsafe_allow_html=True)
    for pf in feedback.get("per_question_feedback", []):
        st.markdown(
            f"""
<div class="custom-card">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <h4 style="margin: 0;">Question {pf.get('question_id')}</h4>
        <span class="badge badge-neutral" style="font-size: 16px; padding: 4px 12px;">Score: {pf.get('score')}/10</span>
    </div>
    <p style="color: #4B5563; margin: 0; font-size: 17px;">{pf.get('feedback')}</p>
</div>
            """,
            unsafe_allow_html=True
        )
