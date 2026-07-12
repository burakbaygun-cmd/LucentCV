from components.icons import get_icon

def get_score_color(score):
    if score >= 90:
        return "success"
    elif score >= 75:
        return "primary"
    elif score >= 60:
        return "warning"
    else:
        return "danger"

def get_score_label(score):
    if score >= 90:
        return "Excellent Match"
    elif score >= 75:
        return "Good Match"
    elif score >= 60:
        return "Fair Match"
    else:
        return "Poor Match"

def render_badge(text, color="neutral", icon_svg=""):
    """
    Renders a premium HTML badge.
    Colors: primary, success, warning, danger, neutral
    """
    icon_html = f"<span style='display: flex; align-items: center; justify-content: center; margin-right: 6px;'>{icon_svg}</span>" if icon_svg else ""
    return f"<span class='badge badge-{color}' style='display: inline-flex; align-items: center;'>{icon_html}{text}</span>"

def render_score_badge(score):
    color = get_score_color(score)
    label = get_score_label(score)
    return render_badge(f"{score}% - {label}", color)

def render_skill_badges(skills, status="success"):
    """
    Renders a string of premium HTML badges for a list of skills.
    """
    if not skills:
        return render_badge("Bulunamadı", "neutral")
    
    icon_svg = get_icon("check_circle", size=16) if status == "success" else get_icon("x_circle", size=16)
    color = "success" if status == "success" else "danger"
    
    html = "<div style='display: flex; flex-wrap: wrap; gap: 8px;'>"
    for s in skills:
        html += render_badge(s, color, icon_svg)
    html += "</div>"
    return html

def render_difficulty_badge(difficulty):
    difficulty_map = {
        "kolay": "success",
        "orta": "warning",
        "zor": "danger",
        "easy": "success",
        "medium": "warning",
        "hard": "danger"
    }
    color = difficulty_map.get(str(difficulty).lower(), "primary")
    return render_badge(difficulty, color)
