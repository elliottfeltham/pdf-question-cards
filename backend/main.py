from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import httpx
from dotenv import load_dotenv
load_dotenv() 

from .pdf import extract_all_text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/upload")
async def upload(file: UploadFile = File(...)):
    text = extract_all_text(file.file)
    return {
        "filename": file.filename,
        "text": text,
    }

@app.get("/api/test-llm")
async def test_llm():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return {"error": "Missing OPENROUTER_API_KEY"}
    
    llm_model = os.getenv("OPENROUTER_MODEL")
    if not llm_model:
        return {"error": "Missing OPENROUTER_MODEL"}
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
    }
    payload = {
        "model": llm_model,
        "messages": [
            {"role": "user", "content": "Say hello, this is a test from my FastAPI app."}
        ]
    }

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(url, headers=headers, json=payload)
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            return {
                "error": True,
                "status": e.response.status_code,
                "details": e.response.text  
            }
        data = response.json()

    return {"raw": data}
