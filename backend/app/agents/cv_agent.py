from google import genai
from app.agents.base import call_gemini

CV_ANALYZER_PROMPT = """Sen bir CV analiz uzmanisin. Verilen CV metnini analiz ederek
yapilandirilmis bilgi cikar.

SADECE asagidaki JSON formatinda cevap ver, baska hicbir metin ekleme:

{
  "skills": [<beceri listesi, string>],
  "experience_years": <tahmini toplam deneyim yili, sayi>,
  "education": [<egitim bilgileri, string listesi>],
  "key_achievements": [<en fazla 3 onemli basari/proje, string listesi>]
}"""

def run(client: genai.Client, cv_text: str) -> dict:
    return call_gemini(client, CV_ANALYZER_PROMPT, f"CV metni:\n\n{cv_text}")
