"""
UygunCV - Agent Orchestration
3 agent'in sirayla calistigi orkestrasyon katmani:
  1. CV Analyzer Agent
  2. Job Analyzer Agent
  3. Matcher Agent
"""

import json
import re
from google import genai

MODEL_NAME = "gemini-2.5-flash"


def clean_json(text: str) -> str:
    """Gemini bazen ```json fence ekliyor, temizle."""
    text = text.strip()
    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"```$", "", text)
    return text.strip()


import time
from google.genai import errors

def call_gemini(client: genai.Client, system_prompt: str, user_content: str, retries=3) -> dict:
    full_prompt = f"{system_prompt}\n\n{user_content}"
    
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=full_prompt,
            )
            cleaned = clean_json(response.text)
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError:
                return {"error": "JSON parse edilemedi", "raw_response": response.text}
        except errors.ClientError as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                if attempt < retries - 1:
                    time.sleep(5)  # Hız sınırına takılırsak 5 saniye bekle
                    continue
            raise e


# ---------------------------------------------------------------------------
# AGENT 1: CV Analyzer
# ---------------------------------------------------------------------------
CV_ANALYZER_PROMPT = """Sen bir CV analiz uzmanisin. Verilen CV metnini analiz ederek
yapilandirilmis bilgi cikar.

SADECE asagidaki JSON formatinda cevap ver, baska hicbir metin ekleme:

{
  "skills": [<beceri listesi, string>],
  "experience_years": <tahmini toplam deneyim yili, sayi>,
  "education": [<egitim bilgileri, string listesi>],
  "key_achievements": [<en fazla 3 onemli basari/proje, string listesi>]
}"""


def run_cv_analyzer(client: genai.Client, cv_text: str) -> dict:
    return call_gemini(client, CV_ANALYZER_PROMPT, f"CV metni:\n\n{cv_text}")


# ---------------------------------------------------------------------------
# AGENT 2: Job Analyzer
# ---------------------------------------------------------------------------
JOB_ANALYZER_PROMPT = """Sen bir is ilani analiz uzmanisin. Verilen ilan metninden
gereksinimleri ve aranan anahtar kelimeleri cikar.

SADECE asagidaki JSON formatinda cevap ver, baska hicbir metin ekleme:

{
  "required_skills": [<zorunlu beceriler, string listesi>],
  "preferred_skills": [<tercih edilen ek beceriler, string listesi>],
  "keywords": [<ATS icin onemli anahtar kelimeler, string listesi>],
  "min_experience_years": <minimum deneyim yili, sayi>
}"""


def run_job_analyzer(client: genai.Client, job_text: str) -> dict:
    return call_gemini(client, JOB_ANALYZER_PROMPT, f"Is ilani metni:\n\n{job_text}")


# ---------------------------------------------------------------------------
# AGENT 3: Matcher (ilk iki agent'in ciktisini birlestirir)
# ---------------------------------------------------------------------------
MATCHER_PROMPT = """Sen bir CV-ilan eslestirme uzmanisin. Sana bir CV analizi ve bir ilan
analizi JSON'u verilecek. Bu ikisini karsilastirarak bir uyum degerlendirmesi yap.

SADECE asagidaki JSON formatinda cevap ver, baska hicbir metin ekleme:

{
  "match_score": <0 ile 100 arasinda tam sayi>,
  "missing_skills": [<CV'de olmayan ama ilanda istenen beceriler>],
  "matching_skills": [<hem CV'de hem ilanda olan beceriler>],
  "recommendations": [<CV'yi guclendirmek icin en fazla 4 somut oneri>]
}"""


def run_matcher(client: genai.Client, cv_analysis: dict, job_analysis: dict) -> dict:
    combined_input = (
        f"CV Analizi:\n{json.dumps(cv_analysis, ensure_ascii=False)}\n\n"
        f"Ilan Analizi:\n{json.dumps(job_analysis, ensure_ascii=False)}"
    )
    return call_gemini(client, MATCHER_PROMPT, combined_input)


# ---------------------------------------------------------------------------
# AGENT 4: Interview Question Generator
# ---------------------------------------------------------------------------
INTERVIEW_GENERATOR_PROMPT = """Sen deneyimli bir Ise Alim (recruiter) uzmanisin.
Sana bir CV analizi, bir ilan analizi ve bir uyum degerlendirmesi verilecek.
Bu bilgilere gore, adaya sorulacak KISIYE OZEL 5 mulakat sorusu hazirla.

Sorular su turlerden olusmali (karisik):
- CV'deki gucli noktalari daha da acmaya yonelik sorular
- CV'de eksik/zayif gorunen becerileri test eden sorular
- Ilan gereksinimlerine ozgu senaryo/davranissal sorular
- Adayin gecmis deneyimlerinden somut ornek isteyen sorular

SADECE asagidaki JSON formatinda cevap ver, baska hicbir metin ekleme:

{
  "questions": [
    {
      "id": 1,
      "question": "<soru metni>",
      "focus_area": "<hangi beceri/konuyu test ettigi, kisa ifade>",
      "question_type": "<'guclu_nokta' | 'eksik_beceri' | 'senaryo' | 'deneyim'>"
    }
  ]
}

Tam olarak 5 soru uret, "questions" listesinde 5 eleman olmali."""


def run_interview_generator(client: genai.Client, cv_analysis: dict, job_analysis: dict, match_result: dict) -> dict:
    combined_input = (
        f"CV Analizi:\n{json.dumps(cv_analysis, ensure_ascii=False)}\n\n"
        f"Ilan Analizi:\n{json.dumps(job_analysis, ensure_ascii=False)}\n\n"
        f"Uyum Degerlendirmesi:\n{json.dumps(match_result, ensure_ascii=False)}"
    )
    return call_gemini(client, INTERVIEW_GENERATOR_PROMPT, combined_input)


# ---------------------------------------------------------------------------
# AGENT 5: Interview Evaluator
# ---------------------------------------------------------------------------
INTERVIEW_EVALUATOR_PROMPT = """Sen deneyimli bir Ise Alim (recruiter) uzmanisin.
Sana mulakat sorulari ve adayin bu sorulara verdigi cevaplar verilecek.
Her cevabi degerlendir ve genel bir mulakat performans raporu hazirla.

Degerlendirirken sunlara dikkat et:
- Cevabin somut/detayli olup olmadigi (genel gecer ifadelerden kacinilmis mi)
- Soruyla ilgili olup olmadigi
- STAR (Durum-Gorev-Aksiyon-Sonuc) yapisina yakinlik (deneyim sorularinda)
- Ilana uygunluk

SADECE asagidaki JSON formatinda cevap ver, baska hicbir metin ekleme:

{
  "overall_score": <0 ile 100 arasinda tam sayi>,
  "per_question_feedback": [
    {
      "question_id": <soru id, sayi>,
      "score": <0 ile 10 arasinda tam sayi>,
      "feedback": "<kisa, yapici geri bildirim>"
    }
  ],
  "strengths": [<mulakat boyunca gozlenen en fazla 3 guclu nokta>],
  "areas_to_improve": [<gelistirilmesi gereken en fazla 3 alan>]
}"""


def run_interview_evaluator(client: genai.Client, questions: list, answers: dict) -> dict:
    qa_pairs = []
    for q in questions:
        qid = q.get("id")
        qa_pairs.append({
            "question_id": qid,
            "question": q.get("question"),
            "answer": answers.get(qid, ""),
        })
    combined_input = f"Soru-Cevap Ciftleri:\n{json.dumps(qa_pairs, ensure_ascii=False)}"
    return call_gemini(client, INTERVIEW_EVALUATOR_PROMPT, combined_input)


# ---------------------------------------------------------------------------
# ORKESTRASYON: uc agent'i sirayla calistir
# ---------------------------------------------------------------------------
def run_full_analysis(client: genai.Client, cv_text: str, job_text: str) -> dict:
    """3 agent'i sirayla calistirir ve tum sonuclari birlestirir."""
    cv_result = run_cv_analyzer(client, cv_text)
    job_result = run_job_analyzer(client, job_text)
    match_result = run_matcher(client, cv_result, job_result)

    return {
        "cv_analysis": cv_result,
        "job_analysis": job_result,
        "match_result": match_result,
    }
