"""Secondary cockpit pages for the JANCOK desktop UI."""

from __future__ import annotations

import os
import socket

import customtkinter as ctk
import psutil

from open_jarvis.health.observability import build_latency_snapshot, build_slo_report
from open_jarvis.integrations.llm_fallback import describe_ai_status
from open_jarvis.runtime.config_runtime import resolved_env
from open_jarvis.ui.security_center import build_security_overview
from open_jarvis.ui.ui_theme import PALETTE, font

PAGE_TITLES = {
    "dashboard": ("DASHBOARD", "Live assistant core and command stream."),
    "system": ("SYSTEM MONITOR", "CPU · RAM · Disk · Network · Microphone · Latency"),
    "modules": ("MODULES", "Desktop launchers, productivity tools, and command modules."),
    "integrations": ("INTEGRATIONS", "OpenRouter, Spotify, Gemini, Weather, and external APIs."),
    "security": ("SECURITY CENTER", "Permissions, confirmations, safe mode, and audit trail."),
    "settings": ("SETTINGS", "Theme, voice, wake word, language, and startup behavior."),
}

PAGE_ITEMS = {
    "system": ["CPU usage", "Memory usage", "Disk status", "Internet status", "Microphone status", "Latency"],
    "modules": ["Application launcher", "Spotify control", "Screenshot capture", "Clipboard reader", "Summarizer", "Mouse and keyboard control"],
    "integrations": ["OpenRouter AI", "Spotify API", "Gemini vision", "Weather service", "Offline fallback", "Local LLM endpoint"],
    "security": ["Confirmation-required commands", "Safe mode", "Dangerous action blocking", "Masked API key status", "Permission profile", "Audit events"],
    "settings": ["Theme", "Accent color", "Voice", "Wake word", "Language", "Startup behavior"],
}


def _mask_status(value: str | None) -> str:
    return "CONFIGURED" if str(value or "").strip() else "MISSING"


def _internet_status() -> str:
    try:
        socket.create_connection(("1.1.1.1", 53), timeout=0.2).close()
    except OSError:
        return "OFFLINE"
    return "ONLINE"


def build_info_page(parent, page_key: str) -> ctk.CTkFrame:
    """Build a full-screen information page with live value labels."""

    title, subtitle = PAGE_TITLES[page_key]

    # Root frame — fills the entire content area
    frame = ctk.CTkFrame(parent, fg_color=PALETTE["bg"])
    frame._value_labels = {}   # type: ignore[attr-defined]
    frame._detail_labels = {}  # type: ignore[attr-defined]
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)

    # ── Header ────────────────────────────────────────────────────────
    header = ctk.CTkFrame(frame, fg_color="transparent")
    header.grid(row=0, column=0, padx=32, pady=(32, 12), sticky="ew")

    # Page title
    ctk.CTkLabel(
        header,
        text=title,
        font=font("display", 32, "bold"),
        text_color=PALETTE["cyan"],
    ).pack(anchor="w")

    # Accent separator
    ctk.CTkFrame(header, fg_color=PALETTE["line_hot"], width=64, height=2).pack(anchor="w", pady=(8, 0))
    ctk.CTkFrame(header, fg_color=PALETTE["line"], height=1).pack(anchor="w", fill="x", pady=(1, 0))

    # Subtitle / description
    ctk.CTkLabel(
        header,
        text=subtitle,
        font=font("mono", 12),
        text_color=PALETTE["text_muted"],
    ).pack(anchor="w", pady=(10, 0))

    # ── Card grid ─────────────────────────────────────────────────────
    grid = ctk.CTkFrame(frame, fg_color="transparent")
    grid.grid(row=1, column=0, padx=32, pady=(8, 32), sticky="nsew")

    # 3-column responsive grid
    for col in range(3):
        grid.grid_columnconfigure(col, weight=1, uniform="col")
    for row in range(2):
        grid.grid_rowconfigure(row, weight=1, uniform="row")

    items = PAGE_ITEMS[page_key]
    for index, item in enumerate(items):
        col = index % 3
        row = index // 3
        card = ctk.CTkFrame(
            grid,
            fg_color=PALETTE["surface"],
            corner_radius=6,
            border_width=1,
            border_color=PALETTE["line"],
        )
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(1, weight=1)

        # Corner accent lines
        _hud_corner(card)

        # Item name
        ctk.CTkLabel(
            card,
            text=item.upper(),
            font=font("mono", 11, "bold"),
            text_color=PALETTE["text"],
        ).pack(anchor="w", padx=20, pady=(18, 2))

        # Value (big, colored)
        value_lbl = ctk.CTkLabel(
            card,
            text="LOADING",
            font=font("mono", 22, "bold"),
            text_color=PALETTE["cyan"],
        )
        value_lbl.pack(anchor="w", padx=20, pady=(4, 2))

        # Detail / sub-text
        detail_lbl = ctk.CTkLabel(
            card,
            text="Awaiting live telemetry",
            font=font("mono", 10),
            text_color=PALETTE["text_muted"],
        )
        detail_lbl.pack(anchor="w", padx=20, pady=(0, 18))

        frame._value_labels[item] = value_lbl    # type: ignore[attr-defined]
        frame._detail_labels[item] = detail_lbl  # type: ignore[attr-defined]

    refresh_info_page(frame, page_key)
    return frame


def _hud_corner(card: ctk.CTkFrame) -> None:
    """Draw small HUD corner accents on a card."""
    accent = PALETTE["line_soft"]
    for x_rel, y_rel, x_off, y_off in [(0, 0, 0, 0), (1, 0, -14, 0), (0, 1, 0, -8), (1, 1, -14, -8)]:
        corner = ctk.CTkFrame(card, fg_color="transparent", width=14, height=8)
        corner.place(relx=x_rel, rely=y_rel, x=x_off, y=y_off)
        ctk.CTkFrame(corner, fg_color=accent, width=12, height=1).place(x=0, y=0 if y_rel == 0 else 7)
        ctk.CTkFrame(corner, fg_color=accent, width=1, height=6).place(x=0 if x_rel == 0 else 13, y=1)


# ── Refresh helpers ────────────────────────────────────────────────────

def refresh_info_pages(pages: dict[str, ctk.CTkFrame]) -> None:
    for page_key, frame in pages.items():
        if page_key != "dashboard":
            refresh_info_page(frame, page_key)


def refresh_info_page(frame: ctk.CTkFrame, page_key: str) -> None:
    values = _build_page_values(page_key)
    for item, (value, detail, color) in values.items():
        lbl = getattr(frame, "_value_labels", {}).get(item)
        det = getattr(frame, "_detail_labels", {}).get(item)
        if lbl:
            lbl.configure(text=value, text_color=color)
        if det:
            det.configure(text=detail)


def _build_page_values(page_key: str) -> dict[str, tuple[str, str, str]]:
    env = resolved_env(os.environ)

    if page_key == "system":
        disk = psutil.disk_usage(os.getcwd())
        latency = build_latency_snapshot()
        return {
            "CPU usage":        (f"{psutil.cpu_percent():.0f}%",          "Live processor load",                    PALETTE["cyan"]),
            "Memory usage":     (f"{psutil.virtual_memory().percent:.0f}%", "System RAM in use",                    PALETTE["cyan"]),
            "Disk status":      (f"{disk.percent:.0f}%",                  "Workspace drive usage",                  PALETTE["cyan"]),
            "Internet status":  (_internet_status(),                       "Fast connectivity probe",               PALETTE["green"]),
            "Microphone status":("READY",                                  "SpeechRecognition runtime installed",    PALETTE["green"]),
            "Latency":          (f"{latency['average_ms']}ms",            f"{latency['count']} recent samples",     PALETTE["amber"]),
        }

    if page_key == "modules":
        return {
            "Application launcher":       ("READY",    "Browser, Chrome, Edge, VS Code, Calculator",    PALETTE["green"]),
            "Spotify control":            ("OPTIONAL", "Requires Spotify credentials for API control",  PALETTE["amber"]),
            "Screenshot capture":         ("READY",    "Desktop screenshot workflow available",          PALETTE["green"]),
            "Clipboard reader":           ("READY",    "Read and summarize copied text",                 PALETTE["green"]),
            "Summarizer":                 ("READY",    "Rules plus AI fallback when configured",         PALETTE["green"]),
            "Mouse and keyboard control": ("GUARDED",  "Risky automation requires confirmation",         PALETTE["amber"]),
        }

    if page_key == "integrations":
        ai = describe_ai_status(env)
        or_key = env.get("GROQ_API_KEY", "")
        or_configured = bool(or_key) and or_key.startswith("sk-or-")
        return {
            "OpenRouter AI": (
                "ACTIVE" if or_configured else "MISSING",
                f"Model routing: {ai['reason']}",
                PALETTE["green"] if or_configured else PALETTE["amber"],
            ),
            "Spotify API": (
                _mask_status(env.get("SPOTIFY_CLIENT_ID")),
                "Client ID and secret stay masked",
                PALETTE["green"] if env.get("SPOTIFY_CLIENT_ID") else PALETTE["amber"],
            ),
            "Gemini vision": (
                _mask_status(env.get("GEMINI_API_KEY")),
                "Optional vision provider",
                PALETTE["green"] if env.get("GEMINI_API_KEY") else PALETTE["amber"],
            ),
            "Weather service":  ("LOCAL READY", "Uses configured command tooling",     PALETTE["cyan"]),
            "Offline fallback": (
                "OFF" if env.get("JARVIS_OFFLINE_STT") != "1" else "ON",
                "Vosk fallback is optional",
                PALETTE["amber"],
            ),
            "Local LLM endpoint": (
                _mask_status(env.get("JARVIS_LOCAL_LLM_URL")),
                ai["mode"],
                PALETTE["cyan"],
            ),
        }

    if page_key == "security":
        overview = build_security_overview(env, actions=["shutdown", "restart", "lock_screen", "type_text", "press_key", "open_web"])
        profile = overview["profile"]
        matrix = overview["permission_matrix"]
        blocked = sum(1 for status in matrix["shutdown"].values() if status == "blocked")
        report = build_slo_report()
        configured = sum(1 for status in overview["secrets"].values() if status == "CONFIGURED")
        return {
            "Confirmation-required commands": (str(len(overview["confirmation_required"])), "Risky desktop actions require approval", PALETTE["green"]),
            "Safe mode":                      ("ON" if profile["id"] == "safe" else "OFF", f"Privacy: {overview['privacy']['retention']}", PALETTE["amber"]),
            "Dangerous action blocking":      ("ENABLED",  f"Shutdown blocked in {blocked} profiles", PALETTE["green"]),
            "Masked API key status":          ("MASKED",   f"{configured} optional secrets configured", PALETTE["green"]),
            "Permission profile":             (profile["label"], "Allowed actions are policy-controlled", PALETTE["cyan"]),
            "Audit events":                   (str(report["events_seen"]), f"{report['warning_count']} warnings, {report['error_count']} errors", PALETTE["amber"]),
        }

    # settings page
    return {
        "Theme":            ("GHOST PROTOCOL HUD", "Dark red+gold cockpit",                          PALETTE["cyan"]),
        "Accent color":     ("RED + GOLD",          "Primary reactor glow palette",                   PALETTE["cyan"]),
        "Voice":            (env.get("JARVIS_TTS_PROVIDER", "edge").upper(), "TTS provider",          PALETTE["cyan"]),
        "Wake word":        (env.get("JARVIS_WAKE_WORD", "jarvis").upper(), "Activation phrase",      PALETTE["cyan"]),
        "Language":         (env.get("JARVIS_LANGUAGE", "EN").upper(), "Voice command language",      PALETTE["cyan"]),
        "Startup behavior": ("ONBOARDING" if not env.get("JARVIS_ONBOARDING_COMPLETE") else "READY", "First-run setup gate", PALETTE["amber"]),
    }
