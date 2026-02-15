import os
import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise Exception("OPENAI_API_KEY is missing in environment variables.")

OPENAI_URL = "https://api.openai.com/v1/audio/speech"

app = FastAPI(
    title="Broken Audio Generator API",
    description="Generate AI audio using OpenAI TTS.",
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
        "message": "Broken Audio Generator API 🔊🔥",
        "usage": "/generate?text=habari%20yako"
    }

@app.get("/generate")
async def generate(text: str = Query(..., min_length=2)):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini-tts",
        "voice": "alloy",
        "input": text
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(OPENAI_URL, json=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )

    return {
        "text": text,
        "audio_base64": response.json().get("audio")
    }
