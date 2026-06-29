"""Deterministic, brief-aware stand-in for the Kimi model.

This is NOT meant to imitate a real LLM's quality. It exists so the pipeline,
sample outputs, and landing-page demo are fully reproducible with zero API cost
or keys. In live mode (--live) these functions are bypassed and the configured
Kimi-compatible model is called with the exact same prompts in agent/prompts/.

Each generator reads real fields from the brief and branches on a few keywords,
so the output genuinely reflects the input rather than being hard-coded.
"""

from __future__ import annotations


def generate(step: str, brief: dict, prior: dict) -> dict:
    return _DISPATCH[step](brief, prior)


def _kind(brief: dict) -> str:
    text = (brief.get("raw_request", "") + " " + brief.get("industry", "")).lower()
    if any(w in text for w in ("tokeniz", "fractional", "rwa", "real estate")):
        return "tokenization"
    if any(w in text for w in ("assistant", "support", "ticket", "payment", "chatbot")):
        return "assistant"
    return "generic"


def _intake(brief: dict, prior: dict) -> dict:
    kind = _kind(brief)
    constraints = list(brief.get("stated_constraints", []))
    systems = brief.get("known_systems", [])
    base = {
        "summary": (
            f"{brief.get('client_name', 'The client')} wants to "
            + ("tokenize part of a UAE commercial real estate portfolio and let "
               "investors buy fractional ownership, with onboarding, income "
               "distribution, and integration into existing property systems."
               if kind == "tokenization" else
               "deploy an AI assistant for customers plus an internal triage "
               "agent for the operations team, without giving customers wrong "
               "financial or regulatory information.")
        ),
        "primary_goals": (
            ["Tokenize a first tranche of buildings for fractional investment",
             "Onboard and verify investors digitally",
             "Automate rental-income distribution",
             "Integrate with existing property-management systems"]
            if kind == "tokenization" else
            ["Reduce repetitive customer support load",
             "Answer customer questions accurately and safely",
             "Help operations triage and summarize incoming tickets"]
        ),
        "functional_requirements": (
            ["Issue tokens representing fractional building ownership",
             "Digital investor onboarding with KYC",
             "Secondary transfers between investors",
             "Automated rental-income distribution",
             "Integration with the property-management system"]
            if kind == "tokenization" else
            ["Answer customer questions in English and Arabic",
             "Look up transaction status via internal API",
             "Draft compliance-safe replies for agents",
             "Summarize and triage incoming support tickets"]
        ),
        "non_functional_requirements": [
            "Aggressive timeline (pilot within one quarter)" if kind == "tokenization"
            else "Must never invent fees, limits, or regulatory rules",
            "Keep sensitive data within the UAE where possible" if kind == "tokenization"
            else "Careful handling of sensitive customer data",
            "Auditable and compliance-aware by design",
        ],
        "constraints": constraints,
        "open_questions": (
            ["Which specific buildings are in the first tranche?",
             "Are target investors retail, accredited, or institutional?",
             "What is the licensing position for offering tokenized assets?",
             "What does the Yardi integration need to read and write?"]
            if kind == "tokenization" else
            ["What is the allowed scope of answers the assistant may give?",
             "Which actions can the assistant take vs only draft for an agent?",
             "What is the source of truth for fees, limits, and KYC status?",
             "What data can leave the customer's region?"]
        ),
        "primary_industry": brief.get("industry", "not specified"),
    }
    if systems:
        base["non_functional_requirements"].append(
            "Must connect to: " + ", ".join(systems))
    return base


def _compliance(brief: dict, prior: dict) -> dict:
    kind = _kind(brief)
    disclaimer = ("These are review-required flags for a qualified human, not "
                  "legal advice. Nothing here is a final compliance conclusion.")
    if kind == "tokenization":
        areas = [
            {"topic": "Virtual asset / security token regulation",
             "why_it_matters": "Offering fractional ownership tokens to investors may fall under virtual-asset or securities oversight.",
             "who_should_review": "UAE-licensed legal counsel and a virtual-asset compliance specialist",
             "severity": "high"},
            {"topic": "Investor KYC / AML",
             "why_it_matters": "Onboarding and secondary transfers need identity verification and anti-money-laundering checks.",
             "who_should_review": "Compliance officer / MLRO",
             "severity": "high"},
            {"topic": "Data residency (UAE)",
             "why_it_matters": "The client asked to keep investor data within the UAE where possible.",
             "who_should_review": "Data protection lead with UAE PDPL knowledge",
             "severity": "medium"},
            {"topic": "Cross-border investor eligibility",
             "why_it_matters": "International investors may trigger rules in their own jurisdictions.",
             "who_should_review": "Legal counsel",
             "severity": "medium"},
        ]
        notes = [
            "Confirm where investor KYC documents are stored and who can access them.",
            "Map which token actions are recorded on-chain vs off-chain for privacy.",
        ]
    else:
        areas = [
            {"topic": "Accuracy of financial / regulatory answers",
             "why_it_matters": "Wrong fee, limit, or KYC information given to a customer could create real harm and liability.",
             "who_should_review": "Compliance officer and legal counsel",
             "severity": "high"},
            {"topic": "Customer data handling (KYC / transactions)",
             "why_it_matters": "The assistant touches personal and transaction data across multiple countries.",
             "who_should_review": "Data protection lead",
             "severity": "high"},
            {"topic": "Cross-border data flow (UAE / KSA / Egypt)",
             "why_it_matters": "Each country may have its own rules on where customer data can be processed.",
             "who_should_review": "Legal counsel per jurisdiction",
             "severity": "medium"},
        ]
        notes = [
            "Define a strict list of topics the assistant may answer vs must escalate.",
            "Log every automated reply for audit and quality review.",
        ]
    return {"disclaimer": disclaimer, "review_areas": areas, "data_handling_notes": notes}


def _architecture(brief: dict, prior: dict) -> dict:
    kind = _kind(brief)
    integrations = brief.get("known_systems", [])
    if kind == "tokenization":
        return {
            "recommended_services": [
                {"service": "Real World Asset (RWA) tokenization",
                 "reason": "Core need: represent fractional building ownership as tokens."},
                {"service": "Smart contract development (with audits)",
                 "reason": "Encode ownership, transfers, and income distribution safely."},
                {"service": "Custodial wallet development",
                 "reason": "Give non-crypto-native investors a simple way to hold tokens."},
                {"service": "Enterprise app development",
                 "reason": "Investor onboarding portal and dashboards."},
                {"service": "RAG development",
                 "reason": "Ground an investor-support assistant in verified documents only."},
            ],
            "proposed_architecture": [
                "Token contract on an audited Layer 1/Layer 2 representing fractional ownership",
                "KYC-gated investor onboarding portal",
                "Custodial wallet so investors need no crypto knowledge",
                "Automated rental-income distribution via smart contract",
                "Integration layer syncing ownership with the property-management system",
                "Human-reviewed investor-support assistant grounded in approved documents",
            ],
            "integrations": integrations or ["Property-management system"],
            "effort_and_risk_flags": [
                {"item": "One-quarter pilot timeline", "impact": "high",
                 "note": "Smart-contract audits and KYC integration are hard to rush."},
                {"item": "Regulatory approval", "impact": "high",
                 "note": "Token offering may need licensing before any public pilot."},
                {"item": "Yardi integration depth", "impact": "medium",
                 "note": "Two-way sync of ownership records can be complex."},
            ],
            "phasing": [
                "Phase 1: Compliance review, architecture sign-off, single-building proof of concept",
                "Phase 2: KYC onboarding, audited contracts, custodial wallets, income distribution",
                "Phase 3: Secondary transfers, multi-building rollout, full system integration",
            ],
        }
    return {
        "recommended_services": [
            {"service": "AI assistants / Agentic AI",
             "reason": "Customer-facing assistant plus internal triage agent."},
            {"service": "RAG development",
             "reason": "Ground answers in verified fees, limits, and policies so the model cannot invent them."},
            {"service": "AI automation / RPA",
             "reason": "Auto-summarize and route incoming tickets for the ops team."},
            {"service": "AI integration",
             "reason": "Connect to Zendesk and the internal transactions API."},
        ],
        "proposed_architecture": [
            "RAG knowledge base built only from approved policy and fee documents",
            "Customer assistant that answers in English and Arabic, with strict escalation rules",
            "Read-only transaction-status lookup via the internal API",
            "Internal triage agent that summarizes and tags tickets in Zendesk",
            "Human-in-the-loop: regulated or low-confidence questions are drafted, not auto-sent",
        ],
        "integrations": integrations or ["Zendesk", "Internal transactions API"],
        "effort_and_risk_flags": [
            {"item": "Answer accuracy on money/regulation", "impact": "high",
             "note": "Must use grounding + confidence thresholds, never free-form generation."},
            {"item": "Bilingual quality (Arabic)", "impact": "medium",
             "note": "Arabic responses need dedicated evaluation."},
            {"item": "Transaction API access", "impact": "medium",
             "note": "Scope and secure exactly what the assistant can read."},
        ],
        "phasing": [
            "Phase 1: Grounded FAQ assistant (answers only, no actions) + internal triage",
            "Phase 2: Transaction-status lookups with strict guardrails",
            "Phase 3: Broader actions after accuracy is proven in production",
        ],
    }


def _proposal(brief: dict, prior: dict) -> dict:
    kind = _kind(brief)
    compliance = prior.get("compliance", {})
    top_risks = [a["topic"] for a in compliance.get("review_areas", [])
                 if a.get("severity") == "high"][:3]
    if kind == "tokenization":
        return {
            "title": "RWA Tokenization Discovery - Gulf Horizon Properties",
            "executive_summary": (
                "Gulf Horizon Properties wants to tokenize a first tranche of UAE "
                "commercial buildings for fractional investment within one quarter. "
                "Elchai can deliver this with audited smart contracts, KYC-gated "
                "onboarding, custodial wallets, and integration into existing "
                "property systems. The biggest dependency is regulatory review, "
                "which must clear before any public pilot."),
            "scope_outline": [
                "Discovery workshop and compliance review",
                "Single-building tokenization proof of concept",
                "KYC investor onboarding flow",
                "Audited smart contracts for ownership and income distribution",
                "Property-management system integration plan",
            ],
            "out_of_scope": [
                "Legal/regulatory licensing (client + counsel responsibility)",
                "Secondary-market trading at this phase",
                "Multi-building rollout before the proof of concept is approved",
            ],
            "key_risks_to_raise": top_risks or ["Regulatory approval", "Timeline"],
            "suggested_next_steps": [
                "Book a 2-hour discovery workshop",
                "Confirm regulatory position with UAE-licensed counsel",
                "Agree the single building for the proof of concept",
            ],
            "human_review_note": "Verify all compliance flags and set pricing before sending to the client.",
        }
    return {
        "title": "AI Support Assistant Discovery - Cedar Pay",
        "executive_summary": (
            "Cedar Pay wants an accurate, bilingual AI assistant for customers and "
            "an internal triage agent for operations, without ever giving wrong "
            "financial or regulatory information. Elchai recommends a grounded "
            "(RAG) approach with strict escalation and human review, starting with "
            "answer-only support before adding any actions."),
        "scope_outline": [
            "Discovery workshop and answer-scope definition",
            "Grounded FAQ assistant (English + Arabic)",
            "Internal ticket triage and summarization in Zendesk",
            "Read-only transaction-status lookup with guardrails",
        ],
        "out_of_scope": [
            "Free-form financial or legal advice",
            "Money-moving actions in the first phase",
            "Unsupervised auto-replies on regulated topics",
        ],
        "key_risks_to_raise": top_risks or ["Answer accuracy", "Customer data handling"],
        "suggested_next_steps": [
            "Book a discovery workshop",
            "Agree the exact list of answerable vs escalate-only topics",
            "Identify the source of truth for fees, limits, and KYC status",
        ],
        "human_review_note": "Verify all compliance flags and set pricing before sending to the client.",
    }


_DISPATCH = {
    "intake": _intake,
    "compliance": _compliance,
    "architecture": _architecture,
    "proposal": _proposal,
}
