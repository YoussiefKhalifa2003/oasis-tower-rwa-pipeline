# OpenClaw Integration

The Python orchestrator (`../agent/orchestrator.py`) is the working POC. OpenClaw is
the production path to expose the same pipeline in Slack, WhatsApp, Teams, or WebChat.

Docs: https://docs.openclaw.ai · Repo: https://github.com/openclaw/openclaw

## Setup

```bash
pnpm add -g openclaw@latest
export KIMI_API_KEY=sk-...
openclaw onboard
```

```bash
cp openclaw.example.json ~/.openclaw/openclaw.json
mkdir -p ~/.openclaw/skills
cp skills/oasis-tower-rwa-pipeline.md ~/.openclaw/skills/
openclaw security audit
```

## Files

| File | Purpose |
|------|---------|
| `openclaw.example.json` | Gateway config |
| `skills/oasis-tower-rwa-pipeline.md` | Four-stage RWA skill |

Example config sets `security: "ask"`. Run `openclaw security audit` before real use.
