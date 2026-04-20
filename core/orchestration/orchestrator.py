"""
CLP-RCLP System Center Entry Point

Main launcher for the orchestrator interface.

Author: AVISPA Research Team
Date: April 2026
"""

import tkinter as tk
import sys
from pathlib import Path

# Add parent directory to path to allow absolute imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.orchestration.ui.interface import OrchestratorInterface


def launch_orchestrator() -> None:
    """Launch the System Center orchestrator interface."""
    root = tk.Tk()
    app = OrchestratorInterface(root)
    root.mainloop()


if __name__ == "__main__":
    launch_orchestrator()
