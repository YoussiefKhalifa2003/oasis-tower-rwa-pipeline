// Oasis Tower RWA pipeline - landing page controller.

(function () {
  "use strict";

  var T = window.I18N;
  var lang = "en";
  var lastResult = null;

  var OASIS_BRIEF = {
    brief_id: "OASIS-RWA-2026",
    client_name: "Oasis Tower SPV (fictional)",
    project_title: "Oasis Tower Fractional Real Estate Tokenization Framework",
    industry: "Real Estate / RWA Tokenization",
    raw_request: "We want to tokenize a first tranche of economic interest in Oasis Tower, a commercial tower in Dubai Internet City, for professional investors. We need a compliance-aware architecture: KYC-gated onboarding, quarterly rental income distribution, transfer restrictions, escrow until minimum subscription, and an auditable link between offering memorandum clauses and on-chain dividend logic. Prefer ERC-3643 or ERC-1400 style permissioned tokens. All regulatory conclusions must be reviewed by counsel.",
    stated_constraints: [
      "Professional investors only in phase one",
      "KYC before wallet whitelisting",
      "Quarterly distributions with maintenance reserve",
      "Escrow until AED 45M minimum subscription",
      "12-month transfer restriction after issuance"
    ],
    known_systems: ["Custodial wallet", "KYC provider", "Escrow bank account"]
  };

  var $ = function (id) { return document.getElementById(id); };
  var chipRow = $("chipRow"), briefInput = $("briefInput"), clientName = $("clientName"),
    runBtn = $("runBtn"), stageOutput = $("stageOutput"), stageSteps = $("stageSteps"),
    demoFoot = $("demoFoot"), downloadBtn = $("downloadBtn"), demoMode = $("demoMode"),
    teleStatus = $("teleStatus"), teleStep = $("teleStep"), teleTokens = $("teleTokens"),
    teleCost = $("teleCost"), teleLatency = $("teleLatency");

  var STEP_ORDER = ["sovereign_guard", "jurisdiction_map", "protocol_outline", "gate", "governance_manifest"];
  var STEP_TITLES = {
    sovereign_guard: "SovereignGuard",
    jurisdiction_map: "JurisdictionMapper",
    protocol_outline: "ProtocolArchitect",
    governance_manifest: "GovernanceManifest"
  };
  var COST_PER_TOKEN = 0.6 / 1e6;
  var selectedBrief = "oasis";
  var running = false;

  function applyLang() {
    var dict = T[lang];
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === "ar" ? "rtl" : "ltr";
    document.body.dir = lang === "ar" ? "rtl" : "ltr";
    document.querySelectorAll("[data-i18n]").forEach(function (n) {
      var k = n.getAttribute("data-i18n");
      if (dict[k] != null) n.innerHTML = dict[k];
    });
    document.querySelectorAll("[data-i18n-ph]").forEach(function (n) {
      var k = n.getAttribute("data-i18n-ph");
      if (dict[k] != null) n.setAttribute("placeholder", dict[k]);
    });
    $("langToggle").textContent = lang === "en" ? "العربية" : "English";
    renderRisks();
    renderMatrix();
    showPresetText();
  }

  function renderRisks() {
    $("riskBody").innerHTML = T[lang].risks.map(function (r) {
      return "<tr><td>" + r[0] + "</td><td>" + r[1] + "</td></tr>";
    }).join("");
  }

  function renderMatrix() {
    var body = $("matrixBody");
    if (!body) return;
    body.innerHTML = T[lang].matrix.map(function (row) {
      return "<tr><td><b>" + row[0] + "</b></td><td>" + row[1] + "</td><td>" + row[2] + "</td><td>" + row[3] + "</td><td>" + row[4] + "</td><td>" + row[5] + "</td></tr>";
    }).join("");
  }

  function list(items) {
    return "<ul>" + items.map(function (i) {
      return typeof i === "string" ? "<li>" + i + "</li>" : "<li>" + JSON.stringify(i) + "</li>";
    }).join("") + "</ul>";
  }

  function setStepState(key, state) {
    var li = stageSteps.querySelector('li[data-key="' + key + '"]');
    if (!li) return;
    li.classList.remove("active", "done");
    if (state) li.classList.add(state);
  }

  function resetSteps() {
    STEP_ORDER.forEach(function (k) { setStepState(k, null); });
    stageOutput.innerHTML = "";
    demoFoot.hidden = true;
  }

  function wait(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }

  function getActiveBrief() {
    if (selectedBrief === "custom") {
      var text = (briefInput.value || "").trim();
      if (!text) return null;
      var name = (clientName.value || "").trim() || "Custom brief";
      return {
        client_name: name,
        project_title: name + " RWA Tokenization (custom brief)",
        industry: "RWA",
        raw_request: text,
        stated_constraints: [],
        known_systems: ["Custodial wallet", "KYC provider"]
      };
    }
    return OASIS_BRIEF;
  }

  function showPresetText() {
    if (selectedBrief === "custom") return;
    briefInput.value = OASIS_BRIEF.raw_request;
    clientName.value = OASIS_BRIEF.client_name;
  }

  function dict() { return T[lang]; }

  function renderSovereignGuard(d) {
    var L = dict();
    var h = '<div class="out-head"><h4>' + STEP_TITLES.sovereign_guard + '</h4><span class="tag">' + L.tag_local + '</span></div>';
    h += "<p><em>" + d.local_tier_note + "</em></p>";
    h += '<div class="kv">' + L.lbl_facts + "</div><ul>";
    (d.extracted_asset_facts || []).forEach(function (f) {
      h += "<li><b>" + f.fact + "</b> <code>" + f.source_chunk + "</code></li>";
    });
    h += "</ul>";
    h += '<div class="kv">' + L.lbl_distribution + "</div><ul>";
    (d.distribution_rules || []).forEach(function (r) {
      h += "<li>" + r.rule + " <code>" + r.source_chunk + "</code></li>";
    });
    h += "</ul>";
    if (d.escalation_items && d.escalation_items.length) {
      h += '<div class="kv">' + L.lbl_escalations + "</div><ul>";
      d.escalation_items.forEach(function (e) {
        h += '<li><span class="sev high">escalate</span> ' + e.question + " <i>(" + e.reason + ")</i></li>";
      });
      h += "</ul>";
    }
    return h;
  }

  function renderJurisdictionMap(d) {
    var L = dict();
    var h = '<div class="out-head"><h4>' + STEP_TITLES.jurisdiction_map + '</h4><span class="tag">' + L.tag_review + '</span></div>';
    h += "<p><em>" + d.disclaimer + "</em></p>";
    h += '<div class="kv">' + L.lbl_mapped + "</div><ul>";
    (d.mapped_requirements || []).forEach(function (m) {
      h += '<li><span class="sev ' + m.severity + '">' + m.severity + "</span> <b>" + m.topic + "</b>: " + m.linked_asset_fact + " <code>" + m.source_chunk + "</code></li>";
    });
    return h + "</ul>";
  }

  function renderProtocolOutline(d) {
    var L = dict();
    var h = '<div class="out-head"><h4>' + STEP_TITLES.protocol_outline + '</h4><span class="tag">' + L.tag_outline + '</span></div>';
    h += "<p><b>" + d.token_standard + "</b></p>";
    h += '<div class="kv">' + L.lbl_modules + "</div><ul>";
    (d.contract_modules || []).forEach(function (m) {
      h += "<li><b>" + m.module + "</b>: " + m.purpose + " <code>" + m.source_chunk + "</code></li>";
    });
    h += "</ul>";
    h += '<div class="kv">' + L.lbl_elchai + "</div><ul>";
    (d.elchai_services_mapped || []).forEach(function (s) {
      h += "<li><b>" + s.service + "</b>: " + s.reason + "</li>";
    });
    return h + "</ul>";
  }

  function renderGate(steps) {
    var L = dict();
    var esc = (steps.sovereign_guard.escalation_items || []).map(function (e) { return e.question; });
    var high = (steps.jurisdiction_map.mapped_requirements || []).filter(function (a) { return a.severity === "high"; }).map(function (a) { return a.topic; });
    var h = '<div class="gate-card"><b>' + L.gate_line + "</b>";
    if (esc.length) h += "<br>" + L.gate_esc + esc.join("; ") + ".";
    if (high.length) h += "<br>" + L.gate_high + high.join(", ") + ".";
    return h + "<br>" + L.gate_ok + "</div>";
  }

  function renderGovernanceManifest(d) {
    var L = dict();
    var h = '<div class="out-head"><h4>' + STEP_TITLES.governance_manifest + '</h4><span class="tag">' + L.tag_manifest + '</span></div>';
    h += '<div class="gate-card"><b>' + d.message + "</b></div>";
    h += "<p>" + d.human_control_ratio + "</p>";
    h += '<div class="kv">' + L.lbl_manifest + "</div>";
    h += "<ul><li>Asset facts: " + d.manifest_summary.asset_facts + "</li>";
    h += "<li>Compliance flags: " + d.manifest_summary.compliance_flags + "</li>";
    h += "<li>Contract modules: " + d.manifest_summary.contract_modules + "</li>";
    h += "<li>Escalations: " + d.manifest_summary.escalations + "</li></ul>";
    h += '<div class="kv">' + L.lbl_nextsteps + "</div>" + list(d.next_steps || []);
    return h + "<p><em>" + d.disclaimer + "</em></p>";
  }

  function appendBlock(html) {
    var b = document.createElement("div");
    b.className = "out-block";
    b.innerHTML = html;
    stageOutput.appendChild(b);
    b.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  function tickTo(node, from, to, fmt, ms) {
    var start = performance.now();
    function frame(now) {
      var p = Math.min((now - start) / ms, 1);
      node.textContent = fmt(from + (to - from) * p);
      if (p < 1) requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  async function run() {
    if (running) return;
    var brief = getActiveBrief();
    if (!brief) { briefInput.focus(); return; }
    running = true;
    runBtn.disabled = true;
    resetSteps();

    var result = window.CompassEngine.run(brief);
    lastResult = result;
    demoMode.textContent = "mode: " + result.meta.mode;
    teleStatus.textContent = dict().status_running;

    var renderers = {
      sovereign_guard: function () { return renderSovereignGuard(result.steps.sovereign_guard); },
      jurisdiction_map: function () { return renderJurisdictionMap(result.steps.jurisdiction_map); },
      protocol_outline: function () { return renderProtocolOutline(result.steps.protocol_outline); },
      gate: function () { return renderGate(result.steps); },
      governance_manifest: function () { return renderGovernanceManifest(result.steps.governance_manifest); }
    };

    var cumTokens = 0;
    var t0 = performance.now();

    for (var i = 0; i < STEP_ORDER.length; i++) {
      var k = STEP_ORDER[i];
      setStepState(k, "active");
      teleStep.textContent = (k === "gate" ? dict().step_gate : STEP_TITLES[k]);
      if (k === "gate") teleStatus.textContent = dict().status_gate;
      await wait(k === "gate" ? 700 : 900);

      if (k !== "gate") {
        var tk = result._tokens[k] || 0;
        var prev = cumTokens;
        cumTokens += tk;
        tickTo(teleTokens, prev, cumTokens, function (v) { return Math.round(v).toLocaleString(); }, 500);
        tickTo(teleCost, prev * COST_PER_TOKEN, cumTokens * COST_PER_TOKEN, function (v) { return "$" + v.toFixed(4); }, 500);
      }
      teleLatency.textContent = Math.round(performance.now() - t0) + " ms";
      appendBlock(renderers[k]());
      setStepState(k, "done");
      if (k === "gate") teleStatus.textContent = dict().status_running;
    }

    teleStatus.textContent = dict().status_done;
    result.meta.tokens_total = cumTokens;
    result.meta.est_cost_usd = +(cumTokens * COST_PER_TOKEN).toFixed(5);
    demoFoot.hidden = false;
    runBtn.disabled = false;
    running = false;
  }

  function download() {
    if (!lastResult) return;
    var blob = new Blob([JSON.stringify(lastResult, null, 2)], { type: "application/json" });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    var name = (lastResult.meta.project_title || "oasis-rwa").toLowerCase().replace(/[^a-z0-9]+/g, "-");
    a.href = url;
    a.download = "oasis-rwa-manifest-" + name + ".json";
    a.click();
    URL.revokeObjectURL(url);
  }

  chipRow.addEventListener("click", function (e) {
    var btn = e.target.closest(".chip");
    if (!btn) return;
    chipRow.querySelectorAll(".chip").forEach(function (c) { c.classList.remove("active"); });
    btn.classList.add("active");
    selectedBrief = btn.getAttribute("data-brief");
    if (selectedBrief === "custom") {
      briefInput.value = "";
      clientName.value = "";
      briefInput.focus();
    } else {
      showPresetText();
    }
  });

  function boot() {
    var lines = [
      "$ openclaw gateway start --config openclaw.example.json",
      "  routing ......... kimi-k2.5 (stages 2-3)",
      "  sovereign tier .. local RAG + redaction [qwen-ready]",
      "  pipeline ........ oasis-tower-rwa-rag",
      "  human gate ...... 20% control (enabled)",
      "[OpenClaw Gate: Awaiting authorized human sign-off]",
      "ready. ◆ Oasis Tower RWA pipeline online."
    ];
    var logEl = $("bootLog");
    var idx = 0;
    function next() {
      if (idx < lines.length) {
        logEl.textContent += lines[idx] + "\n";
        idx++;
        setTimeout(next, idx === 1 ? 260 : 200);
      } else {
        setTimeout(function () { $("boot").classList.add("hidden"); }, 450);
      }
    }
    next();
  }

  function glow() {
    var g = $("glow");
    window.addEventListener("pointermove", function (e) {
      g.style.left = e.clientX + "px";
      g.style.top = e.clientY + "px";
    });
  }

  function reveal() {
    var els = document.querySelectorAll("section > .section-title, .card, .benefit, .stage-card, .dept, .flow-node, .reco, .risk-table, .matrix-wrap, .philosophy");
    els.forEach(function (el) { el.classList.add("reveal"); });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { threshold: 0.12 });
    els.forEach(function (el) { io.observe(el); });
  }

  $("langToggle").addEventListener("click", function () { lang = lang === "en" ? "ar" : "en"; applyLang(); });
  runBtn.addEventListener("click", run);
  downloadBtn.addEventListener("click", download);

  applyLang();
  showPresetText();
  boot();
  glow();
  reveal();

  var nodes = document.querySelectorAll(".pipe-node");
  var hi = 0;
  setInterval(function () {
    nodes.forEach(function (n) { n.classList.remove("active"); });
    if (nodes.length) nodes[hi % nodes.length].classList.add("active");
    hi++;
  }, 1100);
})();
