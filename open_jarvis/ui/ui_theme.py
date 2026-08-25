"""Premium visual design tokens for the NEO desktop UI."""

from __future__ import annotations

PALETTE = {
    "bg": "#060302",
    "bg_elevated": "#0C0602",
    "surface": "#100804",
    "surface_soft": "#1A0C04",
    "surface_glass": "#080401",
    "line": "#4A1A00",
    "line_soft": "#6B2800",
    "line_hot": "#FF2000",
    "cyan": "#FF2000",
    "cyan_soft": "#FF6600",
    "cyan_hot": "#FFD000",
    "blue": "#FF2000",
    "amber": "#FFD000",
    "green": "#FF4400",
    "red": "#FF0000",
    "text": "#FFF0D0",
    "text_muted": "#C8904A",
    "text_faint": "#7A4A20",
    "ink": "#100502",
}

FONTS = {
    "display": "Consolas",
    "ui": "Segoe UI",
    "mono": "Consolas",
}

RADIUS = {
    "card": 8,
    "button": 8,
    "pill": 999,
}


def build_design_tokens() -> dict:
    """Return stable design tokens for tests, docs, and UI modules."""

    return {
        "name": "Cyber Hologram",
        "palette": dict(PALETTE),
        "fonts": dict(FONTS),
        "radius": dict(RADIUS),
        "spacing": {"xs": 6, "sm": 10, "md": 16, "lg": 24, "xl": 34},
    }


def font(kind: str, size: int, weight: str | None = None) -> tuple:
    """Build a CustomTkinter font tuple from theme tokens."""

    family = FONTS.get(kind, FONTS["ui"])
    return (family, size, weight) if weight else (family, size)
