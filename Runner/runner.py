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

# Get the Runner directory
runner_dir = Path(__file__).parent.absolute()
runner_parent = runner_dir.parent.absolute()

# Add paths to sys.path for imports
if str(runner_dir) not in sys.path:
    sys.path.insert(0, str(runner_dir))
if str(runner_parent) not in sys.path:
    sys.path.insert(0, str(runner_parent))

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


