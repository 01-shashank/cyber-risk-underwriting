# Cyber Risk Underwriting Workbench
## Product Requirements

## 1. Problem

Cyber insurance demand is increasing due to ransomware, data breaches, supply-chain attacks, and regulatory penalties.

Manual cyber underwriting is slow, resource-intensive, dependent on specialized expertise, and can result in inconsistent decisions.

The goal of this application is to provide an AI-assisted underwriting workbench that helps underwriters review cyber risk faster, make more consistent decisions, improve pricing transparency, and maintain better portfolio hygiene.

---

## 2. Primary User

Commercial cyber insurance underwriter.

---

## 3. MVP Goals

The MVP must allow an underwriter to:

1. Create and review a cyber insurance application.
2. Review the applicant's cyber-security posture.
3. Record historical cyber incidents.
4. Record vulnerabilities.
5. Assess supply-chain exposure.
6. Assess regulatory exposure.
7. Run a deterministic cyber risk assessment.
8. Generate an AI-assisted risk explanation.
9. Generate an indicative premium.
10. Review an underwriting recommendation.
11. Monitor portfolio-level risk.
12. Compare risk assessments over time.

---

## 4. Core Screens

### Dashboard

Show:

- Total applications
- Pending reviews
- High-risk applications
- Critical applications
- Average risk score
- Total indicative exposure
- Recent assessments
- Portfolio warnings

### Applications

Provide:

- Search
- Filtering
- Sorting
- Risk level
- Application status
- Organization
- Assessment date

### Application Detail

Show:

- Organization information
- Industry
- Revenue
- Employee count
- Coverage requested
- Security controls
- Incidents
- Vulnerabilities
- Supply-chain exposure
- Regulatory exposure
- Risk score
- Risk level
- AI analysis
- Underwriting recommendation
- Indicative premium
- Pricing breakdown
- Assessment history

### Risk Assessment

Allow the underwriter to:

- Validate application data
- Run risk assessment
- View deterministic score
- View AI analysis
- View recommendation
- View pricing

### Portfolio

Show:

- Risk distribution
- High-risk accounts
- Critical accounts
- Stale assessments
- Industry concentration
- Exposure concentration
- Unresolved findings
- Significant risk increases

---

## 5. Risk Levels

The initial prototype should use:

- LOW
- MEDIUM
- HIGH
- CRITICAL

The exact numeric thresholds must be documented in the risk model.

---

## 6. Underwriting Recommendations

The application supports:

- ACCEPT
- REFER
- DECLINE

Recommendations must be explainable.

Human underwriter approval is required.

---

## 7. AI Responsibilities

AI provides:

- Risk summary
- Key risk factors
- Weak controls
- Underwriter questions
- Explanation of the deterministic assessment
- Supporting recommendation

AI must not directly calculate:

- Risk score
- Premium

---

## 8. Pricing

Pricing is indicative only.

The pricing engine must provide a transparent breakdown showing:

- Base premium
- Industry adjustment
- Risk adjustment
- Incident adjustment
- Exposure adjustment
- Final indicative premium

---

## 9. Portfolio Hygiene

The application must identify:

- High-risk accounts
- Critical accounts
- Stale assessments
- Unresolved critical findings
- Industry concentration
- Exposure concentration
- Significant risk increases

---

## 10. Non-Goals

The MVP will not implement:

- Claims management
- Payment processing
- Policy issuance
- Real actuarial pricing
- Real-time threat intelligence
- Broker management
- Complex regulatory automation
- Microservice architecture
- Kubernetes
