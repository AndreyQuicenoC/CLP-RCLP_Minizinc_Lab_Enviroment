"""
================================================================================
Generator GUI - Professional User Interface
================================================================================
Clean, professional GUI for instance generation with real-time logging.
================================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from .themes import ThemeManager, get_theme_dict
from .components import SectionLabel, FlatButton, StatusIndicator
from .layouts import LayoutBuilder, LayoutConfig
import threading
from datetime import datetime

from config import Config
from orchestrator import GeneratorOrchestrator


class GeneratorGUI:
    """Professional GUI for CLP instance generator"""

    def __init__(self, root):
        self.root = root
        self.root.title("AVISPA CLP Instance Generator v2.0")
        self.root.geometry("850x750")
        self.root.resizable(False, False)

        self.config_obj = Config()
        self._setup_colors()
        self.root.configure(bg=self.colors['bg'])

        # Find project root
        self.project_root = self._find_project_root()
        self.orchestrator = GeneratorOrchestrator(
            self.project_root,
            log_callback=self._log
        )

        self.generation_thread = None
        self._create_widgets()

    def _setup_colors(self):
        """Setup color scheme"""
        self.colors = {
            'bg': self.config_obj.COLOR_LIGHT_GRAY,
            'dark_blue': self.config_obj.COLOR_DARK_BLUE,
            'light_blue': self.config_obj.COLOR_LIGHT_BLUE,
            'white': self.config_obj.COLOR_WHITE,
            'gray': self.config_obj.COLOR_GRAY,
            'success': self.config_obj.COLOR_SUCCESS,
            'error': self.config_obj.COLOR_ERROR,
            'warning': self.config_obj.COLOR_WARNING,
            'info': self.config_obj.COLOR_INFO
        }

    def _find_project_root(self):
        """Find CLP-RCLP Minizinc project root"""
        current = Path(__file__).parent.absolute()
        while current.name != 'CLP-RCLP Minizinc' and current.parent != current:
            current = current.parent

        if current.name == 'CLP-RCLP Minizinc':
            return str(current)

        return str(Path(__file__).parent.parent.absolute())

    def _create_widgets(self):
        """Create all GUI widgets"""

        # =====================================================================
        # HEADER
        # =====================================================================

        header = tk.Frame(self.root, bg=self.colors['dark_blue'], height=80)
        header.pack(fill='x')
        header.pack_propagate(False)

        tk.Label(
            header,
            text="AVISPA CLP Instance Generator v2.0",
            font=('Arial', 18, 'bold'),
            bg=self.colors['dark_blue'],
            fg=self.colors['white']
        ).pack(pady=15)

        tk.Label(
            header,
            text="Generate feasible test instances with integrated MiniZinc validation",
            font=('Arial', 9),
            bg=self.colors['dark_blue'],
            fg=self.colors['light_blue']
        ).pack()

        # =====================================================================
        # MAIN CONTENT
        # =====================================================================

        main = tk.Frame(self.root, bg=self.colors['bg'])
        main.pack(fill='both', expand=True, padx=15, pady=15)

        # Parameters section
        params_frame = tk.LabelFrame(
            main,
            text=" Parameters ",
            font=('Arial', 11, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['dark_blue'],
            padx=15,
            pady=15
        )
        params_frame.pack(fill='x', pady=(0, 10))

        # Buses spinbox
        buses_f = tk.Frame(params_frame, bg=self.colors['white'])
        buses_f.pack(fill='x', pady=8)

        tk.Label(
            buses_f,
            text="Buses:",
            font=('Arial', 10),
            bg=self.colors['white'],
            width=12,
            anchor='w'
        ).pack(side='left')

        self.buses_var = tk.IntVar(value=5)
        tk.Spinbox(
            buses_f,
            from_=2, to=20,
            textvariable=self.buses_var,
            font=('Arial', 10),
            width=10,
            state='readonly'
        ).pack(side='left', padx=(0, 20))

        tk.Label(
            buses_f,
            text="(2-20)",
            font=('Arial', 9),
            bg=self.colors['white'],
            fg=self.colors['gray']
        ).pack(side='left')

        # Stations spinbox
        stations_f = tk.Frame(params_frame, bg=self.colors['white'])
        stations_f.pack(fill='x', pady=8)

        tk.Label(
            stations_f,
            text="Stations:",
            font=('Arial', 10),
            bg=self.colors['white'],
            width=12,
            anchor='w'
        ).pack(side='left')

        self.stations_var = tk.IntVar(value=8)
        tk.Spinbox(
            stations_f,
            from_=4, to=25,
            textvariable=self.stations_var,
            font=('Arial', 10),
            width=10,
            state='readonly'
        ).pack(side='left', padx=(0, 20))

        tk.Label(
            stations_f,
            text="(4-25)",
            font=('Arial', 9),
            bg=self.colors['white'],
            fg=self.colors['gray']
        ).pack(side='left')

        # =====================================================================
        # LOGGING
        # =====================================================================

        log_frame = tk.LabelFrame(
            main,
            text=" Generation Log ",
            font=('Arial', 11, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['dark_blue'],
            padx=10,
            pady=10
        )
        log_frame.pack(fill='both', expand=True, pady=(0, 10))

        log_scroll = tk.Scrollbar(log_frame)
        log_scroll.pack(side='right', fill='y')

        self.log_text = tk.Text(
            log_frame,
            font=('Consolas', 9),
            bg='#fafafa',
            fg='#333',
            yscrollcommand=log_scroll.set,
            wrap='word',
            state='disabled'
        )
        self.log_text.pack(fill='both', expand=True)
        log_scroll.config(command=self.log_text.yview)

        # Configure tags
        self.log_text.tag_config('success', foreground=self.colors['success'])
        self.log_text.tag_config('error', foreground=self.colors['error'])
        self.log_text.tag_config('warning', foreground=self.colors['warning'])
        self.log_text.tag_config('info', foreground=self.colors['info'])

        # =====================================================================
        # BUTTONS
        # =====================================================================

        button_frame = tk.Frame(main, bg=self.colors['bg'])
        button_frame.pack(fill='x')

        self.generate_btn = tk.Button(
            button_frame,
            text=" Generate & Validate ",
            font=('Arial', 11, 'bold'),
            bg=self.colors['light_blue'],
            fg=self.colors['white'],
            padx=20,
            pady=10,
            command=self._on_generate
        )
        self.generate_btn.pack(side='left', padx=(0, 10))

        # STOP button - initially disabled
        self.stop_btn = tk.Button(
            button_frame,
            text=" Stop Generation ",
            font=('Arial', 11, 'bold'),
            bg=self.colors['error'],
            fg=self.colors['white'],
            padx=15,
            pady=10,
            command=self._on_stop,
            state='disabled'
        )
        self.stop_btn.pack(side='left', padx=(0, 10))

        tk.Button(
            button_frame,
            text="Clear Log",
            font=('Arial', 10),
            bg=self.colors['gray'],
            fg=self.colors['dark_blue'],
            padx=15,
            pady=8,
            command=self._clear_log
        ).pack(side='left')

        # =====================================================================
        # FOOTER
        # =====================================================================

        footer = tk.Frame(self.root, bg=self.colors['dark_blue'], height=40)
        footer.pack(fill='x', side='bottom')
        footer.pack_propagate(False)

        tk.Label(
            footer,
            text="AVISPA Research Team © 2026  |  v2.0 (Modular)",
            font=('Arial', 9),
            bg=self.colors['dark_blue'],
            fg=self.colors['white']
        ).pack(pady=10)

        # Initial message
        self._log("System ready. Configure parameters and click 'Generate'.",
                 'info')
        self._log(
            f"Project root: {self.project_root}",
            'info'
        )

    def _log(self, message: str, level: str = 'info'):
        """Add message to log"""
        self.log_text.config(state='normal')

        timestamp = datetime.now().strftime('%H:%M:%S')
        prefix = {'success': '[OK]', 'error': '[X]', 'warning': '[!]',
                 'info': 'ℹ'}.get(level, '•')

        self.log_text.insert('end', f"[{timestamp}] {prefix} {message}\n",
                            level)
        self.log_text.see('end')
        self.log_text.config(state='disabled')
        self.root.update()

    def _clear_log(self):
        """Clear log"""
        self.log_text.config(state='normal')
        self.log_text.delete('1.0', 'end')
        self.log_text.config(state='disabled')
        self._log("Log cleared.", 'info')

    def _on_generate(self):
        """Handle generate button click"""
        if self.generation_thread and self.generation_thread.is_alive():
            self._log("Generation already in progress...", 'warning')
            return

        self.generate_btn.config(state='disabled', bg=self.colors['gray'])
        self.stop_btn.config(state='normal', bg=self.colors['error'])
        self.orchestrator.stop_requested = False
        self._log("=" * 60, 'info')

        # Run in background thread
        self.generation_thread = threading.Thread(
            target=self._generate_worker,
            daemon=True
        )
        self.generation_thread.start()

    def _on_stop(self):
        """Handle stop button click"""
        self._log("STOP requested by user...", 'warning')
        self.orchestrator.request_stop()
        self.stop_btn.config(state='disabled', bg=self.colors['gray'])

    def _generate_worker(self):
        """Worker thread for generation"""
        try:
            num_buses = self.buses_var.get()
            num_stations = self.stations_var.get()

            success, dzn_path = self.orchestrator.generate_and_validate(
                num_buses, num_stations
            )

            if success:
                self._log(
                    f"SUCCESS! Instance saved: {Path(dzn_path).name}",
                    'success'
                )
                self.root.after(
                    100,
                    lambda: messagebox.showinfo(
                        "Success",
                        f"Instance generated and validated successfully!\n\n"
                        f"File: {Path(dzn_path).name}\n"
                        f"Location: {Path(dzn_path).parent}"
                    )
                )
            else:
                self._log(
                    "FAILED: Could not generate satisfiable instance.",
                    'error'
                )
                self.root.after(
                    100,
                    lambda: messagebox.showerror(
                        "Failed",
                        "Could not generate a satisfiable instance.\n"
                        "Check log for details."
                    )
                )

        except Exception as e:
            self._log(f"Error during generation: {str(e)}", 'error')
            self.root.after(
                100,
                lambda: messagebox.showerror("Error", f"Error: {str(e)}")
            )

        finally:
            self.generate_btn.config(
                state='normal',
                bg=self.config_obj.COLOR_LIGHT_BLUE
            )
            self.stop_btn.config(state='disabled', bg=self.colors['error'])


def main():
    """Main entry point"""
    root = tk.Tk()
    app = GeneratorGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
