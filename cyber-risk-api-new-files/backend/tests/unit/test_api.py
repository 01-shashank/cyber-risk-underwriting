from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def assessment_payload():
    return {
        "mfa_coverage": 90,
        "edr_coverage": 85,
        "backup_status": "tested_regularly_air_gapped",
        "irp_months_since_test": 4,
        "segmentation_level": "advanced_critical_assets_isolated",
        "ransomware_incidents": 0,
        "data_breach_incidents": 0,
        "incident_trend": "stable",
        "critical_vulns": 0,
        "high_vulns": 2,
        "patch_days": 20,
        "critical_vendor_count": 1,
        "vendor_security_score": 92,
        "regulations": {"HIPAA": "compliant"},
        "compliance_gaps": 0,
        "annual_revenue": 20_000_000,
        "coverage_limit": 1_000_000,
    }


def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_assessment_returns_risk_and_pricing():
    response = client.post("/api/v1/assessments", json=assessment_payload())
    assert response.status_code == 200
    body = response.json()
    assert "risk" in body
    assert "pricing" in body
    assert body["risk"]["final_score"] == 0.0
    assert body["risk"]["risk_level"] == "LOW"
    assert body["pricing"]["indicative_premium"] > 0
    assert "prototype methodology" in body["pricing"]["disclaimer"]


def test_invalid_request_returns_422():
    payload = assessment_payload()
    payload["mfa_coverage"] = 150
    response = client.post("/api/v1/assessments", json=payload)
    assert response.status_code == 422
