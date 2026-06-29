"""Oasis Tower RWA RAG pipeline - OpenClaw-style multi-agent POC.

Pipeline (80% automated draft / 20% human control pattern):
    1. SovereignGuard      - local tier: RAG ingest, PII strip, escalate if not in doc
    2. JurisdictionMapper  - Kimi via OpenClaw routing: VARA/ADGM compliance mapping
    3. ProtocolArchitect   - Kimi: ERC-3643 / ERC-1400 architecture outline (no Solidity)
    --- OPENCLAW GOVERNANCE GATE ---
    4. GovernanceManifest  - deterministic halt + JSON manifest for human sign-off

Run modes:
    Mock (default)  - offline, reproducible via rwa_mock.py + rag_store.py
    Live (--live)   - configured Kimi-compatible model for stages 2-3

Examples:
    python orchestrator.py --brief sample_briefs/oasis_tower_rwa.json --yes
    python orchestrator.py --brief sample_briefs/oasis_tower_rwa.json --live --redact --yes
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import time
from pathlib import Path

from local_qwen import redact_locally
from rag_store import format_citations, retrieve
import rwa_mock

STAGES = [
    ("SovereignGuard", "sovereign_guard.txt", "sovereign_guard", "local"),
    ("JurisdictionMapper", "jurisdiction_mapper.txt", "jurisdiction_map", "kimi"),
    ("ProtocolArchitect", "protocol_architect.txt", "protocol_outline", "kimi"),
    ("GovernanceManifest", None, "governance_manifest", "deterministic"),
]

HERE = Path(__file__).resolve().parent
PROMPTS_DIR = HERE / "prompts"


def load_prompt(filename: str) -> str:
    return (PROMPTS_DIR / filename).read_text(encoding="utf-8")


def banner(text: str) -> None:
    print(f"\n\033[1m{text}\033[0m")


def build_user_content(brief: dict, prior: dict, stage_key: str) -> str:
    parts = [f"CLIENT BRIEF:\n{json.dumps(brief, indent=2)}"]
    if prior:
        parts.append(f"\nPRIOR STAGES:\n{json.dumps(prior, indent=2)}")

    if stage_key == "sovereign_guard":
        memo = retrieve(brief.get("raw_request", ""), "oasis_tower_memo.json", top_k=5)
        parts.append(f"\nRAG CHUNKS (offering memorandum):\n{json.dumps(format_citations(memo), indent=2)}")
    elif stage_key in ("jurisdiction_map", "protocol_outline"):
        comp = retrieve(
            brief.get("raw_request", "") + " VARA ADGM KYC escrow transfer",
            "compliance_modules.json",
            top_k=4,
        )
        parts.append(f"\nRAG CHUNKS (compliance reference):\n{json.dumps(format_citations(comp), indent=2)}")
    return "\n".join(parts)


def _openclaw_gate(results: dict, auto_approve: bool) -> None:
    banner("OPENCLAW GOVERNANCE GATE (20% human control)")
    print("[OpenClaw Gate: Awaiting authorized human sign-off before staging protocol generation]")
    escalations = results.get("sovereign_guard", {}).get("escalation_items", [])
    if escalations:
        print("  Escalations from sovereign tier:")
        for item in escalations:
            print(f"    - {item.get('question')} ({item.get('reason')})")
    high = [
        m["topic"]
        for m in results.get("jurisdiction_map", {}).get("mapped_requirements", [])
        if m.get("severity") == "high"
    ]
    if high:
        print(f"  High-severity compliance topics: {', '.join(high)}")
    if auto_approve:
        print("  --yes supplied: auto-approving for this demo run.")
        return
    answer = input("  Authorize governance manifest compilation? [y/N] ").strip().lower()
    if answer not in ("y", "yes"):
        print("Pipeline halted at OpenClaw gate. No manifest generated.")
        sys.exit(0)


def run_pipeline(brief: dict, live: bool, auto_approve: bool, redact: bool) -> dict:
    results: dict = {}
    timings: dict = {}

    client = None
    if live:
        from kimi_client import KimiClient
        client = KimiClient()

    working_brief = dict(brief)
    if redact or not live:
        banner("Stage 0: Local sovereign tier (Qwen/Ollama optional + regex redaction before external calls)")
        working_brief["raw_request"] = redact_locally(brief.get("raw_request", ""))
        print(working_brief["raw_request"])

    for name, prompt_file, key, tier in STAGES:
        if key == "governance_manifest":
            _openclaw_gate(results, auto_approve)

        banner(f"[{name}] running ({tier}{' · Kimi-compatible live' if live and tier == 'kimi' else ''})...")
        start = time.time()

        if tier == "deterministic":
            output = rwa_mock.run_stage(key, working_brief, results)
        elif live and tier == "kimi":
            system_prompt = load_prompt(prompt_file)
            user_content = build_user_content(working_brief, results, key)
            output = client.complete_json(system_prompt, user_content)
        elif live and tier == "local":
            # Keep sensitive ingest local in live mode too. Kimi is used only for
            # the agentic reasoning stages after redaction/RAG.
            output = rwa_mock.run_stage(key, working_brief, results)
        else:
            output = rwa_mock.run_stage(key, working_brief, results)
            time.sleep(0.25)

        timings[key] = round(time.time() - start, 2)
        results[key] = output
        print(json.dumps(output, indent=2, ensure_ascii=False))

    return {
        "meta": {
            "brief_id": brief.get("brief_id"),
            "project_title": brief.get("project_title", brief.get("client_name")),
            "client_name": brief.get("client_name"),
            "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
            "mode": "live-kimi-k2.5" if live else "mock-rag-pipeline",
            "model": os.environ.get("KIMI_MODEL", "kimi-k2.5") if live else "rwa-mock-engine",
            "local_redaction": redact or not live,
            "pipeline": "oasis-tower-rwa-rag",
            "step_timings_seconds": timings,
        },
        "steps": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Oasis Tower RWA RAG pipeline")
    parser.add_argument("--brief", required=True, help="Path to a brief JSON file")
    parser.add_argument("--live", action="store_true", help="Call configured Kimi-compatible model for Kimi stages")
    parser.add_argument("--yes", action="store_true", help="Auto-approve the OpenClaw gate")
    parser.add_argument("--redact", action="store_true", help="Run local redaction before external calls")
    parser.add_argument("--out", help="Where to write the full result JSON")
    args = parser.parse_args()

    brief_path = Path(args.brief)
    if not brief_path.is_absolute():
        brief_path = HERE / brief_path
    brief = json.loads(brief_path.read_text(encoding="utf-8"))

    result = run_pipeline(brief, args.live, args.yes, args.redact)

    if args.out:
        out_path = Path(args.out)
        if not out_path.is_absolute():
            out_path = HERE / out_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
        banner(f"Saved RWA manifest to {out_path}")
    elif not args.out:
        default_out = HERE / "sample_outputs" / "oasis_tower_rwa.output.json"
        default_out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
