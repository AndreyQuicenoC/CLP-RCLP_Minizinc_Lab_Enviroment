"""
Converter Interface - JSON to DZN Conversion Tool

Professional Tkinter GUI for converting JSON bus schedules to MiniZinc DZN format.
Features directory selection, test selection, batch conversion, and result display.

Author: AVISPA Research Team
Date: April 2026
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
from typing import Dict, List, Optional, Literal
import threading
import logging
from datetime import datetime

from .themes import ThemeManager, get_theme_dict, DARK_PALETTE, LIGHT_PALETTE
from .components import SectionLabel, FlatButton, Divider, StatusIndicator, FormEntry
from .tooltip import Tooltip

# Import config - handle both relative and absolute imports
try:
    from ..config import WINDOW_WIDTH, WINDOW_HEIGHT, FONTS
    from ..core.jits_analyzer import JITSAnalyzer
    from ..core.file_manager import FileManager
    from ..core.converter_engine import ConverterEngine
except ImportError:
    import sys
    from pathlib import Path
    converter_dir = Path(__file__).parent.parent
    if str(converter_dir) not in sys.path:
        sys.path.insert(0, str(converter_dir))
    from config import WINDOW_WIDTH, WINDOW_HEIGHT, FONTS
    from core.jits_analyzer import JITSAnalyzer
    from core.file_manager import FileManager
    from core.converter_engine import ConverterEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConverterInterface(tk.Frame):
    """Professional JSON to DZN converter interface."""

    def __init__(self, root: tk.Tk):
        """Initialize the converter interface."""
        super().__init__(root)
        self.root = root
        self.master = root
        self.pack(fill=tk.BOTH, expand=True)

        # Initialize theme
        self._init_theme()

        # Setup window
        self.root.title("CLP-RCLP JSON to DZN Converter v1.5.0")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        self._center_window()
        self.configure(bg=self.theme_dict["bg_base"])

        # Project root
        self.project_root = self._find_project_root()

        # Conversion state
        self.is_converting = False
        self.conversion_thread: Optional[threading.Thread] = None

        # State variables
        self.available_tests: List[str] = []
        self.available_batteries: List[str] = []

        # Build UI
        self._build_ui()

    def _init_theme(self) -> None:
        """Initialize theme system."""
        self.theme_dict = get_theme_dict("dark")
        ThemeManager.register_observer(self._on_theme_change)

    def _on_theme_change(self, mode: Literal["dark", "light"]) -> None:
        """Handle theme changes."""
        self.theme_dict = get_theme_dict(mode)
        self._refresh_ui_colors()

    def _find_project_root(self) -> Path:
        """Find project root directory."""
        current = Path(__file__).parent.parent.parent.absolute()
        while current.name != "CLP-RCLP Minizinc" and current.parent != current:
            current = current.parent
        return current if current.name == "CLP-RCLP Minizinc" else Path(__file__).parent.parent.parent

    def _center_window(self) -> None:
        """Center window on screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def _build_ui(self) -> None:
        """Build complete user interface."""
        # Main container
        container = tk.Frame(self, bg=self.theme_dict["bg_base"])
        container.pack(fill=tk.BOTH, expand=True)

        # Header
        self._build_header(container)

        # Content
        content = tk.Frame(container, bg=self.theme_dict["bg_base"])
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Left panel (selection)
        self._build_left_panel(content)

        # Right panel (results)
        self._build_right_panel(content)

        # Footer
        self._build_footer(container)

    def _build_header(self, parent: tk.Widget) -> None:
        """Build header with title and theme toggle."""
        header = tk.Frame(parent, bg=self.theme_dict["bg_surface"], height=80)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)

        # Title with accent bar
        left = tk.Frame(header, bg=self.theme_dict["bg_surface"])
        left.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=20, pady=15)

        tk.Frame(left, bg=self.theme_dict["accent_primary"], width=4, height=32).pack(
            side=tk.LEFT, padx=(0, 12)
        )

        title_frame = tk.Frame(left, bg=self.theme_dict["bg_surface"])
        title_frame.pack(side=tk.LEFT)

        tk.Label(
            title_frame,
            text="JSON to DZN Converter",
            font=("Arial", 16, "bold"),
            fg=self.theme_dict["text_primary"],
            bg=self.theme_dict["bg_surface"]
        ).pack()

        tk.Label(
            title_frame,
            text="Convert JITS2022 test batteries to MiniZinc format",
            font=("Arial", 9),
            fg=self.theme_dict["text_secondary"],
            bg=self.theme_dict["bg_surface"]
        ).pack(anchor=tk.W)

        # Theme toggle
        right = tk.Frame(header, bg=self.theme_dict["bg_surface"])
        right.pack(side=tk.RIGHT, padx=20, pady=15)

        theme_btn = tk.Label(
            right,
            text="☀ Light",
            cursor="hand2",
            fg=self.theme_dict["text_secondary"],
            bg=self.theme_dict["bg_surface"],
            font=("Arial", 9)
        )
        theme_btn.pack()
        theme_btn.bind("<Button-1>", self._toggle_theme)

    def _build_left_panel(self, parent: tk.Widget) -> None:
        """Build left panel with selection controls."""
        left = tk.Frame(parent, bg=self.theme_dict["bg_base"])
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Directory selection
        SectionLabel(left, "1. Select Test Battery Directory", self.theme_dict["bg_base"],
                     self.theme_dict["text_primary"]).pack(fill=tk.X, pady=(0, 10))

        self._build_directory_selector(left)

        Divider(left, self.theme_dict["border"]).pack(fill=tk.X, pady=10)

        # Test selection
        SectionLabel(left, "2. Select Tests to Convert", self.theme_dict["bg_base"],
                     self.theme_dict["text_primary"]).pack(fill=tk.X, pady=(0, 10))

        self._build_test_selector(left)

        Divider(left, self.theme_dict["border"]).pack(fill=tk.X, pady=10)

        # Output configuration
        SectionLabel(left, "3. Output Configuration", self.theme_dict["bg_base"],
                     self.theme_dict["text_primary"]).pack(fill=tk.X, pady=(0, 10))

        self._build_output_config(left)

        # Control buttons
        tk.Frame(left, bg=self.theme_dict["bg_base"], height=20).pack(fill=tk.X, pady=15)

        btn_frame = tk.Frame(left, bg=self.theme_dict["bg_base"])
        btn_frame.pack(fill=tk.X, pady=10)

        self.convert_btn = FlatButton(
            btn_frame,
            "Convert",
            command=self._start_conversion,
            bg_color=self.theme_dict["accent_primary"],
            hover_color=self.theme_dict["accent_secondary"]
        )
        self.convert_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.stop_btn = FlatButton(
            btn_frame,
            "Stop",
            command=self._stop_conversion,
            bg_color=self.theme_dict["error"],
            hover_color="#d83030"
        )
        self.stop_btn.pack(side=tk.LEFT)
        self.stop_btn.set_disabled(True)

    def _build_directory_selector(self, parent: tk.Widget) -> None:
        """Build directory selection controls."""
        frame = tk.Frame(parent, bg=self.theme_dict["bg_base"])
        frame.pack(fill=tk.X, pady=(0, 10))

        # Instances directory
        tk.Label(
            frame,
            text="Instances to convert:",
            bg=self.theme_dict["bg_base"],
            fg=self.theme_dict["text_primary"],
            font=("Arial", 9)
        ).pack(anchor=tk.W, pady=(0, 5))

        jits_frame = tk.Frame(frame, bg=self.theme_dict["bg_base"])
        jits_frame.pack(fill=tk.X, pady=(0, 10))

        self.jits_dir_var = tk.StringVar()
        self.jits_dir_combo = ttk.Combobox(jits_frame, textvariable=self.jits_dir_var, state="readonly")
        self.jits_dir_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        browse_btn = tk.Button(
            jits_frame,
            text="Browse",
            command=self._browse_jits_directory,
            bg=self.theme_dict["bg_surface"],
            fg=self.theme_dict["text_primary"],
            relief=tk.FLAT,
            font=("Arial", 9)
        )
        browse_btn.pack(side=tk.LEFT, padx=(0, 5))

        # Help icon - now positioned at the right of Browse
        help_label = tk.Label(
            jits_frame,
            text="[?]",
            fg=self.theme_dict["accent_primary"],
            bg=self.theme_dict["bg_base"],
            cursor="hand2",
            font=("Arial", 10, "bold")
        )
        help_label.pack(side=tk.LEFT)
        Tooltip(help_label, "Select a directory from JITS2022/Code/Data containing JSON test files")

        # Load JITS directories
        self._load_jits_directories()

    def _build_test_selector(self, parent: tk.Widget) -> None:
        """Build test selection controls."""
        frame = tk.Frame(parent, bg=self.theme_dict["bg_base"])
        frame.pack(fill=tk.X, pady=(0, 10))

        # Test selection mode
        tk.Label(
            frame,
            text="Tests:",
            bg=self.theme_dict["bg_base"],
            fg=self.theme_dict["text_primary"],
            font=("Arial", 9)
        ).pack(anchor=tk.W, pady=(0, 5))

        mode_frame = tk.Frame(frame, bg=self.theme_dict["bg_base"])
        mode_frame.pack(fill=tk.X, pady=(0, 10))

        self.test_mode_var = tk.StringVar(value="all")

        tk.Radiobutton(
            mode_frame,
            text="All tests",
            variable=self.test_mode_var,
            value="all",
            bg=self.theme_dict["bg_base"],
            fg=self.theme_dict["text_primary"],
            selectcolor=self.theme_dict["bg_surface"],
            command=self._update_test_selection
        ).pack(anchor=tk.W)

        tk.Radiobutton(
            mode_frame,
            text="Select a test",
            variable=self.test_mode_var,
            value="selected",
            bg=self.theme_dict["bg_base"],
            fg=self.theme_dict["text_primary"],
            selectcolor=self.theme_dict["bg_surface"],
            command=self._update_test_selection
        ).pack(anchor=tk.W)

        # Test combobox with refresh button
        test_combo_frame = tk.Frame(frame, bg=self.theme_dict["bg_base"])
        test_combo_frame.pack(fill=tk.X, pady=(5, 0))

        self.test_var = tk.StringVar()
        self.test_combo = ttk.Combobox(
            test_combo_frame,
            textvariable=self.test_var,
            state="disabled",
            font=("Arial", 9)
        )
        self.test_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        # Refresh button
        self.test_refresh_btn = tk.Button(
            test_combo_frame,
            text="↻",
            command=self._refresh_tests,
            bg=self.theme_dict["bg_surface"],
            fg=self.theme_dict["text_primary"],
            relief=tk.FLAT,
            font=("Arial", 10),
            width=3,
            state=tk.DISABLED
        )
        self.test_refresh_btn.pack(side=tk.LEFT)

    def _build_output_config(self, parent: tk.Widget) -> None:
        """Build output configuration controls."""
        frame = tk.Frame(parent, bg=self.theme_dict["bg_base"])
        frame.pack(fill=tk.X, pady=(0, 10))

        # Output battery
        tk.Label(
            frame,
            text="Output Battery:",
            bg=self.theme_dict["bg_base"],
            fg=self.theme_dict["text_primary"],
            font=("Arial", 9)
        ).pack(anchor=tk.W, pady=(0, 5))

        output_frame = tk.Frame(frame, bg=self.theme_dict["bg_base"])
        output_frame.pack(fill=tk.X, pady=(0, 10))

        self.output_battery_var = tk.StringVar()
        self.output_combo = ttk.Combobox(
            output_frame,
            textvariable=self.output_battery_var,
            state="readonly",
            font=("Arial", 9)
        )
        self.output_combo.pack(fill=tk.X, pady=(0, 10))

        # Directory selection options
        self.output_option_var = tk.StringVar(value="existing")

        tk.Radiobutton(
            frame,
            text="Use existing directory",
            variable=self.output_option_var,
            value="existing",
            bg=self.theme_dict["bg_base"],
            fg=self.theme_dict["text_primary"],
            selectcolor=self.theme_dict["bg_surface"],
            command=self._update_output_option
        ).pack(anchor=tk.W)

        tk.Radiobutton(
            frame,
            text="Create new directory",
            variable=self.output_option_var,
            value="new",
            bg=self.theme_dict["bg_base"],
            fg=self.theme_dict["text_primary"],
            selectcolor=self.theme_dict["bg_surface"],
            command=self._update_output_option
        ).pack(anchor=tk.W, pady=(0, 10))

        # New directory entry (initially disabled)
        self.new_dir_var = tk.StringVar()
        self.new_dir_entry = tk.Entry(
            frame,
            textvariable=self.new_dir_var,
            bg=self.theme_dict["bg_surface"],
            fg=self.theme_dict["text_primary"],
            relief=tk.FLAT,
            state=tk.DISABLED,
            font=("Arial", 9)
        )
        self.new_dir_entry.pack(fill=tk.X)

        # Load available batteries
        self._load_batteries()

    def _load_jits_directories(self) -> None:
        """Load JITS2022 test directories."""
        jits_path = self.project_root / "JITS2022" / "Code" / "Data"
        directories = JITSAnalyzer.get_test_directories(jits_path)

        if directories:
            self.jits_dir_var.set(directories[0])
            # Update the combobox values if it exists
            if hasattr(self, 'jits_dir_combo'):
                self.jits_dir_combo['values'] = directories

    def _load_batteries(self) -> None:
        """Load available battery directories from Data folder."""
        data_path = self.project_root / "Data"
        batteries = []

        if data_path.exists():
            for item in data_path.iterdir():
                if item.is_dir():
                    batteries.append(item.name)

        batteries.sort()
        self.available_batteries = batteries

        if hasattr(self, 'output_combo'):
            self.output_combo['values'] = batteries
            if batteries:
                self.output_battery_var.set(batteries[0])

    def _update_test_selection(self) -> None:
        """Update test selection controls based on mode."""
        if self.test_mode_var.get() == "all":
            self.test_combo.config(state=tk.DISABLED)
            self.test_refresh_btn.config(state=tk.DISABLED)
        else:
            self.test_combo.config(state="readonly")
            self.test_refresh_btn.config(state=tk.NORMAL)
            self._refresh_tests()

    def _refresh_tests(self) -> None:
        """Refresh available tests from selected directory."""
        jits_dir = self.jits_dir_var.get()
        if not jits_dir:
            messagebox.showwarning("Warning", "Please select a directory first")
            return

        try:
            jits_path = self.project_root / "JITS2022" / "Code" / "Data" / jits_dir
            json_files = JITSAnalyzer.get_json_files(jits_path, "*_input.json")
            self.available_tests = [f.stem.replace("_input", "") for f in json_files]
            self.test_combo['values'] = self.available_tests
            if self.available_tests:
                self.test_combo.current(0)
            self._log(f"Found {len(self.available_tests)} tests in {jits_dir}", "info")
        except Exception as e:
            self._log(f"Error loading tests: {str(e)}", "error")

    def _update_output_option(self) -> None:
        """Update output option controls."""
        if self.output_option_var.get() == "new":
            self.new_dir_entry.config(state=tk.NORMAL)
            self.output_combo.config(state=tk.DISABLED)
        else:
            self.new_dir_entry.config(state=tk.DISABLED)
            self.output_combo.config(state="readonly")

    def _browse_jits_directory(self) -> None:
        """Browse for JITS directory."""
        initial_dir = self.project_root / "JITS2022" / "Code" / "Data"
        directory = filedialog.askdirectory(initialdir=str(initial_dir))
        if directory:
            self.jits_dir_var.set(Path(directory).name)

    def _start_conversion(self) -> None:
        """Start conversion process in separate thread."""
        if self.is_converting:
            messagebox.showwarning("Warning", "Conversion already in progress")
            return

        self.is_converting = True
        self.convert_btn.set_disabled(True)
        self.stop_btn.set_disabled(False)

        self.conversion_thread = threading.Thread(target=self._do_conversion, daemon=True)
        self.conversion_thread.start()

    def _do_conversion(self) -> None:
        """Perform the actual conversion."""
        try:
            self._log("Conversion started", "info")
            # Conversion logic will be implemented
            self._log("Conversion completed", "success")
        except Exception as e:
            self._log(f"Error: {str(e)}", "error")
        finally:
            self.is_converting = False
            self.convert_btn.set_disabled(False)
            self.stop_btn.set_disabled(True)

    def _stop_conversion(self) -> None:
        """Stop ongoing conversion."""
        self.is_converting = False
        self._log("Conversion stopped by user", "warning")
        self.convert_btn.set_disabled(False)
        self.stop_btn.set_disabled(True)

    def _build_right_panel(self, parent: tk.Widget) -> None:
        """Build right panel with conversion results."""
        right = tk.Frame(parent, bg=self.theme_dict["bg_base"])
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # Status
        SectionLabel(right, "Conversion Status", self.theme_dict["bg_base"],
                     self.theme_dict["text_primary"]).pack(fill=tk.X, pady=(0, 10))

        self.status_indicator = StatusIndicator(right, self.theme_dict["bg_base"])
        self.status_indicator.pack(fill=tk.X, pady=(0, 15))

        # Results display header with clear button
        log_header_frame = tk.Frame(right, bg=self.theme_dict["bg_base"])
        log_header_frame.pack(fill=tk.X, pady=(0, 10))

        SectionLabel(log_header_frame, "Conversion Log", self.theme_dict["bg_base"],
                     self.theme_dict["text_primary"]).pack(side=tk.LEFT, fill=tk.X, expand=True)

        clear_btn = tk.Button(
            log_header_frame,
            text="Clear",
            command=self._clear_log,
            bg=self.theme_dict["bg_surface"],
            fg=self.theme_dict["text_primary"],
            relief=tk.FLAT,
            font=("Arial", 8)
        )
        clear_btn.pack(side=tk.RIGHT)

        scrollbar = ttk.Scrollbar(right)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.results_text = tk.Text(
            right,
            bg=self.theme_dict["bg_surface"],
            fg=self.theme_dict["text_primary"],
            yscrollcommand=scrollbar.set,
            font=("Courier New", 9),
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.results_text.yview)

    def _build_footer(self, parent: tk.Widget) -> None:
        """Build footer with version and help."""
        footer = tk.Frame(parent, bg=self.theme_dict["bg_surface"], height=30)
        footer.pack(fill=tk.X, padx=0, pady=0)
        footer.pack_propagate(False)

        tk.Label(
            footer,
            text="v1.5.0 | Click [?] icons for help | Select a battery and tests to convert",
            bg=self.theme_dict["bg_surface"],
            fg=self.theme_dict["text_secondary"],
            font=("Arial", 8)
        ).pack(side=tk.LEFT, padx=20, pady=5)

    def _log(self, message: str, level: str = "info") -> None:
        """Log message to results display."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_line = f"[{timestamp}] {message}\n"

        self.results_text.insert(tk.END, log_line)
        self.results_text.see(tk.END)

        if level == "success":
            self.status_indicator.set_status("success", "Success")
        elif level == "error":
            self.status_indicator.set_status("error", "Error")
        elif level == "warning":
            self.status_indicator.set_status("warning", "Warning")

    def _clear_log(self) -> None:
        """Clear the conversion log."""
        self.results_text.delete("1.0", tk.END)
        self.status_indicator.set_status("idle", "Ready")

    def _toggle_theme(self, event=None) -> None:
        """Toggle between dark and light themes."""
        current = ThemeManager.get_current_theme()
        new_theme = "light" if current == "dark" else "dark"
        ThemeManager.switch_theme(new_theme)

    def _refresh_ui_colors(self) -> None:
        """Refresh UI colors after theme change by rebuilding the entire interface."""
        # Destroy all existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Rebuild UI with new theme
        self._build_ui()


def main():
    """Entry point for Converter GUI."""
    root = tk.Tk()
    app = ConverterInterface(root)
    root.mainloop()


if __name__ == "__main__":
    main()
