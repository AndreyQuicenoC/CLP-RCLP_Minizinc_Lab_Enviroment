"""
Layouts Module - Layout builders and constants.
"""

import tkinter as tk
from typing import Dict, Any

class LayoutConfig:
    """Global layout configuration and constants."""
    WINDOW_WIDTH = 1100
    WINDOW_HEIGHT = 750
    MIN_WIDTH = 950
    MIN_HEIGHT = 700
    HEADER_HEIGHT = 70
    FOOTER_HEIGHT = 40
    CONTENT_PADDING = 20
    SECTION_SPACING = 16
    ITEM_SPACING = 12
    ITEM_PADDING_H = 16
    ITEM_PADDING_V = 12
    BUTTON_HEIGHT = 40
    BUTTON_PADDING_H = 16
    BUTTON_PADDING_V = 10
    BUTTON_GROUP_SPACING = 12
    INPUT_HEIGHT = 32
    INPUT_PADDING = 8
    SPINBOX_WIDTH = 100
    LABEL_MIN_WIDTH = 150
    HEADER_PADDING = (CONTENT_PADDING, 16)
    FOOTER_PADDING = (CONTENT_PADDING, 12)

class LayoutBuilder:
    """Helper class for creating consistent layouts."""

    @staticmethod
    def create_header(parent: tk.Widget, title: str, subtitle: str = "",
                     theme: Dict[str, Any] = None) -> tk.Frame:
        """Create a professional header frame."""
        header = tk.Frame(parent, bg=theme["bg_elevated"], height=LayoutConfig.HEADER_HEIGHT)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        content = tk.Frame(header, bg=theme["bg_elevated"])
        content.pack(fill=tk.BOTH, expand=True, padx=LayoutConfig.HEADER_PADDING[0],
                    pady=LayoutConfig.HEADER_PADDING[1])

        title_label = tk.Label(content, text=title, font=theme["font_bold"],
                              fg=theme["text_primary"], bg=theme["bg_elevated"])
        title_label.pack(anchor=tk.W)

        if subtitle:
            subtitle_label = tk.Label(content, text=subtitle, font=theme["font_small"],
                                     fg=theme["text_secondary"], bg=theme["bg_elevated"])
            subtitle_label.pack(anchor=tk.W, pady=(4, 0))
        return header

    @staticmethod
    def create_footer(parent: tk.Widget, left_text: str = "", right_text: str = "",
                     theme: Dict[str, Any] = None) -> tk.Frame:
        """Create a footer frame with optional left/right text."""
        footer = tk.Frame(parent, bg=theme["bg_surface"], height=LayoutConfig.FOOTER_HEIGHT)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)

        if left_text:
            left_label = tk.Label(footer, text=left_text, font=theme["font_small"],
                                 fg=theme["text_secondary"], bg=theme["bg_surface"])
            left_label.pack(side=tk.LEFT, padx=LayoutConfig.FOOTER_PADDING[0])

        if right_text:
            right_label = tk.Label(footer, text=right_text, font=theme["font_small"],
                                  fg=theme["text_muted"], bg=theme["bg_surface"])
            right_label.pack(side=tk.RIGHT, padx=LayoutConfig.FOOTER_PADDING[0])
        return footer

    @staticmethod
    def create_content_area(parent: tk.Widget, theme: Dict[str, Any] = None) -> tk.Frame:
        """Create a main content area with proper padding."""
        content = tk.Frame(parent, bg=theme["bg_base"])
        content.pack(fill=tk.BOTH, expand=True, padx=LayoutConfig.CONTENT_PADDING,
                    pady=LayoutConfig.CONTENT_PADDING)
        return content

    @staticmethod
    def create_divider(parent: tk.Widget, theme: Dict[str, Any] = None) -> tk.Frame:
        """Create a divider line."""
        from .components import Divider
        divider = Divider(parent, theme)
        divider.pack(fill=tk.X, pady=LayoutConfig.ITEM_SPACING)
        return divider
