"""
Theme System for Converter UI

Dark and light theme support with dynamic switching capability.
Synchronized with Runner and Generator themes for consistent design.

Author: AVISPA Research Team
Date: April 2026
"""

from typing import Dict, Literal, Callable, List
import logging

logger = logging.getLogger(__name__)


class ThemeManager:
    """Manage theme switching and observer pattern."""

    _observers: List[Callable[[Literal["dark", "light"]], None]] = []
    _current_theme: Literal["dark", "light"] = "dark"

    @classmethod
    def register_observer(cls, callback: Callable[[Literal["dark", "light"]], None]) -> None:
        """Register a callback to be notified of theme changes."""
        cls._observers.append(callback)

    @classmethod
    def switch_theme(cls, theme: Literal["dark", "light"]) -> None:
        """Switch theme and notify all observers."""
        if theme != cls._current_theme:
            cls._current_theme = theme
            logger.info(f"Theme switched to: {theme}")
            for callback in cls._observers:
                try:
                    callback(theme)
                except Exception as e:
                    logger.error(f"Error notifying theme observer: {e}")

    @classmethod
    def get_current_theme(cls) -> Literal["dark", "light"]:
        """Get current theme."""
        return cls._current_theme


def get_theme_dict(mode: Literal["dark", "light"]) -> Dict[str, str]:
    """
    Get complete theme dictionary for given mode.

    Args:
        mode: "dark" or "light"

    Returns:
        Dictionary mapping color tokens to hex values
    """
    return DARK_PALETTE if mode == "dark" else LIGHT_PALETTE


# Dark theme palette - Synchronized with Runner/Generator
DARK_PALETTE = {
    "bg_base": "#0D0F14",
    "bg_surface": "#141720",
    "bg_elevated": "#1C2030",
    "bg_hover": "#232840",
    "border": "#242B3D",
    "border_active": "#3D8EF5",
    "text_primary": "#E8ECF4",
    "text_secondary": "#8896B3",
    "text_muted": "#4A5568",
    "accent_primary": "#3D8EF5",
    "accent_dim": "#1F4A8C",
    "accent_glow": "#5AAEFF",
    "success": "#22C55E",
    "error": "#EF4444",
    "warning": "#F59E0B",
    "info": "#3D8EF5",
}

# Light theme palette - Synchronized with Runner/Generator
LIGHT_PALETTE = {
    "bg_base": "#F8F9FA",
    "bg_surface": "#FFFFFF",
    "bg_elevated": "#F1F3F5",
    "bg_hover": "#E9ECEF",
    "border": "#CCCCCC",
    "border_active": "#2E5FCC",
    "text_primary": "#1A1A1A",
    "text_secondary": "#555555",
    "text_muted": "#999999",
    "accent_primary": "#2E5FCC",
    "accent_dim": "#5A7FD4",
    "accent_glow": "#5A9FFF",
    "success": "#27AE60",
    "error": "#E74C3C",
    "warning": "#D68910",
    "info": "#2E5FCC",
}
