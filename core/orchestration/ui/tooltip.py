"""
Tooltip Component - Enhanced user experience with helpful hints

Provides professional tooltip support for UI elements with automatic
positioning and theme-aware styling.

Authors: Andrey Quiceno and Juan Francesco García (AVISPA Team)
"""

import tkinter as tk
from typing import Optional


class Tooltip:
    """Create a tooltip for a given widget."""

    def __init__(self, widget: tk.Widget, text: str, theme_dict: dict, delay: int = 500):
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
        self.theme = theme_dict
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

        # Create label
        label = tk.Label(
            tw,
            text=self.text,
            justify=tk.LEFT,
            background=self.theme["bg_elevated"],
            foreground=self.theme["text_primary"],
            relief=tk.FLAT,
            borderwidth=0,
            font=("Arial", 9),
            padx=8,
            pady=6,
            wraplength=200,
        )
        label.pack(ipadx=1)

        # Add border effect with outer frame
        tw.configure(bg=self.theme["border_normal"])

    def hidetip(self) -> None:
        """Hide the tooltip."""
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None
