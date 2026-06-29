# Prompts & Tools Used

Honest log of the tools, prompts, and fallbacks used for the Oasis Tower RWA
Pipeline submission.

## Tools Used

| Tool | Role in this project | Paid? |
|---|---|---|
| Kimi-compatible API path | Optional live JurisdictionMapper and ProtocolArchitect stages | Provider/API cost |
| OpenClaw-style workflow | Gateway/orchestration concept and human gate pattern | Open-source/infrastructure |
| Local RAG + regex redaction | Default sovereign tier for no-key assessment demo | Free |
| Qwen via Ollama | Optional local model tier for future local summarization/redaction experiments | Free/local hardware |
| Python 3.11+ | Orchestrator, RAG store, mock engine, sample outputs | Free |
| FastAPI + Uvicorn | Optional backend wrapper for the orchestrator | Free |
| HTML/CSS/JS | Landing page and browser demo with no build step | Free |

## Intended vs. Implemented Path

- **Intended primary model from the reference idea:** Kimi for agentic reasoning.
- **Implemented default path:** deterministic local mock engine plus local RAG so
  reviewers can run everything with no paid tool.
- **Optional live path:** `python orchestrator.py --live --redact --yes` calls
  the Kimi-compatible client for stages 2 and 3 when `KIMI_API_KEY` is set.
- **Optional local model path:** `agent/local_qwen.py` includes a Qwen/Ollama
  helper. The default demo does not require Ollama.

## Research Prompts

1. Review Elchai Group's public services and identify a relevant workflow.
2. Compare Kimi, Qwen, MiniMax, GLM, and an OpenClaw-style gateway for regulated
   GCC enterprise work.
3. Decide which workflow can be demonstrated safely without real client data.
4. Design a small output that is more practical than a static report.
5. Identify risks: privacy, security, accuracy, hallucination, hardware cost,
   integration difficulty, reliability, and vendor/procurement concerns.

## Agent System Prompts

Prompt files are in `agent/prompts/`:

| File | Stage | Rules |
|---|---|---|
| `sovereign_guard.txt` | SovereignGuard | RAG-only facts; cite chunk ids; escalate missing facts; not legal advice |
| `jurisdiction_mapper.txt` | JurisdictionMapper | Map to compliance chunks; review-required flags only |
| `protocol_architect.txt` | ProtocolArchitect | ERC-3643/ERC-1400 outline only; no production Solidity; cite sources |

Legacy Discovery Compass prompts remain in the repo but are not used by the
current Oasis Tower orchestrator.

## Commands To Reproduce

```bash
# Primary sample output, no key required
cd agent
python orchestrator.py --brief sample_briefs/oasis_tower_rwa.json --yes

# Windows fallback if python is not on PATH
py -3 orchestrator.py --brief sample_briefs/oasis_tower_rwa.json --yes

# Live Kimi-compatible path, requires API key and dependencies
set KIMI_API_KEY=sk-...
python orchestrator.py --brief sample_briefs/oasis_tower_rwa.json --live --redact --yes \
  --out sample_outputs/oasis_tower_rwa.live.json

# Landing page locally
python -m http.server 8123 --directory web

# Optional FastAPI backend
cd server
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

## OpenClaw Skill

`openclaw/skills/oasis-tower-rwa-pipeline.md` describes the same four-stage
workflow for gateway-style deployment. Config:
`openclaw/openclaw.example.json`.
