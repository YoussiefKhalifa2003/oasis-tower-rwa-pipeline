# Oasis Tower RWA Pipeline

RAG-driven POC for fractional real estate tokenization (fictional Oasis Tower brief).
Four stages with an OpenClaw-style human gate:

1. **SovereignGuard** — local RAG + redaction
2. **JurisdictionMapper** — VARA/ADGM/PDPL review flags
3. **ProtocolArchitect** — ERC-3643 architecture outline
4. **GovernanceManifest** — halt + JSON manifest

Written report: `Detailed Report_ Oasis Tower RWA Pipeline.pdf`

## Run the pipeline

```bash
cd agent
python orchestrator.py --brief sample_briefs/oasis_tower_rwa.json --yes
```

Output: `agent/sample_outputs/oasis_tower_rwa.output.json`

## Landing page

```cmd
serve_web.cmd
```

Open `http://localhost:8123`

## Live Kimi path (optional)

```bash
cd agent
pip install -r requirements.txt
set KIMI_API_KEY=sk-...
python orchestrator.py --brief sample_briefs/oasis_tower_rwa.json --live --redact --yes
```

## Layout

```text
ElChai_Assignment/
|-- README.md
|-- Detailed Report_ Oasis Tower RWA Pipeline.pdf
|-- serve_web.cmd
|-- agent/
|-- openclaw/
|-- web/
|-- docs/
`-- server/
```

All client names and corpus text are fictional. Compliance output is review flags only, not legal advice.
