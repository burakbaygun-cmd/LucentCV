from google import genai
from app.agents.base import call_gemini

JOB_ANALYZER_PROMPT = """Sen bir is ilani analiz uzmanisin. Verilen ilan metninden
gereksinimleri ve aranan anahtar kelimeleri cikar.

SADECE asagidaki JSON formatinda cevap ver, baska hicbir metin ekleme:

{
  "required_skills": [<zorunlu beceriler, string listesi>],
  "preferred_skills": [<tercih edilen ek beceriler, string listesi>],
  "keywords": [<ATS icin onemli anahtar kelimeler, string listesi>],
  "min_experience_years": <minimum deneyim yili, sayi>
}"""

def run(client: genai.Client, job_text: str) -> dict:
    return call_gemini(client, JOB_ANALYZER_PROMPT, f"Is ilani metni:\n\n{job_text}")
