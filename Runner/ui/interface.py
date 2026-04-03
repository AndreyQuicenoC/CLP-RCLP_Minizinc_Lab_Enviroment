"""
Runner Interface - Professional Tkinter GUI

Clean, aesthetic interface for running CLP/RCLP tests with results display.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import threading
import logging
from typing import Optional

# Import from parent Runner directory
from config import RunnerConfig
from core.executor import MiniZincExecutor
from core.result_handler import ResultHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RunnerInterface:
    """Professional Runner GUI."""

    def __init__(self, root: tk.Tk):
        """Initialize GUI."""
        self.root = root
        self.root.title("CLP Test Runner v1.2.0")
        self.root.geometry("900x700")
        self.root.resizable(False, False)

        self.config = RunnerConfig()
        self.project_root = self._find_project_root()
        self.executor = None
        self.is_running = False

        self._setup_styles()
        self._create_widgets()

    def _find_project_root(self) -> Path:
        """Find project root directory."""
        current = Path(__file__).parent.parent
        while current != current.parent:
            if (current / "Models" / "clp_model.mzn").exists():
                return current
            current = current.parent
        return Path.cwd()

    def _setup_styles(self) -> None:
        """Setup color and style scheme."""
        self.style = ttk.Style()

        # Configure colors
        self.bg_color = self.config.COLOR_GRAY
        self.root.configure(bg=self.bg_color)

        # Frame style
        self.style.configure(
            "Main.TFrame",
            background=self.bg_color
        )

        # Label style
        self.style.configure(
            "Title.TLabel",
            background=self.bg_color,
            foreground=self.config.COLOR_DARK_BLUE,
            font=(self.config.FONT_FAMILY, self.config.FONT_SIZE_TITLE, "bold")
        )

        self.style.configure(
            "Header.TLabel",
            background=self.bg_color,
            foreground=self.config.COLOR_DARK_BLUE,
            font=(self.config.FONT_FAMILY, self.config.FONT_SIZE_HEADER)
        )

        self.style.configure(
            "Normal.TLabel",
            background=self.bg_color,
            foreground=self.config.COLOR_TEXT_PRIMARY,
            font=(self.config.FONT_FAMILY, self.config.FONT_SIZE_NORMAL)
        )

    def _create_widgets(self) -> None:
        """Create and layout all widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, style="Main.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Title
        title = ttk.Label(main_frame, text="CLP/RCLP Test Runner", style="Title.TLabel")
        title.pack(anchor=tk.W, pady=(0, 20))

        # Directory section
        self._create_directory_section(main_frame)

        # File section
        self._create_file_section(main_frame)

        # Model section
        self._create_model_section(main_frame)

        # Control buttons
        self._create_control_section(main_frame)

        # Status and results
        self._create_results_section(main_frame)

    def _create_directory_section(self, parent: ttk.Frame) -> None:
        """Create directory selector section."""
        label = ttk.Label(parent, text="Select Test Directory:", style="Header.TLabel")
        label.pack(anchor=tk.W, pady=(10, 5))

        dir_frame = ttk.Frame(parent, style="Main.TFrame")
        dir_frame.pack(fill=tk.X, pady=(0, 10))

        self.dir_var = tk.StringVar(value=self.config.DATA_DIRECTORIES[0])
        dir_combo = ttk.Combobox(
            dir_frame,
            textvariable=self.dir_var,
            values=self.config.DATA_DIRECTORIES,
            state="readonly",
            width=50
        )
        dir_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        dir_combo.bind("<<ComboboxSelected>>", lambda e: self._on_directory_changed())

    def _create_file_section(self, parent: ttk.Frame) -> None:
        """Create file selector section."""
        label = ttk.Label(parent, text="Select Test Instance:", style="Header.TLabel")
        label.pack(anchor=tk.W, pady=(10, 5))

        file_frame = ttk.Frame(parent, style="Main.TFrame")
        file_frame.pack(fill=tk.X, pady=(0, 10))

        self.file_var = tk.StringVar()
        file_combo = ttk.Combobox(
            file_frame,
            textvariable=self.file_var,
            state="readonly",
            width=50
        )
        file_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.file_combo = file_combo

        # Refresh button
        refresh_btn = ttk.Button(
            file_frame,
            text="Refresh",
            command=self._refresh_files,
            width=10
        )
        refresh_btn.pack(side=tk.LEFT, padx=(5, 0))

        self._refresh_files()

    def _create_model_section(self, parent: ttk.Frame) -> None:
        """Create model selector section."""
        label = ttk.Label(parent, text="Select Model:", style="Header.TLabel")
        label.pack(anchor=tk.W, pady=(10, 5))

        model_frame = ttk.Frame(parent, style="Main.TFrame")
        model_frame.pack(fill=tk.X, pady=(0, 15))

        self.model_var = tk.StringVar(value="clp")

        for model in self.config.MODELS:
            rb = ttk.Radiobutton(
                model_frame,
                text=model.upper(),
                variable=self.model_var,
                value=model
            )
            rb.pack(side=tk.LEFT, padx=10)

    def _create_control_section(self, parent: ttk.Frame) -> None:
        """Create execution buttons."""
        button_frame = ttk.Frame(parent, style="Main.TFrame")
        button_frame.pack(fill=tk.X, pady=(0, 15))

        # Run button
        self.run_btn = tk.Button(
            button_frame,
            text="Run Test",
            command=self._run_test,
            bg=self.config.COLOR_DARK_BLUE,
            fg=self.config.COLOR_WHITE,
            font=(self.config.FONT_FAMILY, 10, "bold"),
            width=15,
            height=2
        )
        self.run_btn.pack(side=tk.LEFT, padx=5)

        # Stop button (disabled initially)
        self.stop_btn = tk.Button(
            button_frame,
            text="Stop",
            command=self._stop_test,
            bg="#808080",
            fg=self.config.COLOR_WHITE,
            font=(self.config.FONT_FAMILY, 10),
            width=15,
            height=2,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)

    def _create_results_section(self, parent: ttk.Frame) -> None:
        """Create results display section."""
        label = ttk.Label(parent, text="Results:", style="Header.TLabel")
        label.pack(anchor=tk.W, pady=(10, 5))

        # Results text widget with scrollbar
        frame = ttk.Frame(parent, style="Main.TFrame")
        frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.results_text = tk.Text(
            frame,
            height=15,
            width=100,
            bg=self.config.COLOR_WHITE,
            fg=self.config.COLOR_TEXT_PRIMARY,
            yscrollcommand=scrollbar.set,
            font=(self.config.FONT_FAMILY, 9)
        )
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.results_text.yview)

    def _on_directory_changed(self) -> None:
        """Update file list when directory changes."""
        self._refresh_files()

    def _refresh_files(self) -> None:
        """Refresh list of .dzn files in selected directory."""
        try:
            dir_name = self.dir_var.get()
            dir_path = self.project_root / dir_name

            if not dir_path.exists():
                self.file_combo['values'] = []
                return

            dzn_files = sorted([
                f.stem for f in dir_path.glob("*.dzn")
                if not f.stem.endswith("_meta")
            ])

            self.file_combo['values'] = dzn_files
            if dzn_files:
                self.file_combo.current(0)

        except Exception as e:
            logger.error(f"Error refreshing files: {str(e)}")

    def _run_test(self) -> None:
        """Execute test in background thread."""
        if not self.file_var.get():
            messagebox.showwarning("Selection", "Please select a test instance")
            return

        self.is_running = True
        self.run_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)

        # Run in background
        thread = threading.Thread(target=self._execute_test, daemon=True)
        thread.start()

    def _execute_test(self) -> None:
        """Execute test (background thread)."""
        try:
            dir_name = self.dir_var.get()
            file_name = self.file_var.get()
            model = self.model_var.get()

            # Build paths
            dzn_path = self.project_root / dir_name / f"{file_name}.dzn"
            model_path = self.project_root / "Models" / f"{model}_model.mzn"
            output_dir = self.project_root / "Tests" / "Output" / dir_name.split("/")[-1]

            self._log(f"Starting test: {file_name}")
            self._log(f"Directory: {dir_name}")
            self._log(f"Model: {model.upper()}")
            self._log("")

            # Execute
            executor = MiniZincExecutor(str(model_path))
            success, result = executor.execute(str(dzn_path))

            if success and result:
                self._log("[OK] Test PASSED", "success")
                self._log(f"  Buses: {result['num_buses']}")
                self._log(f"  Stations: {result['num_stations']}")
                self._log(f"  Charged: {result['charged_stations']}")
                self._log(f"  Deviation: {result['time_deviation'] / 10} minutes") # Convert back to minutes for display

                # Save results
                handler = ResultHandler(str(output_dir))
                ok, json_path, txt_path = handler.save_results(file_name, result)

                if ok:
                    self._log("")
                    self._log(f"Results saved:")
                    self._log(f"  JSON: {json_path}")
                    self._log(f"  TXT:  {txt_path}")
            else:
                self._log("[ERROR] Test FAILED - UNSATISFIABLE", "error")

        except Exception as e:
            self._log(f"[ERROR] {str(e)}", "error")

        finally:
            self.is_running = False
            self.run_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)

    def _stop_test(self) -> None:
        """Stop execution."""
        self.is_running = False
        self._log("[WARN] Execution stopped", "warning")
        self.run_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

    def _log(self, message: str, level: str = "info") -> None:
        """Add log message to results display."""
        self.results_text.insert(tk.END, f"{message}\n")
        self.results_text.see(tk.END)
        self.root.update()
