# OpenClaw Integration (Production Deployment Path)

The role is *AI Agent & OpenClaw Research Intern*, and the reference video notes
Kimi is "perfect for reuse inside OpenClaw." The Oasis Tower RWA Pipeline runs in
two ways:

- **Python orchestrator** (`../agent/orchestrator.py`): working POC for this submission.
- **OpenClaw gateway**: production path to expose the same staged pipeline in
  Slack, WhatsApp, Teams, or WebChat.

## What OpenClaw is

Open-source (MIT) agent gateway. Model-agnostic: bring a Kimi-compatible API
model for agentic stages and optional Qwen/Ollama for local stages. Repo:
https://github.com/openclaw/openclaw - Docs: https://docs.openclaw.ai

OpenClaw is **not** Elchai's product. It is the orchestration framework named in
the job title, used here as the documented team deployment path.

## Setup on Windows (WSL2 recommended)

```bash
pnpm add -g openclaw@latest
export KIMI_API_KEY=sk-...
openclaw onboard
```

Copy this project's config and skill:

```bash
cp openclaw.example.json ~/.openclaw/openclaw.json
mkdir -p ~/.openclaw/skills
cp skills/oasis-tower-rwa-pipeline.md ~/.openclaw/skills/
openclaw security audit
```

## Files

| File | Purpose |
|------|---------|
| `openclaw.example.json` | Gateway: Kimi-compatible agentic tier + optional Qwen local tier, `security: ask` |
| `skills/oasis-tower-rwa-pipeline.md` | Four-stage RWA skill with governance gate |
| `skills/discovery-brief-analysis.md` | Legacy Discovery Compass skill (archived) |

## Security

Example config sets `security: "ask"`, `ask: "on"`, and empty
`tools.elevated.allowFrom`. Run `openclaw security audit` before any real use.
