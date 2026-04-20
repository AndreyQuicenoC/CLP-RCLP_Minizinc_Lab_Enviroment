"""
Themes Module - Premium color schemes and design tokens for UI.

Provides comprehensive theming with dark and light modes, professional palettes,
typography definitions, and dynamic theme management via singleton pattern.
"""

from typing import Dict, Any, Literal
from dataclasses import dataclass
import sys
from pathlib import Path

# Try to import theme persistence, fall back if not available
try:
    from core.shared.theme_persistence import ThemePersistence
except ImportError:
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
        from core.shared.theme_persistence import ThemePersistence
    except ImportError:
        # Fallback: no persistence
        ThemePersistence = None

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

class Typography:
    """Font families and sizes for consistent typography across UI."""
    ui_normal = ("Segoe UI", 10)
    ui_bold = ("Segoe UI", 10, "bold")
    section = ("Segoe UI", 8, "bold")
    mono = ("Consolas", 9)
    small = ("Segoe UI", 8)

class Spacing:
    """Consistent spacing and padding constants."""
    HEADER_HEIGHT = 70
    FOOTER_HEIGHT = 40
    PAD_LARGE = 20
    PAD_MEDIUM = 16
    PAD_SMALL = 12
    PAD_TINY = 8

class ThemeManager:
    """Singleton theme manager for dynamic theme switching."""
    _instance = None
    _current_mode: Literal["dark", "light"] = None
    _palette: ColorPalette = DARK_PALETTE
    _observers: list = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ThemeManager, cls).__new__(cls)
            # Initialize with saved theme or default
            saved_theme = None
            if ThemePersistence:
                saved_theme = ThemePersistence.get_theme()
            cls._current_mode = saved_theme or "dark"
            cls._palette = DARK_PALETTE if cls._current_mode == "dark" else LIGHT_PALETTE
        return cls._instance

    @classmethod
    def get_palette(cls, mode: Literal["dark", "light"] = None) -> ColorPalette:
        """Get color palette for specified mode. None returns current."""
        if mode is None:
            return cls._palette
        return DARK_PALETTE if mode == "dark" else LIGHT_PALETTE

    @classmethod
    def set_mode(cls, mode: Literal["dark", "light"]) -> None:
        """Switch to specified theme mode."""
        if mode not in ("dark", "light"):
            raise ValueError(f"Invalid mode: {mode}")
        if mode == cls._current_mode:
            return
        cls._current_mode = mode
        cls._palette = DARK_PALETTE if mode == "dark" else LIGHT_PALETTE
        # Persist the theme choice
        if ThemePersistence:
            ThemePersistence.set_theme(mode)
        cls._notify_observers()

    @classmethod
    def get_mode(cls) -> Literal["dark", "light"]:
        """Get current theme mode."""
        return cls._current_mode

    @classmethod
    def register_observer(cls, callback) -> None:
        """Register callback for theme change notifications."""
        if callback not in cls._observers:
            cls._observers.append(callback)

    @classmethod
    def unregister_observer(cls, callback) -> None:
        """Unregister theme change callback."""
        if callback in cls._observers:
            cls._observers.remove(callback)

    @classmethod
    def _notify_observers(cls) -> None:
        """Notify all observers of theme mode change."""
        for callback in cls._observers:
            try:
                callback(cls._current_mode)
            except Exception as e:
                print(f"Error notifying observer: {e}")

def get_theme_dict(mode: Literal["dark", "light"] = None) -> Dict[str, Any]:
    """
    Get complete theme dictionary with all design tokens.

    Provides unified dictionary with colors, typography, and spacing for UI styling.

    Args:
        mode: Theme mode ("dark" or "light"). If None, uses current mode.

    Returns:
        Dictionary with 26+ design tokens covering colors, fonts, and spacing.
    """
    palette = ThemeManager.get_palette(mode)
    return {
        # Colors - Backgrounds (4)
        "bg_base": palette.bg_base,
        "bg_surface": palette.bg_surface,
        "bg_elevated": palette.bg_elevated,
        "bg_hover": palette.bg_hover,

        # Colors - Accents (3)
        "accent_primary": palette.accent_primary,
        "accent_dim": palette.accent_dim,
        "accent_glow": palette.accent_glow,

        # Colors - Status (3)
        "success": palette.success,
        "warning": palette.warning,
        "error": palette.error,

        # Colors - Text (4)
        "text_primary": palette.text_primary,
        "text_secondary": palette.text_secondary,
        "text_muted": palette.text_muted,
        "text_code": palette.text_code,

        # Colors - Borders (2)
        "border_normal": palette.border_normal,
        "border_active": palette.border_active,

        # Typography - Font Tuples (5)
        "font_ui": Typography.ui_normal,
        "font_bold": Typography.ui_bold,
        "font_section": Typography.section,
        "font_mono": Typography.mono,
        "font_small": Typography.small,

        # Spacing & Measurements (6)
        "padding_large": Spacing.PAD_LARGE,
        "padding_medium": Spacing.PAD_MEDIUM,
        "padding_small": Spacing.PAD_SMALL,
        "padding_tiny": Spacing.PAD_TINY,
        "header_height": Spacing.HEADER_HEIGHT,
        "footer_height": Spacing.FOOTER_HEIGHT,
    }
