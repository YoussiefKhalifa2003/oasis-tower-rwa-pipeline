# Oasis Tower RWA Pipeline

**Elchai Group Pre-Interview Assessment**  
**Candidate:** Youssief Khalifa  
**Role:** AI Agent & OpenClaw Research Intern  
**Selected model/tool:** Kimi-compatible agentic layer + OpenClaw-style orchestration + local/Qwen-ready sovereign tier

A practical research POC for **fractional real estate tokenization** using a
fictional Oasis Tower brief. The project shows how an open-source/open-weight
model workflow could support Elchai-style RWA, AI agent, RAG, and smart contract
delivery while keeping sensitive data and production decisions under control.

Start with [SUBMISSION.md](SUBMISSION.md) for the assessor-facing answer. Use
[DETAILED_REPORT.md](DETAILED_REPORT.md) for the deeper discussion of the model
matrix, architecture, risks, and recommendation. This README is the technical tour.

## What It Does

Four pipeline stages with an OpenClaw-style human gate:

1. **SovereignGuard** - local RAG and redaction; escalates facts not in the source corpus.
2. **JurisdictionMapper** - Kimi-compatible live path for VARA/ADGM/PDPL-style review flags.
3. **ProtocolArchitect** - Kimi-compatible live path for an ERC-3643/ERC-1400 architecture outline.
4. **GovernanceManifest** - deterministic halt and JSON manifest for human sign-off.

The default mode is free and offline. It uses deterministic local logic so a
reviewer can run the project with no API key, no paid account, and no GPU.

## Run The Pipeline

```bash
cd agent
python orchestrator.py --brief sample_briefs/oasis_tower_rwa.json --yes
```

If `python` is not on PATH on Windows:

```bash
cd agent
py -3 orchestrator.py --brief sample_briefs/oasis_tower_rwa.json --yes
```

Output is saved to:

```text
agent/sample_outputs/oasis_tower_rwa.output.json
```

## Run The Landing Page

```bash
serve_web.cmd
```

Then visit:

```text
http://localhost:8123
```

The landing page includes:

- Interactive browser demo at the top
- Required landing page elements: headline, subheadline, problem, solution,
  three benefits, use case, CTA, and layout
- Pipeline stages and model comparison matrix
- Architecture, risks, and recommendation
- Bilingual English/Arabic UI
- JSON governance manifest download

## Optional Live Kimi Path

Live mode requires a Moonshot/Kimi-compatible API key and the `openai` Python
package from `agent/requirements.txt`.

```bash
cd agent
pip install -r requirements.txt
set KIMI_API_KEY=sk-...
python orchestrator.py --brief sample_briefs/oasis_tower_rwa.json --live --redact --yes
```

Set `KIMI_MODEL` if your account uses a different Kimi model name:

```bash
set KIMI_MODEL=your-available-kimi-model
```

## Quick Scripts

PowerShell may block `.ps1` files on some Windows machines. The `.cmd` scripts
are the safest reviewer path:

```cmd
serve_web.cmd              REM landing page at http://localhost:8123
agent\run_demo.cmd         REM offline pipeline + sample output
agent\run_live.cmd         REM live Kimi path, requires KIMI_API_KEY
```

## Repository Map

```text
ElChai_Assignment/
|-- SUBMISSION.md
|-- DETAILED_REPORT.md
|-- README.md
|-- serve_web.cmd
|-- agent/
|   |-- orchestrator.py
|   |-- brief_parser.py
|   |-- rwa_mock.py
|   |-- rag_store.py
|   |-- local_qwen.py
|   |-- kimi_client.py
|   |-- prompts/
|   |-- rag_corpus/
|   |-- sample_briefs/
|   `-- sample_outputs/
|-- openclaw/
|   |-- openclaw.example.json
|   `-- skills/
|-- web/
|   |-- index.html
|   |-- styles.css
|   |-- app.js
|   |-- engine.js
|   `-- i18n.js
|-- docs/
|   |-- architecture.md
|   |-- risks-and-recommendation.md
|   `-- prompts-and-tools-log.md
`-- demo/
    `-- README.md
```

## Honesty Notes

- All client names, asset facts, and corpus text are fictional.
- Compliance output is review-required analysis, never legal advice.
- No production Solidity is generated.
- Qwen/Ollama is the intended local model option; the default assessment demo
  stays offline with local RAG and regex redaction for reproducibility.
- OpenClaw is used as the documented orchestration/gateway concept; the working
  POC is implemented in Python and mirrored in browser JavaScript.
