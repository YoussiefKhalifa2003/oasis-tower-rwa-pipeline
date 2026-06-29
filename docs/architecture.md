# Architecture: Oasis Tower RWA Pipeline

## What it is

A RAG-driven research POC for fractional real estate tokenization. It takes a
fictional client brief (Oasis Tower SPV, Dubai) plus a committed offering
memorandum corpus, and produces a structured governance manifest: grounded asset
facts, compliance review flags, a permissioned-token architecture outline, and a
deterministic halt for human sign-off.

This aligns with RWA tokenization workflows Elchai Group publicly sells. It does
not claim to describe Elchai's internal operations.

## Pipeline

```text
Client brief (JSON) + RAG corpus
  |
  v
Stage 0: Local sovereign tier
  - local RAG over the offering memo
  - regex redaction by default
  - optional Qwen/Ollama helper when configured
  |
  v
1. SovereignGuard
  - extracts source-grounded asset facts
  - escalates missing regulatory facts
  |
  v
2. JurisdictionMapper
  - Kimi-compatible live path
  - maps asset facts to VARA/ADGM/PDPL-style review flags
  |
  v
3. ProtocolArchitect
  - Kimi-compatible live path
  - drafts ERC-3643/ERC-1400 architecture outline with citations
  |
  v
OpenClaw-style governance gate
  - awaiting authorized human sign-off
  |
  v
4. GovernanceManifest
  - deterministic JSON manifest
  - status: HALTED until review
```

Each model-facing stage is a system prompt in `agent/prompts/` plus the brief,
prior stage outputs, and retrieved RAG chunks injected by `orchestrator.py`.

## RAG Layer

| Corpus file | Contents | Used in |
|---|---|---|
| `rag_corpus/oasis_tower_memo.json` | 5 fictional offering-memo chunks | Stage 1 and cited in stage 3 |
| `rag_corpus/compliance_modules.json` | VARA, ADGM, PDPL, ERC reference snippets | Stages 2 and 3 |

Retrieval is keyword token overlap (`rag_store.py`): offline, reproducible, and
no vector database required for the assessment. Every fact in SovereignGuard
output should cite a chunk id or become an escalation item.

## Model Tiers

| Tier | Model/tool | Where it runs | Used for |
|---|---|---|---|
| Sovereign | Local RAG + optional Qwen/Ollama | Local machine | RAG ingest, redaction, source grounding |
| Agentic | Kimi-compatible model | Moonshot-compatible API when live mode is enabled | Jurisdiction mapping and protocol architecture |
| Control | Deterministic Python + OpenClaw-style gate | Local machine | Human sign-off manifest |

The split is a practical deployment choice: sensitive data is handled locally
first, while larger agentic reasoning can be routed externally only after
redaction and with human-approved guardrails.

## Orchestration

- **Working POC:** `agent/orchestrator.py` runs the pipeline in mock mode by
  default and can call the Kimi-compatible client with `--live`.
- **Browser demo:** `web/engine.js` mirrors the mock engine so reviewers can run
  the project with no backend and no API key.
- **Deployment concept:** `openclaw/` contains an example gateway config and
  skill file for routing the same staged workflow through an OpenClaw-style setup.

## Control Pattern

The project uses an 80/20 pattern: AI drafts the structured analysis, while the
final 20% is human review and authorization. Stage 4 is not an LLM call. It
compiles a manifest and stops. No Solidity is generated in this POC.
