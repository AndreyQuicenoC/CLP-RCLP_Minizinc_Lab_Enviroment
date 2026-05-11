"""
Theme persistence module for maintaining user preference across sessions and tools.
"""

import json
from pathlib import Path
from typing import Literal

class ThemePersistence:
    """Manages theme preference persistence."""

    CONFIG_FILE = Path(__file__).parent.parent.parent / ".theme_config.json"
    DEFAULT_THEME = "dark"

    @classmethod
    def get_theme(cls) -> Literal["dark", "light"]:
        """Get saved theme preference or default."""
        try:
            if cls.CONFIG_FILE.exists():
                with open(cls.CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                    theme = config.get("theme", cls.DEFAULT_THEME)
                    if theme in ("dark", "light"):
                        return theme
        except (json.JSONDecodeError, IOError):
            pass
        return cls.DEFAULT_THEME

    @classmethod
    def set_theme(cls, theme: Literal["dark", "light"]) -> None:
        """Save theme preference."""
        if theme not in ("dark", "light"):
            return

        try:
            config = {}
            if cls.CONFIG_FILE.exists():
                try:
                    with open(cls.CONFIG_FILE, 'r') as f:
                        config = json.load(f)
                except (json.JSONDecodeError, IOError):
                    config = {}

            config["theme"] = theme

            cls.CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(cls.CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=2)
        except IOError:
            pass
