"""
Theme System for Converter UI

Dark and light theme support with dynamic switching capability.

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


# Dark theme palette
DARK_PALETTE = {
    "bg_base": "#1a1a1a",
    "bg_surface": "#2a2a2a",
    "bg_hover": "#3a3a3a",
    "border": "#404040",
    "text_primary": "#e0e0e0",
    "text_secondary": "#a0a0a0",
    "accent_primary": "#6366f1",
    "accent_secondary": "#8b5cf6",
    "success": "#10b981",
    "error": "#ef4444",
    "warning": "#f59e0b",
    "info": "#3b82f6",
}

# Light theme palette
LIGHT_PALETTE = {
    "bg_base": "#f8f9fa",
    "bg_surface": "#ffffff",
    "bg_hover": "#f0f1f3",
    "border": "#d0d0d0",
    "text_primary": "#1a1a1a",
    "text_secondary": "#666666",
    "accent_primary": "#6366f1",
    "accent_secondary": "#8b5cf6",
    "success": "#059669",
    "error": "#dc2626",
    "warning": "#d97706",
    "info": "#2563eb",
}
