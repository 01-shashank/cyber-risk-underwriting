const API_BASE = "";

function value(id) {
  const el = document.getElementById(id);
  if (!el) return null;
  if (el.type === "number") return el.value === "" ? null : Number(el.value);
  return el.value || null;
}

function buildPayload() {
  const regulations = {};
  document.querySelectorAll('input[name="reg"]:checked').forEach((el) => {
    regulations[el.value] = document.getElementById("regulation_status").value;
  });

  return {
    mfa_coverage: value("mfa_coverage"),
    edr_coverage: value("edr_coverage"),
    backup_status: value("backup_status"),
    irp_months_since_test: value("irp_months_since_test"),
    segmentation_level: value("segmentation_level"),
    ransomware_incidents: value("ransomware_incidents"),
    data_breach_incidents: value("data_breach_incidents"),
    incident_trend: value("incident_trend"),
    critical_vulns: value("critical_vulns"),
    high_vulns: value("high_vulns"),
    patch_days: value("patch_days"),
    critical_vendor_count: value("critical_vendor_count"),
    vendor_security_score: value("vendor_security_score"),
    regulations,
    compliance_gaps: value("compliance_gaps"),
    annual_revenue: value("annual_revenue"),
    coverage_limit: value("coverage_limit")
  };
}

function money(n) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 2
  }).format(n);
}

function renderDimensions(scores) {
  const labels = {
    controls: "Controls",
    incidents: "Incidents",
    vulnerabilities: "Vulnerabilities",
    supply_chain: "Supply chain",
    regulatory: "Regulatory"
  };

  document.getElementById("dimensions").innerHTML =
    Object.entries(scores).map(([key, score]) => `
      <div class="dimension">
        <span>${labels[key]}</span>
        <div class="dim-bar"><div style="width:${Math.min(score,100)}%"></div></div>
        <strong>${score.toFixed(1)}</strong>
      </div>
    `).join("");
}

function renderDrivers(drivers) {
  const el = document.getElementById("drivers");

  if (!drivers.length) {
    el.innerHTML = '<div class="empty">No material risk contributors.</div>';
    return;
  }

  el.innerHTML = drivers.slice(0, 5).map((d, i) => `
    <div class="driver">
      <div>
        <div class="driver-name">${i + 1}. ${d.factor}</div>
        <div class="driver-meta">${d.dimension.replace("_", " ")}</div>
      </div>
      <div class="driver-score">+${d.contribution_points.toFixed(2)} pts</div>
    </div>
  `).join("");
}

function renderPremium(p) {
  document.getElementById("premium").textContent = money(p.indicative_premium);

  document.getElementById("breakdown").innerHTML = `
    <div class="break-row"><span>Base premium</span><strong>${money(p.base_premium)}</strong></div>
    <div class="break-row"><span>Revenue factor</span><strong>${p.revenue_factor.toFixed(2)}×</strong></div>
    <div class="break-row"><span>Risk multiplier</span><strong>${p.risk_multiplier.toFixed(2)}×</strong></div>
    <div class="break-row"><span>Incident multiplier</span><strong>${p.incident_multiplier.toFixed(2)}×</strong></div>
    <div class="break-row"><span>Coverage factor</span><strong>${p.coverage_factor.toFixed(2)}×</strong></div>
  `;
}

function renderResult(body) {
  const r = body.risk;

  document.getElementById("score").textContent = r.final_score.toFixed(2);
  document.getElementById("risk-label").textContent = r.risk_level;
  document.getElementById("status-pill").textContent = r.assessment_status;
  document.getElementById("status-pill").className = "pill";
  document.getElementById("action").textContent = r.recommended_action;
  document.getElementById("score-meter").style.width = `${Math.min(r.final_score, 100)}%`;

  renderDimensions(r.dimension_scores);
  renderDrivers(r.contributing_factors);
  renderPremium(body.pricing);

  document.getElementById("ai-btn").disabled = false;
  document.getElementById("ai-output").classList.add("hidden");
  window.latestAssessment = body;
}

function demo() {
  document.getElementById("mfa_coverage").value = 55;
  document.getElementById("edr_coverage").value = 70;
  document.getElementById("backup_status").value = "backups_exist_no_recent_test";
  document.getElementById("irp_months_since_test").value = 12;
  document.getElementById("segmentation_level").value = "dmz_only";
  document.getElementById("ransomware_incidents").value = 1;
  document.getElementById("data_breach_incidents").value = 0;
  document.getElementById("incident_trend").value = "stable";
  document.getElementById("critical_vulns").value = 4;
  document.getElementById("high_vulns").value = 12;
  document.getElementById("patch_days").value = 75;
  document.getElementById("critical_vendor_count").value = 3;
  document.getElementById("vendor_security_score").value = 65;
  document.getElementById("compliance_gaps").value = 1;
  document.getElementById("annual_revenue").value = 20000000;
  document.getElementById("coverage_limit").value = 2000000;
}

document.getElementById("load-demo").addEventListener("click", demo);

document.getElementById("assessment-form").addEventListener("submit", async (event) => {
  event.preventDefault();

  document.getElementById("error").classList.add("hidden");
  document.getElementById("run-btn").disabled = true;
  document.getElementById("run-btn").querySelector("span").textContent = "Calculating…";

  try {
    const response = await fetch(`${API_BASE}/api/v1/assessments`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(buildPayload())
    });

    const body = await response.json();

    if (!response.ok) {
      throw new Error(body.detail || "Assessment failed.");
    }

    renderResult(body);
  } catch (err) {
    document.getElementById("error").textContent =
      `Unable to run assessment: ${err.message}.`;
    document.getElementById("error").classList.remove("hidden");
  } finally {
    document.getElementById("run-btn").disabled = false;
    document.getElementById("run-btn").querySelector("span").textContent =
      "Run risk assessment";
  }
});

document.getElementById("ai-btn").addEventListener("click", () => {
  const body = window.latestAssessment;
  if (!body) return;

  const r = body.risk;
  const top = r.contributing_factors
    .slice(0, 3)
    .map(x => x.factor)
    .join(", ");

  document.getElementById("ai-output").innerHTML = `
    <h4>Prototype underwriting analysis</h4>
    <p><strong>${r.risk_level} risk (${r.final_score.toFixed(2)}/100).</strong>
    The assessment identifies ${top || "no material drivers"} as the leading contributors.
    Recommended action is <strong>${r.recommended_action}</strong>.
    This deterministic summary is intended for human underwriter review.</p>
  `;

  document.getElementById("ai-output").classList.remove("hidden");
});

demo();
