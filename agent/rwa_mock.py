"""RWA + RAG pipeline mock engine for Oasis Tower POC."""

from __future__ import annotations

from brief_parser import parse_brief
from rag_store import format_citations, retrieve


def run_stage(stage: str, brief: dict, prior: dict) -> dict:
    return _DISPATCH[stage](brief, prior)


def _memo_chunks(brief: dict) -> list[dict]:
    q = brief.get("raw_request", "") + " " + " ".join(brief.get("stated_constraints", []))
    return retrieve(q, "oasis_tower_memo.json", top_k=5)


def _compliance_chunks(brief: dict) -> list[dict]:
    q = brief.get("raw_request", "") + " token KYC escrow transfer VARA ADGM PDPL"
    return retrieve(q, "compliance_modules.json", top_k=4)


def _sovereign_guard(brief: dict, prior: dict) -> dict:
    p = parse_brief(brief)
    chunks = _memo_chunks(brief) if p["is_oasis_preset"] else []
    ids = [c["id"] for c in chunks]

    facts = [
        {"fact": f"{p['asset_label']}, {p['valuation']}", "source_chunk": p["fact_source"]},
        {"fact": f"First tranche: {p['tranche']} economic interest in SPV", "source_chunk": p["fact_source"]},
    ]
    rules = [
        {"rule": "Quarterly distribution, last business day of Mar/Jun/Sep/Dec", "source_chunk": p["rule_source"]},
        {"rule": f"{p['reserve']} maintenance reserve before distribution", "source_chunk": p["rule_source"]},
    ]
    escalations = [
        {"question": "Is retail investor participation allowed in phase one?", "reason": "Brief targets professional/qualified investors; retail path not defined"},
        {"question": "Final VARA licensing path for this token class?", "reason": "Not defined in submitted brief or memo corpus"},
    ]
    if not p["is_oasis_preset"]:
        escalations.insert(0, {
            "question": "Validate all facts against client's full offering memorandum",
            "reason": "Custom brief: facts parsed from request text only (Oasis memo corpus not used)",
        })

    return {
        "redacted_fields": ["investor_relations_email"],
        "extracted_asset_facts": facts,
        "distribution_rules": rules,
        "escalation_items": escalations,
        "rag_chunks_used": ids if ids else ["client-brief"],
        "local_tier_note": "Processed on-prem by the local sovereign tier (Qwen/Ollama-ready) before any external API call",
        "citations": format_citations(chunks) if chunks else [
            {"id": "client-brief", "section": "Submitted request", "excerpt": (brief.get("raw_request") or "")[:220]},
        ],
    }


def _jurisdiction_map(brief: dict, prior: dict) -> dict:
    p = parse_brief(brief)
    comp = _compliance_chunks(brief)
    return {
        "disclaimer": "Review-required flags only, not legal advice.",
        "jurisdiction_focus": ["UAE", "Dubai"],
        "mapped_requirements": [
            {"topic": "Virtual asset / token classification", "linked_asset_fact": f"Fractional interest in {p['asset_label']}", "source_chunk": "vara-001", "severity": "high"},
            {"topic": "Marketing and disclosure to UAE investors", "linked_asset_fact": f"Professional investor tranche ({p['tranche']})", "source_chunk": "vara-002", "severity": "high"},
            {"topic": "Permissioned transfer and custody", "linked_asset_fact": f"{p['transfer_lock']} transfer restriction", "source_chunk": "adgm-001", "severity": "medium"},
            {"topic": "Investor KYC data residency", "linked_asset_fact": "KYC before whitelisting", "source_chunk": "pdpl-001", "severity": "high"},
        ],
        "fractional_distribution_flags": [
            f"Quarterly distribution logic must match brief ({p['reserve']} reserve); counsel to confirm tax withholding",
        ],
        "escrow_timeline_flags": [
            f"Escrow release tied to {p['escrow']} minimum per client-brief",
        ],
        "data_residency_notes": [
            "Run KYC document text through local tier before external LLM calls (pdpl-001)",
        ],
        "citations": format_citations(comp),
    }


def _protocol_outline(brief: dict, prior: dict) -> dict:
    p = parse_brief(brief)
    src = p["fact_source"]
    return {
        "token_standard": "ERC-3643 (T-REX) style permissioned token (outline only)",
        "contract_modules": [
            {"module": "IdentityRegistry + whitelist", "purpose": "KYC-gated wallet onboarding", "source_chunk": src},
            {"module": "ComplianceModule", "purpose": f"Enforce {p['transfer_lock']} transfer restrictions", "source_chunk": p["lock_source"]},
            {"module": "DividendDistribution", "purpose": f"Quarterly pro-rata distributions with {p['reserve']} reserve", "source_chunk": p["rule_source"]},
            {"module": "EscrowController", "purpose": f"Hold subscriptions until {p['escrow']} minimum raise", "source_chunk": p["escrow_source"]},
        ],
        "distribution_logic_outline": [
            "Read net rental income feed (off-chain oracle with audit trail)",
            f"Apply {p['reserve']} maintenance reserve per client brief",
            "Pro-rata payout to whitelisted holders on quarterly schedule",
        ],
        "transfer_restriction_outline": [
            f"{p['transfer_lock']} lock from issuance",
            "Re-run compliance check on secondary transfers",
        ],
        "integration_points": brief.get("known_systems", []),
        "audit_requirements": [
            "Third-party smart contract audit before mainnet",
            "Formal verification of transfer rules recommended (erc-001)",
        ],
        "elchai_services_mapped": [
            {"service": "Real World Asset (RWA) tokenization", "reason": f"Core offering for {p['asset_label']}"},
            {"service": "Smart contract development (with audits)", "reason": "Permissioned token and distribution logic"},
            {"service": "Custodial wallet development", "reason": "Professional investor onboarding"},
            {"service": "Enterprise app development", "reason": "Investor portal and reporting"},
            {"service": "RAG development", "reason": "Ground agent answers in offering memo and policy docs"},
        ],
    }


def _governance_manifest(brief: dict, prior: dict) -> dict:
    high = [
        m["topic"]
        for m in prior.get("jurisdiction_map", {}).get("mapped_requirements", [])
        if m.get("severity") == "high"
    ]
    return {
        "project": brief.get("project_title", brief.get("client_name")),
        "openclaw_gate_status": "HALTED",
        "message": "[OpenClaw Gate: Awaiting authorized human sign-off before staging protocol generation]",
        "human_control_ratio": "20% human review / 80% automated draft (enterprise control pattern)",
        "manifest_summary": {
            "asset_facts": len(prior.get("sovereign_guard", {}).get("extracted_asset_facts", [])),
            "compliance_flags": len(prior.get("jurisdiction_map", {}).get("mapped_requirements", [])),
            "contract_modules": len(prior.get("protocol_outline", {}).get("contract_modules", [])),
            "escalations": len(prior.get("sovereign_guard", {}).get("escalation_items", [])),
        },
        "high_severity_review": high,
        "next_steps": [
            "Legal counsel reviews jurisdiction_map output",
            "Engineering estimates audit timeline for protocol_outline",
            "No Solidity deployment until signed manifest",
        ],
        "disclaimer": "Demo manifest only. Not for production or client use.",
    }


_DISPATCH = {
    "sovereign_guard": _sovereign_guard,
    "jurisdiction_map": _jurisdiction_map,
    "protocol_outline": _protocol_outline,
    "governance_manifest": _governance_manifest,
}
