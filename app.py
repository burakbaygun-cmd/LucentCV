"""
UygunCV - Streamlit Ana Uygulama

Calistirma:
    export GEMINI_API_KEY="senin-api-keyin"
    streamlit run app.py
"""

import os
import streamlit as st
from google import genai

from agents import run_full_analysis, run_interview_generator, run_interview_evaluator
from memory import save_analysis, get_history

st.set_page_config(page_title="UygunCV", layout="wide")

API_KEY = os.environ.get("GEMINI_API_KEY")

st.title("UygunCV — CV-İlan Uyum Analizi")
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

if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "interview_questions" not in st.session_state:
    st.session_state.interview_questions = None
if "interview_answers" not in st.session_state:
    st.session_state.interview_answers = {}
if "interview_feedback" not in st.session_state:
    st.session_state.interview_feedback = None

tab_analiz, tab_mulakat, tab_gecmis = st.tabs(
    ["Yeni Analiz", "Akıllı Mülakat", "Geçmiş Analizler"]
)

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
            st.session_state.last_result = result
            # Yeni bir analiz yapildiginda eski mulakat verilerini sifirla
            st.session_state.interview_questions = None
            st.session_state.interview_answers = {}
            st.session_state.interview_feedback = None

            match = result.get("match_result", {})
            cv_analysis = result.get("cv_analysis", {})
            job_analysis = result.get("job_analysis", {})

            st.subheader(f"Uyum Skoru: {match.get('match_score', 'N/A')} / 100")
            st.progress(min(max(match.get("match_score", 0), 0), 100) / 100)

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.markdown("**Eşleşen Beceriler**")
                for s in match.get("matching_skills", []):
                    st.write(f"- {s}")
            with col_b:
                st.markdown("**Eksik Beceriler**")
                for s in match.get("missing_skills", []):
                    st.write(f"- {s}")
            with col_c:
                st.markdown("**Öneriler**")
                for r in match.get("recommendations", []):
                    st.write(f"- {r}")

            with st.expander("Detaylı CV Analizi"):
                st.json(cv_analysis)
            with st.expander("Detaylı İlan Analizi"):
                st.json(job_analysis)

with tab_mulakat:
    st.subheader("Akıllı Mülakat Simülasyonu")
    st.caption(
        "Önce 'Yeni Analiz' sekmesinde bir CV-ilan analizi yapın; ardından burada "
        "size özel hazırlanmış mülakat sorularını cevaplayabilirsiniz."
    )

    if st.session_state.last_result is None:
        st.info("Önce 'Yeni Analiz' sekmesinden bir CV-ilan analizi yapmalısınız.")
    else:
        result = st.session_state.last_result
        cv_analysis = result.get("cv_analysis", {})
        job_analysis = result.get("job_analysis", {})
        match_result = result.get("match_result", {})

        if st.session_state.interview_questions is None:
            if st.button("Mülakat Sorularını Oluştur", type="primary"):
                with st.spinner("Mülakat soruları hazırlanıyor..."):
                    q_result = run_interview_generator(client, cv_analysis, job_analysis, match_result)
                st.session_state.interview_questions = q_result.get("questions", [])
                st.rerun()
        else:
            questions = st.session_state.interview_questions
            st.markdown("### Sorularınız")

            with st.form("interview_form"):
                for q in questions:
                    qid = q.get("id")
                    st.markdown(f"**{qid}. {q.get('question')}**  \n*Odak: {q.get('focus_area', '')}*")
                    answer = st.text_area(
                        f"Cevabınız (Soru {qid})",
                        key=f"answer_{qid}",
                        value=st.session_state.interview_answers.get(qid, ""),
                        height=100,
                    )
                    st.session_state.interview_answers[qid] = answer

                submitted = st.form_submit_button("Cevapları Değerlendir")

            if submitted:
                with st.spinner("Cevaplarınız değerlendiriliyor..."):
                    feedback = run_interview_evaluator(
                        client, questions, st.session_state.interview_answers
                    )
                st.session_state.interview_feedback = feedback

            if st.session_state.interview_feedback:
                fb = st.session_state.interview_feedback
                st.markdown("---")
                st.subheader(f"Genel Mülakat Skoru: {fb.get('overall_score', 'N/A')} / 100")

                for pf in fb.get("per_question_feedback", []):
                    st.markdown(
                        f"**Soru {pf.get('question_id')} — Puan: {pf.get('score')}/10**  \n"
                        f"{pf.get('feedback')}"
                    )

                col_s, col_i = st.columns(2)
                with col_s:
                    st.markdown("**Güçlü Yönler**")
                    for s in fb.get("strengths", []):
                        st.write(f"- {s}")
                with col_i:
                    st.markdown("**Geliştirilmesi Gerekenler**")
                    for a in fb.get("areas_to_improve", []):
                        st.write(f"- {a}")

            if st.button("Soruları Yeniden Oluştur"):
                st.session_state.interview_questions = None
                st.session_state.interview_answers = {}
                st.session_state.interview_feedback = None
                st.rerun()

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
