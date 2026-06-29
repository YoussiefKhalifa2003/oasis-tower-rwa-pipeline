from __future__ import annotations

import json
import os
import re
import urllib.request

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/generate")
QWEN_MODEL = os.environ.get("QWEN_MODEL", "qwen2.5:7b")

_PATTERNS = {
    "email": re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    "phone": re.compile(r"\+?\d[\d\s().-]{7,}\d"),
    "money": re.compile(r"(?:AED|USD|SAR|\$)\s?[\d,.]+\s?(?:billion|million|m|bn)?", re.I),
}


def redact_locally(text: str) -> str:
    redacted = text
    redacted = _PATTERNS["email"].sub("[REDACTED_EMAIL]", redacted)
    redacted = _PATTERNS["phone"].sub("[REDACTED_PHONE]", redacted)
    redacted = _PATTERNS["money"].sub("[REDACTED_AMOUNT]", redacted)
    return redacted


def summarize_with_qwen(text: str, timeout: int = 60) -> str:
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
