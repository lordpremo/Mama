import os
import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise Exception("OPENAI_API_KEY is missing in environment variables.")

OPENAI_URL = "https://api.openai.com/v1/videos/generations"

app = FastAPI(
    title="Broken Video Generator API",
    description="Generate AI videos using OpenAI.",
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
        "message": "Broken Video Generator API 🎬🔥",
        "usage": "/generate?prompt=robot%20dancing"
    }

@app.get("/generate")
async def generate(prompt: str = Query(..., min_length=3)):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini-video",   # ⭐ MODEL SAHIHI
        "prompt": prompt
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(OPENAI_URL, json=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )

    return {
        "prompt": prompt,
        "result": response.json()
    }
