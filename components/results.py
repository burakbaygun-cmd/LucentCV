import streamlit as st
from components.badges import render_skill_badges, get_score_color, get_score_label
from components.cards import render_html_card
from components.icons import get_icon

def render_results_dashboard(result):
    match = result.get("match_result", {})
    cv_analysis = result.get("cv_analysis", {})
    job_analysis = result.get("job_analysis", {})
    
    score = min(max(match.get("match_score", 0), 0), 100)
    color_class = get_score_color(score)
    label = get_score_label(score)
    
    # Top Score Section
    st.markdown(
        f"""
<div class="score-container">
    <div class="score-circle score-{color_class}">
        {score}%
    </div>
    <div class="score-label">{label}</div>
</div>
        """,
        unsafe_allow_html=True
    )
    
    # Skills Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"<div style='display: flex; align-items: center; gap: 8px; margin-bottom: 16px;'><span style='color: #10B981;'>{get_icon('check_circle', size=24)}</span><h3 style='margin: 0 !important;'>Strengths</h3></div>", unsafe_allow_html=True)
        skills_html = render_skill_badges(match.get("matching_skills", []), "success")
        render_html_card(skills_html)
        
    with col2:
        st.markdown(f"<div style='display: flex; align-items: center; gap: 8px; margin-bottom: 16px;'><span style='color: #EF4444;'>{get_icon('x_circle', size=24)}</span><h3 style='margin: 0 !important;'>Missing Skills</h3></div>", unsafe_allow_html=True)
        missing_html = render_skill_badges(match.get("missing_skills", []), "danger")
        render_html_card(missing_html)
        
    # Recommendations
    st.markdown(f"<div style='display: flex; align-items: center; gap: 8px; margin-bottom: 16px;'><span style='color: #F59E0B;'>{get_icon('lightbulb', size=24)}</span><h3 style='margin: 0 !important;'>Recommendations</h3></div>", unsafe_allow_html=True)
    recs = match.get("recommendations", [])
    if recs:
        recs_html = ""
        for i, r in enumerate(recs):
            recs_html += f'<div class="rec-item"><strong>{i+1}.</strong> {r}</div>'
        render_html_card(recs_html)
    else:
        render_html_card("<div class='text-secondary'>No recommendations found.</div>")
        
    # Summaries
    col_cv, col_job = st.columns(2)
    with col_cv:
        st.markdown(f"<div style='display: flex; align-items: center; gap: 8px; margin-bottom: 16px;'><span style='color: #4F46E5;'>{get_icon('file_text', size=24)}</span><h3 style='margin: 0 !important;'>Resume Summary</h3></div>", unsafe_allow_html=True)
        exp_years = cv_analysis.get('experience_years', 'Not specified')
        edu = "<br>".join(cv_analysis.get('education', [])) or 'Not specified'
        achievements = "<ul>" + "".join([f"<li>{a}</li>" for a in cv_analysis.get('key_achievements', [])]) + "</ul>" if cv_analysis.get('key_achievements') else 'Not specified'
        
        cv_summary_html = f"""
        <div style="color: #4B5563;">
            <p><strong>Experience:</strong> {exp_years} Years</p>
            <p><strong>Education:</strong><br> {edu}</p>
            <p><strong>Key Achievements:</strong></p>
            {achievements}
        </div>
        """
        render_html_card(cv_summary_html)
        
    with col_job:
        st.markdown(f"<div style='display: flex; align-items: center; gap: 8px; margin-bottom: 16px;'><span style='color: #4F46E5;'>{get_icon('briefcase', size=24)}</span><h3 style='margin: 0 !important;'>Job Requirements</h3></div>", unsafe_allow_html=True)
        min_exp = job_analysis.get('min_experience_years', 'Not specified')
        req_skills = ", ".join(job_analysis.get('required_skills', [])) or 'Not specified'
        pref_skills = ", ".join(job_analysis.get('preferred_skills', [])) or 'Not specified'
        
        job_summary_html = f"""
        <div style="color: #4B5563;">
            <p><strong>Minimum Experience:</strong> {min_exp} Years</p>
            <p><strong>Required Skills:</strong><br> {req_skills}</p>
            <p><strong>Preferred Skills:</strong><br> {pref_skills}</p>
        </div>
        """
        render_html_card(job_summary_html)
