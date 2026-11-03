from collections import defaultdict, deque
import json
import os
from time import monotonic
from typing import Any
import uuid

from dotenv import load_dotenv
from fastapi import Body, FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import httpx
import nbformat as nbf

from .notebook import items_to_notebook
from .pdf import PDFLimitError, PDFValidationError, extract_all_text
from .prompts import WHOLE_PROMPT


load_dotenv()

MAX_PDF_BYTES = 10 * 1024 * 1024
MAX_PDF_PAGES = 100
MAX_TEXT_CHARACTERS = 30_000
RATE_LIMIT_REQUESTS = 5
RATE_LIMIT_WINDOW_SECONDS = 60

app = FastAPI()

frontend_origins = [
    origin.strip()
    for origin in os.getenv("FRONTEND_ORIGINS", "http://localhost:5173").split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=frontend_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

request_times: dict[str, deque[float]] = defaultdict(deque)


def enforce_generation_rate_limit(request: Request) -> None:
    client_host = request.client.host if request.client else "unknown"
    now = monotonic()
    recent = request_times[client_host]
    while recent and now - recent[0] >= RATE_LIMIT_WINDOW_SECONDS:
        recent.popleft()

    if len(recent) >= RATE_LIMIT_REQUESTS:
        retry_after = max(1, int(RATE_LIMIT_WINDOW_SECONDS - (now - recent[0])))
        raise HTTPException(
            status_code=429,
            detail="Too many question-generation requests. Please try again shortly.",
            headers={"Retry-After": str(retry_after)},
        )
    recent.append(now)


def normalise_questions(payload: Any) -> list[dict[str, str]]:
    if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
        raise ValueError("Provider response does not contain an items list")

    raw_items = payload["items"]
    if not 1 <= len(raw_items) <= 10:
        raise ValueError("Provider returned an unexpected number of items")

    questions: list[dict[str, str]] = []
    for item in raw_items:
        if not isinstance(item, dict):
            raise ValueError("Provider returned a malformed item")

        item_type = item.get("type")
        prompt = item.get("prompt_md")
        solution = item.get("solution_md")
        if item_type not in {"theory", "coding"}:
            raise ValueError("Provider returned an unsupported item type")
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Provider returned an empty question")
        if not isinstance(solution, str) or not solution.strip():
            raise ValueError("Provider returned an empty solution")

        question = {
            "id": str(uuid.uuid4()),
            "type": item_type,
            "prompt_md": prompt.strip(),
            "solution_md": solution.strip(),
        }
        solution_code = item.get("solution_code")
        if item_type == "coding" and isinstance(solution_code, str):
            question["solution_code"] = solution_code
        questions.append(question)

    return questions


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/generate_questions")
async def generate_questions(request: Request, file: UploadFile = File(...)):
    enforce_generation_rate_limit(request)

    content_type = (file.content_type or "").split(";", 1)[0].lower()
    if content_type != "application/pdf":
        raise HTTPException(status_code=415, detail="Only PDF uploads are supported.")

    pdf_bytes = await file.read(MAX_PDF_BYTES + 1)
    await file.close()
    if not pdf_bytes:
        raise HTTPException(status_code=400, detail="The uploaded PDF is empty.")
    if len(pdf_bytes) > MAX_PDF_BYTES:
        raise HTTPException(status_code=413, detail="PDF exceeds the 10 MB upload limit.")

    try:
        text = extract_all_text(
            pdf_bytes,
            max_pages=MAX_PDF_PAGES,
            max_characters=MAX_TEXT_CHARACTERS,
        )
    except PDFLimitError as exc:
        raise HTTPException(status_code=413, detail=str(exc)) from exc
    except PDFValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if not text.strip():
        raise HTTPException(status_code=422, detail="No readable text was found in the PDF.")

    api_key = os.getenv("OPENROUTER_API_KEY")
    llm_model = os.getenv("OPENROUTER_MODEL")
    if not api_key or not llm_model:
        raise HTTPException(status_code=503, detail="Question generation is not configured.")

    prompt = WHOLE_PROMPT.format(lecture_text=text, max_items=10)
    headers = {"Authorization": f"Bearer {api_key}"}
    provider_payload = {
        "model": llm_model,
        "messages": [
            {
                "role": "system",
                "content": (
                    'Return strictly valid JSON only: {"items":[...]}. '
                    "Use ONLY information from TEXT. Avoid generic CS questions. "
                    "Prefer high-value, lecture-specific concepts. "
                    "Each item: type ('theory'|'coding'), prompt_md (<=25 words), "
                    "solution_md (<=80 words), and solution_code for coding questions (Python). "
                    "Do not include starter code. Ensure JSON is well-formed and parsable."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "top_p": 0.9,
        "max_tokens": 1200,
    }

    try:
        async with httpx.AsyncClient(timeout=60, follow_redirects=False) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=provider_payload,
            )
            response.raise_for_status()
            provider_data = response.json()
        content = provider_data["choices"][0]["message"]["content"]
        if not isinstance(content, str):
            raise ValueError("Provider returned non-text content")
    except (httpx.HTTPError, KeyError, IndexError, TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=502,
            detail="The question-generation provider returned an invalid response.",
        ) from exc

    clean_content = content.strip()
    if clean_content.startswith("```"):
        clean_content = clean_content.removeprefix("```json").removeprefix("```").strip()
        if clean_content.endswith("```"):
            clean_content = clean_content[:-3].strip()

    try:
        questions = normalise_questions(json.loads(clean_content))
    except (json.JSONDecodeError, ValueError) as exc:
        raise HTTPException(
            status_code=502,
            detail="The question-generation provider returned malformed question data.",
        ) from exc

    return {"questions": questions}


@app.post("/api/export/notebook")
def export_notebook(payload: dict = Body(...)):
    title = str(payload.get("title", "Lecture Notebook"))[:120]
    items = payload.get("items", [])
    if not isinstance(items, list) or len(items) > 50:
        raise HTTPException(status_code=400, detail="Notebook export supports up to 50 items.")

    notebook = items_to_notebook(title, items)
    data = nbf.writes(notebook)
    safe_name = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_")).rstrip()
    filename = (safe_name or "notebook").replace(" ", "_")
    return Response(
        content=data,
        media_type="application/x-ipynb+json",
        headers={"Content-Disposition": f'attachment; filename="{filename}.ipynb"'},
    )
