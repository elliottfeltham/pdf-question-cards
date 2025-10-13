from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

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
    # Just echo back for now
    content = await file.read()
    return {
        "filename": file.filename,
        "size": len(content),
        "message": "Backend is receiving files correctly!"
    }
