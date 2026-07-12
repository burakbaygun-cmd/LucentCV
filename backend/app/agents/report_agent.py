import json
from google import genai
from app.agents.base import call_gemini

REPORT_AGENT_PROMPT = """Sen bir Raporlama (Data formatting) uzmanısın.
Sana sistemde yapılmış tüm analiz (CV, İş, Eşleşme, Yönetici Özeti) verilecek.
Bu veriyi Markdown formatında güzel, okunabilir ve profesyonel bir rapora dönüştür.

SADECE aşağıdaki JSON formatında cevap ver:

{
  "markdown_report": "<Markdown metni burada olacak>"
}"""

def run(client: genai.Client, full_data: dict) -> dict:
    combined_input = f"Tüm Analiz Verisi:\n{json.dumps(full_data, ensure_ascii=False)}"
    return call_gemini(client, REPORT_AGENT_PROMPT, combined_input)
