"""
JSON to DZN Converter - Main Entry Point

Professional interface for converting JITS2022 test batteries from JSON format
to MiniZinc DZN format with integer scaling.

Usage:
    python Converter/converter.py

Author: AVISPA Research Team
Date: April 2026
"""

import sys
import os
from pathlib import Path

# Get the project root
converter_dir = Path(__file__).parent.absolute()
project_root = converter_dir.parent.parent.absolute()

# Add ONLY the project root to sys.path
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# Change to Converter directory context
os.chdir(converter_dir)

if __name__ == "__main__":
    try:
        import tkinter as tk
        from ui.interface import ConverterInterface

        root = tk.Tk()
        app = ConverterInterface(root)
        root.mainloop()
    except ImportError as e:
        print(f"Error importing Converter: {e}")
        print(f"Converter directory: {converter_dir}")
        print(f"sys.path: {sys.path[:3]}")
        raise
