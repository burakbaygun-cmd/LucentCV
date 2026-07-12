import json
from google import genai
from app.agents.base import call_gemini

SUMMARY_AGENT_PROMPT = """Sen bir İnsan Kaynakları (HR) danışmanısın.
Sana bir CV analizi, bir iş ilanı analizi ve eşleşme skoru verilecek.
Amacın, adaya yönelik profesyonel ve cesaretlendirici, kısa (1-2 paragraf) bir Yönetici Özeti (Executive Summary) yazmaktır.

SADECE aşağıdaki JSON formatında cevap ver:

{
  "summary": "<Yönetici özeti metni (Türkçe)>"
}"""

def run(client: genai.Client, cv_analysis: dict, job_analysis: dict, match_result: dict) -> dict:
    combined_input = (
        f"CV Analizi:\n{json.dumps(cv_analysis, ensure_ascii=False)}\n\n"
        f"Ilan Analizi:\n{json.dumps(job_analysis, ensure_ascii=False)}\n\n"
        f"Uyum Degerlendirmesi:\n{json.dumps(match_result, ensure_ascii=False)}"
    )
    return call_gemini(client, SUMMARY_AGENT_PROMPT, combined_input)
