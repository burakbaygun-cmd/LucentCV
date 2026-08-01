import json
import re
import time
from google import genai
from google.genai import errors
from app.core.config import settings
from app.core.logging import logger

# Only currently-supported Gemini models belong here. gemini-2.0-flash was
# retired by Google on 2026-06-01 and gemini-1.5-flash even earlier -- an
# expired model ID always 404s, silently pushing every single call straight
# to the fallback below with no visible error anywhere.
MODELS_TO_TRY = ["gemini-3.5-flash", "gemini-2.5-flash"]

def get_client():
    return genai.Client(api_key=settings.GEMINI_API_KEY)

def clean_json(text: str) -> str:
    """Gemini bazen ```json fence ekliyor, temizle."""
    text = text.strip()
    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"^```\s*", "", text)
    text = re.sub(r"```$", "", text)
    return text.strip()


class AIGenerationError(Exception):
    """
    Raised when every configured Gemini model has failed (or returned
    unusable output) for a given call. Callers must NOT swallow this and
    substitute a fake "successful" result -- doing so previously caused
    quota errors to silently masquerade as a completed-but-empty analysis
    that got saved to the database with no indication anything went wrong.
    """
    def __init__(self, message: str, is_quota_error: bool = False):
        self.is_quota_error = is_quota_error
        super().__init__(message)


def call_gemini(client: genai.Client, system_prompt: str, user_content: str, agent_type: str, retries: int = 2) -> dict:
    """
    Calls Gemini, trying each model in MODELS_TO_TRY up to `retries` times.
    Raises AIGenerationError if every model/attempt fails -- callers should
    let this propagate up to the API layer so the user sees a real error
    instead of a silently-empty "successful" analysis.
    """
    full_prompt = f"{system_prompt}\n\n{user_content}"
    last_error_str = None
    saw_quota_error = False

    for model_name in MODELS_TO_TRY:
        for attempt in range(retries):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=full_prompt,
                )
                cleaned = clean_json(response.text)
                try:
                    return json.loads(cleaned)
                except json.JSONDecodeError:
                    logger.warning(f"[{agent_type}] {model_name} returned non-JSON output, retrying...")
                    last_error_str = "The model returned a response that was not valid JSON."
                    if attempt < retries - 1:
                        continue
                    break  # try the next model
            except errors.ClientError as e:
                error_str = str(e)
                last_error_str = error_str
                if "503" in error_str or "UNAVAILABLE" in error_str:
                    if attempt < retries - 1:
                        time.sleep(3)
                        continue
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    saw_quota_error = True
                    logger.warning(f"[{agent_type}] {model_name} failed ({error_str[:120]}), trying next model...")
                    break  # try the next model
                if "NOT_FOUND" in error_str or "404" in error_str:
                    logger.warning(f"[{agent_type}] {model_name} failed ({error_str[:120]}), trying next model...")
                    break  # try the next model
                raise e

    # Every configured model failed for every attempt -- surface a real error
    # instead of returning a fake, structurally-valid-but-empty result.
    logger.error(f"[{agent_type}] all models exhausted: {last_error_str}")
    if saw_quota_error:
        raise AIGenerationError(
            "AI servisi kota sınırına ulaştı. Lütfen birkaç dakika sonra tekrar deneyin.",
            is_quota_error=True,
        )
    raise AIGenerationError(
        "AI servisi şu anda yanıt veremiyor. Lütfen birkaç dakika sonra tekrar deneyin.",
        is_quota_error=False,
    )
