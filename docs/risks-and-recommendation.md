# Risks, Limitations & Final Recommendation

## Model Comparison Matrix (GCC Enterprise Context)

| Model / Framework | Local deployment | Cost profile | Best use for Elchai-style work | Main limitation |
|---|---|---|---|---|
| Kimi K2-family | Not suitable for ordinary consumer GPU deployment at full scale | External API/provider pricing; check current provider terms | Multi-step agentic reasoning, architecture drafting, code planning | External API introduces procurement, data residency, and vendor-review questions |
| Qwen 2.5 / Qwen3 family | Practical in quantized form through tools like Ollama, depending on model size and hardware | Local infrastructure cost | Sovereign RAG, document parsing, redaction, pre-filtering before external calls | Lower ceiling than frontier-scale external models for very long-horizon agentic work |
| GLM / MiniMax | Depends on model and quantization | Provider/local deployment dependent | Multimodal extraction, KYC assets, visual documents, floor plans | Less directly demonstrated in this POC |
| OpenClaw-style gateway | Local/team service | Infrastructure and maintenance cost | Controlled orchestration and human-in-the-loop gates | Requires security hardening, access control, and operational ownership |

## Risks and Limitations

| # | Risk | Why it matters | POC mitigation | Residual risk |
|---|---|---|---|---|
| 1 | Privacy / data residency | GCC banking, real estate, and investor data may be sensitive | Fictional data only; local redaction; no real client data | Production requires legal/IT review and approved data handling |
| 2 | Security | Agent systems can become dangerous if connected to tools without controls | Human gate; no autonomous deployment; OpenClaw config example uses guarded routing | Real deployment needs hardening, audit, and permission design |
| 3 | Hallucination | Wrong compliance text or unsupported facts can mislead decision-makers | RAG citations; escalate-if-not-in-source; review-required language | Human counsel must still review all compliance items |
| 4 | Model accuracy | Incorrect architecture outline can waste engineering or audit budget | Structured prompts, citations, deterministic manifest stage | Output quality depends on corpus quality and prompt coverage |
| 5 | Local hardware | Larger open models may require significant memory or GPU resources | Hybrid tier: local lightweight handling plus optional external agentic model | Heavy local inference may need costly hardware |
| 6 | Integration | Real RWA work needs KYC, custody, payments, wallets, CRM/ERP, and audit systems | POC isolates early discovery and architecture handoff | Each production integration is a separate project |
| 7 | Reliability | API downtime, local model failures, or invalid JSON can disrupt workflows | Offline mock path; deterministic browser demo; simple retry logic in Kimi client | Live mode still depends on provider uptime and credentials |
| 8 | Vendor / procurement risk | External model providers may not meet every client policy | Model-agnostic design and local pre-filtering | Procurement approval is required before real client use |

## Final Recommendation

**Test as a limited internal research POC with guardrails. Do not use on real
client data yet.**

Recommended production pattern:

**Localized sensitive-data tier + external agentic tier + deterministic human gate**

This means local RAG/redaction first, Kimi or another approved agentic model only
after data review, and an OpenClaw-style governance gate before any blockchain
artifact or client-facing recommendation is produced.

The POC is useful for internal pilots, workshops, and client demos on synthetic
briefs. Reassess after review by Elchai's AI, infrastructure, and legal teams.
