import os
from dotenv import load_dotenv

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_api_model = os.getenv("GEMINI_API_MODEL")
gemini_base_url = os.getenv("GEMINI_BASE_URL")

if not gemini_api_key or not gemini_api_model or not gemini_base_url:
    print("Please set environment variable or check api key or base url or model name.")
    exit(1)

class Secrets:
    def __init__(self):
        self.gemini_api_key = gemini_api_key
        self.gemini_api_model = gemini_api_model
        self.gemini_base_url = gemini_base_url