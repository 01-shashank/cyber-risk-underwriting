# CYBER RISK UNDERWRITING WORKBENCH — DETERMINISTIC RISK MODEL

## 1. EXECUTIVE SUMMARY

This document defines the deterministic risk scoring model for the Cyber Risk Underwriting Workbench. The model calculates a single numeric risk score (0–100) based on five independent risk dimensions. Each dimension contributes to the final score according to its documented weight.

**Key Principles:**
- **Deterministic**: Same input data always produces the same score
- **Simple**: Pure arithmetic and explicit rules; no machine learning
- **Explainable**: Underwriters can understand why a score was calculated
- **Auditable**: All calculations are preserved and traceable
- **Capstone-appropriate**: 15 scoring factors demonstrating real underwriting logic, simple enough to review in one meeting

---

## 2. RISK SCORE DEFINITION

### Numeric Range and Risk Levels

| Score Range | Risk Level | Interpretation | Underwriting Action |
|---|---|---|---|
| 0.0–24.9 | **LOW** | Excellent posture; minimal risk | ACCEPT |
| 25.0–49.9 | **MEDIUM** | Acceptable with some gaps | REFER for review |
| 50.0–74.9 | **HIGH** | Significant concerns; elevated risk | REFER or DECLINE |
| 75.0–100 | **CRITICAL** | Severe deficiencies; unacceptable | DECLINE |

### Boundary Definitions

- **Score 0.0–24.9**: Risk Level = LOW
- **Score 25.0–49.9**: Risk Level = MEDIUM (starts at 25.0 exactly)
- **Score 50.0–74.9**: Risk Level = HIGH (starts at 50.0 exactly)
- **Score 75.0–100.0**: Risk Level = CRITICAL (starts at 75.0 exactly)

### Important: Human Underwriter Review Required

This risk score is a **recommendation only** for human underwriter review. Underwriters retain full authority to accept, refer, or decline any application regardless of the calculated risk score. The model is a prototype decision-support tool, not an autonomous insurance system.

---

## 3. THE FIVE RISK DIMENSIONS

Each dimension produces a normalized 0–100 risk score. The five scores are then weighted and combined to produce the **final risk score**.

| Dimension | Weight | Focus | Factor Count |
|---|---|---|---|
| **Security Controls** | 40% | Preventive defenses | 5 factors |
| **Cyber Incidents** | 25% | Historical track record | 3 factors |
| **Vulnerabilities** | 15% | Technical exposure | 3 factors |
| **Supply Chain** | 12% | Third-party risk | 2 factors |
| **Regulatory** | 8% | Compliance gaps | 2 factors |

**Total: 15 scoring factors** across all five dimensions.

**Weight Rationale:**
- Controls (40%): Foundation of defense; most important factor
- Incidents (25%): Organizations hit by ransomware/breach have proven risk
- Vulnerabilities (15%): Technical exposure; important but managed through controls
- Supply Chain (12%): Emerging risk; but typically secondary to direct posture
- Regulatory (8%): Compliance gaps matter; smaller weight for capstone scope

---

## 4. DIMENSION 1: SECURITY CONTROLS (40% Weight)

### Purpose
Evaluate the organization's defensive capabilities based on presence and coverage of critical controls.

### Scoring Approach

For each control, assess coverage level (percentage of systems/users) and map to a penalty. Sum all penalties, normalize to 0–100.

```
Controls_Risk_Score = MIN(SUM(Control_Penalties) / Max_Possible_Penalty * 100, 100)
Max_Possible_Penalty = 95
```

### Control Factors (5 factors)

#### **Factor 1.1: Multi-Factor Authentication (MFA) Coverage**

| Coverage Level | Penalty |
|---|---|
| Not implemented (0%) | +25 |
| 1–50% coverage | +15 |
| 51–80% coverage | +8 |
| 81–100% coverage | 0 |

**Definition**: Percentage of user accounts/systems requiring MFA.

**Why it matters**: MFA prevents account compromise; single most effective preventive control.

---

#### **Factor 1.2: Endpoint Detection & Response (EDR) Coverage**

| Coverage Level | Penalty |
|---|---|
| Not deployed (0%) | +20 |
| 1–50% of endpoints | +12 |
| 51–80% of endpoints | +6 |
| 81–100% of endpoints | 0 |

**Definition**: Percentage of endpoints (desktops, laptops, servers) with EDR agent deployed.

**Why it matters**: EDR detects and contains ransomware and lateral movement; critical for incident response.

---

#### **Factor 1.3: Backup & Recovery Plan**

| Status | Penalty |
|---|---|
| No plan or untested | +20 |
| Backups exist; no recent test | +12 |
| Regular backups; tested in past 12 months | +6 |
| Tested regularly + air-gapped copy maintained | 0 |

**Definition**: Documented backup strategy with recovery testing and offline backup copy.

**Why it matters**: Ransomware defense; ability to recover without extortion payment.

---

#### **Factor 1.4: Incident Response Plan**

| Status | Penalty |
|---|---|
| None or unknown | +15 |
| Exists; not tested in past 2 years | +8 |
| Exists; tested in past 12 months | +4 |
| Exists; tested in past 6 months | 0 |

**Definition**: Documented plan for detecting, containing, and recovering from security incidents.

**Why it matters**: Tested IR plans reduce incident damage; indicates preparedness.

---

#### **Factor 1.5: Network Segmentation**

| Level | Penalty |
|---|---|
| No segmentation (flat network) | +15 |
| DMZ only | +8 |
| DMZ + limited internal segments | +4 |
| Advanced segmentation (critical assets isolated) | 0 |

**Definition**: Network access controls separating systems by trust zone.

**Why it matters**: Limits lateral movement during breach; critical for containment.

---

### Controls Dimension Calculation

```
Max_Penalty = 25 + 20 + 20 + 15 + 15 = 95
Total_Penalty = MFA + EDR + Backup + IRP + Segmentation
Controls_Risk_Score = MIN(Total_Penalty / 95 * 100, 100)
```

---

## 5. DIMENSION 2: CYBER INCIDENTS (25% Weight)

### Purpose
Evaluate risk exposure based on historical security incidents. Organizations with recent incidents are at higher risk of repeat compromise.

### Scoring Approach

Count specific incident types and adjust for frequency trend.

```
Incidents_Risk_Score = MIN(SUM(Incident_Penalties) / Max_Possible_Penalty * 100, 100)
Max_Possible_Penalty = 95
```

### Incident Factors (3 factors)

#### **Factor 2.1: Ransomware Incidents (Last 3 Years)**

| Count | Penalty |
|---|---|
| 0 incidents | 0 |
| 1 incident | +20 |
| 2 incidents | +35 |
| 3+ incidents | +50 |

**Definition**: Confirmed ransomware attacks (encryption or extortion) in past 36 months.

**Why it matters**: Ransomware is the dominant cyber threat; repeat victims indicate systemic issues.

---

#### **Factor 2.2: Data Breach Incidents (Last 3 Years)**

| Count | Penalty |
|---|---|
| 0 incidents | 0 |
| 1 incident | +15 |
| 2+ incidents | +30 |

**Definition**: Confirmed unauthorized access/exfiltration of sensitive data (excludes ransomware).

**Why it matters**: Breaches drive regulatory fines and customer trust damage.

---

#### **Factor 2.3: Incident Frequency Trend**

| Direction (last 12 months vs. prior 12 months) | Adjustment |
|---|---|
| Increasing | +15 |
| Stable | 0 |
| Decreasing | 0 |

**Definition**: Are incidents becoming more common (increasing), staying same (stable), or fewer (decreasing)?

**Why it matters**: Trend indicates whether organization is improving controls or deteriorating. No credit for improvements; risk is baseline.

---

### Incidents Dimension Calculation

```
Max_Penalty = 50 + 30 + 15 = 95
Total_Penalty = Ransomware + DataBreach + Trend
Incidents_Risk_Score = MIN(Total_Penalty / 95 * 100, 100)
```

---

## 6. DIMENSION 3: VULNERABILITIES (15% Weight)

### Purpose
Evaluate technical exposure based on known unpatched vulnerabilities and patch management speed.

### Scoring Approach

Assess current vulnerability inventory and patch responsiveness.

```
Vulnerabilities_Risk_Score = MIN(SUM(Vuln_Penalties) / Max_Possible_Penalty * 100, 100)
Max_Possible_Penalty = 70
```

### Vulnerability Factors (3 factors)

#### **Factor 3.1: Unpatched Critical Vulnerabilities (Current)**

| Count | Penalty |
|---|---|
| 0 | 0 |
| 1–3 | +15 |
| 4+ | +30 |

**Definition**: CVSS 9.0+ or known Remote Code Execution vulnerability with no patch deployed.

**Why it matters**: Each critical vuln is an active compromise vector; actively exploited in the wild.

---

#### **Factor 3.2: Unpatched High-Severity Vulnerabilities (Current)**

| Count | Penalty |
|---|---|
| 0–5 | 0 |
| 6–15 | +10 |
| 16+ | +20 |

**Definition**: CVSS 7.0–8.9; unpatched in production.

**Why it matters**: High vulns are exploitable; scale indicates poor patch discipline.

---

#### **Factor 3.3: Patch Management Cadence**

| Average Time to Patch Critical Vulns | Penalty |
|---|---|
| Unknown / no tracking | +20 |
| >90 days | +15 |
| 60–90 days | +10 |
| <60 days | 0 |

**Definition**: Average time from vulnerability disclosure to patch deployment (last 12 months).

**Why it matters**: Fast patching reduces exposure window; slow patching increases risk of exploitation.

---

### Vulnerabilities Dimension Calculation

```
Max_Penalty = 30 + 20 + 20 = 70
Total_Penalty = CriticalVulns + HighVulns + PatchCadence
Vulnerabilities_Risk_Score = MIN(Total_Penalty / 70 * 100, 100)
```

---

## 7. DIMENSION 4: SUPPLY CHAIN (12% Weight)

### Purpose
Evaluate third-party risk. Vendors with poor security or critical functions are potential compromise vectors.

### Scoring Approach

Count critical vendors and assess their security posture.

```
SupplyChain_Risk_Score = MIN(SUM(Vendor_Penalties) / Max_Possible_Penalty * 100, 100)
Max_Possible_Penalty = 60
```

### Supply Chain Factors (2 factors)

#### **Factor 4.1: Critical Vendor Count**

| Count | Penalty |
|---|---|
| 0–1 | 0 |
| 2–3 | +10 |
| 4–5 | +20 |
| 6+ | +35 |

**Definition**: Critical vendor = provides services/products where compromise or outage would severely impact business (e.g., cloud provider, payment processor, identity system, core SaaS).

**Why it matters**: Each critical vendor expands attack surface; multiple vendors increase supply-chain risk.

---

#### **Factor 4.2: Vendor Security Assessment**

| Status | Penalty |
|---|---|
| No assessment or unknown | +25 |
| Low security rating (0–40/100) | +20 |
| Moderate (41–70/100) | +10 |
| Good (71–85/100) | +5 |
| Excellent (86–100/100) | 0 |

**Definition**: Based on vendor attestations (SOC 2 Type II, ISO 27001), security questionnaire scores, or third-party ratings.

**Why it matters**: Vendor security posture directly affects customer exposure through supply-chain attacks.

---

### Supply Chain Dimension Calculation

```
Max_Penalty = 35 + 25 = 60
Total_Penalty = VendorCount + VendorSecurityRating
SupplyChain_Risk_Score = MIN(Total_Penalty / 60 * 100, 100)
```

---

## 8. DIMENSION 5: REGULATORY (8% Weight)

### Purpose
Evaluate compliance risk. Organizations subject to strict regulations or with compliance gaps face higher regulatory and reputational risk.

### Scoring Approach

For capstone simplicity, use the **highest regulation penalty** plus **compliance gaps**.

```
Regulatory_Risk_Score = MIN(Regulatory_Penalty / Max_Possible_Penalty * 100, 100)
Max_Possible_Penalty = 30
```

### Regulatory Factors (2 factors)

#### **Factor 5.1: Applicable Regulations & Compliance Status**

For each regulation that applies, score its compliance. The **highest penalty** among applicable regulations is used (not summed).

| Regulation | Compliant | Partially Compliant | Non-Compliant |
|---|---|---|---|
| GDPR | 0 | +8 | +15 |
| HIPAA | 0 | +10 | +20 |
| PCI-DSS | 0 | +8 | +15 |
| CCPA | 0 | +6 | +12 |
| State Data Privacy Laws | 0 | +5 | +10 |

**Definition**:
- **Compliant**: Organization meets all material requirements; documented controls
- **Partially Compliant**: Organization meets some requirements; known gaps being remediated  
- **Non-Compliant**: Organization fails material requirements; no active remediation

**Why it matters**: Regulatory violations result in fines, reputational damage, and customer trust loss.

**Capstone Note**: This simplified methodology (highest regulation + gaps) is appropriate for a prototype underwriting model. Production systems may require per-regulation tracking and more sophisticated compliance assessment.

---

#### **Factor 5.2: Compliance Gaps Summary**

| Situation | Penalty |
|---|---|
| 0 gaps | 0 |
| 1–2 gaps | +5 |
| 3+ gaps | +10 |

**Definition**: Material requirements of applicable regulations not currently met.

**Why it matters**: More gaps = higher compliance risk; indicates incomplete security program.

---

### Regulatory Dimension Calculation

```
Highest_Regulation_Penalty = MAX(penalties for applicable regulations)
Gap_Penalty = compliance gap adjustment
Regulatory_Penalty = Highest_Regulation_Penalty + Gap_Penalty
Regulatory_Risk_Score = MIN(Regulatory_Penalty / 30 * 100, 100)

If no regulation applies: Regulatory_Penalty = 0
```

**Example**: Organization subject to HIPAA and State Privacy Laws

- HIPAA: Partially compliant → +10
- State Privacy Laws: Compliant → +0
- Highest regulation: +10
- Compliance gaps: 1 gap → +5
- Regulatory_Penalty = 10 + 5 = 15
- Regulatory_Risk_Score = 15 / 30 * 100 = 50.0

---

## 9. FINAL RISK SCORE CALCULATION

### Weighted Aggregation

Once all five dimension scores are calculated (each 0–100), combine using documented weights:

```
Final_Risk_Score = (Controls × 0.40) 
                 + (Incidents × 0.25) 
                 + (Vulnerabilities × 0.15) 
                 + (SupplyChain × 0.12) 
                 + (Regulatory × 0.08)
```

**Result**: Naturally bounded in range [0, 100].

### Risk Level Assignment

```
IF Final_Risk_Score < 25.0
  THEN Risk_Level = "LOW"
ELSE IF Final_Risk_Score < 50.0
  THEN Risk_Level = "MEDIUM"
ELSE IF Final_Risk_Score < 75.0
  THEN Risk_Level = "HIGH"
ELSE
  THEN Risk_Level = "CRITICAL"
```

---

## 10. IDENTIFYING TOP CONTRIBUTING FACTORS

For transparency, surface the 3–5 factors that most influenced the final score.

### Algorithm

For each factor, calculate its contribution to the final 0–100 risk score:

```
Factor_Contribution_to_Final_Score = 
  (Factor_Penalty / Dimension_Max_Penalty) 
  × Dimension_Weight 
  × 100
```

**Example**: 
- MFA penalty: 15
- Controls maximum penalty: 95
- Controls weight: 0.40

```
Contribution = (15 / 95) × 0.40 × 100 = 6.32 points
```

This means MFA directly contributed 6.32 of the 100 points to the final risk score.

**Algorithm**: Rank all 15 factors by contribution and present top 3–5 to underwriter.

---

## 11. HANDLING MISSING DATA

**Policy**: When input data is incomplete, **assume worst-case** for that factor (conservative approach).

### Missing Data Rules

| Missing Data | Assumption |
|---|---|
| MFA coverage unknown | Assume 0% (+25 penalty) |
| EDR status unknown | Assume 0% (+20 penalty) |
| Backup plan unknown | Assume no plan (+20 penalty) |
| IRP status unknown | Assume none (+15 penalty) |
| Segmentation unknown | Assume flat network (+15 penalty) |
| Ransomware history unknown | Assume 3+ incidents (+50 penalty) |
| Data breach history unknown | Assume 2+ incidents (+30 penalty) |
| Critical vuln count unknown | Assume 4+ (+30 penalty) |
| High vuln count unknown | Assume 16+ (+20 penalty) |
| Patch cadence unknown | Assume unknown (+20 penalty) |
| Vendor count unknown | Assume 6+ (+35 penalty) |
| Vendor security unknown | Assume not assessed (+25 penalty) |
| Regulation compliance unknown | Assume non-compliant (+worst-case regulation penalty) |
| Gaps unknown | Assume 3+ (+10 penalty) |

### Missing Data Flag

When significant data is missing:
1. **Calculate score using worst-case assumptions**
2. **Flag assessment as "PRELIMINARY"** with list of missing items
3. **Recommend underwriter follow-up** to gather data
4. **Allow re-running assessment** once data collected

**Example Flag**:
```json
{
  "assessment_status": "PRELIMINARY",
  "missing_data": [
    "MFA coverage percentage",
    "Ransomware incident history",
    "Patch management process"
  ],
  "note": "Schedule follow-up call to complete assessment."
}
```

---

## 12. WORKED EXAMPLES

### Example 1: LOW-RISK ORGANIZATION

**Organization**: TechCorp Inc. — 200 employees, healthcare IT vendor

#### Data Inputs

| Dimension | Factor | Value |
|---|---|---|
| **Controls** | MFA | 90% → +0 |
| | EDR | 85% → +0 |
| | Backup | Monthly tested + air-gapped → +0 |
| | IRP | Tested 4 months ago → +0 |
| | Segmentation | Advanced → +0 |
| **Incidents** | Ransomware (3y) | 0 → +0 |
| | Data Breach (3y) | 0 → +0 |
| | Trend | Stable → 0 |
| **Vulnerabilities** | Critical | 0 → +0 |
| | High | 2 → +0 |
| | Patch Cadence | 20-day avg → +0 |
| **Supply Chain** | Critical Vendors | 1 (cloud provider) → +0 |
| | Vendor Security | Excellent (92/100) → +0 |
| **Regulatory** | HIPAA | Compliant → +0 |
| | Compliance Gaps | 0 → +0 |

#### Dimension Calculations

**Controls**: (0+0+0+0+0) / 95 × 100 = **0.0**

**Incidents**: (0+0+0) / 95 × 100 = **0.0**

**Vulnerabilities**: (0+0+0) / 70 × 100 = **0.0**

**Supply Chain**: (0+0) / 60 × 100 = **0.0**

**Regulatory**: Highest regulation: 0, Gaps: 0 → (0+0) / 30 × 100 = **0.0**

#### Final Score

```
Final = (0.0 × 0.40) + (0.0 × 0.25) + (0.0 × 0.15) + (0.0 × 0.12) + (0.0 × 0.08)
      = 0.0
```

**Risk Level**: **LOW** (0.0)

**Top Contributing Factors**: No significant risk drivers; excellent across all dimensions.

**Underwriter Recommendation**: **Recommended Action: ACCEPT.** Excellent cybersecurity organization with strong controls, no incident history, and full regulatory compliance. Standard terms approved; monitor annually.

---

### Example 2: MEDIUM-RISK ORGANIZATION

**Organization**: RetailMax Ltd. — 500 employees, retail chain

#### Data Inputs

| Dimension | Factor | Value |
|---|---|---|
| **Controls** | MFA | 55% → +15 |
| | EDR | 45% → +12 |
| | Backup | Quarterly test → +6 |
| | IRP | Tested 14 months ago → +8 |
| | Segmentation | DMZ + 2 segments → +4 |
| **Incidents** | Ransomware (3y) | 1 → +20 |
| | Data Breach (3y) | 0 → +0 |
| | Trend | Stable → 0 |
| **Vulnerabilities** | Critical | 1 → +15 |
| | High | 8 → +10 |
| | Patch Cadence | 75 days → +10 |
| **Supply Chain** | Critical Vendors | 3 → +10 |
| | Vendor Security | Moderate (55/100) → +10 |
| **Regulatory** | PCI-DSS | Partially compliant → +8 |
| | Compliance Gaps | 1 gap → +5 |

#### Dimension Calculations

**Controls**: (15+12+6+8+4) / 95 × 100 = 45 / 95 × 100 = **47.4**

**Incidents**: (20+0+0) / 95 × 100 = 20 / 95 × 100 = **21.1**

**Vulnerabilities**: (15+10+10) / 70 × 100 = 35 / 70 × 100 = **50.0**

**Supply Chain**: (10+10) / 60 × 100 = 20 / 60 × 100 = **33.3**

**Regulatory**: Highest regulation: 8 (PCI-DSS partial), Gaps: 5 → (8+5) / 30 × 100 = 13 / 30 × 100 = **43.3**

#### Final Score

```
Final = (47.4 × 0.40) + (21.1 × 0.25) + (50.0 × 0.15) + (33.3 × 0.12) + (43.3 × 0.08)
      = 18.96 + 5.28 + 7.50 + 4.00 + 3.46
      = 39.2
```

**Risk Level**: **MEDIUM** (39.2)

#### Top Contributing Factors

Using the contribution formula: `(Penalty / Max) × Weight × 100`

1. **Vulnerabilities Dimension (50.0 score × 0.15 weight)**: 7.50 points direct contribution
   - High vulns (8 count): (10/70) × 0.15 × 100 = 2.14 points
   - Critical vulns (1 count): (15/70) × 0.15 × 100 = 3.21 points
   - Patch cadence (75 days): (10/70) × 0.15 × 100 = 2.14 points

2. **MFA Coverage (55%, penalty +15)**: (15/95) × 0.40 × 100 = **6.32 points**
   - Recommendation: Expand to 90%+ of systems

3. **One Past Ransomware Incident (penalty +20)**: (20/95) × 0.25 × 100 = **5.26 points**
   - Note: Good recovery; focus on prevention improvements

4. **EDR Coverage (45%, penalty +12)**: (12/95) × 0.40 × 100 = **5.05 points**
   - Recommendation: Deploy to additional endpoints

**Underwriter Recommendation**: **Recommended Action: REFER for review.** Reasonable cybersecurity posture with clear remediation path. Primary concerns: (1) patch management cycle slower than industry best practice, (2) EDR coverage incomplete, (3) one past ransomware event, (4) partial PCI-DSS compliance. 

Coverage conditional on: commitment to MFA expansion to 80%+ within 60 days, patch cycle reduction to <60 days within 90 days, vendor security assessment completion within 60 days. Reassess in 6 months with evidence of improvements.

---

### Example 3: HIGH-RISK ORGANIZATION

**Organization**: LegacyBank Corp. — 1,000 employees, regional bank

#### Data Inputs

| Dimension | Factor | Value |
|---|---|---|
| **Controls** | MFA | 30% → +15 |
| | EDR | 25% → +12 |
| | Backup | Untested → +12 |
| | IRP | Outdated, not tested → +8 |
| | Segmentation | DMZ only → +8 |
| **Incidents** | Ransomware (3y) | 2 → +35 |
| | Data Breach (3y) | 1 → +15 |
| | Trend | Increasing → +15 |
| **Vulnerabilities** | Critical | 5 → +30 |
| | High | 22 → +20 |
| | Patch Cadence | >90 days → +15 |
| **Supply Chain** | Critical Vendors | 5 → +20 |
| | Vendor Security | Moderate (48/100) → +10 |
| **Regulatory** | HIPAA | Non-compliant → +20 |
| | Compliance Gaps | 4 gaps → +10 |

#### Dimension Calculations

**Controls**: (15+12+12+8+8) / 95 × 100 = 55 / 95 × 100 = **57.9**

**Incidents**: (35+15+15) / 95 × 100 = 65 / 95 × 100 = **68.4**

**Vulnerabilities**: (30+20+15) / 70 × 100 = 65 / 70 × 100 = **92.9**

**Supply Chain**: (20+10) / 60 × 100 = 30 / 60 × 100 = **50.0**

**Regulatory**: Highest regulation: 20 (HIPAA non-compliant), Gaps: 10 → (20+10) / 30 × 100 = 30 / 30 × 100 = **100.0** (capped)

#### Final Score

```
Final = (57.9 × 0.40) + (68.4 × 0.25) + (92.9 × 0.15) + (50.0 × 0.12) + (100.0 × 0.08)
      = 23.16 + 17.10 + 13.94 + 6.00 + 8.00
      = 68.2
```

**Risk Level**: **HIGH** (68.2)

#### Top Contributing Factors

1. **Vulnerabilities Dimension (92.9 score × 0.15 weight)**: 13.94 points
   - Massive unpatched critical/high vulnerability inventory with poor patch discipline

2. **Incidents Dimension (68.4 score × 0.25 weight)**: 17.10 points
   - Two ransomware, one breach, increasing frequency trend in past 12 months

3. **Controls Dimension (57.9 score × 0.40 weight)**: 23.16 points
   - Weak MFA/EDR coverage, untested backups, outdated incident response plan

4. **Regulatory Non-Compliance (HIPAA, 4 gaps)**: 8.00 points
   - (30/30) × 0.08 × 100 = 8.00

**Underwriter Recommendation**: **Recommended Action: REFER for senior underwriter review, likely DECLINE.**

Pattern of incidents escalating (2 ransomware, 1 breach in 3 years with increasing trend); legacy infrastructure with poor preventive controls (MFA 30%, EDR 25%, untested backups); massive unpatched vulnerability exposure (5 critical, 22 high); non-compliance with HIPAA on 4 material requirements.

**If coverage is to be considered**: Organization must demonstrate (within 90 days) commitment and progress on: (1) external security audit, (2) MFA/EDR deployment roadmap, (3) backup recovery testing, (4) incident response plan update and tabletop exercise, (5) HIPAA compliance remediation plan, (6) vendor security assessment completion. Reassess in 6 months with evidence of measurable control improvements and no new incidents. Current risk profile unacceptable for standard terms.

---

### Example 4: CRITICAL-RISK ORGANIZATION

**Organization**: OldSchool Manufacturing — 200 employees, industrial control systems

#### Data Inputs

| Dimension | Factor | Value |
|---|---|---|
| **Controls** | MFA | 0% → +25 |
| | EDR | 0% → +20 |
| | Backup | No plan → +20 |
| | IRP | None → +15 |
| | Segmentation | Flat network → +15 |
| **Incidents** | Ransomware (3y) | 3 → +50 |
| | Data Breach (3y) | 1 → +15 |
| | Trend | Increasing → +15 |
| **Vulnerabilities** | Critical | 8 → +30 |
| | High | 40 → +20 |
| | Patch Cadence | Unknown → +20 |
| **Supply Chain** | Critical Vendors | 6 → +35 |
| | Vendor Security | Unknown → +25 |
| **Regulatory** | PCI-DSS | Non-compliant → +15 |
| | Compliance Gaps | 3+ gaps (unknown) → +10 |

#### Dimension Calculations

**Controls**: (25+20+20+15+15) / 95 × 100 = 95 / 95 × 100 = **100.0**

**Incidents**: (50+15+15) / 95 × 100 = 80 / 95 × 100 = **84.2**

**Vulnerabilities**: (30+20+20) / 70 × 100 = 70 / 70 × 100 = **100.0**

**Supply Chain**: (35+25) / 60 × 100 = 60 / 60 × 100 = **100.0**

**Regulatory**: Highest regulation: 15 (PCI-DSS non-compliant), Gaps: 10 → (15+10) / 30 × 100 = 25 / 30 × 100 = **83.3**

#### Final Score

```
Final = (100.0 × 0.40) + (84.2 × 0.25) + (100.0 × 0.15) + (100.0 × 0.12) + (83.3 × 0.08)
      = 40.00 + 21.05 + 15.00 + 12.00 + 6.66
      = 94.71
```

**Risk Level**: **CRITICAL** (94.71)

#### Top Contributing Factors

1. **Controls Dimension (100.0 score × 0.40 weight)**: 40.00 points
   - No MFA, no EDR, no backups, no incident response plan, flat network

2. **Incidents Dimension (84.2 score × 0.25 weight)**: 21.05 points
   - Three ransomware attacks in three years, one data breach, increasing incident frequency

3. **Vulnerabilities Dimension (100.0 score × 0.15 weight)**: 15.00 points
   - Eight critical and 40 high-severity unpatched vulnerabilities; no patch process

4. **Supply Chain Dimension (100.0 score × 0.12 weight)**: 12.00 points
   - Six critical vendors with no security assessment; unmanaged third-party risk

**Underwriter Recommendation**: **Recommended Action: DECLINE.**

Organization lacks foundational cybersecurity controls (0% MFA, 0% EDR, no backup/recovery plan, no incident response capability); has suffered three ransomware attacks in three years with worsening frequency; operates a massive unpatched vulnerability inventory (8 critical, 40 high) with no documented patch process; relies on six unassessed critical vendors; is non-compliant with PCI-DSS on multiple material requirements.

Risk is unacceptable for underwriting at this time. Organization must complete comprehensive remediation including:
1. MFA and EDR deployment (minimum 90% coverage)
2. Backup/recovery plan with documented testing
3. Incident response plan with tabletop exercise
4. Vulnerability management program with <60 day patch SLA
5. Critical vendor security assessment completion
6. PCI-DSS compliance audit and remediation

Reapply in 12 months with independent security audit and evidence of sustained control improvements.

---

## 13. BOUNDARY CONDITION EXAMPLES

### Boundary: LOW → MEDIUM (Score = 25.0)

All dimensions scoring 25.0:

```
Final = (25 × 0.40) + (25 × 0.25) + (25 × 0.15) + (25 × 0.12) + (25 × 0.08)
      = 25.0
```

**Risk Level**: **MEDIUM** (25.0 is the start of MEDIUM range)

---

### Boundary: MEDIUM → HIGH (Score = 50.0)

All dimensions scoring 50.0:

```
Final = 50.0
```

**Risk Level**: **HIGH** (50.0 is the start of HIGH range)

---

### Boundary: HIGH → CRITICAL (Score = 75.0)

All dimensions scoring 75.0:

```
Final = 75.0
```

**Risk Level**: **CRITICAL** (75.0 is the start of CRITICAL range)

---

### Boundary: Single Dimension Dominates

Perfect controls but catastrophic incidents (100 score):

```
Final = (0 × 0.40) + (100 × 0.25) + (0 × 0.15) + (0 × 0.12) + (0 × 0.08)
      = 25.0 = MEDIUM
```

**Interpretation**: Severe incident history alone elevates an otherwise excellent organization to MEDIUM risk.

---

## 14. TEST PLAN

### Category 1: Factor Scoring

- [ ] TC1.1: MFA 81% coverage → 0 penalty
- [ ] TC1.2: MFA 0% coverage → 25 penalty
- [ ] TC1.3: EDR 60% coverage → 6 penalty
- [ ] TC1.4: Backup quarterly tested → 6 penalty
- [ ] TC1.5: IRP tested 5 months ago → 0 penalty
- [ ] TC1.6: Segmentation advanced → 0 penalty

### Category 2: Dimension Score Calculation

- [ ] TC2.1: All controls perfect → 0.0
- [ ] TC2.2: All controls worst → 100.0 (capped)
- [ ] TC2.3: Controls mid-range 45/95 → 47.4
- [ ] TC2.4: Incidents no history → 0.0
- [ ] TC2.5: Incidents 2 ransomware + breach → 68.4
- [ ] TC2.6: Vulnerabilities 35/70 → 50.0
- [ ] TC2.7: SupplyChain 20/60 → 33.3
- [ ] TC2.8: Regulatory compliant, 0 gaps → 0.0
- [ ] TC2.9: Regulatory HIPAA non-compliant + 4 gaps → 100.0 (capped)

### Category 3: Final Score Weighted Calculation

- [ ] TC3.1: All dimensions 0 → 0.0
- [ ] TC3.2: All dimensions 50 → 50.0
- [ ] TC3.3: All dimensions 100 → 100.0
- [ ] TC3.4: Controls 100, others 0 → 40.0
- [ ] TC3.5: Incidents 100, others 0 → 25.0
- [ ] TC3.6: Vulnerabilities 100, others 0 → 15.0
- [ ] TC3.7: Mixed (40,30,50,35,25) → 38.9

### Category 4: Risk Level Assignment

- [ ] TC4.1: Score 0.0 → LOW
- [ ] TC4.2: Score 24.9 → LOW
- [ ] TC4.3: Score 25.0 → MEDIUM
- [ ] TC4.4: Score 49.9 → MEDIUM
- [ ] TC4.5: Score 50.0 → HIGH
- [ ] TC4.6: Score 74.9 → HIGH
- [ ] TC4.7: Score 75.0 → CRITICAL
- [ ] TC4.8: Score 100.0 → CRITICAL

### Category 5: Missing Data Handling

- [ ] TC5.1: MFA unknown → assume 0% (+25), flagged PRELIMINARY
- [ ] TC5.2: Ransomware unknown → assume 3+ (+50), flagged PRELIMINARY
- [ ] TC5.3: Multiple missing → all worst-case penalties applied, flagged PRELIMINARY

### Category 6: Incident Trend (No Negative Scores)

- [ ] TC6.1: Decreasing trend → 0 adjustment (no penalty reduction)
- [ ] TC6.2: Stable trend → 0 adjustment
- [ ] TC6.3: Increasing trend → +15 adjustment
- [ ] TC6.4: Perfect controls with decreasing incidents → score ≥ 0 (never negative)

### Category 7: Contributing Factors Calculation

- [ ] TC7.1: MFA (15 penalty, 95 max, 40% weight) → (15/95) × 0.40 × 100 = 6.32 points
- [ ] TC7.2: Ransomware (20 penalty, 95 max, 25% weight) → (20/95) × 0.25 × 100 = 5.26 points
- [ ] TC7.3: High vulns (10 penalty, 70 max, 15% weight) → (10/70) × 0.15 × 100 = 2.14 points
- [ ] TC7.4: Top 3 factors ranked by contribution, descending

### Category 8: Regulatory Simplified Scoring

- [ ] TC8.1: One regulation compliant, no gaps → 0.0
- [ ] TC8.2: Two regulations; HIPAA partial (10) + GDPR compliant (0) → highest 10
- [ ] TC8.3: HIPAA non-compliant (20) + 3 gaps (10) → 30/30 × 100 = 100.0
- [ ] TC8.4: No applicable regulations → regulatory penalty 0.0

### Category 9: Determinism

- [ ] TC9.1: Same input → same output, identical to machine precision
- [ ] TC9.2: Run 1 score matches Run 2 score on identical data

### Category 10: Worked Examples Consistency

- [ ] TC10.1: Example 1 (LOW) final score 0.0 matches calculation
- [ ] TC10.2: Example 2 (MEDIUM) final score 39.2 matches calculation
- [ ] TC10.3: Example 3 (HIGH) final score 68.2 matches calculation
- [ ] TC10.4: Example 4 (CRITICAL) final score 94.71 matches calculation

---

## 15. SUMMARY TABLE: MODEL CONSTANTS

| Component | Value | Notes |
|---|---|---|
| **Score Range** | 0.0–100.0 | Inclusive; real-valued |
| **Risk Level: LOW** | 0.0–24.9 | Excellent posture |
| **Risk Level: MEDIUM** | 25.0–49.9 | Acceptable with gaps |
| **Risk Level: HIGH** | 50.0–74.9 | Elevated risk |
| **Risk Level: CRITICAL** | 75.0–100.0 | Unacceptable risk |
| **Total Scoring Factors** | 15 | Across 5 dimensions |
| **Dimension: Controls** | 40% weight | 5 factors; max penalty 95 |
| **Dimension: Incidents** | 25% weight | 3 factors; max penalty 95 |
| **Dimension: Vulnerabilities** | 15% weight | 3 factors; max penalty 70 |
| **Dimension: Supply Chain** | 12% weight | 2 factors; max penalty 60 |
| **Dimension: Regulatory** | 8% weight | 2 factors; max penalty 30 |
| **Weight Sum** | 100% | 0.40 + 0.25 + 0.15 + 0.12 + 0.08 |
| **Missing Data Policy** | Worst-case | Conservative for underwriting |
| **Incident Trend: Decreasing** | 0 adjustment | No credit for improvements |
| **Regulatory Scoring** | Highest + Gaps | Simplified for capstone; not summed |

---

## 16. IMPLEMENTATION NOTES

### Capstone Prototype — Not Production Insurance

This risk model is a **capstone demonstration** of underwriting logic, not a production insurance system. It is designed to:

- Demonstrate deterministic risk scoring
- Show meaningful business logic
- Support human underwriter decision-making
- Provide audit trails and explainability
- Work seamlessly with AI-assisted explanations (future)

### What This Model Does NOT Include

- Machine learning or statistical models
- LLM-based scoring (AI used only for explanation later, not calculation)
- Real actuarial formulas or pricing
- Autonomous insurance decisions
- Real-time threat intelligence feeds
- Microservices or Kubernetes
- Enterprise IAM or SSO
- Complex external integrations

### Simplicity

This model is intentionally simple:
- **15 scoring factors** (not dozens)
- **Simplified regulatory scoring** (highest + gaps, not per-regulation)
- **Pure arithmetic** (no ML, statistics, or complex algorithms)
- **Transparent calculation** (every step auditable and explainable)
- **Implementable in 1–2 days** as Python backend service
- **Testable in 1 day** with 25–30 focused unit tests
- **Reviewable in 30 minutes** for capstone demonstration

### Out of Scope (Future Enhancement)

- Industry-specific scoring variations
- Threat intelligence integration
- Real-time vulnerability data feeds
- Behavioral/dynamic risk factors
- Automated policy issuance
- Claims management
- Payment processing
- Production actuarial pricing

---

## 17. APPROVAL

| Role | Approval | Date |
|---|---|---|
| Architecture Review | ☐ Approved | |
| Capstone Lead | ☐ Approved | |
| Implementation Ready | ☐ Ready | |

---

**Document Version**: 1.0  
**Status**: FINAL — READY FOR IMPLEMENTATION  
**Last Updated**: 2025-01-18