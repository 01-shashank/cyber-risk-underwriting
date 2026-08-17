# Cyber Risk Underwriting Workbench

## 1. Project Overview

This project is a capstone application for AI-assisted cyber insurance underwriting.

The application should help insurance underwriters:

1. Review cyber insurance applications faster.
2. Evaluate cyber risk consistently.
3. Understand the reasons behind a risk assessment.
4. Generate transparent indicative pricing.
5. Identify portfolio-level risk and hygiene issues.

The application is a prototype for demonstration purposes and is not intended to provide real insurance advice, actuarial pricing, or regulatory advice.

---

## 2. Core User

The primary user is a commercial cyber insurance underwriter.

The user should be able to:

1. View submitted insurance applications.
2. Review an organization's cyber-security profile.
3. Review historical cyber incidents.
4. Review vulnerabilities and security controls.
5. Run a cyber risk assessment.
6. View a deterministic risk score.
7. View an AI-generated explanation of the assessment.
8. View an indicative premium and transparent pricing breakdown.
9. Accept, refer, or decline an application.
10. Monitor portfolio-level risk.
11. Compare the organization's current assessment with previous assessments.

---

## 3. Technology Stack

### Frontend

- React
- TypeScript
- Vite
- Tailwind CSS

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic

### Database

- PostgreSQL

### AI

Use a local/open-source LLM through Ollama where practical.

The AI layer must be replaceable so that the application is not tightly coupled to a single LLM provider.

### Testing

- pytest for backend
- Vitest for frontend

### Infrastructure

- Docker
- Docker Compose

### CI/CD

- GitHub Actions

---

## 4. Architecture Principles

Keep the architecture lightweight and appropriate for a capstone.

Use a modular monolith.

Do NOT introduce microservices unless there is a strong technical reason.

Keep these concerns separate:

- API layer
- Business logic
- Data access
- Risk engine
- Pricing engine
- AI service
- Validation
- Frontend presentation

Business logic must not be embedded directly inside API route handlers.

---

## 5. Risk Assessment Architecture

Risk assessment must contain two distinct components.

### Deterministic Risk Engine

The deterministic risk engine is responsible for calculating the numeric risk score.

The score must:

- Be deterministic.
- Be reproducible.
- Be explainable.
- Be bounded between 0 and 100.
- Have documented scoring rules.
- Be independently testable.

Potential risk factors include:

- MFA coverage
- Endpoint detection and response
- Backup strategy
- Incident response plan
- Previous ransomware incidents
- Previous data breaches
- Critical vulnerabilities
- Supply-chain exposure
- Regulatory exposure
- Security training
- Network segmentation

The exact scoring model must be documented before implementation.

### AI Analysis

The AI must NOT independently calculate the risk score.

The AI should use the structured assessment results to provide:

- Executive risk summary
- Key risk factors
- Weak or missing controls
- Underwriter questions
- Explanation of the deterministic score
- Supporting underwriting recommendation

The AI must not invent facts that are not present in the application data.

---

## 6. Pricing Architecture

Pricing must be deterministic and transparent.

The AI must NOT calculate the premium.

The pricing engine should use a documented prototype methodology involving factors such as:

- Base premium
- Industry factor
- Risk factor
- Incident factor
- Exposure factor

The system must display the pricing calculation and individual adjustments.

Clearly label the result as:

"Indicative premium — prototype methodology, not an actual insurance quote."

---

## 7. Underwriting Recommendation

The application should support three primary recommendation outcomes:

- ACCEPT
- REFER
- DECLINE

The recommendation must be explainable.

The system should show the major factors contributing to the recommendation.

Human underwriter review remains required.

The AI should be treated as an assistant, not an autonomous decision maker.

---

## 8. Portfolio Hygiene

The portfolio module should identify issues such as:

- High-risk accounts
- Critical-risk accounts
- Stale assessments
- Unresolved critical findings
- Industry concentration
- Exposure concentration
- Significant increases in risk score
- Significant changes in cyber-security posture

Portfolio warnings should include:

- Severity
- Affected applications
- Explanation
- Recommended action

---

## 9. Assessment Versioning

Risk assessments must be versioned.

When multiple assessments exist for an organization, the system should be able to compare:

- Previous risk score
- Current risk score
- Score change
- Changed security controls
- New incidents
- Changed vulnerabilities
- Changed risk findings

The system should explain why the risk changed.

---

## 10. Security Requirements

Follow secure development practices.

- Never hardcode secrets.
- Use environment variables.
- Validate API input.
- Use parameterized database access through SQLAlchemy.
- Do not log sensitive information.
- Validate AI responses.
- Protect AI endpoints against abuse.
- Consider prompt injection risks.
- Do not expose internal prompts unnecessarily.
- Implement appropriate authentication and authorization when authentication is introduced.
- Configure CORS securely.
- Do not commit `.env` files containing secrets.

---

## 11. Code Quality

Prefer:

- Readable code
- Small focused functions
- Strong typing
- Clear names
- Explicit error handling
- Reusable components
- Testable business logic
- Minimal abstraction

Avoid:

- Over-engineering
- Premature optimization
- Unnecessary design patterns
- Unnecessary dependencies
- Large functions
- Duplicated business logic
- Magic numbers
- Hardcoded secrets

---

## 12. API Design

Use RESTful APIs.

Use appropriate HTTP methods and status codes.

Validate request and response models using Pydantic.

API routes should remain thin.

Business logic belongs in service modules.

---

## 13. Frontend Principles

The UI should feel like a professional internal enterprise underwriting application.

Prioritize:

- Clear information hierarchy
- Readability
- Consistent components
- Responsive layout
- Loading states
- Empty states
- Error states
- Accessible controls

Avoid excessive animations and decorative elements.

Charts should only be used when they communicate a meaningful business insight.

---

## 14. Testing Principles

Prioritize tests for business-critical behavior.

Required testing areas include:

- Risk scoring
- Risk score boundaries
- Pricing calculations
- Invalid input
- Missing data
- Assessment version comparison
- Portfolio warning generation
- AI response validation
- Important API endpoints

Do not generate tests merely to increase coverage numbers.

---

## 15. Git and GitHub Workflow

Work should be organized around GitHub Issues.

For meaningful features:

1. Create an issue.
2. Create a feature branch.
3. Implement the issue.
4. Write/update tests.
5. Run validation.
6. Create a pull request.
7. Review the changes.
8. Address review findings.
9. Merge only after checks pass.

Commit messages should clearly describe the change.

---

## 16. Copilot Development Rules

When working on an issue:

1. Inspect existing code before making changes.
2. Understand existing architecture.
3. Do not rewrite unrelated code.
4. Do not introduce dependencies without justification.
5. Explain important architectural decisions.
6. Implement only the requested scope.
7. Add appropriate tests.
8. Review generated code critically.
9. Identify assumptions.
10. Never claim functionality that has not been implemented or tested.

Copilot should assist development, not replace engineering judgment.

---

## 17. Scope Control

The MVP should include:

- Dashboard
- Application management
- Organization profile
- Cyber-security profile
- Incident history
- Vulnerability information
- Deterministic risk assessment
- AI risk analysis
- Indicative pricing
- Underwriting recommendation
- Portfolio hygiene
- Assessment comparison

Do NOT add:

- Claims management
- Payments
- Policy administration
- Real actuarial pricing
- Real-time threat intelligence
- Complex broker management
- Kubernetes
- Microservices
- Unnecessary external integrations

unless explicitly required later.

---

## 18. Important Domain Consideration

The application should consistently reflect the original business problem:

Cyber insurance demand is increasing because of ransomware, data breaches, supply-chain attacks, and regulatory penalties.

The solution should therefore demonstrate:

- Faster risk review
- Better risk selection
- Better pricing transparency
- Improved portfolio hygiene
- Scalable underwriting capacity

Every major feature should support at least one of these outcomes.
