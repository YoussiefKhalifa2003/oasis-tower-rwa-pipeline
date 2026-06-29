"""Optional local 'sovereign' tier: Qwen running through Ollama.

This is the privacy-first helper described in the plan. Before any brief is sent
to an external API, RedactionHelper can run locally on approved on-prem or
developer hardware to strip or mask obvious personal / sensitive details.
Nothing here leaves the machine.

Requires Ollama (https://ollama.com) with a Qwen model pulled, e.g.:
    ollama pull qwen2.5:7b
"""

from __future__ import annotations

import json
import os
import re
import urllib.request


OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
QWEN_MODEL = os.environ.get("QWEN_MODEL", "qwen2.5:7b")

# Lightweight local regexes so redaction also works with no model running.
_PATTERNS = {
    "email": re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    "phone": re.compile(r"\+?\d[\d\s().-]{7,}\d"),
    "money": re.compile(r"(?:AED|USD|SAR|\$)\s?[\d,.]+\s?(?:billion|million|m|bn)?", re.I),
}


def redact_locally(text: str) -> str:
    """Mask obvious identifiers using local regexes only (no network)."""
    redacted = text
    redacted = _PATTERNS["email"].sub("[REDACTED_EMAIL]", redacted)
    redacted = _PATTERNS["phone"].sub("[REDACTED_PHONE]", redacted)
    redacted = _PATTERNS["money"].sub("[REDACTED_AMOUNT]", redacted)
    return redacted


def summarize_with_qwen(text: str, timeout: int = 60) -> str:
    """Ask a locally hosted Qwen model to summarize text. Falls back to a
    truncated copy if Ollama is not reachable, so the pipeline never hard-fails.
    """
    prompt = (
        "Summarize the following client brief in 3 plain sentences. "
        "Do not add information that is not present.\n\n" + text
    )
    payload = json.dumps({
        "model": QWEN_MODEL,
        "prompt": prompt,
        "stream": False,
    }).encode("utf-8")
    try:
        req = urllib.request.Request(OLLAMA_URL, data=payload,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("response", "").strip()
    except Exception:
        return text[:400] + ("..." if len(text) > 400 else "")
