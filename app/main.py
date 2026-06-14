import os
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

from app.db import SessionLocal, init_db
from app.models import InferenceLog

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="promptkeep", lifespan=lifespan)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


class GenerateRequest(BaseModel):
    prompt: str
    model: str = "llama-3.1-8b-instant"


class GenerateResponse(BaseModel):
    output: str
    model: str
    latency_ms: float


@app.get("/")
def root():
    return {"status": "ok", "service": "promptkeep"}


@app.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest):
    if not os.getenv("GROQ_API_KEY"):
        raise HTTPException(500, "GROQ_API_KEY not set")

    start = time.perf_counter()
    completion = client.chat.completions.create(
        model=req.model,
        messages=[{"role": "user", "content": req.prompt}],
    )
    latency_ms = (time.perf_counter() - start) * 1000
    output = completion.choices[0].message.content

    db = SessionLocal()
    try:
        db.add(InferenceLog(
            model=req.model,
            prompt=req.prompt,
            output=output,
            latency_ms=latency_ms,
        ))
        db.commit()
    finally:
        db.close()

    return GenerateResponse(output=output, model=req.model, latency_ms=latency_ms)


@app.get("/logs")
def list_logs(limit: int = 20):
    db = SessionLocal()
    try:
        rows = (
            db.query(InferenceLog)
            .order_by(InferenceLog.created_at.desc())
            .limit(limit)
            .all()
        )
        return [
            {
                "id": r.id,
                "created_at": r.created_at.isoformat(),
                "model": r.model,
                "prompt": r.prompt[:120],
                "output": r.output[:200],
                "latency_ms": round(r.latency_ms, 1),
            }
            for r in rows
        ]
    finally:
        db.close()