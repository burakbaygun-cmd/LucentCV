import os
import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def get_supabase_client() -> Client:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_ANON_KEY")
    if not url or not key:
        st.error("SUPABASE_URL and SUPABASE_ANON_KEY ortam değişkenleri bulunamadı. Lütfen terminalde export ederek uygulamayı yeniden başlatın.")
        st.stop()
    return create_client(url, key)

def save_analysis(cv_text: str, job_text: str, result: dict) -> str:
    """Yeni bir analiz sonucunu Supabase'e ekler ve id dondurur."""
    client = get_supabase_client()
    match = result.get("match_result", {})
    
    data = {
        "cv_text": cv_text,
        "job_text": job_text,
        "match_score": match.get("match_score", 0),
        "summary": "CV analizi başarıyla tamamlandı.",
        "strengths": match.get("matching_skills", []),
        "weaknesses": match.get("missing_skills", []),
        "missing_skills": match.get("missing_skills", []),
        "recommendations": match.get("recommendations", []),
        "raw_response": result,
        "status": "completed"
    }
    
    try:
        res = client.table("analyses").insert(data).execute()
        if res.data:
            return res.data[0]["id"]
    except Exception as e:
        st.error(f"Veritabanı hatası (save_analysis): {e}")
    return None

def get_history() -> list:
    """Gecmis analizlerin ozet listesini Supabase'den dondurur (en yeni once)."""
    client = get_supabase_client()
    try:
        res = client.table("analyses").select("*").order("created_at", desc=True).execute()
        
        # Orijinal memory.py formatina dondur
        history = []
        for row in res.data:
            history.append({
                "id": row["id"],
                "timestamp": row["created_at"],
                "cv_snippet": row["cv_text"][:100] if row["cv_text"] else "",
                "job_snippet": row["job_text"][:100] if row["job_text"] else "",
                "match_score": row["match_score"],
                "result": row["raw_response"],
            })
        return history
    except Exception as e:
        st.error(f"Veritabanı hatası (get_history): {e}")
        return []

def get_interview_questions(analysis_id: str) -> list:
    """Verilen analiz icin daha once olusturulmus mulakat sorularini dondurur."""
    client = get_supabase_client()
    try:
        res = client.table("interview_questions").select("*").eq("analysis_id", analysis_id).order("order_index").execute()
        return res.data
    except Exception as e:
        st.error(f"Veritabanı hatası (get_interview_questions): {e}")
        return []

def save_interview_questions(analysis_id: str, questions: list) -> list:
    """Olusturulan mulakat sorularini Supabase'e kaydeder."""
    client = get_supabase_client()
    data = []
    for i, q in enumerate(questions):
        data.append({
            "analysis_id": analysis_id,
            "question": q.get("question"),
            "category": q.get("question_type", q.get("focus_area")),
            "order_index": i
        })
    try:
        res = client.table("interview_questions").insert(data).execute()
        return res.data
    except Exception as e:
        st.error(f"Veritabanı hatası (save_interview_questions): {e}")
        return []

def save_interview_answers(answers_data: list):
    """Kullanicinin verdigi cevaplari ve degerlendirme sonuclarini kaydeder."""
    client = get_supabase_client()
    try:
        res = client.table("interview_answers").insert(answers_data).execute()
        return res.data
    except Exception as e:
        st.error(f"Veritabanı hatası (save_interview_answers): {e}")
        return []
