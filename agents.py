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


def call_gemini(client: genai.Client, system_prompt: str, user_content: str) -> dict:
    full_prompt = f"{system_prompt}\n\n{user_content}"
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=full_prompt,
    )
    cleaned = clean_json(response.text)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {"error": "JSON parse edilemedi", "raw_response": response.text}


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
