"""OpenRouter provider — routes commands to any AI model via OpenRouter API.

OpenRouter is an OpenAI-compatible gateway that gives access to hundreds of
models (Gemini, Claude, Llama, Mistral, etc.) under a single API key.  This
provider automatically picks a model that fits the task complexity:

  • simple  → google/gemini-2.5-flash  (fast, cheap)
  • complex → google/gemini-2.5-pro    (powerful)
  • fallback → meta-llama/llama-3.1-8b-instruct:free (no-cost safety net)
"""

from __future__ import annotations

import json
import time
from typing import Any

try:
    import requests as _requests
    _REQUESTS_OK = True
except ImportError:  # pragma: no cover
    _REQUESTS_OK = False

from open_jarvis.providers.base import ProviderRequest, ProviderResponse
from open_jarvis.security.jarvis_admin import format_actionable_message

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_TIMEOUT = 30  # seconds

# Model ladder — tweak freely
MODEL_FLASH   = "google/gemini-2.5-flash"
MODEL_PRO     = "google/gemini-2.5-pro"
MODEL_FREE    = "meta-llama/llama-3.1-8b-instruct:free"

# Keywords that signal a complex / long task → use the pro model
_COMPLEX_SIGNALS = {
    "analyze", "explain", "write", "code", "script", "summarize",
    "generate", "compare", "research", "describe", "calculate",
    "translate", "debug", "optimize", "design", "plan", "create",
}

# Cool-down so we don't hammer the API after an error
_OPENROUTER_COOLDOWN_SECONDS = 60
_openrouter_cooldown_until = 0.0


def is_openrouter_cooling_down(now: float | None = None) -> bool:
    return (time.time() if now is None else now) < _openrouter_cooldown_until


def activate_openrouter_cooldown(seconds: int = _OPENROUTER_COOLDOWN_SECONDS, now: float | None = None) -> None:
    global _openrouter_cooldown_until
    _openrouter_cooldown_until = (time.time() if now is None else now) + max(1, seconds)


def _pick_model(command: str) -> str:
    words = set(command.lower().split())
    if words & _COMPLEX_SIGNALS or len(command) > 180:
        return MODEL_PRO
    return MODEL_FLASH


def _safe_error(text: str) -> str:
    t = str(text).lower()
    if "rate" in t or "quota" in t or "429" in t or "limit" in t:
        return "rate_limited"
    if "auth" in t or "key" in t or "unauthorized" in t or "403" in t or "401" in t:
        return "provider_auth_failed"
    return "provider_error"


def _extract_json(text: str) -> dict[str, Any]:
    value = (text or "").strip()
    if "```" in value:
        chunks = value.split("```")
        value = next(
            (c[4:].strip() if c.startswith("json") else c.strip() for c in chunks if "{" in c),
            value,
        )
    start = value.find("{")
    end = value.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("No JSON object in OpenRouter response")
    return json.loads(value[start : end + 1])


class OpenRouterProvider:
    """Route commands through OpenRouter with smart model selection."""

    name = "openrouter"

    def __init__(
        self,
        *,
        api_key: str | None = None,
        enabled: bool = True,
        model: str = "",          # "" = auto-select per request
        system_prompt: str = "",
    ) -> None:
        self.api_key = (api_key or "").strip()
        self.enabled = enabled
        self.forced_model = model.strip()  # if set, always use this model
        self.system_prompt = system_prompt

    def _call(self, command: str, context: str = "") -> tuple[str, str]:
        """POST to OpenRouter and return (raw_text, model_used)."""
        model = self.forced_model or _pick_model(command)
        system = f"{context}\n\n{self.system_prompt}" if context else self.system_prompt
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": command},
            ],
            "temperature": 0.1,
            "max_tokens": 600,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/open-jarvis",
            "X-Title": "JANCOK Assistant",
        }
        resp = _requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=OPENROUTER_TIMEOUT)
        if resp.status_code == 429:
            raise RuntimeError("rate_limited: 429 from OpenRouter")
        if resp.status_code in {401, 403}:
            raise RuntimeError(f"provider_auth_failed: HTTP {resp.status_code}")
        resp.raise_for_status()
        data = resp.json()
        text = data["choices"][0]["message"]["content"]
        return text, model

    def analyze(self, request: ProviderRequest) -> ProviderResponse:
        if not request.allow_cloud:
            return ProviderResponse(provider=self.name, status="unavailable", error="Cloud disabled.")
        if not self.enabled:
            return ProviderResponse(provider=self.name, status="unavailable", error="OpenRouter provider disabled.")
        if not self.api_key:
            return ProviderResponse(provider=self.name, status="unavailable", error="OpenRouter API key missing.")
        if not _REQUESTS_OK:
            return ProviderResponse(provider=self.name, status="unavailable", error="requests library not installed.")
        if is_openrouter_cooling_down():
            return ProviderResponse(provider=self.name, status="error", error="rate_limited", action=_rate_limit_action())

        started = time.perf_counter()
        try:
            text, model = self._call(request.command, request.context or "")
            action = _extract_json(text)
            return ProviderResponse(
                provider=f"{self.name}:{model}",
                status="success",
                action=action,
                latency_ms=(time.perf_counter() - started) * 1000,
            )
        except (RuntimeError, OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
            err = _safe_error(str(exc))
            if err == "rate_limited":
                activate_openrouter_cooldown()
                return ProviderResponse(provider=self.name, status="error", error=err, action=_rate_limit_action())
            return ProviderResponse(provider=self.name, status="error", error=err)

    def summarize(self, text: str) -> ProviderResponse:
        if not self.enabled or not self.api_key or not _REQUESTS_OK:
            return ProviderResponse(provider=self.name, status="unavailable", error="OpenRouter unavailable.")
        try:
            content, _ = self._call(f"Summarize this in 3-4 sentences:\n\n{text[:4000]}")
            return ProviderResponse(provider=self.name, status="success", text=content.strip())
        except (RuntimeError, OSError, ValueError, KeyError) as exc:
            return ProviderResponse(provider=self.name, status="error", error=_safe_error(str(exc)))


def _rate_limit_action() -> dict[str, Any]:
    return {
        "action": "talk",
        "params": {},
        "response": format_actionable_message(
            "Cloud AI is temporarily rate-limited, sir.",
            "OpenRouter is cooling down after hitting the request limit.",
            "I will handle simple commands locally and retry the cloud shortly.",
        ),
    }
