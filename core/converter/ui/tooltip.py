"""
Tooltip Component - Enhanced user experience with helpful hints

Provides professional tooltip support for UI elements with automatic
positioning and theme-aware styling.

Author: AVISPA Research Team
Date: April 2026
"""

import tkinter as tk
from typing import Optional, Dict, Any


class Tooltip:
    """Create a tooltip for a given widget."""

    def __init__(self, widget: tk.Widget, text: str, theme_dict: Dict[str, Any] = None, delay: int = 500):
        """
        Initialize tooltip.

        Args:
            widget: Widget to attach tooltip to
            text: Tooltip text content
            theme_dict: Theme dictionary for styling
            delay: Delay in milliseconds before showing tooltip
        """
        self.widget = widget
        self.text = text
        self.theme = theme_dict or {}
        self.delay = delay
        self.tipwindow: Optional[tk.Toplevel] = None
        self.id: Optional[str] = None
        self.x = self.y = 0

        # Bind events
        self.widget.bind("<Enter>", self.enter, add=True)
        self.widget.bind("<Leave>", self.leave, add=True)
        self.widget.bind("<ButtonPress>", self.leave, add=True)

    def enter(self, event=None) -> None:
        """Show tooltip on mouse enter."""
        self.schedule()

    def leave(self, event=None) -> None:
        """Hide tooltip on mouse leave."""
        self.unschedule()
        self.hidetip()

    def schedule(self) -> None:
        """Schedule tooltip display."""
        self.unschedule()
        self.id = self.widget.after(self.delay, self.showtip)

    def unschedule(self) -> None:
        """Cancel scheduled tooltip display."""
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None

    def showtip(self) -> None:
        """Display the tooltip."""
        if self.tipwindow or not self.text:
            return

        # Create tooltip window
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_attributes("-topmost", True)

        # Position tooltip below widget
        x = self.widget.winfo_rootx() + self.widget.winfo_width() // 2
        y = self.widget.winfo_rooty() + self.widget.winfo_height()
        tw.wm_geometry(f"+{x}+{y}")

        # Get colors from theme or use defaults
        bg_color = self.theme.get("bg_surface", "#2a2a2a")
        fg_color = self.theme.get("text_primary", "#e0e0e0")
        border_color = self.theme.get("border", "#404040")

        # Create label
        label = tk.Label(
            tw,
            text=self.text,
            justify=tk.LEFT,
            background=bg_color,
            foreground=fg_color,
            relief=tk.FLAT,
            borderwidth=0,
            font=("Arial", 9),
            padx=8,
            pady=6,
            wraplength=200,
        )
        label.pack(ipadx=1)

        # Add border effect with outer frame
        tw.configure(bg=border_color)

    def hidetip(self) -> None:
        """Hide the tooltip."""
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None
