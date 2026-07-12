import json
from google import genai
from app.agents.base import call_gemini

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

def run(client: genai.Client, cv_analysis: dict, job_analysis: dict, match_result: dict) -> dict:
    combined_input = (
        f"CV Analizi:\n{json.dumps(cv_analysis, ensure_ascii=False)}\n\n"
        f"Ilan Analizi:\n{json.dumps(job_analysis, ensure_ascii=False)}\n\n"
        f"Uyum Degerlendirmesi:\n{json.dumps(match_result, ensure_ascii=False)}"
    )
    return call_gemini(client, INTERVIEW_GENERATOR_PROMPT, combined_input)
