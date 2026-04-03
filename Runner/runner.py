"""
CLP-RCLP Test Runner v1.2.0

Professional interface for executing and managing CLP/RCLP test instances.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from ui.interface import main

if __name__ == "__main__":
    main()
