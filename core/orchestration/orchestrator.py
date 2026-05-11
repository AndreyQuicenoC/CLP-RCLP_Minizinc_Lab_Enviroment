"""
CLP-RCLP System Center Entry Point

Main launcher for the orchestrator interface.

Author: AVISPA Research Team
Date: April 2026
"""

import tkinter as tk
import sys
from pathlib import Path

# Get the project root and add it to sys.path
orchestration_dir = Path(__file__).parent.absolute()
project_root = orchestration_dir.parent.parent.absolute()

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from core.orchestration.ui.interface import OrchestratorInterface


def launch_orchestrator() -> None:
    """Launch the System Center orchestrator interface."""
    root = tk.Tk()
    app = OrchestratorInterface(root)
    root.mainloop()


if __name__ == "__main__":
    launch_orchestrator()
