"""
Tooltip Component

Hover tooltips for UI elements.

Author: AVISPA Research Team
Date: April 2026
"""

import tkinter as tk
from typing import Optional


class Tooltip:
    """Create a tooltip for a Tkinter widget."""

    def __init__(self, widget: tk.Widget, text: str, bg_color: str = "#3a3a3a",
                 fg_color: str = "#e0e0e0"):
        """
        Initialize tooltip.

        Args:
            widget: Widget to attach tooltip to
            text: Tooltip text
            bg_color: Background color
            fg_color: Text color
        """
        self.widget = widget
        self.text = text
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.tipwindow: Optional[tk.Toplevel] = None
        self.id: Optional[str] = None
        self.x = self.y = 0

        self.widget.bind("<Enter>", self._on_enter, add=True)
        self.widget.bind("<Leave>", self._on_leave, add=True)
        self.widget.bind("<ButtonPress>", self._on_leave, add=True)

    def _on_enter(self, event=None):
        """Show tooltip on mouse enter."""
        if self.tipwindow or not self.text:
            return

        x = self.widget.winfo_rootx() + 10
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5

        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            tw,
            text=self.text,
            justify=tk.LEFT,
            background=self.bg_color,
            foreground=self.fg_color,
            relief=tk.SOLID,
            borderwidth=1,
            wraplength=300,
            font=("Arial", 9)
        )
        label.pack(ipadx=5, ipady=3)

    def _on_leave(self, event=None):
        """Hide tooltip on mouse leave."""
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None
