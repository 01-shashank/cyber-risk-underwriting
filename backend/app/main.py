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

# Allow frontend/API access during the capstone demo.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Frontend is served directly by FastAPI.
FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"


@app.get("/", include_in_schema=False)
def frontend() -> FileResponse:
    """Serve the underwriting dashboard."""
    return FileResponse(FRONTEND_DIR / "index.html")


# Register API routes after the frontend root route.
app.include_router(router)
