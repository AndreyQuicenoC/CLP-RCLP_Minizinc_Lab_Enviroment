"""
CLP-RCLP System Center Entry Point

Main launcher for the orchestrator interface.

Author: AVISPA Research Team
Date: April 2026
"""

import tkinter as tk
from ui.interface import OrchestratorInterface


def launch_orchestrator() -> None:
    """Launch the System Center orchestrator interface."""
    root = tk.Tk()
    app = OrchestratorInterface(root)
    root.mainloop()


if __name__ == "__main__":
    launch_orchestrator()
