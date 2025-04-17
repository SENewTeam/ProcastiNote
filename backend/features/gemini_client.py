import os
import requests


GEMINI_API_KEY = "AIzaSyCytqPzYupgqQzPy_heU8kLOfMv46ojgWo"
class GeminiHttpClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GeminiHttpClient, cls).__new__(cls)
            cls._instance.api_key = GEMINI_API_KEY
            cls._instance.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={cls._instance.api_key}"
        return cls._instance

    def send_request(self, prompt):
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        response = requests.post(
            self.api_url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": response.text}
