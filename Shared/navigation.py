"""
Navigation Utility - Back navigation to Orchestrator

Provides functionality to return from any tool to the System Center.

Author: AVISPA Research Team
Date: April 2026
"""

import tkinter as tk
import subprocess
from pathlib import Path


def return_to_orchestrator(current_window: tk.Tk) -> None:
    """
    Close current window and launch the Orchestrator (System Center).

    Args:
        current_window: The window to close (tk.Tk instance)
    """
    # Close current window
    current_window.destroy()

    # Launch orchestrator
    try:
        orchestrator_path = Path(__file__).parent.parent / "Orchestrator" / "orchestrator.py"
        if orchestrator_path.exists():
            subprocess.Popen(["python", str(orchestrator_path)])
    except Exception as e:
        print(f"Error launching orchestrator: {e}")
