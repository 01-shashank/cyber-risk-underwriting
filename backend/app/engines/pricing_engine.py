"""Deterministic indicative cyber-insurance pricing engine.

This is a capstone prototype pricing methodology, not an actuarial model.
It contains no LLM calls, external data, or statistical pricing.
"""

from __future__ import annotations

from typing import Any, Mapping

BASE_PREMIUM = 5000.0
DISCLAIMER = "Indicative premium — prototype methodology, not an actual insurance quote."

REVENUE_FACTORS = (
    (10_000_000, 0.80),
    (50_000_000, 1.00),
    (250_000_000, 1.25),
    (float("inf"), 1.50),
)

RISK_FACTORS = (
    (24.9, 0.80),
    (49.9, 1.00),
    (74.9, 1.35),
    (100.0, 1.75),
)

COVERAGE_FACTORS = {
    1_000_000: 1.00,
    2_000_000: 1.60,
    5_000_000: 3.50,
}


def _number(value: Any, name: str, *, minimum: float = 0.0) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    if value < minimum:
        raise ValueError(f"{name} must be >= {minimum}")
    return float(value)


def revenue_factor(annual_revenue: float) -> float:
    """Return the revenue multiplier."""
    revenue = _number(annual_revenue, "annual_revenue")
    for upper_bound, factor in REVENUE_FACTORS:
        if revenue < upper_bound or upper_bound == float("inf"):
            return factor
    raise AssertionError("Unreachable revenue band")


def risk_multiplier(risk_score: float) -> float:
    """Return the risk multiplier for a 0–100 deterministic risk score."""
    score = _number(risk_score, "risk_score")
    if score > 100:
        raise ValueError("risk_score must be between 0 and 100")
    for upper_bound, factor in RISK_FACTORS:
        if score <= upper_bound:
            return factor
    raise AssertionError("Unreachable risk band")


def incident_multiplier(
    ransomware_incidents: int, data_breach_incidents: int
) -> float:
    """Return the incident multiplier from ransomware and breach counts."""
    ransomware = _number(ransomware_incidents, "ransomware_incidents")
    breaches = _number(data_breach_incidents, "data_breach_incidents")
    if not ransomware.is_integer() or not breaches.is_integer():
        raise ValueError("incident counts must be whole numbers")
    total = int(ransomware + breaches)
    if total == 0:
        return 0.90
    if total == 1:
        return 1.10
    return 1.30


def coverage_factor(coverage_limit: int | float) -> float:
    """Return the multiplier for a supported coverage limit."""
    limit = _number(coverage_limit, "coverage_limit")
    if limit not in COVERAGE_FACTORS:
        supported = ", ".join(f"${int(x):,}" for x in COVERAGE_FACTORS)
        raise ValueError(f"coverage_limit must be one of: {supported}")
    return COVERAGE_FACTORS[int(limit)]


def calculate_premium(data: Mapping[str, Any]) -> dict[str, Any]:
    """Calculate an indicative premium from the approved prototype rules."""
    required = (
        "annual_revenue",
        "risk_score",
        "ransomware_incidents",
        "data_breach_incidents",
        "coverage_limit",
    )
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")

    revenue = revenue_factor(data["annual_revenue"])
    risk = risk_multiplier(data["risk_score"])
    incidents = incident_multiplier(
        data["ransomware_incidents"], data["data_breach_incidents"]
    )
    coverage = coverage_factor(data["coverage_limit"])

    premium = BASE_PREMIUM * revenue * risk * incidents * coverage

    return {
        "base_premium": BASE_PREMIUM,
        "revenue_factor": revenue,
        "risk_multiplier": risk,
        "incident_multiplier": incidents,
        "coverage_factor": coverage,
        "indicative_premium": round(premium, 2),
        "disclaimer": DISCLAIMER,
    }


# Convenient alias for service/API code.
calculate_indicative_premium = calculate_premium
