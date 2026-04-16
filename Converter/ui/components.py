"""
Reusable UI Components

Custom Tkinter widgets for consistent UI design.

Author: AVISPA Research Team
Date: April 2026
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional, Dict, Any


class FlatButton(tk.Frame):
    """Flat button with custom styling and theme support - matching Runner design."""

    def __init__(self, parent: tk.Widget, text: str, command: Callable = None,
                 theme: Dict[str, Any] = None, accent: bool = False, disabled: bool = False, **kwargs):
        super().__init__(parent, **kwargs)
        self._theme = theme
        self.command = command
        self._disabled = disabled
        self._accent = accent

        # Set background
        if theme:
            self.configure(bg=theme.get("bg_base", "#0D0F14"), highlightthickness=0)
        else:
            self.configure(highlightthickness=0)

        # Determine colors
        if accent:
            normal_bg = theme.get("accent_primary", "#3D8EF5") if theme else "#3D8EF5"
            normal_fg = "#FFFFFF"
            hover_bg = theme.get("accent_glow", "#5AAEFF") if theme else "#5AAEFF"
        else:
            normal_bg = theme.get("bg_elevated", "#1C2030") if theme else "#1C2030"
            normal_fg = theme.get("text_primary", "#E8ECF4") if theme else "#E8ECF4"
            hover_bg = theme.get("bg_hover", "#232840") if theme else "#232840"

        disabled_bg = theme.get("bg_elevated", "#1C2030") if theme else "#1C2030"
        disabled_fg = theme.get("text_muted", "#4A5568") if theme else "#4A5568"

        self.normal_bg = normal_bg
        self.normal_fg = normal_fg
        self.hover_bg = hover_bg
        self.disabled_bg = disabled_bg
        self.disabled_fg = disabled_fg

        self.button = tk.Label(
            self,
            text=text,
            fg=disabled_fg if disabled else normal_fg,
            bg=disabled_bg if disabled else normal_bg,
            font=("Segoe UI", 10, "bold") if not disabled else ("Segoe UI", 10),
            cursor="arrow" if disabled else "hand2",
            padx=16,
            pady=10
        )
        self.button.pack(fill=tk.BOTH, expand=True)

        if not disabled:
            self.button.bind("<Button-1>", self._on_click)
            self.button.bind("<Enter>", self._on_hover)
            self.button.bind("<Leave>", self._on_leave)

    def _on_click(self, event):
        if self.command and not self._disabled:
            self.command()

    def _on_hover(self, event):
        if not self._disabled:
            self.button.config(bg=self.hover_bg)

    def _on_leave(self, event):
        if not self._disabled:
            self.button.config(bg=self.normal_bg)

    def set_disabled(self, disabled: bool) -> None:
        """Enable/disable button."""
        self._disabled = disabled
        if disabled:
            self.button.config(bg=self.disabled_bg, fg=self.disabled_fg, cursor="arrow", state=tk.DISABLED)
        else:
            self.button.config(bg=self.normal_bg, fg=self.normal_fg, cursor="hand2", state=tk.NORMAL)


class SectionLabel(tk.Label):
    """Section header label."""

    def __init__(self, parent: tk.Widget, text: str, bg_color: str = "#2a2a2a",
                 fg_color: str = "#e0e0e0", **kwargs):
        super().__init__(
            parent,
            text=text,
            bg=bg_color,
            fg=fg_color,
            font=("Arial", 12, "bold"),
            anchor=tk.W,
            **kwargs
        )


class Divider(tk.Frame):
    """Visual divider line."""

    def __init__(self, parent: tk.Widget, bg_color: str = "#404040", **kwargs):
        super().__init__(parent, bg=bg_color, height=1, **kwargs)
        self.pack_propagate(False)


class StatusIndicator(tk.Frame):
    """Status indicator with color and text."""

    STATUS_COLORS = {
        "idle": "#a0a0a0",
        "running": "#3b82f6",
        "success": "#10b981",
        "error": "#ef4444",
        "warning": "#f59e0b",
    }

    def __init__(self, parent: tk.Widget, bg_color: str = "#2a2a2a", **kwargs):
        super().__init__(parent, bg=bg_color, **kwargs)
        self.bg_color = bg_color

        # Status dot
        self.dot = tk.Canvas(
            self,
            width=12,
            height=12,
            bg=bg_color,
            highlightthickness=0
        )
        self.dot.pack(side=tk.LEFT, padx=(0, 8))
        self.dot.create_oval(1, 1, 11, 11, fill=self.STATUS_COLORS["idle"], outline="")

        # Status text
        self.label = tk.Label(
            self,
            text="Ready",
            bg=bg_color,
            fg="#a0a0a0",
            font=("Arial", 9)
        )
        self.label.pack(side=tk.LEFT)

    def set_status(self, status: str, text: str = "") -> None:
        """Set status and optional text."""
        color = self.STATUS_COLORS.get(status, "#a0a0a0")
        self.dot.delete("all")
        self.dot.create_oval(1, 1, 11, 11, fill=color, outline="")

        if text:
            self.label.config(text=text)


class FormEntry(tk.Frame):
    """Labeled entry field."""

    def __init__(self, parent: tk.Widget, label: str, bg_color: str = "#2a2a2a",
                 fg_color: str = "#e0e0e0", **kwargs):
        super().__init__(parent, bg=bg_color, **kwargs)

        # Label
        tk.Label(
            self,
            text=label,
            bg=bg_color,
            fg=fg_color,
            font=("Arial", 10)
        ).pack(anchor=tk.W, pady=(0, 5))

        # Entry
        self.entry = tk.Entry(
            self,
            bg="#3a3a3a",
            fg=fg_color,
            borderwidth=1,
            relief=tk.SOLID,
            font=("Arial", 10)
        )
        self.entry.pack(fill=tk.X)

    def get(self) -> str:
        """Get entry value."""
        return self.entry.get()

    def set(self, value: str) -> None:
        """Set entry value."""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)

