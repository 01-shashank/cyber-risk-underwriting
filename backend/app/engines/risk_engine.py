"""Deterministic cyber risk scoring engine.

The rules in this module are intentionally explicit and mirror
docs/risk-model.md. No LLM, ML model, network call, or external data source
is used to calculate risk.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


DIMENSION_WEIGHTS = {
    "controls": 0.40,
    "incidents": 0.25,
    "vulnerabilities": 0.15,
    "supply_chain": 0.12,
    "regulatory": 0.08,
}

DIMENSION_MAX_PENALTIES = {
    "controls": 95,
    "incidents": 95,
    "vulnerabilities": 70,
    "supply_chain": 60,
    "regulatory": 30,
}

SUPPORTED_REGULATIONS = {
    "GDPR": {"compliant": 0, "partially_compliant": 8, "non_compliant": 15},
    "HIPAA": {"compliant": 0, "partially_compliant": 10, "non_compliant": 20},
    "PCI-DSS": {"compliant": 0, "partially_compliant": 8, "non_compliant": 15},
    "CCPA": {"compliant": 0, "partially_compliant": 6, "non_compliant": 12},
    "State Data Privacy Laws": {
        "compliant": 0,
        "partially_compliant": 5,
        "non_compliant": 10,
    },
}

# Canonical factor names and their parent dimensions.
FACTOR_DIMENSIONS = {
    "MFA Coverage": "controls",
    "EDR Coverage": "controls",
    "Backup & Recovery": "controls",
    "Incident Response Plan": "controls",
    "Network Segmentation": "controls",
    "Ransomware Incidents": "incidents",
    "Data Breach Incidents": "incidents",
    "Incident Frequency Trend": "incidents",
    "Unpatched Critical Vulnerabilities": "vulnerabilities",
    "Unpatched High-Severity Vulnerabilities": "vulnerabilities",
    "Patch Management Cadence": "vulnerabilities",
    "Critical Vendor Count": "supply_chain",
    "Vendor Security Assessment": "supply_chain",
    "Applicable Regulation Compliance": "regulatory",
    "Compliance Gaps": "regulatory",
}


@dataclass(frozen=True)
class RiskAssessment:
    """Structured result returned by :func:`calculate_risk`."""

    final_score: float
    risk_level: str
    recommended_action: str
    assessment_status: str
    dimension_scores: dict[str, float]
    factor_penalties: dict[str, float]
    contributing_factors: list[dict[str, Any]]
    missing_data: list[str]


def _require_number(data: Mapping[str, Any], key: str) -> float | int | None:
    value = data.get(key)
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{key} must be numeric or None")
    if value < 0:
        raise ValueError(f"{key} cannot be negative")
    return value


def _coverage_penalty(
    value: Any, thresholds: tuple[tuple[float, float], ...], missing_penalty: int,
) -> tuple[int, bool]:
    if value is None:
        return missing_penalty, True
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("coverage must be numeric or None")
    if not 0 <= value <= 100:
        raise ValueError("coverage must be between 0 and 100")
    for upper, penalty in thresholds:
        if value <= upper:
            return penalty, False
    return 0, False


def _status_penalty(value: Any, mapping: Mapping[str, int], missing_penalty: int) -> tuple[int, bool]:
    if value is None:
        return missing_penalty, True
    if value not in mapping:
        raise ValueError(f"unsupported status: {value!r}")
    return mapping[value], False


def _count_penalty(value: Any, rules: tuple[tuple[int, int], ...], missing_penalty: int) -> tuple[int, bool]:
    if value is None:
        return missing_penalty, True
    value = _require_number({"value": value}, "value")
    value = int(value)
    for upper, penalty in rules:
        if value <= upper:
            return penalty, False
    return rules[-1][1], False


def _risk_level(score: float) -> str:
    if score < 25:
        return "LOW"
    if score < 50:
        return "MEDIUM"
    if score < 75:
        return "HIGH"
    return "CRITICAL"


def _recommended_action(level: str) -> str:
    return {
        "LOW": "ACCEPT",
        "MEDIUM": "REFER",
        "HIGH": "REFER or DECLINE",
        "CRITICAL": "DECLINE",
    }[level]


def _dimension_score(total: float, maximum: float) -> float:
    return min(total / maximum * 100.0, 100.0)


def _regulatory_penalty(
    regulations: Any, gaps: Any
) -> tuple[int, bool, list[str]]:
    missing = []
    if regulations is None:
        highest = 20
        missing.append("Regulation compliance")
    else:
        if not isinstance(regulations, Mapping):
            raise ValueError("regulations must be a mapping of regulation to compliance status")
        highest = 0
        for name, status in regulations.items():
            if name not in SUPPORTED_REGULATIONS:
                raise ValueError(f"unsupported regulation: {name}")
            penalty, _ = _status_penalty(
                status, SUPPORTED_REGULATIONS[name], 20
            )
            highest = max(highest, penalty)

    if gaps is None:
        gap_penalty = 10
        missing.append("Compliance gaps")
    else:
        if isinstance(gaps, bool) or not isinstance(gaps, (int, float)) or gaps < 0:
            raise ValueError("compliance_gaps must be a non-negative number or None")
        gap_penalty = 0 if gaps == 0 else 5 if gaps <= 2 else 10

    return min(highest + gap_penalty, 30), bool(missing), missing


def calculate_risk(data: Mapping[str, Any]) -> dict[str, Any]:
    """Calculate a complete deterministic risk assessment.

    Expected input keys:
    mfa_coverage, edr_coverage, backup_status, irp_months_since_test,
    segmentation_level, ransomware_incidents, data_breach_incidents,
    incident_trend, critical_vulns, high_vulns, patch_days,
    critical_vendor_count, vendor_security_score, regulations,
    compliance_gaps.

    ``None`` means the information is unknown and triggers the documented
    conservative worst-case assumption.
    """
    if not isinstance(data, Mapping):
        raise ValueError("assessment data must be a mapping")

    penalties: dict[str, float] = {}
    missing: list[str] = []

    p, m = _coverage_penalty(data.get("mfa_coverage"), ((0, 25), (50, 15), (80, 8), (100, 0)), 25)
    penalties["MFA Coverage"] = p
    if m: missing.append("MFA coverage percentage")

    p, m = _coverage_penalty(data.get("edr_coverage"), ((0, 20), (50, 12), (80, 6), (100, 0)), 20)
    penalties["EDR Coverage"] = p
    if m: missing.append("EDR coverage percentage")

    p, m = _status_penalty(
        data.get("backup_status"),
        {
            "no_plan_or_untested": 20,
            "backups_exist_no_recent_test": 12,
            "regular_backups_tested_12_months": 6,
            "tested_regularly_air_gapped": 0,
        },
        20,
    )
    penalties["Backup & Recovery"] = p
    if m: missing.append("Backup and recovery status")

    irp = data.get("irp_months_since_test")
    if irp is None:
        p, m = 15, True
    else:
        if isinstance(irp, bool) or not isinstance(irp, (int, float)) or irp < 0:
            raise ValueError("irp_months_since_test must be a non-negative number or None")
        p = 0 if irp <= 6 else 4 if irp <= 12 else 8
        m = False
    penalties["Incident Response Plan"] = p
    if m: missing.append("Incident response plan test age")

    p, m = _status_penalty(
        data.get("segmentation_level"),
        {
            "flat_network": 15,
            "dmz_only": 8,
            "dmz_plus_limited_internal": 4,
            "advanced_critical_assets_isolated": 0,
        },
        15,
    )
    penalties["Network Segmentation"] = p
    if m: missing.append("Network segmentation level")

    p, m = _count_penalty(data.get("ransomware_incidents"), ((0, 0), (1, 20), (2, 35), (10**9, 50)), 50)
    penalties["Ransomware Incidents"] = p
    if m: missing.append("Ransomware incident history")

    p, m = _count_penalty(data.get("data_breach_incidents"), ((0, 0), (1, 15), (10**9, 30)), 30)
    penalties["Data Breach Incidents"] = p
    if m: missing.append("Data breach incident history")

    trend = data.get("incident_trend")
    if trend is None:
        p, m = 15, True
    else:
        if trend not in {"increasing", "stable", "decreasing"}:
            raise ValueError("incident_trend must be increasing, stable, decreasing, or None")
        p, m = {"increasing": 15, "stable": 0, "decreasing": 0}[trend], False
    penalties["Incident Frequency Trend"] = p
    if m: missing.append("Incident frequency trend")

    p, m = _count_penalty(data.get("critical_vulns"), ((0, 0), (3, 15), (10**9, 30)), 30)
    penalties["Unpatched Critical Vulnerabilities"] = p
    if m: missing.append("Critical vulnerability count")

    p, m = _count_penalty(data.get("high_vulns"), ((5, 0), (15, 10), (10**9, 20)), 20)
    penalties["Unpatched High-Severity Vulnerabilities"] = p
    if m: missing.append("High vulnerability count")

    patch_days = data.get("patch_days")
    if patch_days is None:
        p, m = 20, True
    else:
        if isinstance(patch_days, bool) or not isinstance(patch_days, (int, float)) or patch_days < 0:
            raise ValueError("patch_days must be a non-negative number or None")
        p = 0 if patch_days < 60 else 10 if patch_days <= 90 else 15
        m = False
    penalties["Patch Management Cadence"] = p
    if m: missing.append("Patch management cadence")

    p, m = _count_penalty(data.get("critical_vendor_count"), ((1, 0), (3, 10), (5, 20), (10**9, 35)), 35)
    penalties["Critical Vendor Count"] = p
    if m: missing.append("Critical vendor count")

    vendor_score = data.get("vendor_security_score")
    if vendor_score is None:
        p, m = 25, True
    else:
        if isinstance(vendor_score, bool) or not isinstance(vendor_score, (int, float)) or not 0 <= vendor_score <= 100:
            raise ValueError("vendor_security_score must be between 0 and 100 or None")
        p = 20 if vendor_score <= 40 else 10 if vendor_score <= 70 else 5 if vendor_score <= 85 else 0
        m = False
    penalties["Vendor Security Assessment"] = p
    if m: missing.append("Vendor security assessment")

    regulatory_penalty, _, reg_missing = _regulatory_penalty(data.get("regulations"), data.get("compliance_gaps"))
    penalties["Applicable Regulation Compliance"] = regulatory_penalty
    penalties["Compliance Gaps"] = 0  # included in the combined regulatory factor result
    missing.extend(reg_missing)

    dimension_factors = {
        "controls": [
            "MFA Coverage", "EDR Coverage", "Backup & Recovery",
            "Incident Response Plan", "Network Segmentation",
        ],
        "incidents": [
            "Ransomware Incidents", "Data Breach Incidents",
            "Incident Frequency Trend",
        ],
        "vulnerabilities": [
            "Unpatched Critical Vulnerabilities",
            "Unpatched High-Severity Vulnerabilities",
            "Patch Management Cadence",
        ],
        "supply_chain": ["Critical Vendor Count", "Vendor Security Assessment"],
        "regulatory": ["Applicable Regulation Compliance", "Compliance Gaps"],
    }

    dimension_scores: dict[str, float] = {}
    for dimension, factors in dimension_factors.items():
        total = sum(penalties[f] for f in factors)
        dimension_scores[dimension] = _dimension_score(
            total, DIMENSION_MAX_PENALTIES[dimension]
        )

    final_score = sum(
        dimension_scores[d] * DIMENSION_WEIGHTS[d]
        for d in DIMENSION_WEIGHTS
    )
    final_score = round(min(max(final_score, 0.0), 100.0), 2)
    level = _risk_level(final_score)

    contributions = []
    for factor, penalty in penalties.items():
        if factor == "Compliance Gaps":
            continue
        dimension = FACTOR_DIMENSIONS[factor]
        contribution = (
            penalty / DIMENSION_MAX_PENALTIES[dimension]
            * DIMENSION_WEIGHTS[dimension]
            * 100
        )
        contributions.append({
            "factor": factor,
            "dimension": dimension,
            "penalty": penalty,
            "contribution_points": round(contribution, 2),
        })
    contributions.sort(key=lambda x: (-x["contribution_points"], x["factor"]))

    return {
        "final_score": final_score,
        "risk_level": level,
        "recommended_action": _recommended_action(level),
        "assessment_status": "PRELIMINARY" if missing else "FINAL",
        "dimension_scores": {k: round(v, 2) for k, v in dimension_scores.items()},
        "factor_penalties": penalties,
        "contributing_factors": contributions[:5],
        "missing_data": missing,
    }


# Backward-friendly alias for callers that prefer an engine-style name.
calculate_assessment = calculate_risk
