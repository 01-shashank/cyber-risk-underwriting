import pytest

from backend.app.engines.pricing_engine import (
    BASE_PREMIUM,
    DISCLAIMER,
    calculate_premium,
    coverage_factor,
    incident_multiplier,
    revenue_factor,
    risk_multiplier,
)


def test_revenue_bands():
    assert revenue_factor(9_999_999) == 0.80
    assert revenue_factor(10_000_000) == 1.00
    assert revenue_factor(50_000_000) == 1.25
    assert revenue_factor(250_000_001) == 1.50


@pytest.mark.parametrize(
    "score,expected",
    [(0, 0.80), (24.9, 0.80), (25, 1.00), (49.9, 1.00),
     (50, 1.35), (74.9, 1.35), (75, 1.75), (100, 1.75)],
)
def test_risk_bands(score, expected):
    assert risk_multiplier(score) == expected


def test_incident_bands():
    assert incident_multiplier(0, 0) == 0.90
    assert incident_multiplier(1, 0) == 1.10
    assert incident_multiplier(0, 1) == 1.10
    assert incident_multiplier(1, 1) == 1.30
    assert incident_multiplier(2, 0) == 1.30


def test_coverage_bands():
    assert coverage_factor(1_000_000) == 1.00
    assert coverage_factor(2_000_000) == 1.60
    assert coverage_factor(5_000_000) == 3.50


def test_formula_and_breakdown():
    result = calculate_premium({
        "annual_revenue": 20_000_000,
        "risk_score": 68.2,
        "ransomware_incidents": 1,
        "data_breach_incidents": 0,
        "coverage_limit": 2_000_000,
    })
    expected = BASE_PREMIUM * 1.00 * 1.35 * 1.10 * 1.60
    assert result["indicative_premium"] == round(expected, 2)
    assert result["base_premium"] == 5000.0
    assert result["revenue_factor"] == 1.00
    assert result["risk_multiplier"] == 1.35
    assert result["incident_multiplier"] == 1.10
    assert result["coverage_factor"] == 1.60


def test_rounding():
    result = calculate_premium({
        "annual_revenue": 20_000_000,
        "risk_score": 25,
        "ransomware_incidents": 0,
        "data_breach_incidents": 0,
        "coverage_limit": 1_000_000,
    })
    assert isinstance(result["indicative_premium"], float)
    assert round(result["indicative_premium"], 2) == result["indicative_premium"]


@pytest.mark.parametrize("revenue", [-1, "10m", True])
def test_invalid_revenue(revenue):
    with pytest.raises(ValueError):
        revenue_factor(revenue)


@pytest.mark.parametrize("score", [-1, 100.01, "high", True])
def test_invalid_risk_score(score):
    with pytest.raises(ValueError):
        risk_multiplier(score)


def test_invalid_coverage():
    with pytest.raises(ValueError):
        coverage_factor(3_000_000)


def test_invalid_incident_count():
    with pytest.raises(ValueError):
        incident_multiplier(-1, 0)
    with pytest.raises(ValueError):
        incident_multiplier(1.5, 0)


def test_missing_input():
    with pytest.raises(ValueError):
        calculate_premium({"annual_revenue": 10_000_000})


def test_disclaimer():
    result = calculate_premium({
        "annual_revenue": 5_000_000,
        "risk_score": 20,
        "ransomware_incidents": 0,
        "data_breach_incidents": 0,
        "coverage_limit": 1_000_000,
    })
    assert result["disclaimer"] == DISCLAIMER


def test_deterministic():
    data = {
        "annual_revenue": 100_000_000,
        "risk_score": 75,
        "ransomware_incidents": 2,
        "data_breach_incidents": 0,
        "coverage_limit": 5_000_000,
    }
    assert calculate_premium(data) == calculate_premium(data)
