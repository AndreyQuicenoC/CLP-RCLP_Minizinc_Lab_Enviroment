"""
Generator Interface - Professional Instance Generation GUI

Premium dark/light mode UI for generating feasible CLP/RCLP test instances with MiniZinc validation,
real-time logging, and professional theme support.

Authors: Andrey Quiceno and Juan Francesco García (AVISPA Team)

Architecture:
- Dynamic theme switching (dark/light modes, dark default)
- Modular components from .components module
- Real-time generation logging with color-coded messages
- Professional layout with header, parameters, log, and controls
- Thread-safe background generation (no UI freezing)
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from typing import Dict, Any, Literal, Optional
import threading
import logging
from datetime import datetime

# Import modular theme system
from .themes import ThemeManager, get_theme_dict, DARK_PALETTE, LIGHT_PALETTE
from .components import SectionLabel, FlatButton, Divider, StatusIndicator
from .layouts import LayoutBuilder, LayoutConfig

# Import navigation utility
from core.shared.navigation import return_to_orchestrator
from core.shared.project_paths import ProjectPaths

# Import Generator core modules
from core.generator.config import Config
from core.generator.orchestrator import GeneratorOrchestrator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GeneratorInterface(tk.Frame):
    """Professional instance generator interface with theme switching support."""

    def __init__(self, root: tk.Tk):
        """
        Initialize the Generator interface.

        Sets up theming, observes theme changes, builds UI, and applies styling.
        """
        super().__init__(root)
        self.root = root
        self.master = root
        self.pack(fill=tk.BOTH, expand=True)

        # Initialize theme system
        self._init_theme()

        # Setup window properties
        self.root.title("AVISPA CLP Instance Generator v1.3.0")
        self.root.geometry("750x600")
        self.root.resizable(False, False)
        self._center_window()
        self.configure(bg=self.theme_dict["bg_base"])

        # Find project root for file operations
        self.project_root = ProjectPaths.get_project_root()

        # Initialize core module
        self.orchestrator = GeneratorOrchestrator(
            self.project_root,
            log_callback=self._log
        )

        # Thread management
        self.generation_thread: Optional[threading.Thread] = None
        self.is_generating = False

        # Build UI
        self._build_ui()
        self._apply_ttk_theme()

    def _init_theme(self) -> None:
        """Initialize theme system and register observer for dynamic switching."""
        self.theme_dict = get_theme_dict("dark")
        ThemeManager.register_observer(self._on_theme_change)

    def _on_theme_change(self, mode: Literal["dark", "light"]) -> None:
        """
        Called when theme mode changes (dark ↔ light).

        Refreshes the theme dictionary and updates all UI colors dynamically.
        """
        self.theme_dict = get_theme_dict(mode)
        self._refresh_ui_colors()

    def _center_window(self) -> None:
        """Center window on screen (horizontal and vertical)."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def _build_ui(self) -> None:
        """Build the complete user interface."""
        # Main container
        container = tk.Frame(self, bg=self.theme_dict["bg_base"])
        container.pack(fill=tk.BOTH, expand=True)

        # Header
        self._build_header(container)

        # Content area
        content = tk.Frame(container, bg=self.theme_dict["bg_base"])
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Parameters section
        self._build_parameters_section(content)

        # Log section
        self._build_log_section(content)

        # Controls section
        self._build_controls_section(content)

        # Footer
        self._build_footer(container)

    def _build_header(self, parent: tk.Widget) -> None:
        """Build the header with title and theme toggle."""
        header = tk.Frame(parent, bg=self.theme_dict["bg_elevated"], height=70)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)

        # Left side: Back button + Title with accent bar
        left = tk.Frame(header, bg=self.theme_dict["bg_elevated"])
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=15)

        # Back button
        back_btn = tk.Label(
            left,
            text="<",
            cursor="hand2",
            fg=self.theme_dict["accent_primary"],
            bg=self.theme_dict["bg_elevated"],
            font=("Arial", 18, "bold"),
            padx=8
        )
        back_btn.pack(side=tk.LEFT, padx=(0, 8))
        back_btn.bind("<Button-1>", lambda e: self._on_back_click())
        from .tooltip import Tooltip
        Tooltip(back_btn, "Return to System Center", self.theme_dict)

        tk.Frame(left, bg=self.theme_dict["accent_primary"], width=4, height=24).pack(
            side=tk.LEFT, padx=(0, 12), fill=tk.Y
        )

        title_frame = tk.Frame(left, bg=self.theme_dict["bg_elevated"])
        title_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(
            title_frame,
            text="AVISPA CLP Instance Generator",
            font=self.theme_dict["font_bold"],
            fg=self.theme_dict["text_primary"],
            bg=self.theme_dict["bg_elevated"],
        ).pack(anchor="w")

        tk.Label(
            title_frame,
            text="Generate feasible test instances with integrated MiniZinc validation",
            font=self.theme_dict["font_small"],
            fg=self.theme_dict["text_secondary"],
            bg=self.theme_dict["bg_elevated"],
        ).pack(anchor="w")

        # Right side: Theme toggle
        right = tk.Frame(header, bg=self.theme_dict["bg_elevated"])
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=20, pady=10)

        toggle_text = "🌙 Dark" if ThemeManager.get_mode() == "light" else "☀ Light"
        self.theme_toggle_btn = FlatButton(
            right,
            toggle_text,
            command=self._toggle_theme,
            theme=self.theme_dict,
            accent=False,
        )
        self.theme_toggle_btn.pack()

    def _build_parameters_section(self, parent: tk.Widget) -> None:
        """Build the parameters configuration section."""
        # Section header
        SectionLabel(parent, "Parameters", self.theme_dict).pack(anchor="w", pady=(0, 12))

        # Parameters frame
        params_frame = tk.Frame(parent, bg=self.theme_dict["bg_elevated"])
        params_frame.pack(fill=tk.X, pady=(0, 16))

        # Buses parameter
        buses_frame = tk.Frame(params_frame, bg=self.theme_dict["bg_elevated"])
        buses_frame.pack(fill=tk.X, padx=12, pady=8)

        tk.Label(
            buses_frame,
            text="Number of Buses:",
            font=self.theme_dict["font_ui"],
            fg=self.theme_dict["text_primary"],
            bg=self.theme_dict["bg_elevated"],
            width=20,
            anchor="w",
        ).pack(side=tk.LEFT)

        self.buses_var = tk.IntVar(value=5)
        self.buses_spinbox = tk.Spinbox(
            buses_frame,
            from_=2,
            to=20,
            textvariable=self.buses_var,
            font=self.theme_dict["font_ui"],
            bg=self.theme_dict["bg_elevated"],
            fg=self.theme_dict["text_primary"],
            insertbackground=self.theme_dict["accent_primary"],
            relief=tk.FLAT,
            bd=1,
            width=6,
        )
        self.buses_spinbox.pack(side=tk.LEFT, padx=8)

        # Stations parameter
        stations_frame = tk.Frame(params_frame, bg=self.theme_dict["bg_elevated"])
        stations_frame.pack(fill=tk.X, padx=12, pady=8)

        tk.Label(
            stations_frame,
            text="Number of Stations:",
            font=self.theme_dict["font_ui"],
            fg=self.theme_dict["text_primary"],
            bg=self.theme_dict["bg_elevated"],
            width=20,
            anchor="w",
        ).pack(side=tk.LEFT)

        self.stations_var = tk.IntVar(value=10)
        self.stations_spinbox = tk.Spinbox(
            stations_frame,
            from_=4,
            to=25,
            textvariable=self.stations_var,
            font=self.theme_dict["font_ui"],
            bg=self.theme_dict["bg_elevated"],
            fg=self.theme_dict["text_primary"],
            insertbackground=self.theme_dict["accent_primary"],
            relief=tk.FLAT,
            bd=1,
            width=6,
        )
        self.stations_spinbox.pack(side=tk.LEFT, padx=8)

    def _build_log_section(self, parent: tk.Widget) -> None:
        """Build the generation log display section."""
        # Section header with clear button
        log_header_frame = tk.Frame(parent, bg=self.theme_dict["bg_base"])
        log_header_frame.pack(fill=tk.X, pady=(16, 8))

        SectionLabel(log_header_frame, "Generation Log", self.theme_dict).pack(
            side=tk.LEFT, anchor="w", expand=True
        )

        clear_btn = tk.Label(
            log_header_frame,
            text="[Clear]",
            font=self.theme_dict["font_ui"],
            fg=self.theme_dict["accent_glow"],
            bg=self.theme_dict["bg_base"],
            cursor="hand2",
        )
        clear_btn.pack(side=tk.RIGHT, anchor="e")
        clear_btn.bind("<Button-1>", lambda _: self._clear_log())

        # Log text widget
        log_frame = tk.Frame(parent, bg=self.theme_dict["bg_base"])
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 16))

        self.log_text = tk.Text(
            log_frame,
            height=15,
            width=90,
            bg=self.theme_dict["bg_elevated"],
            fg=self.theme_dict["text_code"],
            font=self.theme_dict["font_mono"],
            relief=tk.FLAT,
            bd=0,
            insertbackground=self.theme_dict["accent_primary"],
        )
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)

        # Configure log text tags for colored output
        self.log_text.tag_configure(
            "success",
            foreground=self.theme_dict["success"],
            font=(self.theme_dict["font_mono"][0], self.theme_dict["font_mono"][1], "bold"),
        )
        self.log_text.tag_configure(
            "error",
            foreground=self.theme_dict["error"],
            font=(self.theme_dict["font_mono"][0], self.theme_dict["font_mono"][1], "bold"),
        )
        self.log_text.tag_configure("warning", foreground=self.theme_dict["warning"])
        self.log_text.tag_configure("info", foreground=self.theme_dict["accent_glow"])
        self.log_text.tag_configure("muted", foreground=self.theme_dict["text_muted"])

    def _build_controls_section(self, parent: tk.Widget) -> None:
        """Build the control buttons section."""
        controls = tk.Frame(parent, bg=self.theme_dict["bg_base"])
        controls.pack(fill=tk.X)

        Divider(controls, self.theme_dict).pack(fill=tk.X, pady=(0, 12))

        # Button row
        btn_frame = tk.Frame(controls, bg=self.theme_dict["bg_base"])
        btn_frame.pack(fill=tk.X, anchor="w")

        self.generate_btn = FlatButton(
            btn_frame,
            "Generate & Validate",
            command=self._start_generation,
            theme=self.theme_dict,
            accent=True,
        )
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 8), fill=tk.X, expand=True)

        self.stop_btn = FlatButton(
            btn_frame,
            "Stop",
            command=self._stop_generation,
            theme=self.theme_dict,
            accent=False,
            disabled=True,
        )
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 8), fill=tk.X, expand=True)

        clear_btn = FlatButton(
            btn_frame,
            "Clear Log",
            command=self._clear_log,
            theme=self.theme_dict,
            accent=False,
        )
        clear_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def _build_footer(self, parent: tk.Widget) -> None:
        """Build the footer with project info."""
        footer = tk.Frame(parent, bg=self.theme_dict["bg_surface"], height=40)
        footer.pack(fill=tk.X, padx=0, pady=0)
        footer.pack_propagate(False)

        tk.Label(
            footer,
            text="AVISPA Research · CLP Instance Generation",
            font=self.theme_dict["font_small"],
            fg=self.theme_dict["text_secondary"],
            bg=self.theme_dict["bg_surface"],
        ).pack(side=tk.LEFT, padx=12, pady=8)

        tk.Label(
            footer,
            text="v1.3.0",
            font=self.theme_dict["font_small"],
            fg=self.theme_dict["text_muted"],
            bg=self.theme_dict["bg_surface"],
        ).pack(side=tk.RIGHT, padx=12, pady=8)

    def _apply_ttk_theme(self) -> None:
        """Apply TTK styling based on current theme."""
        style = ttk.Style(self.root)
        style.theme_use("clam")

        # Scrollbar styling
        style.configure(
            "Dark.Vertical.TScrollbar",
            background=self.theme_dict["bg_elevated"],
            troughcolor=self.theme_dict["bg_surface"],
            bordercolor=self.theme_dict["bg_surface"],
            arrowcolor=self.theme_dict["text_muted"],
            width=8,
            relief="flat",
        )

    def _on_back_click(self) -> None:
        """Handle back button click - return to Orchestrator."""
        return_to_orchestrator(self.root)

    def _toggle_theme(self) -> None:
        """Toggle between dark and light theme modes."""
        current_mode = ThemeManager.get_mode()
        new_mode = "light" if current_mode == "dark" else "dark"
        ThemeManager.set_mode(new_mode)

    def _refresh_ui_colors(self) -> None:
        """Refresh UI colors after theme change."""
        # Destruir todo
        for widget in self.winfo_children():
            widget.destroy()

        # Reconstruir UI con nuevo tema
        self._build_ui()
        self._apply_ttk_theme()
    

    def _log(self, message: str, tag: str = "muted") -> None:
        """Add a message to the generation log."""
        self.log_text.insert(tk.END, message + "\n", tag)
        self.log_text.see(tk.END)
        self.log_text.update()

    def _clear_log(self) -> None:
        """Clear the generation log."""
        self.log_text.delete("1.0", tk.END)

    def _start_generation(self) -> None:
        """Start the instance generation process."""
        buses = self.buses_var.get()
        stations = self.stations_var.get()

        if buses < 2 or buses > 20 or stations < 4 or stations > 25:
            messagebox.showwarning(
                "Invalid Parameters",
                "Buses: 2-20, Stations: 4-25"
            )
            return

        self._log(f"Starting generation: {buses} buses, {stations} stations", "info")
        self.generate_btn.set_disabled(True)
        self.stop_btn.set_disabled(False)
        self.is_generating = True

        self.generation_thread = threading.Thread(
            target=self._run_generation,
            args=(buses, stations),
            daemon=True
        )
        self.generation_thread.start()

    def _run_generation(self, buses: int, stations: int) -> None:
        """Run generation in background thread."""
        try:
            self._log(f"Generating instance with {buses} buses and {stations} stations...", "info")
            result = self.orchestrator.generate_and_validate(buses, stations)

            if result.get("success"):
                self._log("Generation completed successfully!", "success")
                self._log(f"Instance saved: {result.get('filename', 'unknown')}", "success")
            else:
                error_msg = result.get("error", "Unknown error")
                self._log(f"Generation failed: {error_msg}", "error")

        except Exception as e:
            self._log(f"Exception during generation: {str(e)}", "error")
        finally:
            self.is_generating = False
            self.generate_btn.set_disabled(False)
            self.stop_btn.set_disabled(True)

    def _stop_generation(self) -> None:
        """Stop the currently running generation."""
        self.is_generating = False
        self._log("Generation stopped by user", "warning")
        self.generate_btn.set_disabled(False)
        self.stop_btn.set_disabled(True)


def main():
    """Main entry point for the generator interface."""
    root = tk.Tk()
    app = GeneratorInterface(root)
    root.mainloop()


if __name__ == "__main__":
    main()