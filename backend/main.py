from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import httpx
import uuid
from dotenv import load_dotenv 
from .pdf import extract_all_text
from .prompts import WHOLE_PROMPT

load_dotenv()
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

@app.post("/api/generate_questions")
async def generate_questions(file: UploadFile = File(...)):
    # Extract text from PDF
    text = extract_all_text(file.file)
    if len(text) > 30000:
        return {"error": "PDF text exceeds 30,000 characters limit."}

    # Prepare LLM request
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return {"error": "Missing OPENROUTER_API_KEY"}
    
    llm_model = os.getenv("OPENROUTER_MODEL")
    if not llm_model:
        return {"error": "Missing OPENROUTER_MODEL"}
    
    prompt = WHOLE_PROMPT.format(lecture_text=text, max_items=10)
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
    }
    payload = {
        "model": llm_model,
        "messages": [
        {
          "role": "system",
          "content": (
            'Return strictly valid JSON only: {"items":[...]}. '
            "Use ONLY information from TEXT. Avoid generic CS questions. "
            "Prefer high-value, lecture-specific concepts. "
            "Each item: type ('theory'|'coding'), prompt_md (≤25 words), solution_md (≤80 words), "
            "starter_code/solution_code for coding questions (Python)."
            "Ensure starter_code doesn't give away the solution."
            "Ensure JSON is well-formed and parsable."
            )},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,  
        "top_p": 0.9,
        "max_tokens": 1200,
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
    
    
    content = data["choices"][0]["message"]["content"]

    # Clean up code block if present
    clean_content = content.strip()
    if clean_content.startswith("```"):
        clean_content = clean_content.removeprefix("```json").removeprefix("```").strip()
        if clean_content.endswith("```"):
            clean_content = clean_content[:-3].strip()

    # Parse JSON
    try:
        json_data = json.loads(clean_content)
    except json.JSONDecodeError as e:
        return {
            "error": "Failed to parse JSON from LLM response",
            "details": str(e),
            "raw_content": clean_content
        }
    
    items = json_data.get("items")

    items = [{"id": str(uuid.uuid4()), **item} for item in items]

    return {"questions": items}
    
