"""
Themes Module - High-quality color schemes and design tokens for Runner UI.
"""

from typing import Dict, Any, Literal
from dataclasses import dataclass

@dataclass
class ColorPalette:
    """Comprehensive color definitions for a theme."""
    bg_base: str
    bg_surface: str
    bg_elevated: str
    bg_hover: str
    accent_primary: str
    accent_dim: str
    accent_glow: str
    success: str
    warning: str
    error: str
    text_primary: str
    text_secondary: str
    text_muted: str
    text_code: str
    border_normal: str
    border_active: str

DARK_PALETTE = ColorPalette(
    bg_base="#0D0F14", bg_surface="#141720", bg_elevated="#1C2030", bg_hover="#232840",
    accent_primary="#3D8EF5", accent_dim="#1F4A8C", accent_glow="#5AAEFF",
    success="#22C55E", warning="#F59E0B", error="#EF4444",
    text_primary="#E8ECF4", text_secondary="#8896B3", text_muted="#4A5568", text_code="#A8C4F0",
    border_normal="#242B3D", border_active="#3D8EF5",
)

LIGHT_PALETTE = ColorPalette(
    bg_base="#F8F9FA", bg_surface="#FFFFFF", bg_elevated="#F1F3F5", bg_hover="#E9ECEF",
    accent_primary="#2E5FCC", accent_dim="#5A7FD4", accent_glow="#5A9FFF",
    success="#27AE60", warning="#D68910", error="#E74C3C",
    text_primary="#1A1A1A", text_secondary="#555555", text_muted="#999999", text_code="#003D99",
    border_normal="#CCCCCC", border_active="#2E5FCC",
)

class ThemeManager:
    """Singleton theme manager."""
    _instance = None
    _current_mode: Literal["dark", "light"] = "dark"
    _palette: ColorPalette = DARK_PALETTE
    _observers: list = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ThemeManager, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_palette(cls, mode: Literal["dark", "light"] = None) -> ColorPalette:
        if mode is None:
            return cls._palette
        return DARK_PALETTE if mode == "dark" else LIGHT_PALETTE

    @classmethod
    def set_mode(cls, mode: Literal["dark", "light"]) -> None:
        if mode not in ("dark", "light"):
            raise ValueError(f"Invalid mode: {mode}")
        if mode == cls._current_mode:
            return
        cls._current_mode = mode
        cls._palette = DARK_PALETTE if mode == "dark" else LIGHT_PALETTE
        cls._notify_observers()

    @classmethod
    def get_mode(cls) -> Literal["dark", "light"]:
        return cls._current_mode

    @classmethod
    def register_observer(cls, callback) -> None:
        if callback not in cls._observers:
            cls._observers.append(callback)

    @classmethod
    def unregister_observer(cls, callback) -> None:
        if callback in cls._observers:
            cls._observers.remove(callback)

    @classmethod
    def _notify_observers(cls) -> None:
        for callback in cls._observers:
            try:
                callback(cls._current_mode)
            except Exception:
                pass
