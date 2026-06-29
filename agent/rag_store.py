"""Minimal RAG retrieval for the Oasis Tower POC.

No vector DB required: keyword overlap over committed JSON chunks keeps the
demo reproducible offline. Live mode can swap in embeddings later; the interface
stays the same.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

CORPUS_DIR = Path(__file__).resolve().parent / "rag_corpus"


def _load_chunks(filename: str) -> list[dict]:
    data = json.loads((CORPUS_DIR / filename).read_text(encoding="utf-8"))
    return data.get("chunks", [])


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def retrieve(query: str, corpus_file: str, top_k: int = 4) -> list[dict]:
    """Return top_k chunks by simple token overlap score."""
    q = _tokens(query)
    if not q:
        return []
    scored: list[tuple[float, dict]] = []
    for chunk in _load_chunks(corpus_file):
        text = chunk.get("text", "")
        t = _tokens(text)
        if not t:
            continue
        score = len(q & t) / len(q | t)
        if score > 0:
            scored.append((score, chunk))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [c for _, c in scored[:top_k]]


def format_citations(chunks: list[dict]) -> list[dict]:
    return [{"id": c["id"], "section": c.get("section", c.get("jurisdiction", "")), "excerpt": c["text"][:220]} for c in chunks]
