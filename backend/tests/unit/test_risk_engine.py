import pytest

from backend.app.engines.risk_engine import calculate_risk


def perfect_data():
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
    }


def test_perfect_example_is_low():
    result = calculate_risk(perfect_data())
    assert result["final_score"] == 0.0
    assert result["risk_level"] == "LOW"
    assert result["recommended_action"] == "ACCEPT"
    assert result["assessment_status"] == "FINAL"


def test_all_worst_case_is_critical():
    data = {
        "mfa_coverage": 0,
        "edr_coverage": 0,
        "backup_status": "no_plan_or_untested",
        "irp_months_since_test": None,
        "segmentation_level": "flat_network",
        "ransomware_incidents": 3,
        "data_breach_incidents": 1,
        "incident_trend": "increasing",
        "critical_vulns": 8,
        "high_vulns": 40,
        "patch_days": None,
        "critical_vendor_count": 6,
        "vendor_security_score": None,
        "regulations": {"PCI-DSS": "non_compliant"},
        "compliance_gaps": 3,
    }
    result = calculate_risk(data)
    assert result["risk_level"] == "CRITICAL"
    assert result["final_score"] > 75


def test_incident_trend_decreasing_never_creates_negative_score():
    data = perfect_data()
    data["incident_trend"] = "decreasing"
    result = calculate_risk(data)
    assert result["dimension_scores"]["incidents"] == 0.0
    assert result["final_score"] == 0.0


@pytest.mark.parametrize(
    "score,expected",
    [(0, "LOW"), (24.99, "LOW"), (25, "MEDIUM"),
     (49.99, "MEDIUM"), (50, "HIGH"), (74.99, "HIGH"), (75, "CRITICAL"),
     (100, "CRITICAL")],
)
def test_risk_level_boundaries(monkeypatch, score, expected):
    # Exercise the public classification through a controlled calculation.
    from backend.app.engines import risk_engine
    monkeypatch.setattr(
        risk_engine,
        "_dimension_score",
        lambda total, maximum: score,
    )
    result = calculate_risk(perfect_data())
    assert result["risk_level"] == expected


def test_missing_data_is_worst_case_and_preliminary():
    data = perfect_data()
    data["mfa_coverage"] = None
    data["ransomware_incidents"] = None
    result = calculate_risk(data)
    assert result["assessment_status"] == "PRELIMINARY"
    assert "MFA coverage percentage" in result["missing_data"]
    assert "Ransomware incident history" in result["missing_data"]
    assert result["factor_penalties"]["MFA Coverage"] == 25
    assert result["factor_penalties"]["Ransomware Incidents"] == 50


def test_regulatory_uses_highest_penalty_plus_gaps():
    data = perfect_data()
    data["regulations"] = {
        "GDPR": "partially_compliant",      # 8
        "HIPAA": "non_compliant",           # 20
    }
    data["compliance_gaps"] = 3             # 10
    result = calculate_risk(data)
    assert result["factor_penalties"]["Applicable Regulation Compliance"] == 30
    assert result["dimension_scores"]["regulatory"] == 100.0


def test_top_factor_formula():
    data = perfect_data()
    data["mfa_coverage"] = 45  # +15
    result = calculate_risk(data)
    mfa = next(x for x in result["contributing_factors"] if x["factor"] == "MFA Coverage")
    assert mfa["contribution_points"] == 6.32


def test_deterministic():
    data = perfect_data()
    assert calculate_risk(data) == calculate_risk(data)


def test_invalid_coverage_rejected():
    data = perfect_data()
    data["mfa_coverage"] = 101
    with pytest.raises(ValueError):
        calculate_risk(data)


def test_invalid_regulation_rejected():
    data = perfect_data()
    data["regulations"] = {"UNKNOWN": "non_compliant"}
    with pytest.raises(ValueError):
        calculate_risk(data)


def test_all_dimension_weights_sum_to_one():
    from backend.app.engines.risk_engine import DIMENSION_WEIGHTS
    assert sum(DIMENSION_WEIGHTS.values()) == pytest.approx(1.0)
