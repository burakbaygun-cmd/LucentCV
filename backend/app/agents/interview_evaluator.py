import json
from google import genai
from app.agents.base import call_gemini

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

def run(client: genai.Client, questions: list, answers: dict) -> dict:
    qa_pairs = []
    for q in questions:
        qid = q.get("id")
        qa_pairs.append({
            "question_id": qid,
            "question": q.get("question"),
            "answer": answers.get(str(qid), answers.get(qid, "")),
        })
    combined_input = f"Soru-Cevap Ciftleri:\n{json.dumps(qa_pairs, ensure_ascii=False)}"
    return call_gemini(client, INTERVIEW_EVALUATOR_PROMPT, combined_input)
