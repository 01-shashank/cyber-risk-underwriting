const API_BASE = "http://127.0.0.1:8000";

const $ = (id) => document.getElementById(id);

function value(id) {
  const el = $(id);
  if (!el) return null;
  if (el.type === "number") return el.value === "" ? null : Number(el.value);
  return el.value || null;
}

function buildPayload() {
  const regulations = {};
  document.querySelectorAll('input[name="reg"]:checked').forEach((el) => {
    regulations[el.value] = $("regulation_status").value;
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
  return new Intl.NumberFormat("en-US", {style:"currency", currency:"USD", maximumFractionDigits:2}).format(n);
}

function renderDimensions(scores) {
  const labels = {
    controls: "Controls",
    incidents: "Incidents",
    vulnerabilities: "Vulnerabilities",
    supply_chain: "Supply chain",
    regulatory: "Regulatory"
  };
  $("dimensions").innerHTML = Object.entries(scores).map(([key, score]) => `
    <div class="dimension">
      <span>${labels[key]}</span>
      <div class="dim-bar"><div style="width:${Math.min(score,100)}%"></div></div>
      <strong>${score.toFixed(1)}</strong>
    </div>`).join("");
}

function renderDrivers(drivers) {
  if (!drivers.length) {
    $("drivers").innerHTML = '<div class="empty">No material risk contributors.</div>';
    return;
  }
  $("drivers").innerHTML = drivers.slice(0, 5).map((d, i) => `
    <div class="driver">
      <div>
        <div class="driver-name">${i + 1}. ${d.factor}</div>
        <div class="driver-meta">${d.dimension.replace("_"," ")}</div>
      </div>
      <div class="driver-score">+${d.contribution_points.toFixed(2)} pts</div>
    </div>`).join("");
}

function renderPremium(p) {
  $("premium").textContent = money(p.indicative_premium);
  $("breakdown").innerHTML = `
    <div class="break-row"><span>Base premium</span><strong>${money(p.base_premium)}</strong></div>
    <div class="break-row"><span>Revenue factor</span><strong>${p.revenue_factor.toFixed(2)}×</strong></div>
    <div class="break-row"><span>Risk multiplier</span><strong>${p.risk_multiplier.toFixed(2)}×</strong></div>
    <div class="break-row"><span>Incident multiplier</span><strong>${p.incident_multiplier.toFixed(2)}×</strong></div>
    <div class="break-row"><span>Coverage factor</span><strong>${p.coverage_factor.toFixed(2)}×</strong></div>`;
}

function renderResult(body) {
  const r = body.risk;
  $("score").textContent = r.final_score.toFixed(2);
  $("risk-label").textContent = r.risk_level;
  $("status-pill").textContent = r.assessment_status;
  $("status-pill").className = "pill";
  $("action").textContent = r.recommended_action;
  $("score-meter").style.width = `${Math.min(r.final_score, 100)}%`;
  renderDimensions(r.dimension_scores);
  renderDrivers(r.contributing_factors);
  renderPremium(body.pricing);
  $("ai-btn").disabled = false;
  $("ai-output").classList.add("hidden");
  window.latestAssessment = body;
}

function demo() {
  $("mfa_coverage").value = 55;
  $("edr_coverage").value = 70;
  $("backup_status").value = "backups_exist_no_recent_test";
  $("irp_months_since_test").value = 12;
  $("segmentation_level").value = "dmz_only";
  $("ransomware_incidents").value = 1;
  $("data_breach_incidents").value = 0;
  $("incident_trend").value = "stable";
  $("critical_vulns").value = 4;
  $("high_vulns").value = 12;
  $("patch_days").value = 75;
  $("critical_vendor_count").value = 3;
  $("vendor_security_score").value = 65;
  $("compliance_gaps").value = 1;
  $("annual_revenue").value = 20_000_000;
  $("coverage_limit").value = 2_000_000;
}

$("load-demo").addEventListener("click", demo);

$("assessment-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  $("error").classList.add("hidden");
  $("run-btn").disabled = true;
  $("run-btn").querySelector("span").textContent = "Calculating…";

  try {
    const response = await fetch(`${API_BASE}/api/v1/assessments`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(buildPayload())
    });
    const body = await response.json();
    if (!response.ok) throw new Error(body.detail || "Assessment failed.");
    renderResult(body);
  } catch (err) {
    $("error").textContent = `Unable to run assessment: ${err.message}. Make sure the FastAPI server is running at ${API_BASE}.`;
    $("error").classList.remove("hidden");
  } finally {
    $("run-btn").disabled = false;
    $("run-btn").querySelector("span").textContent = "Run risk assessment";
  }
});

$("ai-btn").addEventListener("click", () => {
  const body = window.latestAssessment;
  if (!body) return;
  const r = body.risk;
  const top = r.contributing_factors.slice(0, 3).map(x => x.factor).join(", ");
  $("ai-output").innerHTML = `
    <h4>Prototype underwriting analysis</h4>
    <p><strong>${r.risk_level} risk (${r.final_score.toFixed(2)}/100).</strong>
    The assessment identifies ${top || "no material drivers"} as the leading contributors.
    Recommended action is <strong>${r.recommended_action}</strong>.
    This deterministic summary is intended for human underwriter review.</p>`;
  $("ai-output").classList.remove("hidden");
});

demo();
