"""Assessment API for the Cyber Risk Underwriting Workbench."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.app.engines.pricing_engine import calculate_premium
from backend.app.engines.risk_engine import calculate_risk

router = APIRouter(prefix="/api/v1", tags=["assessments"])


class AssessmentRequest(BaseModel):
    mfa_coverage: float | None = Field(default=None, ge=0, le=100)
    edr_coverage: float | None = Field(default=None, ge=0, le=100)
    backup_status: str | None = None
    irp_months_since_test: float | None = Field(default=None, ge=0)
    segmentation_level: str | None = None

    ransomware_incidents: int | None = Field(default=None, ge=0)
    data_breach_incidents: int | None = Field(default=None, ge=0)
    incident_trend: str | None = None

    critical_vulns: int | None = Field(default=None, ge=0)
    high_vulns: int | None = Field(default=None, ge=0)
    patch_days: float | None = Field(default=None, ge=0)

    critical_vendor_count: int | None = Field(default=None, ge=0)
    vendor_security_score: float | None = Field(default=None, ge=0, le=100)

    regulations: dict[str, str] | None = None
    compliance_gaps: int | None = Field(default=None, ge=0)

    annual_revenue: float = Field(gt=0)
    coverage_limit: int = Field(gt=0)


class AssessmentResponse(BaseModel):
    risk: dict[str, Any]
    pricing: dict[str, Any]


@router.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "cyber-risk-underwriting-api",
    }


@router.post("/assessments", response_model=AssessmentResponse)
def create_assessment(
    request: AssessmentRequest,
) -> AssessmentResponse:
    data = request.model_dump()

    try:
        risk = calculate_risk(data)

        pricing = calculate_premium(
            {
                "annual_revenue": data["annual_revenue"],
                "risk_score": risk["final_score"],
                "ransomware_incidents": data["ransomware_incidents"] or 0,
                "data_breach_incidents": data["data_breach_incidents"] or 0,
                "coverage_limit": data["coverage_limit"],
            }
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    return AssessmentResponse(
        risk=risk,
        pricing=pricing,
    )
