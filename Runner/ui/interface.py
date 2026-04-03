"""
Runner Interface - Premium Dark Industrial GUI
Fully functional, high-quality UX/UI redesign.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import threading
import logging

from config import RunnerConfig
from core.executor import MiniZincExecutor
from core.result_handler import ResultHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────
#  Design Tokens
# ─────────────────────────────────────────────────────────────
class T:
    BG_BASE      = "#0D0F14"
    BG_SURFACE   = "#141720"
    BG_ELEVATED  = "#1C2030"
    BG_HOVER     = "#232840"

    ACCENT       = "#3D8EF5"
    ACCENT_DIM   = "#1F4A8C"
    ACCENT_GLOW  = "#5AAEFF"

    SUCCESS      = "#22C55E"
    WARNING      = "#F59E0B"
    ERROR        = "#EF4444"

    TEXT_PRIMARY = "#E8ECF4"
    TEXT_SEC     = "#8896B3"
    TEXT_MUTED   = "#4A5568"
    TEXT_CODE    = "#A8C4F0"

    BORDER       = "#242B3D"
    BORDER_ACT   = "#3D8EF5"

    FONT_UI      = ("Segoe UI", 10)
    FONT_BOLD    = ("Segoe UI", 10, "bold")
    FONT_SMALL   = ("Segoe UI", 8, "bold")
    FONT_MONO    = ("Consolas", 9)
    FONT_SECTION = ("Segoe UI", 8, "bold")

    PAD_X        = 20
    PAD_Y        = 16


# ─────────────────────────────────────────────────────────────
#  TTK Theme
# ─────────────────────────────────────────────────────────────

def apply_ttk_theme(root: tk.Tk) -> None:
    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure(
        "Dark.TCombobox",
        fieldbackground=T.BG_ELEVATED,
        background=T.BG_ELEVATED,
        foreground=T.TEXT_PRIMARY,
        selectbackground=T.ACCENT_DIM,
        selectforeground=T.TEXT_PRIMARY,
        bordercolor=T.BORDER,
        darkcolor=T.BG_ELEVATED,
        lightcolor=T.BG_ELEVATED,
        arrowcolor=T.TEXT_SEC,
        arrowsize=12,
        padding=(10, 6),
        font=T.FONT_UI,
        relief="flat",
    )
    style.map(
        "Dark.TCombobox",
        fieldbackground=[("focus", T.BG_ELEVATED), ("readonly", T.BG_ELEVATED)],
        bordercolor=[("focus", T.BORDER_ACT), ("!focus", T.BORDER)],
        foreground=[("disabled", T.TEXT_MUTED)],
        arrowcolor=[("hover", T.ACCENT)],
    )
    root.option_add("*TCombobox*Listbox.background",      T.BG_ELEVATED)
    root.option_add("*TCombobox*Listbox.foreground",      T.TEXT_PRIMARY)
    root.option_add("*TCombobox*Listbox.selectBackground",T.ACCENT_DIM)
    root.option_add("*TCombobox*Listbox.selectForeground",T.TEXT_PRIMARY)
    root.option_add("*TCombobox*Listbox.font",            T.FONT_UI)
    root.option_add("*TCombobox*Listbox.relief",          "flat")

    style.configure(
        "Dark.Vertical.TScrollbar",
        background=T.BG_ELEVATED,
        troughcolor=T.BG_SURFACE,
        bordercolor=T.BG_SURFACE,
        arrowcolor=T.TEXT_MUTED,
        darkcolor=T.BG_ELEVATED,
        lightcolor=T.BG_ELEVATED,
        relief="flat",
        width=8,
    )
    style.map("Dark.Vertical.TScrollbar",
              background=[("active", T.TEXT_MUTED)])


# ─────────────────────────────────────────────────────────────
#  Custom Widgets
# ─────────────────────────────────────────────────────────────

class SectionLabel(tk.Frame):
    def __init__(self, parent, text: str, bg: str = T.BG_SURFACE):
        super().__init__(parent, bg=bg)
        tk.Frame(self, bg=T.ACCENT, width=3).pack(side=tk.LEFT, fill=tk.Y, pady=1)
        tk.Label(self, text=text.upper(), bg=bg, fg=T.TEXT_SEC,
                 font=T.FONT_SECTION, padx=8).pack(side=tk.LEFT)


class Divider(tk.Frame):
    def __init__(self, parent, **kw):
        super().__init__(parent, bg=T.BORDER, height=1, **kw)


class PillRadio(tk.Frame):
    """Segmented-control radio selector."""

    def __init__(self, parent, variable: tk.StringVar, options: list):
        super().__init__(parent, bg=T.BG_ELEVATED,
                         highlightthickness=1, highlightbackground=T.BORDER)
        self.var = variable
        self._btns: dict = {}

        for col, opt in enumerate(options):
            lbl = tk.Label(self, text=opt.upper(),
                           bg=T.BG_ELEVATED, fg=T.TEXT_SEC,
                           font=("Segoe UI", 9, "bold"),
                           padx=24, pady=9, cursor="hand2")
            lbl.grid(row=0, column=col, sticky="nsew")
            self.grid_columnconfigure(col, weight=1)
            self._btns[opt] = lbl
            lbl.bind("<Button-1>", lambda _e, v=opt: self._select(v))
            lbl.bind("<Enter>",    lambda _e, b=lbl, v=opt: self._hover(b, v, True))
            lbl.bind("<Leave>",    lambda _e, b=lbl, v=opt: self._hover(b, v, False))

        self._select(variable.get())

    def _select(self, value: str) -> None:
        self.var.set(value)
        for k, btn in self._btns.items():
            btn.config(bg=T.ACCENT if k == value else T.BG_ELEVATED,
                       fg="#FFFFFF" if k == value else T.TEXT_SEC)

    def _hover(self, btn, value: str, entering: bool) -> None:
        if value == self.var.get():
            return
        btn.config(bg=T.BG_HOVER if entering else T.BG_ELEVATED,
                   fg=T.TEXT_PRIMARY if entering else T.TEXT_SEC)


class FlatButton(tk.Label):
    """Button implemented as tk.Label — avoids ttk dark-mode issues."""

    def __init__(self, parent, text: str, command,
                 accent: bool = False, enabled: bool = True, **kw):
        self._accent  = accent
        self._command = command
        self._enabled = enabled

        if accent:
            self._bg, self._fg, self._hover_bg = T.ACCENT, "#FFFFFF", T.ACCENT_GLOW
        else:
            self._bg, self._fg, self._hover_bg = T.BG_ELEVATED, T.TEXT_SEC, T.BG_HOVER

        super().__init__(
            parent,
            text=text,
            bg=self._bg if enabled else T.BG_ELEVATED,
            fg=self._fg if enabled else T.TEXT_MUTED,
            font=("Segoe UI", 9, "bold"),
            padx=0, pady=11,
            cursor="hand2" if enabled else "arrow",
            relief="flat",
            highlightthickness=1,
            highlightbackground=T.ACCENT if accent else T.BORDER,
            **kw,
        )

        self._setup_bindings()

    # ✅ RENAMED
    def _setup_bindings(self):
        if self._enabled:
            self.bind("<Enter>",           self._on_enter)
            self.bind("<Leave>",           self._on_leave)
            self.bind("<Button-1>",        self._on_press)
            self.bind("<ButtonRelease-1>", self._on_release)

    # ✅ RENAMED
    def _remove_bindings(self):
        for s in ("<Enter>", "<Leave>", "<Button-1>", "<ButtonRelease-1>"):
            self.unbind(s)

    def _on_enter(self, _e):
        self.config(bg=self._hover_bg, fg="#FFFFFF")

    def _on_leave(self, _e):
        self.config(bg=self._bg, fg=self._fg)

    def _on_press(self, _e):
        self.config(bg=T.ACCENT_DIM if self._accent else T.BORDER)

    def _on_release(self, _e):
        self.config(bg=self._bg, fg=self._fg)
        if self._command:
            self._command()

    def set_enabled(self, enabled: bool):
        self._enabled = enabled
        self._remove_bindings()

        if enabled:
            self.config(
                bg=self._bg,
                fg=self._fg,
                cursor="hand2",
                highlightbackground=T.ACCENT if self._accent else T.BORDER
            )
            self._setup_bindings()
        else:
            self.config(
                bg=T.BG_ELEVATED,
                fg=T.TEXT_MUTED,
                cursor="arrow",
                highlightbackground=T.BORDER
            )

class StatusDot(tk.Canvas):
    _COLORS = {"idle": T.TEXT_MUTED, "running": T.ACCENT,
               "success": T.SUCCESS, "error": T.ERROR, "warning": T.WARNING}

    def __init__(self, parent, **kw):
        super().__init__(parent, width=10, height=10,
                         bg=T.BG_SURFACE, highlightthickness=0, **kw)
        self._state = "idle"
        self._dot   = self.create_oval(1, 1, 9, 9, fill=T.TEXT_MUTED, outline="")
        self._job   = None

    def set_state(self, state: str):
        self._state = state
        if self._job:
            self.after_cancel(self._job)
            self._job = None
        self.itemconfig(self._dot, fill=self._COLORS.get(state, T.TEXT_MUTED))
        if state == "running":
            self._blink()

    def _blink(self):
        cur = self.itemcget(self._dot, "fill")
        self.itemconfig(self._dot, fill=T.ACCENT if cur != T.ACCENT else T.BG_SURFACE)
        if self._state == "running":
            self._job = self.after(500, self._blink)


# ─────────────────────────────────────────────────────────────
#  Main Application
# ─────────────────────────────────────────────────────────────

class RunnerInterface:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("CLP Runner  v1.2")
        self.root.geometry("940x730")
        self.root.resizable(False, False)
        self.root.configure(bg=T.BG_BASE)

        apply_ttk_theme(root)

        self.config       = RunnerConfig()
        self.project_root = self._find_project_root()
        self.is_running   = False

        self._build_ui()

    def _find_project_root(self) -> Path:
        current = Path(__file__).parent.parent
        while current != current.parent:
            if (current / "Models" / "clp_model.mzn").exists():
                return current
            current = current.parent
        return Path.cwd()

    # ── build UI ─────────────────────────────────────────────

    def _build_ui(self):
        self._build_header()
        self._build_footer()          # anchor footer first

        body = tk.Frame(self.root, bg=T.BG_BASE)
        body.pack(fill=tk.BOTH, expand=True,
                  padx=T.PAD_X, pady=(T.PAD_Y // 2, T.PAD_Y))

        left = tk.Frame(body, bg=T.BG_BASE, width=300)
        left.pack(side=tk.LEFT, fill=tk.Y)
        left.pack_propagate(False)
        self._build_config_panel(left)

        tk.Frame(body, bg=T.BG_BASE, width=14).pack(side=tk.LEFT)

        right = tk.Frame(body, bg=T.BG_BASE)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self._build_results_panel(right)

    def _build_header(self):
        bar = tk.Frame(self.root, bg=T.BG_SURFACE,
                       highlightthickness=1, highlightbackground=T.BORDER)
        bar.pack(fill=tk.X)

        inner = tk.Frame(bar, bg=T.BG_SURFACE)
        inner.pack(fill=tk.X, padx=T.PAD_X, pady=13)

        tk.Frame(inner, bg=T.ACCENT, width=4).pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(inner, text="  CLP RUNNER",
                 bg=T.BG_SURFACE, fg=T.TEXT_PRIMARY,
                 font=("Segoe UI", 13, "bold")).pack(side=tk.LEFT)
        tk.Label(inner, text="v1.2",
                 bg=T.BG_SURFACE, fg=T.TEXT_MUTED,
                 font=("Segoe UI", 9)).pack(side=tk.LEFT, padx=(6, 0), pady=(4, 0))

        sf = tk.Frame(inner, bg=T.BG_SURFACE)
        sf.pack(side=tk.RIGHT)
        self._status_dot = StatusDot(sf)
        self._status_dot.pack(side=tk.LEFT, padx=(0, 6))
        self._status_lbl = tk.Label(sf, text="IDLE",
                                    bg=T.BG_SURFACE, fg=T.TEXT_MUTED,
                                    font=("Segoe UI", 8, "bold"))
        self._status_lbl.pack(side=tk.LEFT)

    def _build_footer(self):
        bar = tk.Frame(self.root, bg=T.BG_SURFACE,
                       highlightthickness=1, highlightbackground=T.BORDER)
        bar.pack(fill=tk.X, side=tk.BOTTOM)

        inner = tk.Frame(bar, bg=T.BG_SURFACE)
        inner.pack(fill=tk.X, padx=T.PAD_X, pady=5)
        tk.Label(inner, text="MiniZinc Executor  ·  CLP/RCLP Solver",
                 bg=T.BG_SURFACE, fg=T.TEXT_MUTED, font=("Segoe UI", 8)).pack(side=tk.LEFT)
        tk.Label(inner, text="Runner Interface  ·  v1.2.0",
                 bg=T.BG_SURFACE, fg=T.TEXT_MUTED, font=("Segoe UI", 8)).pack(side=tk.RIGHT)

    def _build_config_panel(self, parent):
        card = tk.Frame(parent, bg=T.BG_SURFACE,
                        highlightthickness=1, highlightbackground=T.BORDER)
        card.pack(fill=tk.X, pady=(T.PAD_Y // 2, 0))

        p = dict(padx=16)

        # Directory
        SectionLabel(card, "Directory").pack(anchor="w", pady=(14, 6), **p)
        self._dir_var = tk.StringVar(value=self.config.DATA_DIRECTORIES[0])
        dir_cb = ttk.Combobox(card, textvariable=self._dir_var,
                               values=self.config.DATA_DIRECTORIES,
                               state="readonly", style="Dark.TCombobox")
        dir_cb.pack(fill=tk.X, pady=(0, 2), **p)
        self._dir_var.trace_add("write", lambda *_: self._on_dir_changed())

        Divider(card).pack(fill=tk.X, pady=12, **p)

        # Test Instance
        SectionLabel(card, "Test Instance").pack(anchor="w", pady=(0, 6), **p)
        row = tk.Frame(card, bg=T.BG_SURFACE)
        row.pack(fill=tk.X, pady=(0, 2), **p)

        self._file_var = tk.StringVar()
        self._file_cb  = ttk.Combobox(row, textvariable=self._file_var,
                                       state="readonly", style="Dark.TCombobox")
        self._file_cb.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ref = tk.Label(row, text=" ↺ ", bg=T.BG_ELEVATED, fg=T.TEXT_SEC,
                       font=("Segoe UI", 12), cursor="hand2",
                       highlightthickness=1, highlightbackground=T.BORDER,
                       padx=4, pady=3)
        ref.pack(side=tk.LEFT, padx=(6, 0))
        ref.bind("<Button-1>", lambda _e: self._refresh_files())
        ref.bind("<Enter>",    lambda _e: ref.config(fg=T.ACCENT, highlightbackground=T.BORDER_ACT))
        ref.bind("<Leave>",    lambda _e: ref.config(fg=T.TEXT_SEC, highlightbackground=T.BORDER))

        Divider(card).pack(fill=tk.X, pady=12, **p)

        # Model
        SectionLabel(card, "Model").pack(anchor="w", pady=(0, 8), **p)
        self._model_var = tk.StringVar(value=self.config.MODELS[0])
        PillRadio(card, self._model_var, self.config.MODELS).pack(
            fill=tk.X, pady=(0, 16), **p)

        # Actions
        Divider(card).pack(fill=tk.X, **p)
        actions = tk.Frame(card, bg=T.BG_SURFACE)
        actions.pack(fill=tk.X, padx=16, pady=14)

        self._run_btn = FlatButton(actions, "▶   RUN TEST",
                                   command=self._run_test, accent=True)
        self._run_btn.pack(fill=tk.X)

        self._stop_btn = FlatButton(actions, "■   STOP",
                                    command=self._stop_test,
                                    accent=False, enabled=False)
        self._stop_btn.pack(fill=tk.X, pady=(8, 0))

        self._refresh_files()

    def _build_results_panel(self, parent):
        hdr = tk.Frame(parent, bg=T.BG_SURFACE,
                       highlightthickness=1, highlightbackground=T.BORDER)
        hdr.pack(fill=tk.X)

        hi = tk.Frame(hdr, bg=T.BG_SURFACE)
        hi.pack(fill=tk.X, padx=14, pady=9)
        tk.Label(hi, text="OUTPUT LOG", bg=T.BG_SURFACE, fg=T.TEXT_SEC,
                 font=T.FONT_SECTION).pack(side=tk.LEFT)

        clr = tk.Label(hi, text="CLEAR", bg=T.BG_SURFACE, fg=T.TEXT_MUTED,
                       font=("Segoe UI", 8, "bold"), cursor="hand2")
        clr.pack(side=tk.RIGHT)
        clr.bind("<Button-1>", lambda _e: self._clear_log())
        clr.bind("<Enter>",    lambda _e: clr.config(fg=T.ACCENT))
        clr.bind("<Leave>",    lambda _e: clr.config(fg=T.TEXT_MUTED))

        wrap = tk.Frame(parent, bg=T.BG_BASE,
                        highlightthickness=1, highlightbackground=T.BORDER)
        wrap.pack(fill=tk.BOTH, expand=True, pady=(1, 0))

        vsb = ttk.Scrollbar(wrap, orient="vertical",
                             style="Dark.Vertical.TScrollbar")
        vsb.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 2), pady=4)

        self._log_text = tk.Text(
            wrap, bg=T.BG_BASE, fg=T.TEXT_CODE, font=T.FONT_MONO,
            relief="flat", bd=0, padx=14, pady=12,
            yscrollcommand=vsb.set,
            insertbackground=T.ACCENT,
            selectbackground=T.ACCENT_DIM,
            selectforeground=T.TEXT_PRIMARY,
            wrap=tk.WORD, cursor="arrow",
        )
        self._log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.config(command=self._log_text.yview)

        self._log_text.tag_config("success", foreground=T.SUCCESS, font=("Consolas", 9, "bold"))
        self._log_text.tag_config("error",   foreground=T.ERROR,   font=("Consolas", 9, "bold"))
        self._log_text.tag_config("warning", foreground=T.WARNING)
        self._log_text.tag_config("info",    foreground=T.TEXT_CODE)
        self._log_text.tag_config("muted",   foreground=T.TEXT_MUTED)
        self._log_text.tag_config("key",     foreground=T.TEXT_SEC)
        self._log_text.tag_config("value",   foreground=T.ACCENT_GLOW)
        self._log_text.tag_config("section", foreground=T.TEXT_MUTED, font=("Consolas", 8))

        self._log("System ready.  Select a directory, instance and model — then press RUN TEST.", "muted")

    # ── events ───────────────────────────────────────────────

    def _on_dir_changed(self):
        self._refresh_files()

    def _refresh_files(self):
        try:
            dir_name = self._dir_var.get()
            dir_path = self.project_root / dir_name
            if not dir_path.exists():
                self._file_cb.config(values=[])
                self._file_var.set("")
                return
            files = sorted(f.stem for f in dir_path.glob("*.dzn")
                           if not f.stem.endswith("_meta"))
            self._file_cb.config(values=files)
            if files:
                self._file_cb.current(0)
            else:
                self._file_var.set("")
        except Exception as exc:
            logger.error("Error refreshing files: %s", exc)

    def _run_test(self):
        if not self._file_var.get():
            messagebox.showwarning("Selection Required",
                                   "Please select a test instance.")
            return
        self.is_running = True
        self._run_btn.set_enabled(False)
        self._stop_btn.set_enabled(True)
        self._set_status("running", "RUNNING")
        self._log_text.delete("1.0", tk.END)
        threading.Thread(target=self._execute_test, daemon=True).start()

    def _execute_test(self):
        try:
            dir_name  = self._dir_var.get()
            file_name = self._file_var.get()
            model     = self._model_var.get()

            dzn_path   = self.project_root / dir_name / f"{file_name}.dzn"
            model_path = self.project_root / "Models" / f"{model}_model.mzn"
            out_dir    = self.project_root / "Tests" / "Output" / dir_name.split("/")[-1]

            self._log("─" * 52, "section")
            self._log_kv("Instance",  file_name)
            self._log_kv("Directory", dir_name)
            self._log_kv("Model",     model.upper())
            self._log("─" * 52, "section")
            self._log("")

            executor = MiniZincExecutor(str(model_path))
            success, result = executor.execute(str(dzn_path))

            if success and result:
                self._log("  ✓  TEST PASSED", "success")
                self._log("")
                self._log_kv("Buses",     result["num_buses"])
                self._log_kv("Stations",  result["num_stations"])
                self._log_kv("Charged",   result["charged_stations"])
                self._log_kv("Deviation", f"{result['time_deviation'] / 10} min")

                handler = ResultHandler(str(out_dir))
                ok, json_path, txt_path = handler.save_results(file_name, result)
                if ok:
                    self._log("")
                    self._log("  Saved:", "muted")
                    self._log_kv("  JSON", json_path)
                    self._log_kv("  TXT",  txt_path)

                self._set_status("success", "PASSED")
            else:
                self._log("  ✗  TEST FAILED — UNSATISFIABLE", "error")
                self._set_status("error", "FAILED")

        except Exception as exc:
            self._log(f"  ✗  ERROR: {exc}", "error")
            self._set_status("error", "ERROR")
        finally:
            self.is_running = False
            self._log("")
            self._log("─" * 52, "section")
            self._restore_buttons()

    def _stop_test(self):
        self.is_running = False
        self._log("  ⚠  Execution stopped by user.", "warning")
        self._set_status("warning", "STOPPED")
        self._restore_buttons()

    def _clear_log(self):
        self._log_text.delete("1.0", tk.END)
        self._set_status("idle", "IDLE")

    # ── helpers ──────────────────────────────────────────────

    def _restore_buttons(self):
        self._run_btn.set_enabled(True)
        self._stop_btn.set_enabled(False)

    def _set_status(self, state: str, label: str):
        _c = {"idle": T.TEXT_MUTED, "running": T.ACCENT,
              "success": T.SUCCESS, "error": T.ERROR, "warning": T.WARNING}
        self._status_dot.set_state(state)
        self._status_lbl.config(text=label, fg=_c.get(state, T.TEXT_MUTED))

    def _log(self, msg: str, tag: str = "info"):
        self._log_text.insert(tk.END, msg + "\n", tag)
        self._log_text.see(tk.END)
        self.root.update_idletasks()

    def _log_kv(self, key: str, value):
        self._log_text.insert(tk.END, f"  {key:<14}", "key")
        self._log_text.insert(tk.END, f"  {value}\n",  "value")
        self._log_text.see(tk.END)
        self.root.update_idletasks()


# ─────────────────────────────────────────────────────────────
#  Entry Point
# ─────────────────────────────────────────────────────────────

def main():
    root = tk.Tk()
    RunnerInterface(root)
    root.mainloop()


if __name__ == "__main__":
    main()