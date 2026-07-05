"""
UygunCV - Streamlit Ana Uygulama

Calistirma:
    export GEMINI_API_KEY="senin-api-keyin"
    streamlit run app.py
"""

import os
import streamlit as st
from google import genai

from agents import run_full_analysis
from memory import save_analysis, get_history

st.set_page_config(page_title="UygunCV", page_icon="📄", layout="wide")

API_KEY = os.environ.get("GEMINI_API_KEY")

st.title("📄 UygunCV — CV-İlan Uyum Analizi")
st.caption(
    "CV'nizi ve başvurmak istediğiniz iş ilanını yapıştırın; "
    "3 aşamalı AI agent zinciri uyum skorunuzu ve önerilerinizi çıkarsın."
)

if not API_KEY:
    st.error(
        "GEMINI_API_KEY ortam değişkeni bulunamadı. "
        "Terminalde `export GEMINI_API_KEY=\"...\"` çalıştırıp uygulamayı yeniden başlatın."
    )
    st.stop()

client = genai.Client(api_key=API_KEY)

tab_analiz, tab_gecmis = st.tabs(["🔍 Yeni Analiz", "🕑 Geçmiş Analizler"])

with tab_analiz:
    col1, col2 = st.columns(2)
    with col1:
        cv_text = st.text_area("CV Metni", height=300, placeholder="CV'nizi buraya yapıştırın...")
    with col2:
        job_text = st.text_area("İş İlanı Metni", height=300, placeholder="İlan metnini buraya yapıştırın...")

    if st.button("Analiz Et", type="primary"):
        if not cv_text.strip() or not job_text.strip():
            st.warning("Lütfen hem CV hem de ilan metnini girin.")
        else:
            with st.spinner("Agent'lar çalışıyor: CV analiz ediliyor..."):
                result = run_full_analysis(client, cv_text, job_text)

            save_analysis(cv_text, job_text, result)

            match = result.get("match_result", {})
            cv_analysis = result.get("cv_analysis", {})
            job_analysis = result.get("job_analysis", {})

            st.subheader(f"Uyum Skoru: {match.get('match_score', 'N/A')} / 100")
            st.progress(min(max(match.get("match_score", 0), 0), 100) / 100)

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.markdown("**✅ Eşleşen Beceriler**")
                for s in match.get("matching_skills", []):
                    st.write(f"- {s}")
            with col_b:
                st.markdown("**❌ Eksik Beceriler**")
                for s in match.get("missing_skills", []):
                    st.write(f"- {s}")
            with col_c:
                st.markdown("**💡 Öneriler**")
                for r in match.get("recommendations", []):
                    st.write(f"- {r}")

            with st.expander("Detaylı CV Analizi"):
                st.json(cv_analysis)
            with st.expander("Detaylı İlan Analizi"):
                st.json(job_analysis)

with tab_gecmis:
    history = get_history()
    if not history:
        st.info("Henüz kayıtlı analiz yok.")
    else:
        for entry in history:
            score = entry.get("match_score", "N/A")
            with st.expander(f"{entry['timestamp']} — Skor: {score}"):
                st.write("**CV (ilk 100 karakter):**", entry["cv_snippet"])
                st.write("**İlan (ilk 100 karakter):**", entry["job_snippet"])
                st.json(entry["result"])
