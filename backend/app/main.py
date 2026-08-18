"""FastAPI application entry point."""

from fastapi import FastAPI
from backend.app.api.routes import router

app = FastAPI(
    title="Cyber Risk Underwriting Workbench",
    version="0.1.0",
    description="Capstone prototype for deterministic cyber risk assessment and indicative pricing.",
)

app.include_router(router)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "Cyber Risk Underwriting Workbench",
        "status": "running",
        "docs": "/docs",
    }
