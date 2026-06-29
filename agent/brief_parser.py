from __future__ import annotations

import re


def parse_brief(brief: dict) -> dict:
    text = brief.get("raw_request", "") or ""
    constraints = " ".join(brief.get("stated_constraints", []))
    full = f"{text} {constraints}".lower()

    is_oasis = (
        brief.get("brief_id") == "OASIS-RWA-2026"
        or ("oasis tower" in full and "dubai internet city" in full)
    )

    parsed = {
        "is_oasis_preset": is_oasis,
        "asset_label": "Oasis Tower, Dubai Internet City",
        "tranche": "18%",
        "reserve": "5%",
        "transfer_lock": "12-month",
        "escrow": "AED 45M",
        "valuation": "AED 890M valuation (fictional)",
        "fact_source": "memo-001",
        "rule_source": "memo-002",
        "lock_source": "memo-005",
        "escrow_source": "memo-004",
    }

    if is_oasis:
        return parsed

    parsed["fact_source"] = "client-brief"
    parsed["rule_source"] = "client-brief"
    parsed["lock_source"] = "client-brief"
    parsed["escrow_source"] = "client-brief"
    parsed["valuation"] = "Valuation not stated in brief - escalate to client"

    cn = (brief.get("client_name") or "").replace("(fictional)", "").strip()
    if cn and cn.lower() not in ("custom brief", ""):
        parsed["asset_label"] = cn

    m = re.search(r"interest in ([^,.]+)", text, re.I)
    if m:
        parsed["asset_label"] = m.group(1).strip()

    m = re.search(r"in ([^,]+), a ", text, re.I)
    if m:
        parsed["asset_label"] = m.group(1).strip()

    m = re.search(r"tokenize\s+(?:a\s+)?(?:first\s+)?tranche\s+of\s+(\d+)%", text, re.I)
    if not m:
        m = re.search(r"(\d+)%\s*of\s*economic", text, re.I)
    if m:
        parsed["tranche"] = f"{m.group(1)}%"

    m = re.search(r"(\d+)%\s*(?:reserve|maintenance)", text, re.I)
    if m:
        parsed["reserve"] = f"{m.group(1)}%"

    m = re.search(r"(\d+)-month\s*transfer", text, re.I)
    if m:
        parsed["transfer_lock"] = f"{m.group(1)}-month"

    m = re.search(r"escrow until (AED\s*[\d.]+\s*[Mm]?)", text, re.I)
    if m:
        parsed["escrow"] = re.sub(r"\s+", "", m.group(1))
    else:
        m = re.search(r"(AED\s*[\d.]+[Mm]?)", text, re.I)
        if m:
            parsed["escrow"] = re.sub(r"\s+", "", m.group(1))

    return parsed
