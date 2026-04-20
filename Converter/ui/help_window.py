"""
Styled Help Window Component

Professional, reusable help window with theme support.

Author: AVISPA Research Team
Date: April 2026
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Optional


class HelpWindow(tk.Toplevel):
    """Styled help window matching application theme."""

    def __init__(self, parent: tk.Widget, title: str, content: str, theme: Dict[str, Any]):
        """
        Initialize help window.

        Args:
            parent: Parent widget
            title: Window title
            content: Help content text
            theme: Theme dictionary
        """
        super().__init__(parent)
        self.title(title)
        self.geometry("600x500")
        self.resizable(True, True)

        self.theme = theme
        self.configure(bg=theme["bg_base"])

        # Center window on parent
        self._center_on_parent(parent)

        # Build UI
        self._build_ui(content)

        # Make window modal
        self.transient(parent)
        self.grab_set()

    def _center_on_parent(self, parent: tk.Widget) -> None:
        """Center help window on parent window."""
        self.update_idletasks()
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_w = parent.winfo_width()
        parent_h = parent.winfo_height()

        win_w = self.winfo_width()
        win_h = self.winfo_height()

        x = parent_x + (parent_w - win_w) // 2
        y = parent_y + (parent_h - win_h) // 2

        self.geometry(f"+{x}+{y}")

    def _build_ui(self, content: str) -> None:
        """Build help window UI."""
        # Header
        header = tk.Frame(self, bg=self.theme["bg_surface"], height=60)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)

        # Accent bar
        tk.Frame(
            header,
            bg=self.theme["accent_primary"],
            width=4,
            height=32
        ).pack(side=tk.LEFT, padx=(0, 12), pady=14)

        # Title
        tk.Label(
            header,
            text="Help & Requirements",
            font=("Arial", 14, "bold"),
            fg=self.theme["text_primary"],
            bg=self.theme["bg_surface"]
        ).pack(side=tk.LEFT, padx=10, pady=15)

        # Content frame
        content_frame = tk.Frame(self, bg=self.theme["bg_base"])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # Scrollbar
        scrollbar = ttk.Scrollbar(content_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Text widget
        text_widget = tk.Text(
            content_frame,
            bg=self.theme["bg_surface"],
            fg=self.theme["text_primary"],
            font=("Courier New", 9),
            relief=tk.FLAT,
            padx=15,
            pady=15,
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD
        )
        text_widget.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        scrollbar.config(command=text_widget.yview)

        # Insert content
        text_widget.insert("1.0", content)
        text_widget.config(state=tk.DISABLED)

        # Footer
        footer = tk.Frame(self, bg=self.theme["bg_surface"], height=40)
        footer.pack(fill=tk.X, padx=0, pady=0)
        footer.pack_propagate(False)

        close_btn = tk.Button(
            footer,
            text="Close",
            command=self.destroy,
            bg=self.theme["accent_primary"],
            fg="#FFFFFF",
            relief=tk.FLAT,
            font=("Arial", 9, "bold"),
            padx=20,
            pady=8,
            cursor="hand2"
        )
        close_btn.pack(pady=8)


def show_help(parent: tk.Widget, title: str, content: str, theme: Dict[str, Any]) -> None:
    """
    Show a styled help window.

    Args:
        parent: Parent widget
        title: Window title
        content: Help content
        theme: Theme dictionary
    """
    HelpWindow(parent, title, content, theme)
