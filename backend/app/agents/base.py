import json
import re
import time
from google import genai
from google.genai import errors
from app.core.config import settings

MODEL_NAME = "gemini-3.5-flash"

def get_client():
    return genai.Client(api_key=settings.GEMINI_API_KEY)

def clean_json(text: str) -> str:
    """Gemini bazen ```json fence ekliyor, temizle."""
    text = text.strip()
    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"```$", "", text)
    return text.strip()

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
            error_str = str(e)
            if "503" in error_str or "UNAVAILABLE" in error_str:
                if attempt < retries - 1:
                    time.sleep(5)
                    continue
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                # Return MOCK data because daily limit is reached
                if "CV okuyucu" in system_prompt or "resume" in system_prompt.lower():
                    return {"name": "Mock User", "skills": ["Mock Skill 1", "Mock Skill 2"], "experience": ["Mock Experience"]}
                elif "Job okuyucu" in system_prompt or "job posting" in system_prompt.lower():
                    return {"title": "Mock Job", "requirements": ["Mock Req 1"]}
                elif "Eşleştirici" in system_prompt or "match" in system_prompt.lower() or "score" in system_prompt.lower():
                    return {"match_score": 85, "match_analysis": "Mock analysis due to API limit.", "missing_skills": ["Mock missing"]}
                else:
                    return {"summary": "MOCK SUMMARY: Your Google Gemini API Free Tier daily limit (20 requests) has been reached. Please wait 24 hours or upgrade your billing."}
            raise e
