import os
import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise Exception("OPENAI_API_KEY is missing in environment variables.")

OPENAI_URL = "https://api.openai.com/v1/chat/completions"

app = FastAPI(
    title="Broken Global Translator API",
    description="Translate any language to any language using AI.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "Broken Global Translator API 🌍🔥",
        "usage": "/translate?text=habari%20yako&to=en"
    }

@app.get("/translate")
async def translate(
    text: str = Query(..., min_length=1),
    to: str = Query(..., min_length=2)
):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    Detect the language of this text: '{text}'.
    Then translate it into '{to}'.
    Return ONLY the translated text.
    """

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a global translation engine."},
            {"role": "user", "content": prompt}
        ]
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(OPENAI_URL, json=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )

    translated = response.json()["choices"][0]["message"]["content"]

    return {
        "original": text,
        "translated_to": to,
        "translation": translated
    }
