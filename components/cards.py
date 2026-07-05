import streamlit as st

def empty_state(icon_svg, message, button_text=None, button_callback=None):
    """Renders a beautiful empty state using SVGs instead of emojis."""
    st.markdown(
        f"""
<div class="empty-state">
    <div class="empty-state-icon">{icon_svg}</div>
    <h3 style="margin-top: 16px;">Görünüşe göre burada bir şey yok</h3>
    <p>{message}</p>
</div>
        """,
        unsafe_allow_html=True
    )
    if button_text:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(button_text, use_container_width=True, type="primary"):
                if button_callback:
                    button_callback()

def render_html_card(html_content, class_name="custom-card"):
    st.markdown(
        f"""
<div class="{class_name}">
    {html_content}
</div>
        """,
        unsafe_allow_html=True
    )
