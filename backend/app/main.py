"""FastAPI application entry point."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from backend.app.api.routes import router

app = FastAPI(
    title="Cyber Risk Underwriting Workbench",
    version="0.1.0",
    description=(
        "Capstone prototype for deterministic cyber risk "
        "assessment and indicative pricing."
    ),
)

# Frontend and API are served from the same Codespace port.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Frontend location.
FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"


@app.get("/", include_in_schema=False)
def frontend() -> FileResponse:
    """Serve the underwriting dashboard."""
    return FileResponse(FRONTEND_DIR / "index.html")


# API routes:
# /api/v1/health
# /api/v1/assessments
app.include_router(router)
