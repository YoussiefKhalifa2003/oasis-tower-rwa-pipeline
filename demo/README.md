# Demo Video: Recording Guide

Record a short walkthrough after the landing page and terminal demo are working.
You can upload it to Loom, YouTube unlisted, Google Drive, or include the file in
your final submission package.

**Target length:** 90 seconds. Record it as an internal engineering demo, not a
slide presentation.

## Pre-flight

1. Start the landing page:

   ```cmd
   serve_web.cmd
   ```

2. Open `http://localhost:8123`.
3. Run the terminal pipeline once before recording so output is warm:

   ```cmd
   cd agent
   python orchestrator.py --brief sample_briefs/oasis_tower_rwa.json --yes
   ```

   If `python` is not available:

   ```cmd
   py -3 orchestrator.py --brief sample_briefs/oasis_tower_rwa.json --yes
   ```

4. Close unrelated tabs and notifications.

## Shot List

### 0:00-0:15 - Frame the project

Say:

> This is my Elchai assessment POC: Oasis Tower, a RAG-driven RWA tokenization
> pipeline. It uses a Kimi-compatible agentic tier, a local sovereign RAG and
> redaction tier, and an OpenClaw-style governance gate before anything reaches
> blockchain implementation.

### 0:15-0:45 - Run the Python pipeline

Show:

```cmd
cd agent
python orchestrator.py --brief sample_briefs/oasis_tower_rwa.json --yes
```

Narrate:

- SovereignGuard extracts source-grounded asset facts and escalation items.
- JurisdictionMapper maps review-required VARA/ADGM/PDPL-style topics.
- ProtocolArchitect drafts an ERC-3643/ERC-1400 architecture outline.
- The OpenClaw-style gate stops the workflow for human sign-off.

Pause briefly on:

```text
[OpenClaw Gate: Awaiting authorized human sign-off before staging protocol generation]
```

### 0:45-1:10 - Browser demo

Switch to the landing page and click **Run RWA pipeline**.

Point out:

- telemetry: status, step, tokens, estimated cost
- a `memo-002` or `vara-001` citation
- the governance manifest download button

### 1:10-1:30 - Close with recommendation

Show `openclaw/openclaw.example.json` or the risk section.

Say:

> My recommendation is limited internal testing with guardrails. Keep sensitive
> documents local first, use an approved agentic model only after redaction, and
> require a human gate before client delivery or smart contract implementation.

## Submission Reminder

When sending the final email, include the live landing page URL, repository URL,
and walkthrough video URL in the email body. The repository itself is already
complete and runnable locally.
