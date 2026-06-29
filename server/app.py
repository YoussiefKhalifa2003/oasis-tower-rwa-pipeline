from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

AGENT_DIR = Path(__file__).resolve().parent.parent / "agent"
sys.path.insert(0, str(AGENT_DIR))

import orchestrator  # noqa: E402

app = FastAPI(title="Oasis Tower RWA Pipeline API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

OASIS_BRIEF = AGENT_DIR / "sample_briefs" / "oasis_tower_rwa.json"


class CustomBrief(BaseModel):
    raw_request: str = Field(..., min_length=20)
    client_name: str = "Custom brief"
    project_title: str = "Custom RWA brief"
    stated_constraints: list[str] = Field(default_factory=list)
    known_systems: list[str] = Field(default_factory=lambda: ["Custodial wallet", "KYC provider"])


def _load_oasis() -> dict[str, Any]:
    return json.loads(OASIS_BRIEF.read_text(encoding="utf-8"))


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "pipeline": "oasis-tower-rwa-rag"}


@app.get("/run")
def run_get(live: bool = False, redact: bool = False) -> dict[str, Any]:
    brief = _load_oasis()
    return orchestrator.run_pipeline(brief, live=live, auto_approve=True, redact=redact)


@app.post("/run")
def run_post(body: CustomBrief, live: bool = False, redact: bool = False) -> dict[str, Any]:
    brief = body.model_dump()
    return orchestrator.run_pipeline(brief, live=live, auto_approve=True, redact=redact)
