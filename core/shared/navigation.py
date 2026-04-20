"""
Navigation Utility - Back navigation to Orchestrator

Provides functionality to return from any tool to the System Center.

Uses dynamic path resolution to work across any system configuration.

Author: AVISPA Research Team
Date: April 2026
"""

import tkinter as tk
import subprocess
from pathlib import Path
import logging

from .path_resolver import ToolPathResolver

logger = logging.getLogger(__name__)


def return_to_orchestrator(current_window: tk.Tk) -> None:
    """
    Close current window and launch the Orchestrator (System Center).

    Uses dynamic path resolution to find orchestrator.py regardless
    of system configuration or directory naming conventions.

    Args:
        current_window: The window to close (tk.Tk instance)
    """
    # Close current window
    current_window.destroy()

    # Launch orchestrator using dynamic path resolution
    try:
        # Find orchestrator script dynamically
        orchestrator_path = _find_orchestrator_path()

        if orchestrator_path and orchestrator_path.exists():
            logger.info(f"Launching orchestrator from: {orchestrator_path}")
            subprocess.Popen(["python", str(orchestrator_path)])
        else:
            logger.error(f"Orchestrator not found at: {orchestrator_path}")
    except Exception as e:
        logger.error(f"Error launching orchestrator: {e}")
        print(f"Error launching orchestrator: {e}")


def _find_orchestrator_path() -> Path:
    """
    Dynamically find the orchestrator script path.

    Searches for orchestration/orchestrator.py in the core directory.

    Returns:
        Path: Path to orchestrator.py if found
    """
    current = Path(__file__).parent.parent.parent.absolute()

    # Primary path: core/orchestration/orchestrator.py
    path = current / "core" / "orchestration" / "orchestrator.py"
    if path.exists():
        return path

    # Legacy path: orchestration/orchestrator.py (in case core is root)
    path = current / "orchestration" / "orchestrator.py"
    if path.exists():
        return path

    logger.warning(f"Could not find orchestrator in: {current}")
    return path  # Return the primary path even if not found (for error reporting)
