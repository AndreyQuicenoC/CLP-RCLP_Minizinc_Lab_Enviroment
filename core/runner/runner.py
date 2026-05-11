"""
CLP-RCLP Test Runner v1.3.0

Professional interface for executing and managing CLP/RCLP test instances
with real-time monitoring, dark/light theme support, and result generation.

Authors: Andrey Quiceno and Juan Francesco García (AVISPA Team)

Usage: python Runner/runner.py (from project root)
"""

import sys
import os
from pathlib import Path

# Get the project root
runner_dir = Path(__file__).parent.absolute()
project_root = runner_dir.parent.parent.absolute()

# Add ONLY the project root to sys.path
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Change to Runner directory context for proper imports
os.chdir(runner_dir)

# Now import the interface
if __name__ == "__main__":
    try:
        # Direct import from ui module
        from ui.interface import RunnerInterface
        import tkinter as tk

        root = tk.Tk()
        app = RunnerInterface(root)
        root.mainloop()
    except ImportError as e:
        print(f"Error importing Runner: {e}")
        print(f"Runner directory: {runner_dir}")
        print(f"sys.path: {sys.path[:3]}")
        raise


