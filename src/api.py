
from fastapi import FastAPI
from pydantic import BaseModel, Field
import os

from dotenv import load_dotenv
from fastapi import HTTPException
from openai import OpenAI

from service import run_research
from api_schemas import ResearchRequest, ResearchResponse

app = FastAPI(
    title="Agentic Research Assistant API",
    description="REST API for a multi-agent AI research workflow",
    version="1.0.0",
)


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "agentic-research-assistant"
    }


@app.post("/api/research",response_model=ResearchResponse)
def create_research(request: ResearchRequest):
    load_dotenv()

    # Prevent accidental paid API calls
    if os.getenv("ENABLE_LIVE_API") != "true":
        return {
            "message": "Live research is disabled",
            "question": request.question,
            "status": "disabled"
        }

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="OpenAI API key is not configured."
        )

    client = OpenAI(
        api_key=api_key,
        timeout=60.0,
        max_retries=0
    )

    try:
        result = run_research(client, request.question)

        return {
            "question": request.question,
            "status": "completed",
            "review": result["review"].model_dump(),
            "brief": result["brief"].model_dump(),
            "revision_count": result.get("revision_count", 0)
        }

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Research workflow failed."
        )
