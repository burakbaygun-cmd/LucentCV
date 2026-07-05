import streamlit as st
from datetime import datetime
from components.badges import get_score_color, get_score_label
from components.icons import get_icon

def format_date(iso_date_str):
    try:
        dt = datetime.fromisoformat(iso_date_str.replace("Z", "+00:00"))
        return dt.strftime("%B %d, %Y - %H:%M")
    except Exception:
        return iso_date_str

def render_history_card(entry):
    """
    Renders a beautiful premium history card.
    Returns (view_clicked, interview_clicked).
    """
    score = entry.get("match_score", 0)
    color_class = get_score_color(score)
    label = get_score_label(score)
    date_str = format_date(entry.get("timestamp", ""))
    
    cv_snip = entry.get("cv_snippet", "")[:100]
    job_snip = entry.get("job_snippet", "")[:100]
    
    result = entry.get("result", {})
    job_analysis = result.get("job_analysis", {})
    # Attempt to extract job title/company, fallback to generic
    job_title = job_analysis.get("job_title", "Position Not Specified")
    company_name = job_analysis.get("company", "Company Not Specified")
    
    # If the backend doesn't provide these, we just use a generic title
    if job_title == "Position Not Specified" and company_name == "Company Not Specified":
        job_title = "Resume Match Analysis"
        company_name = ""
        
    company_html = f'<div style="font-size: 14px; color: #6B7280; margin-bottom: 16px;">{company_name}</div>' if company_name else '<div style="margin-bottom: 16px;"></div>'
    
    match_result = result.get("match_result", {})
    skills = match_result.get("matching_skills", [])[:3] # Show max 3 skills
    
    from components.badges import render_skill_badges
    skills_html = render_skill_badges(skills, "success") if skills else ""
    if len(match_result.get("matching_skills", [])) > 3:
        skills_html = skills_html.replace('</div>', f'<span style="font-size: 12px; color: #6B7280; margin-left: 8px;">+{len(match_result.get("matching_skills", [])) - 3} more</span></div>')

    html_content = f"""
<div class="custom-card" style="padding: 24px; margin-bottom: 0; display: flex; flex-direction: column; height: 100%;">
<div style="display: flex; justify-content: space-between; align-items: flex-start;">
<div>
<h3 style="margin: 0 0 4px 0; font-size: 20px; color: #111827;">{job_title}</h3>
{company_html}
</div>
<div style="text-align: right;">
<div style="font-size: 12px; color: #9CA3AF; margin-bottom: 8px;">{date_str}</div>
<div style="display: inline-flex; align-items: center; background: var(--{color_class}-bg, #F3F4F6); padding: 4px 12px; border-radius: 999px; border: 1px solid var(--{color_class}-border, #E5E7EB);">
<div style="font-size: 16px; font-weight: 700; color: var(--{color_class}-color, #4F46E5); margin-right: 8px;">{score}%</div>
<div style="font-size: 12px; font-weight: 500; color: var(--{color_class}-color, #4F46E5);">{label}</div>
</div>
</div>
</div>
<div style="margin-bottom: 16px; flex-grow: 1;">
<p style="margin: 0 0 8px 0; font-size: 14px; color: #4B5563; line-height: 1.5;"><strong>Job:</strong> {job_snip}...</p>
<p style="margin: 0; font-size: 14px; color: #4B5563; line-height: 1.5;"><strong>Resume:</strong> {cv_snip}...</p>
</div>
<div style="margin-bottom: 24px;">
{skills_html}
</div>
</div>
"""
    st.markdown(html_content, unsafe_allow_html=True)
    
    # Render view button
    view_clicked = st.button("View Analysis", key=f"view_{entry['id']}", use_container_width=True)
    st.markdown("<div style='margin-bottom: 32px;'></div>", unsafe_allow_html=True)
            
    return view_clicked
