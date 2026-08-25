"""Config-aware local-first provider router.

Priority chain:
  1. Local rules engine  (fastest, no API calls)
  2. OpenRouter          (smart model selection via openrouter.ai)
  3. Groq                (legacy fallback if OpenRouter key is missing)
"""

from __future__ import annotations

import os
from dataclasses import replace
from pathlib import Path
from typing import Any

from open_jarvis.config.manager import ConfigManager
from open_jarvis.memory import build_context_prompt
from open_jarvis.memory.memory_store import MEMORY_FILE
from open_jarvis.providers.base import ProviderRequest, ProviderResponse
from open_jarvis.providers.groq import GroqProvider
from open_jarvis.providers.openrouter import OpenRouterProvider
from open_jarvis.providers.local import LocalProvider


class ProviderRouter:
    """Route commands through local rules before optional cloud fallback."""

    def __init__(
        self,
        *,
        config_manager: ConfigManager | None = None,
        local_provider: Any | None = None,
        cloud_provider: Any | None = None,
        memory_path: str | Path = MEMORY_FILE,
    ) -> None:
        self.config_manager = config_manager or ConfigManager()
        self.local_provider = local_provider
        self.cloud_provider = cloud_provider
        self.memory_path = memory_path

    def route(self, command: str) -> ProviderResponse:
        self.config_manager.load()
        local = self.local_provider or LocalProvider(
            enabled=bool(self.config_manager.get("ai.local_provider_enabled", True))
        )
        try:
            local_response = local.analyze(
                ProviderRequest(command=command, allow_cloud=False, allow_memory_context=False)
            )
        except (RuntimeError, ValueError, TypeError, AttributeError, OSError):
            local_response = ProviderResponse(
                provider=str(getattr(local, "name", "local")),
                status="error",
                error="local_provider_error",
            )
        if local_response.ok:
            return local_response

        if not self._cloud_allowed():
            return ProviderResponse(
                provider="local",
                status="unsupported",
                error=local_response.error or "Local provider could not route this command.",
            )

        request = ProviderRequest(
            command=command,
            context=self._memory_context(),
            allow_cloud=True,
            allow_memory_context=True,
            metadata={"fallback_from": local_response.provider},
        )
        cloud = self.cloud_provider or self._best_cloud_provider()
        try:
            response = cloud.analyze(request)
        except (RuntimeError, ValueError, TypeError, AttributeError, OSError):
            return ProviderResponse(
                provider=str(getattr(cloud, "name", "cloud")),
                status="error",
                error="provider_error",
                fallback_used=True,
            )
        if isinstance(response, ProviderResponse):
            return replace(response, fallback_used=True)
        response.fallback_used = True
        return response

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _cloud_allowed(self) -> bool:
        """Allow cloud if JARVIS_ENABLE_GROQ is set in env OR config enables it."""
        env_enabled = os.getenv("JARVIS_ENABLE_GROQ", "").strip().lower() in {"1", "true", "yes", "on"}
        env_key = bool(os.getenv("GROQ_API_KEY", "").strip())
        config_enabled = bool(self.config_manager.get("ai.cloud_fallback_enabled", False)) and bool(
            self.config_manager.get("ai.groq_enabled", False)
        )
        return (env_enabled and env_key) or config_enabled

    def _memory_context(self) -> str:
        return build_context_prompt(config_manager=self.config_manager, memory_file=self.memory_path)

    def _best_cloud_provider(self) -> OpenRouterProvider | GroqProvider:
        """Return OpenRouter if key looks like an OR key, else fall back to Groq."""
        api_key = os.getenv("GROQ_API_KEY", "")
        # OpenRouter keys start with sk-or-
        if api_key.startswith("sk-or-"):
            model = os.getenv("JARVIS_GROQ_MODEL", "")  # '' = auto-select
            return OpenRouterProvider(api_key=api_key, enabled=True, model=model)
        # Fallback: treat key as a real Groq key
        model = os.getenv("JARVIS_GROQ_MODEL", "") or str(
            self.config_manager.get("ai.groq_model", "llama-3.1-8b-instant")
        )
        return GroqProvider(
            api_key=api_key,
            enabled=True,
            model=model,
        )
