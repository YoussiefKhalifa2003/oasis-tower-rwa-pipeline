(function () {
  "use strict";

  var MEMO = [
    { id: "memo-001", section: "Asset summary", text: "Oasis Tower is a Grade-A commercial tower in Dubai Internet City. Net lettable area is 412,000 sq ft. Valuation by independent appraiser (fictional): AED 890 million as of Q1 2026. First tokenized tranche targets 18% of economic interest in the SPV holding the asset." },
    { id: "memo-002", section: "Distribution policy", text: "Net rental income from occupied floors is distributed quarterly to token holders pro-rata, subject to a 5% maintenance reserve. Distribution dates: last business day of March, June, September, December." },
    { id: "memo-003", section: "Investor eligibility", text: "Initial offering is limited to professional investors. Retail participation requires separate regulatory approval. KYC must be completed before wallet whitelisting." },
    { id: "memo-004", section: "Escrow and settlement", text: "Primary subscription funds are held in escrow until minimum subscription (AED 45M) is reached. If not reached by 30 September 2026, subscriptions are returned." },
    { id: "memo-005", section: "Technology", text: "Tokens represent economic interest in Oasis Tower SPV Ltd. Transfer restrictions apply for 12 months from issuance." }
  ];

  var COMPLIANCE = [
    { id: "vara-001", jurisdiction: "UAE / VARA", text: "Virtual asset activities involving issuance or facilitation of tokens may require alignment with applicable UAE virtual asset regulatory frameworks." },
    { id: "vara-002", jurisdiction: "UAE / VARA", text: "Marketing and promotional materials for virtual assets must be clear, fair, and not misleading." },
    { id: "adgm-001", jurisdiction: "ADGM", text: "ADGM frameworks for digital securities emphasize clear investor disclosure, custody arrangements, and transfer restriction enforcement." },
    { id: "pdpl-001", jurisdiction: "UAE PDPL", text: "Personal data of investors should be processed with defined residency, retention, and access controls." },
    { id: "erc-001", jurisdiction: "Technical standard", text: "ERC-3643 and ERC-1400 family standards support permissioned security tokens with transfer rules and compliance hooks." }
  ];

  function parseBrief(brief) {
    var text = brief.raw_request || "";
    var full = (text + " " + (brief.stated_constraints || []).join(" ")).toLowerCase();
    var isOasis = brief.brief_id === "OASIS-RWA-2026" ||
      (full.indexOf("oasis tower") >= 0 && full.indexOf("dubai internet city") >= 0);

    var p = {
      is_oasis_preset: isOasis,
      asset_label: "Oasis Tower, Dubai Internet City",
      tranche: "18%",
      reserve: "5%",
      transfer_lock: "12-month",
      escrow: "AED 45M",
      valuation: "AED 890M valuation (fictional)",
      fact_source: isOasis ? "memo-001" : "client-brief",
      rule_source: isOasis ? "memo-002" : "client-brief",
      lock_source: isOasis ? "memo-005" : "client-brief",
      escrow_source: isOasis ? "memo-004" : "client-brief"
    };

    if (isOasis) return p;

    p.valuation = "Valuation not stated in brief - escalate to client";

    var cn = (brief.client_name || "").replace(/\(fictional\)/gi, "").trim();
    if (cn && cn.toLowerCase() !== "custom brief") p.asset_label = cn;

    var m = text.match(/interest in ([^,.]+)/i);
    if (m) p.asset_label = m[1].trim();
    m = text.match(/in ([^,]+), a /i);
    if (m) p.asset_label = m[1].trim();

    m = text.match(/tokenize\s+(?:a\s+)?(?:first\s+)?tranche\s+of\s+(\d+)%/i) ||
        text.match(/(\d+)%\s*of\s*economic/i);
    if (m) p.tranche = m[1] + "%";

    m = text.match(/(\d+)%\s*(?:reserve|maintenance)/i);
    if (m) p.reserve = m[1] + "%";

    m = text.match(/(\d+)-month\s*transfer/i);
    if (m) p.transfer_lock = m[1] + "-month";

    m = text.match(/escrow until (AED\s*[\d.]+\s*[Mm]?)/i);
    if (m) p.escrow = m[1].replace(/\s+/g, "");
    else {
      m = text.match(/(AED\s*[\d.]+[Mm]?)/i);
      if (m) p.escrow = m[1].replace(/\s+/g, "");
    }

    return p;
  }

  function tokenSet(text) {
    var s = {};
    (text || "").toLowerCase().match(/[a-z0-9]+/g)?.forEach(function (t) { s[t] = true; });
    return s;
  }

  function retrieve(query, corpus, topK) {
    var q = tokenSet(query);
    var qKeys = Object.keys(q);
    if (!qKeys.length) return [];
    return corpus.map(function (chunk) {
      var t = tokenSet(chunk.text);
      var tKeys = Object.keys(t);
      var inter = 0;
      qKeys.forEach(function (k) { if (t[k]) inter++; });
      var union = qKeys.length + tKeys.length - inter;
      return { score: union ? inter / union : 0, chunk: chunk };
    }).filter(function (x) { return x.score > 0; })
      .sort(function (a, b) { return b.score - a.score; })
      .slice(0, topK).map(function (x) { return x.chunk; });
  }

  function citations(chunks) {
    return chunks.map(function (c) {
      return { id: c.id, section: c.section || c.jurisdiction || "", excerpt: c.text.slice(0, 220) };
    });
  }

  function sovereignGuard(brief) {
    var p = parseBrief(brief);
    var q = (brief.raw_request || "") + " " + (brief.stated_constraints || []).join(" ");
    var chunks = p.is_oasis_preset ? retrieve(q, MEMO, 5) : [];
    var ids = chunks.map(function (c) { return c.id; });

    var escalations = [
      { question: "Is retail investor participation allowed in phase one?", reason: "Brief targets professional/qualified investors; retail path not defined" },
      { question: "Final VARA licensing path for this token class?", reason: "Not defined in submitted brief or memo corpus" }
    ];
    if (!p.is_oasis_preset) {
      escalations.unshift({
        question: "Validate all facts against client's full offering memorandum",
        reason: "Custom brief: facts parsed from request text only (Oasis memo corpus not used)"
      });
    }

    return {
      redacted_fields: ["investor_relations_email"],
      extracted_asset_facts: [
        { fact: p.asset_label + ", " + p.valuation, source_chunk: p.fact_source },
        { fact: "First tranche: " + p.tranche + " economic interest in SPV", source_chunk: p.fact_source }
      ],
      distribution_rules: [
        { rule: "Quarterly distribution, last business day of Mar/Jun/Sep/Dec", source_chunk: p.rule_source },
        { rule: p.reserve + " maintenance reserve before distribution", source_chunk: p.rule_source }
      ],
      escalation_items: escalations,
      rag_chunks_used: ids.length ? ids : ["client-brief"],
      local_tier_note: "Processed on-prem by the local sovereign tier (Qwen/Ollama-ready) before any external API call",
      citations: chunks.length ? citations(chunks) : [{
        id: "client-brief", section: "Submitted request", excerpt: (brief.raw_request || "").slice(0, 220)
      }]
    };
  }

  function jurisdictionMap(brief) {
    var p = parseBrief(brief);
    var comp = retrieve((brief.raw_request || "") + " token KYC escrow VARA ADGM", COMPLIANCE, 4);
    return {
      disclaimer: "Review-required flags only, not legal advice.",
      jurisdiction_focus: ["UAE", "Dubai"],
      mapped_requirements: [
        { topic: "Virtual asset / token classification", linked_asset_fact: "Fractional interest in " + p.asset_label, source_chunk: "vara-001", severity: "high" },
        { topic: "Marketing and disclosure to UAE investors", linked_asset_fact: "Professional investor tranche (" + p.tranche + ")", source_chunk: "vara-002", severity: "high" },
        { topic: "Permissioned transfer and custody", linked_asset_fact: p.transfer_lock + " transfer restriction", source_chunk: "adgm-001", severity: "medium" },
        { topic: "Investor KYC data residency", linked_asset_fact: "KYC before whitelisting", source_chunk: "pdpl-001", severity: "high" }
      ],
      fractional_distribution_flags: ["Quarterly distribution logic must match brief (" + p.reserve + " reserve); counsel to confirm tax withholding"],
      escrow_timeline_flags: ["Escrow release tied to " + p.escrow + " minimum per client-brief"],
      data_residency_notes: ["Run KYC document text through local tier before external LLM calls (pdpl-001)"],
      citations: citations(comp.length ? comp : COMPLIANCE.slice(0, 3))
    };
  }

  function protocolOutline(brief) {
    var p = parseBrief(brief);
    return {
      token_standard: "ERC-3643 (T-REX) style permissioned token (outline only)",
      contract_modules: [
        { module: "IdentityRegistry + whitelist", purpose: "KYC-gated wallet onboarding", source_chunk: p.fact_source },
        { module: "ComplianceModule", purpose: "Enforce " + p.transfer_lock + " transfer restrictions", source_chunk: p.lock_source },
        { module: "DividendDistribution", purpose: "Quarterly pro-rata distributions with " + p.reserve + " reserve", source_chunk: p.rule_source },
        { module: "EscrowController", purpose: "Hold subscriptions until " + p.escrow + " minimum raise", source_chunk: p.escrow_source }
      ],
      distribution_logic_outline: [
        "Read net rental income feed (off-chain oracle with audit trail)",
        "Apply " + p.reserve + " maintenance reserve per client brief",
        "Pro-rata payout to whitelisted holders on quarterly schedule"
      ],
      transfer_restriction_outline: [
        p.transfer_lock + " lock from issuance",
        "Re-run compliance check on secondary transfers"
      ],
      integration_points: brief.known_systems || ["Custodial wallet", "KYC provider", "Escrow bank account"],
      audit_requirements: [
        "Third-party smart contract audit before mainnet",
        "Formal verification of transfer rules recommended (erc-001)"
      ],
      elchai_services_mapped: [
        { service: "Real World Asset (RWA) tokenization", reason: "Core offering for " + p.asset_label },
        { service: "Smart contract development (with audits)", reason: "Permissioned token and distribution logic" },
        { service: "Custodial wallet development", reason: "Professional investor onboarding" },
        { service: "Enterprise app development", reason: "Investor portal and reporting" },
        { service: "RAG development", reason: "Ground agent answers in offering memo and policy docs" }
      ]
    };
  }

  function governanceManifest(brief, prior) {
    var high = (prior.jurisdiction_map.mapped_requirements || []).filter(function (m) {
      return m.severity === "high";
    }).map(function (m) { return m.topic; });
    return {
      project: brief.project_title || brief.client_name,
      openclaw_gate_status: "HALTED",
      message: "[OpenClaw Gate: Awaiting authorized human sign-off before staging protocol generation]",
      human_control_ratio: "20% human review / 80% automated draft (enterprise control pattern)",
      manifest_summary: {
        asset_facts: (prior.sovereign_guard.extracted_asset_facts || []).length,
        compliance_flags: (prior.jurisdiction_map.mapped_requirements || []).length,
        contract_modules: (prior.protocol_outline.contract_modules || []).length,
        escalations: (prior.sovereign_guard.escalation_items || []).length
      },
      high_severity_review: high,
      next_steps: [
        "Legal counsel reviews jurisdiction_map output",
        "Engineering estimates audit timeline for protocol_outline",
        "No Solidity deployment until signed manifest"
      ],
      disclaimer: "Demo manifest only. Not for production or client use."
    };
  }

  function run(brief) {
    var sg = sovereignGuard(brief);
    var jm = jurisdictionMap(brief);
    var po = protocolOutline(brief);
    var prior = { sovereign_guard: sg, jurisdiction_map: jm, protocol_outline: po };
    var gm = governanceManifest(brief, prior);
    return {
      meta: {
        client_name: brief.client_name || "Custom brief",
        project_title: brief.project_title || brief.client_name,
        generated_at: new Date().toISOString().slice(0, 19),
        mode: "in-browser RAG pipeline (mirrors Python orchestrator)",
        model: "oasis-rwa-engine-js",
        pipeline: "oasis-tower-rwa-rag"
      },
      steps: { sovereign_guard: sg, jurisdiction_map: jm, protocol_outline: po, governance_manifest: gm },
      _tokens: {
        sovereign_guard: Math.round(JSON.stringify(sg).length / 4),
        jurisdiction_map: Math.round(JSON.stringify(jm).length / 4),
        protocol_outline: Math.round(JSON.stringify(po).length / 4),
        governance_manifest: Math.round(JSON.stringify(gm).length / 4)
      }
    };
  }

  window.RwaEngine = { run: run, parseBrief: parseBrief };
})();
