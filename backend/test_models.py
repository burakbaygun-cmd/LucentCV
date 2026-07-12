import os
import ssl
import httpx
from dotenv import load_dotenv

ssl._create_default_https_context = ssl._create_unverified_context
original_init = httpx.Client.__init__
def patched_init(self, *args, **kwargs):
    kwargs['verify'] = False
    original_init(self, *args, **kwargs)
httpx.Client.__init__ = patched_init

from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
for m in client.models.list():
    print(m.name)
