import json
from google import genai
from app.agents.base import call_gemini

MATCHER_PROMPT = """Sen bir CV-ilan eslestirme uzmanisin. Sana bir CV analizi ve bir ilan
analizi JSON'u verilecek. Bu ikisini karsilastirarak bir uyum degerlendirmesi yap.

SADECE asagidaki JSON formatinda cevap ver, baska hicbir metin ekleme:

{
  "match_score": <0 ile 100 arasinda tam sayi>,
  "missing_skills": [<CV'de olmayan ama ilanda istenen beceriler>],
  "matching_skills": [<hem CV'de hem ilanda olan beceriler>],
  "recommendations": [<CV'yi guclendirmek icin en fazla 4 somut oneri>]
}"""

def run(client: genai.Client, cv_analysis: dict, job_analysis: dict) -> dict:
    combined_input = (
        f"CV Analizi:\n{json.dumps(cv_analysis, ensure_ascii=False)}\n\n"
        f"Ilan Analizi:\n{json.dumps(job_analysis, ensure_ascii=False)}"
    )
    return call_gemini(client, MATCHER_PROMPT, combined_input)
