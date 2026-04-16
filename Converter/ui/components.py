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
    """Flat button with custom styling."""

    def __init__(self, parent: tk.Widget, text: str, command: Callable = None,
                 bg_color: str = "#6366f1", fg_color: str = "#ffffff",
                 hover_color: str = "#4f46e5", **kwargs):
        super().__init__(parent, bg=bg_color, **kwargs)
        self.config(width=120, height=40)
        self.pack_propagate(False)

        self.bg_color = bg_color
        self.hover_color = hover_color
        self.command = command

        self.button = tk.Label(
            self,
            text=text,
            fg=fg_color,
            bg=bg_color,
            font=("Arial", 10, "bold"),
            cursor="hand2"
        )
        self.button.pack(fill=tk.BOTH, expand=True)

        self.button.bind("<Button-1>", self._on_click)
        self.button.bind("<Enter>", self._on_hover)
        self.button.bind("<Leave>", self._on_leave)

    def _on_click(self, event):
        if self.command:
            self.command()

    def _on_hover(self, event):
        self.config(bg=self.hover_color)
        self.button.config(bg=self.hover_color)

    def _on_leave(self, event):
        self.config(bg=self.bg_color)
        self.button.config(bg=self.bg_color)

    def set_disabled(self, disabled: bool) -> None:
        """Enable/disable button."""
        state = tk.DISABLED if disabled else tk.NORMAL
        self.button.config(state=state)


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
