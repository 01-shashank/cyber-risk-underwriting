# Cyber Risk Underwriting Workbench

> GitHub Copilot Capstone Project — AI-assisted cyber insurance underwriting prototype

## Overview

Cyber insurance demand is increasing due to ransomware, data breaches, supply-chain attacks, and regulatory requirements.

The **Cyber Risk Underwriting Workbench** is a lightweight commercial P&C underwriting prototype that helps underwriters perform a faster, consistent, and explainable cyber risk review.

The application evaluates an organization's cyber posture across **15 deterministic risk factors**, calculates an overall risk score, identifies the strongest contributing risk factors, recommends an underwriting action, and generates an indicative premium.

The system is designed as decision support for human underwriters and does not replace professional underwriting judgment.

---

## Problem

Cyber underwriting requires assessment of:

- Security controls
- Historical cyber incidents
- Vulnerabilities and patching
- Supply-chain exposure
- Regulatory compliance

Manual assessment can result in:

- Longer underwriting turnaround times
- Inconsistent risk decisions
- Difficulty identifying key risk drivers
- Higher operational effort
- Limited underwriting capacity

---

## Solution

The workbench provides a single underwriting workflow:

```text
Organization Profile
        ↓
Cyber Risk Inputs
        ↓
15-Factor Deterministic Risk Engine
        ↓
Risk Score (0–100)
        ↓
Risk Classification
LOW / MEDIUM / HIGH / CRITICAL
        ↓
Underwriting Recommendation
ACCEPT / REFER / DECLINE
        ↓
Risk Driver Analysis
        ↓
Indicative Premium
```

---

## Key Features

### Deterministic Risk Assessment

The risk engine evaluates 15 factors across five dimensions:

| Dimension | Weight |
|---|---:|
| Controls | 40% |
| Incidents | 25% |
| Vulnerabilities | 15% |
| Supply Chain | 12% |
| Regulatory | 8% |

The risk score is calculated using deterministic arithmetic rather than an LLM or machine-learning model.

This provides:

- Repeatable results
- Transparent calculations
- Easy testing
- Easy auditing
- Predictable behavior

### Risk Classification

| Score | Risk Level |
|---:|---|
| 0–24.9 | LOW |
| 25–49.9 | MEDIUM |
| 50–74.9 | HIGH |
| 75–100 | CRITICAL |

Recommendations:

- ACCEPT
- REFER
- DECLINE

### Explainable Risk Drivers

The system identifies the strongest contributors to the overall risk score.

Each contributing factor includes its dimension, penalty, and contribution to the overall score.

### Dimension-Level Risk Profile

The dashboard visualizes:

- Controls
- Incidents
- Vulnerabilities
- Supply Chain
- Regulatory

### Indicative Pricing

The prototype calculates an indicative premium using:

- Base premium
- Revenue factor
- Risk multiplier
- Incident multiplier
- Coverage factor

> Pricing is illustrative prototype methodology and is not an actual insurance quote.

### Interactive Dashboard

The frontend provides:

- Organization profile inputs
- Security controls
- Incident information
- Vulnerability information
- Supply-chain information
- Regulatory information
- Demo data
- Risk visualization
- Risk drivers
- Underwriting recommendation
- Indicative premium

---

## Architecture

```text
┌─────────────────────────────────────────────┐
│       Cyber Risk Underwriting Workbench     │
│                                             │
│  ┌───────────────────────────────────────┐  │
│  │          Frontend Dashboard           │  │
│  │        HTML + CSS + JavaScript        │  │
│  └──────────────────┬────────────────────┘  │
│                     │                       │
│                     ▼                       │
│  ┌───────────────────────────────────────┐  │
│  │               FastAPI                 │  │
│  │                                       │  │
│  │ GET  /api/v1/health                   │  │
│  │ POST /api/v1/assessments              │  │
│  └──────────────────┬────────────────────┘  │
│                     │                       │
│            ┌────────┴────────┐              │
│            ▼                 ▼              │
│     ┌─────────────┐   ┌──────────────┐     │
│     │ Risk Engine │   │Pricing Engine │     │
│     │ 15 factors  │   │  Indicative  │     │
│     │ 5 dimensions│   │   premium     │     │
│     └─────────────┘   └──────────────┘     │
└─────────────────────────────────────────────┘
```

The frontend and backend are served from the same FastAPI application on a single port.

---

## Technology Stack

### Backend

- Python
- FastAPI
- Pydantic
- Uvicorn

### Frontend

- HTML
- CSS
- JavaScript

### Testing

- pytest

### Development

- GitHub
- GitHub Codespaces
- GitHub Copilot

---

## Project Structure

```text
cyber-risk-underwriting/
├── .github/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── engines/
│   │   │   ├── risk_engine.py
│   │   │   └── pricing_engine.py
│   │   └── main.py
│   └── tests/
│       └── unit/
├── docs/
│   └── risk-model.md
├── frontend/
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   └── README.md
├── README.md
├── requirements.txt
└── LICENSE
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Git

### Clone

```bash
git clone https://github.com/01-shashank/cyber-risk-underwriting.git
cd cyber-risk-underwriting
```

### Install dependencies

```bash
pip install -r requirements.txt
```

For a virtual environment:

```bash
python -m venv .venv
```

Linux / macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

Then:

```bash
pip install -r requirements.txt
```

---

## Running the Tests

Run:

```bash
pytest -q
```

Current test suite:

```text
46 passed
```

The tests validate:

- Individual risk factors
- Dimension calculations
- Final score calculation
- Risk-level boundaries
- Recommendation logic
- Missing-data behavior
- Contributing-factor calculations
- Pricing-related behavior

---

## Running the Application

Start the FastAPI application:

```bash
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

Open:

```text
http://localhost:8000
```

The underwriting dashboard is served directly by FastAPI.

### API Documentation

```text
http://localhost:8000/docs
```

---

## API

### Health Check

```http
GET /api/v1/health
```

Example:

```json
{
  "status": "ok",
  "service": "cyber-risk-underwriting-api"
}
```

### Create Assessment

```http
POST /api/v1/assessments
```

The response contains:

```text
Risk
├── Final score
├── Risk level
├── Recommended action
├── Assessment status
├── Dimension scores
├── Factor penalties
├── Contributing factors
└── Missing data

Pricing
├── Base premium
├── Revenue factor
├── Risk multiplier
├── Incident multiplier
├── Coverage factor
├── Indicative premium
└── Disclaimer
```

---

## Risk Model

The authoritative scoring methodology is documented in:

```text
docs/risk-model.md
```

The model contains:

- 15 scoring factors
- 5 weighted dimensions
- Deterministic arithmetic
- Four risk levels
- Recommendation logic
- Missing-data handling
- Boundary conditions
- Contributing-factor calculations
- Worked examples
- Test cases

The actual numerical risk score is calculated by the deterministic risk engine, not by an LLM.

---

## Testing Strategy

The automated test suite validates:

### Factor-level behavior

Individual risk factors are tested against their documented penalty rules.

### Dimension-level behavior

The weighted dimensions are tested independently.

### Final score

The complete deterministic calculation is tested against expected values.

### Boundary conditions

The risk-level thresholds are explicitly tested around:

```text
25
50
75
```

### Missing data

The documented missing-data policy is validated through automated tests.

### Explainability

Contributing-factor calculations are validated against the underlying scoring formula.

---

## GitHub Copilot Usage

GitHub Copilot was used as an AI development assistant throughout the project.

Copilot assisted with:

- Project scaffolding
- Backend implementation
- Risk-engine implementation
- Unit-test development
- API implementation
- Frontend development
- Debugging
- Refactoring
- Documentation

Copilot-assisted code was reviewed and validated through automated testing and manual end-to-end testing.

The underlying risk calculation remains deterministic and explainable.

---

## Design Principles

### Explainability

Every risk result can be traced to documented factors and calculations.

### Determinism

Identical inputs produce identical risk results.

### Human-in-the-loop

The system provides decision support rather than replacing professional underwriting judgment.

### Separation of Concerns

```text
Risk Calculation
       ↓
Recommendation
       ↓
Indicative Pricing
       ↓
Presentation
```

### Scope Control

The project intentionally focuses on the core underwriting workflow rather than attempting to build a complete commercial insurance platform.

---

## Demonstration Flow

```text
1. Open the dashboard
2. Load demo assessment
3. Review organization inputs
4. Run assessment
5. Review risk score
6. Review risk classification
7. Review recommendation
8. Review dimension scores
9. Review contributing factors
10. Review indicative premium
```

Example:

```text
Risk Score: 37.31 / 100
Risk Level: MEDIUM
Recommended Action: REFER
```

---

## Limitations

This is a capstone prototype and does not implement:

- Production authentication
- Carrier-specific underwriting rules
- Live cyber-threat intelligence
- External vulnerability databases
- Production actuarial pricing
- Policy issuance
- Claims management
- Broker integrations
- Production database infrastructure

A production implementation would require additional security, actuarial, regulatory, and infrastructure controls.

---

## Future Enhancements

Potential extensions include:

1. External cyber-risk data integrations
2. Historical assessment and portfolio tracking
3. Underwriter authentication and roles
4. Carrier-specific scoring configurations
5. Historical claims data
6. Advanced actuarial pricing
7. AI-generated underwriting summaries
8. Portfolio-level analytics
9. Threat-intelligence integrations
10. Cloud deployment

---

## Prototype Disclaimer

This project is a capstone prototype for demonstration and educational purposes.

Risk scores, recommendations, and premium calculations are illustrative and should not be interpreted as actual insurance quotes, binding underwriting decisions, financial advice, or production actuarial pricing.

Real-world deployment would require validated data, carrier-specific underwriting rules, actuarial models, regulatory review, security controls, and human underwriting oversight.

---

## Capstone Outcome

The Cyber Risk Underwriting Workbench demonstrates an explainable digital workflow for cyber insurance underwriting by combining:

- A deterministic 15-factor cyber-risk model
- Five weighted risk dimensions
- Explainable risk drivers
- Underwriting recommendations
- Indicative pricing
- REST APIs
- Interactive web UI
- Automated testing
- AI-assisted development with GitHub Copilot

The prototype provides a focused foundation for faster and more consistent cyber underwriting review while maintaining transparency and human oversight.

---

## Repository

https://github.com/01-shashank/cyber-risk-underwriting
