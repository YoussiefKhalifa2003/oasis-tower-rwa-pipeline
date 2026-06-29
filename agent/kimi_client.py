"""Thin wrapper around a Kimi-compatible model via Moonshot's OpenAI-compatible API.

Kimi exposes an OpenAI-compatible endpoint, so we reuse the official `openai`
client and only change the base URL and API key. See:
https://platform.moonshot.ai

Environment variables:
    KIMI_API_KEY    Your Moonshot API key (required for live mode).
    KIMI_BASE_URL   Defaults to https://api.moonshot.ai/v1
    KIMI_MODEL      Defaults to kimi-k2.5  (set to a model your account can access)
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass


DEFAULT_BASE_URL = "https://api.moonshot.ai/v1"
DEFAULT_MODEL = "kimi-k2.5"


@dataclass
class KimiResponse:
    text: str
    model: str
    usage: dict


class KimiClient:
    """Calls Kimi and returns parsed JSON, with simple retries.

    The agents in this project always ask the model for JSON, so this client
    enforces JSON output and gives a clear error if the model returns junk.
    """

    def __init__(self, api_key: str | None = None, base_url: str | None = None,
                 model: str | None = None):
        # Imported lazily so the project still runs in mock mode with no deps.
        from openai import OpenAI

        self.api_key = api_key or os.environ.get("KIMI_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "KIMI_API_KEY is not set. Run in mock mode (no --live flag) or "
                "export your Moonshot key first."
            )
        self.model = model or os.environ.get("KIMI_MODEL", DEFAULT_MODEL)
        self._client = OpenAI(
            api_key=self.api_key,
            base_url=base_url or os.environ.get("KIMI_BASE_URL", DEFAULT_BASE_URL),
        )

    def complete_json(self, system_prompt: str, user_content: str,
                      temperature: float = 0.3, max_retries: int = 3) -> dict:
        """Send one system+user turn and parse the reply as JSON."""
        last_error: Exception | None = None
        for attempt in range(1, max_retries + 1):
            try:
                resp = self._client.chat.completions.create(
                    model=self.model,
                    temperature=temperature,
                    response_format={"type": "json_object"},
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_content},
                    ],
                )
                raw = resp.choices[0].message.content or "{}"
                return json.loads(raw)
            except json.JSONDecodeError as exc:
                last_error = exc
            except Exception as exc:  # network / rate-limit / transient
                last_error = exc
                time.sleep(min(2 ** attempt, 8))
        raise RuntimeError(f"Kimi call failed after {max_retries} attempts: {last_error}")
