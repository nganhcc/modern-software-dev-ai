from __future__ import annotations

import os
import re
import json
from typing import Any, Dict, List
from ollama import chat
from dotenv import load_dotenv

load_dotenv()

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)

DEFAULT_OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
LLM_RESPONSE_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "action_items": {
            "type": "array",
            "items": {"type": "string"},
        }
    },
    "required": ["action_items"],
}


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    return _dedupe_preserve_order(extracted)


def extract_action_items_llm(text: str) -> List[str]:
    result = extract_action_items_llm_with_meta(text)
    return result["items"]


def extract_action_items_llm_with_meta(text: str) -> Dict[str, Any]:
    raw_text = text.strip()
    if not raw_text:
        return {
            "items": [],
            "extraction_method": "rules",
            "fallback_reason": "empty input",
        }

    prompt = (
        "Extract only actionable tasks from the input text. "
        "Return concise action items with no numbering or bullets. "
        "Ignore narrative lines that are not actions."
    )

    fallback_reason: str | None = None
    try:
        response = chat(
            model=DEFAULT_OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": raw_text},
            ],
            format=LLM_RESPONSE_SCHEMA,
            options={"temperature": 0},
        )

        response_content = str(response.get("message", {}).get("content", "")).strip()
        parsed = json.loads(response_content)
        llm_items = parsed.get("action_items", []) if isinstance(parsed, dict) else []
        if not isinstance(llm_items, list):
            llm_items = []

        normalized = _normalize_extracted_items(llm_items)
        if normalized:
            return {
                "items": normalized,
                "extraction_method": "llm",
                "fallback_reason": None,
            }
        fallback_reason = "llm returned no usable action items"
    except Exception as exc:  # pragma: no cover - exercised with mocks in tests
        fallback_reason = f"llm extraction failed: {exc}"

    return {
        "items": extract_action_items(raw_text),
        "extraction_method": "rules",
        "fallback_reason": fallback_reason,
    }


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters


def _normalize_extracted_items(items: List[Any]) -> List[str]:
    cleaned_items: List[str] = []
    for item in items:
        if not isinstance(item, str):
            continue
        cleaned = item.strip()
        if not cleaned:
            continue
        cleaned = BULLET_PREFIX_PATTERN.sub("", cleaned)
        cleaned = cleaned.removeprefix("[ ]").strip()
        cleaned = cleaned.removeprefix("[todo]").strip()
        if cleaned:
            cleaned_items.append(cleaned)
    return _dedupe_preserve_order(cleaned_items)


def _dedupe_preserve_order(items: List[str]) -> List[str]:
    seen: set[str] = set()
    unique: List[str] = []
    for item in items:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique
