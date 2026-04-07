"""
Runner Interface - Professional MiniZinc Test Executor GUI

Premium dark/light mode UI for executing CLP/RCLP test instances with real-time monitoring,
result generation, and professional theme support.

Authors: Andrey Quiceno and Juan Francesco García (AVISPA Team)

Architecture:
- Dynamic theme switching (dark/light modes)
- Modular components from .components module
- TTK-based styling for dropdown/scrollbar consistency
- Two-panel layout: Config (left) + Results (right)
- Real-time execution monitoring with status indicators
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from typing import Dict, Any, Literal, Optional, Callable
import threading
import logging

# Import modular theme system
from .themes import ThemeManager, get_theme_dict, DARK_PALETTE, LIGHT_PALETTE
from .components import SectionLabel, FlatButton, Divider, StatusIndicator
from .layouts import LayoutBuilder, LayoutConfig

# Import Runner core modules
try:
    from config import RunnerConfig
    from core.executor import MiniZincExecutor
    from core.result_handler import ResultHandler
except ImportError:
    from ..config import RunnerConfig
    from ..core.executor import MiniZincExecutor
    from ..core.result_handler import ResultHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RunnerInterface(tk.Frame):
    """Professional MiniZinc test runner interface with theme switching support."""

    def __init__(self, root: tk.Tk):
        """
        Initialize the Runner interface.

        Sets up theming, observes theme changes, builds UI, and applies styling.
        """
        super().__init__(root)
        self.root = root
        self.master = root
        self.pack(fill=tk.BOTH, expand=True)

        # Initialize theme system
        self._init_theme()

        # Setup window properties
        self.root.title("CLP-RCLP Test Runner v1.3.0")
        self.root.geometry("850x650")
        self.root.resizable(False, False)
        self.configure(bg=self.theme_dict["bg_base"])

        # Initialize core modules
        self.executor: Optional[MiniZincExecutor] = None
        self.result_handler: Optional[ResultHandler] = None
        self.execution_thread: Optional[threading.Thread] = None
        self.is_running = False

        # Find project root for file operations
        self.project_root = self._find_project_root()

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

    def _find_project_root(self) -> str:
        """Find the CLP-RCLP Minizinc project root directory."""
        current = Path(__file__).parent.absolute()
        while current.name != "CLP-RCLP Minizinc" and current.parent != current:
            current = current.parent
        return str(current) if current.name == "CLP-RCLP Minizinc" else str(Path(__file__).parent.parent.parent)

    def _build_ui(self) -> None:
        """Build the complete user interface with two-panel layout."""
        # Main container
        container = tk.Frame(self, bg=self.theme_dict["bg_base"])
        container.pack(fill=tk.BOTH, expand=True)

        # Header
        self._build_header(container)

        # Content area (two panels)
        content = tk.Frame(container, bg=self.theme_dict["bg_base"])
        content.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)

        # Left panel (config)
        self._build_left_panel(content)

        # Right panel (results)
        self._build_right_panel(content)

        # Footer
        self._build_footer(container)

    def _build_header(self, parent: tk.Widget) -> None:
        """Build the header with title and status indicator."""
        header = tk.Frame(parent, bg=self.theme_dict["bg_surface"], height=70)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)

        # Left side: Title with accent bar
        left = tk.Frame(header, bg=self.theme_dict["bg_surface"])
        left.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=20, pady=15)

        tk.Frame(left, bg=self.theme_dict["accent_primary"], width=4, height=24).pack(
            side=tk.LEFT, padx=(0, 12)
        )

        tk.Label(
            left,
            text="CLP-RCLP TEST RUNNER",
            font=self.theme_dict["font_bold"],
            fg=self.theme_dict["text_primary"],
            bg=self.theme_dict["bg_surface"],
        ).pack(side=tk.LEFT)

        # Right side: Status and theme toggle
        right = tk.Frame(header, bg=self.theme_dict["bg_surface"])
        right.pack(side=tk.RIGHT, fill=tk.Y, padx=20, pady=10)

        # StatusIndicator (modular component)
        self.status_indicator = StatusIndicator(right, "Ready", self.theme_dict)
        self.status_indicator.pack(side=tk.LEFT, padx=(0, 16))

        # Theme toggle button
        toggle_text = "🌙 Dark" if ThemeManager.get_mode() == "light" else "☀ Light"
        self.theme_toggle_btn = FlatButton(
            right,
            toggle_text,
            command=self._toggle_theme,
            theme=self.theme_dict,
            accent=False,
        )
        self.theme_toggle_btn.pack(side=tk.LEFT)

    def _build_left_panel(self, parent: tk.Widget) -> None:
        """Build left configuration panel."""
        left_panel = tk.Frame(parent, bg=self.theme_dict["bg_surface"], width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        left_panel.pack_propagate(False)

        # Scrollable content area
        canvas = tk.Canvas(
            left_panel,
            bg=self.theme_dict["bg_surface"],
            highlightthickness=0,
            bd=0,
        )
        scrollbar = ttk.Scrollbar(
            left_panel, orient=tk.VERTICAL, command=canvas.yview
        )
        scrollable_frame = tk.Frame(canvas, bg=self.theme_dict["bg_surface"])
        scrollable_frame.bind(
            "<Configure>",
            lambda _: canvas.configure(scrollregion=canvas.bbox("all")),
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Config card
        card = tk.Frame(
            scrollable_frame,
            bg=self.theme_dict["bg_elevated"],
            relief=tk.FLAT,
            bd=0,
        )
        card.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        # Directory selection
        SectionLabel(card, "Directory", self.theme_dict).pack(anchor="w", padx=12, pady=(14, 6))
        self.dir_var = tk.StringVar()
        dirs = ["Battery Own", "Battery Generated", "Battery Project Integer", "Battery Project Variant"]
        self.dir_combo = ttk.Combobox(
            card,
            textvariable=self.dir_var,
            values=dirs,
            state="readonly",
            style="Dark.TCombobox",
        )
        self.dir_combo.current(0)
        self.dir_combo.pack(fill=tk.X, padx=12, pady=(0, 12))

        Divider(card, self.theme_dict).pack(fill=tk.X, padx=12, pady=12)

        # Test instance selection
        SectionLabel(card, "Instance", self.theme_dict).pack(anchor="w", padx=12, pady=(0, 6))
        inst_frame = tk.Frame(card, bg=self.theme_dict["bg_elevated"])
        inst_frame.pack(fill=tk.X, padx=12, pady=(0, 12))

        self.instance_var = tk.StringVar()
        self.instance_combo = ttk.Combobox(
            inst_frame,
            textvariable=self.instance_var,
            state="readonly",
            style="Dark.TCombobox",
            width=25,
        )
        self.instance_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)

        refresh_btn = FlatButton(inst_frame, "Refresh", command=self._refresh_instances,
                                theme=self.theme_dict, accent=False)
        refresh_btn.pack(side=tk.LEFT, padx=(6, 0))

        Divider(card, self.theme_dict).pack(fill=tk.X, padx=12, pady=12)

        # Model selection
        SectionLabel(card, "Model", self.theme_dict).pack(anchor="w", padx=12, pady=(0, 8))
        self.model_var = tk.StringVar(value="CLP")

        model_frame = tk.Frame(card, bg=self.theme_dict["bg_elevated"])
        model_frame.pack(fill=tk.X, padx=12, pady=(0, 12))

        for model in ["CLP", "RCLP"]:
            rb = tk.Radiobutton(
                model_frame,
                text=model,
                variable=self.model_var,
                value=model,
                bg=self.theme_dict["bg_elevated"],
                fg=self.theme_dict["text_primary"],
                selectcolor=self.theme_dict["accent_primary"],
                activebackground=self.theme_dict["bg_hover"],
            )
            rb.pack(side=tk.LEFT, padx=8)

        Divider(card, self.theme_dict).pack(fill=tk.X, padx=12, pady=12)

        # Action buttons
        btn_frame = tk.Frame(card, bg=self.theme_dict["bg_elevated"])
        btn_frame.pack(fill=tk.X, padx=12, pady=(0, 12))

        self.run_btn = FlatButton(
            btn_frame,
            "Run Test",
            command=self._start_execution,
            theme=self.theme_dict,
            accent=True,
        )
        self.run_btn.pack(fill=tk.X, pady=(0, 8))

        self.stop_btn = FlatButton(
            btn_frame,
            "Stop",
            command=self._stop_execution,
            theme=self.theme_dict,
            accent=False,
            disabled=True,
        )
        self.stop_btn.pack(fill=tk.X)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _build_right_panel(self, parent: tk.Widget) -> None:
        """Build right results display panel."""
        right_panel = tk.Frame(parent, bg=self.theme_dict["bg_base"])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Output log header
        log_header = tk.Frame(right_panel, bg=self.theme_dict["bg_surface"], height=40)
        log_header.pack(fill=tk.X, padx=12, pady=(12, 0))
        log_header.pack_propagate(False)

        tk.Label(
            log_header,
            text="OUTPUT LOG",
            font=self.theme_dict["font_section"],
            fg=self.theme_dict["text_secondary"],
            bg=self.theme_dict["bg_surface"],
        ).pack(side=tk.LEFT, anchor="w")

        clear_btn = tk.Label(
            log_header,
            text="[Clear]",
            font=self.theme_dict["font_ui"],
            fg=self.theme_dict["accent_glow"],
            bg=self.theme_dict["bg_surface"],
            cursor="hand2",
        )
        clear_btn.pack(side=tk.RIGHT, anchor="e")
        clear_btn.bind("<Button-1>", lambda _: self._clear_log())

        # Log display
        wrap = tk.Frame(right_panel, bg=self.theme_dict["bg_base"])
        wrap.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        self.log_text = tk.Text(
            wrap,
            height=25,
            width=60,
            bg=self.theme_dict["bg_elevated"],
            fg=self.theme_dict["text_code"],
            font=self.theme_dict["font_mono"],
            relief=tk.FLAT,
            bd=0,
            insertbackground=self.theme_dict["accent_primary"],
        )
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(wrap, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)

        # Configure log text tags for colored output
        self.log_text.tag_configure("success", foreground=self.theme_dict["success"], font=(self.theme_dict["font_mono"][0], self.theme_dict["font_mono"][1], "bold"))
        self.log_text.tag_configure("error", foreground=self.theme_dict["error"], font=(self.theme_dict["font_mono"][0], self.theme_dict["font_mono"][1], "bold"))
        self.log_text.tag_configure("warning", foreground=self.theme_dict["warning"])
        self.log_text.tag_configure("info", foreground=self.theme_dict["accent_glow"])
        self.log_text.tag_configure("muted", foreground=self.theme_dict["text_muted"])
        self.log_text.tag_configure("key", foreground=self.theme_dict["text_secondary"])
        self.log_text.tag_configure("value", foreground=self.theme_dict["accent_glow"])

    def _build_footer(self, parent: tk.Widget) -> None:
        """Build the footer with project info."""
        footer = tk.Frame(parent, bg=self.theme_dict["bg_surface"], height=40)
        footer.pack(fill=tk.X, padx=0, pady=0)
        footer.pack_propagate(False)

        tk.Label(
            footer,
            text="MiniZinc Test Executor · CLP/RCLP Solver",
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

        # Combobox styling
        style.configure(
            "Dark.TCombobox",
            fieldbackground=self.theme_dict["bg_elevated"],
            background=self.theme_dict["bg_elevated"],
            foreground=self.theme_dict["text_primary"],
            selectbackground=self.theme_dict["accent_dim"],
            selectforeground=self.theme_dict["text_primary"],
            bordercolor=self.theme_dict["border_normal"],
            darkcolor=self.theme_dict["bg_elevated"],
            lightcolor=self.theme_dict["bg_elevated"],
            arrowcolor=self.theme_dict["text_secondary"],
            padding=(10, 6),
            font=self.theme_dict["font_ui"],
            relief="flat",
        )
        style.map(
            "Dark.TCombobox",
            fieldbackground=[("focus", self.theme_dict["bg_elevated"])],
            bordercolor=[("focus", self.theme_dict["border_active"])],
            foreground=[("disabled", self.theme_dict["text_muted"])],
        )

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

    def _toggle_theme(self) -> None:
        """Toggle between dark and light theme modes."""
        current_mode = ThemeManager.get_mode()
        new_mode = "light" if current_mode == "dark" else "dark"
        ThemeManager.set_mode(new_mode)

    def _refresh_ui_colors(self) -> None:
        """Refresh all UI colors after theme change (full UI rebuild recommended)."""
        # Update backgrounds
        self.configure(bg=self.theme_dict["bg_base"])
        self.root.configure(bg=self.theme_dict["bg_base"])

        # Update theme toggle button text
        toggle_text = "☀ Light" if ThemeManager.get_mode() == "dark" else "🌙 Dark"
        self.theme_toggle_btn.configure(text=toggle_text)

        # For comprehensive color update, UI rebuild would be ideal
        # This is a simplified approach; full refresh requires widget tree traversal

    def _refresh_instances(self) -> None:
        """Refresh the list of available test instances."""
        directory = self.dir_var.get()
        if not directory:
            return

        data_path = Path(self.project_root) / "Data" / directory
        instances = sorted([f.stem for f in data_path.glob("*.dzn")]) if data_path.exists() else []

        self.instance_combo["values"] = instances
        if instances:
            self.instance_combo.current(0)

        self._log(f"Found {len(instances)} instances in {directory}", "info")

    def _log(self, message: str, tag: str = "muted") -> None:
        """Add a message to the output log."""
        self.log_text.insert(tk.END, message + "\n", tag)
        self.log_text.see(tk.END)

    def _clear_log(self) -> None:
        """Clear the output log."""
        self.log_text.delete("1.0", tk.END)

    def _start_execution(self) -> None:
        """Start execution of the selected test instance."""
        instance = self.instance_var.get()
        model = self.model_var.get()
        directory = self.dir_var.get()

        if not instance or not model or not directory:
            messagebox.showwarning("Missing Selection", "Please select directory, instance, and model.")
            return

        self._log(f"Starting execution: {instance} ({model})", "info")
        self.status_indicator.set_status("running", "Running...")
        self.run_btn.set_disabled(True)
        self.stop_btn.set_disabled(False)
        self.is_running = True

        self.execution_thread = threading.Thread(
            target=self._execute_test,
            args=(directory, instance, model),
            daemon=True
        )
        self.execution_thread.start()

    def _execute_test(self, directory: str, instance: str, model: str) -> None:
        """Execute test in background thread."""
        try:
            config = RunnerConfig()
            executor = MiniZincExecutor(config)

            data_path = Path(self.project_root) / "Data" / directory
            instance_path = data_path / f"{instance}.dzn"

            if not instance_path.exists():
                self._log(f"Instance not found: {instance_path}", "error")
                self.status_indicator.set_status("error", "Error")
                return

            self._log(f"Executing: {model} solver on {instance}", "key")
            result = executor.execute(str(instance_path), model)

            if result["success"]:
                self._log("Execution completed successfully", "success")
                self.status_indicator.set_status("success", "Success")
                handler = ResultHandler(str(Path(self.project_root) / "Tests" / "Output"))
                handler.save_results(instance, result, directory)
            else:
                self._log(f"Execution failed: {result.get('error', 'Unknown error')}", "error")
                self.status_indicator.set_status("error", "Error")

        except Exception as e:
            self._log(f"Exception during execution: {e}", "error")
            self.status_indicator.set_status("error", "Error")
        finally:
            self.is_running = False
            self.run_btn.set_disabled(False)
            self.stop_btn.set_disabled(True)
            self.status_indicator.set_status("idle", "Ready")

    def _stop_execution(self) -> None:
        """Stop the currently running test execution."""
        if self.is_running:
            self._log("Execution stopped by user", "warning")
            self.is_running = False
            self.run_btn.set_disabled(False)
            self.stop_btn.set_disabled(True)
            self.status_indicator.set_status("idle", "Ready")
