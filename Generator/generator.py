"""
================================================================================
AVISPA CLP Test Instance Generator v3.0
================================================================================
Professional test instance generator with integrated MiniZinc validation.

Architecture (v3.0 - Modular):
  - config.py: Centralized configuration
  - core/instance_generator.py: Expert algorithm for feasible instances
  - core/minizinc_exporter.py: DZN export with metadata
  - core/instance_validator.py: MiniZinc validation with robust timeout
  - core/instance_manager.py: File management and cleanup
  - orchestrator.py: Workflow coordination (formerly generator_orchestrator)
  - ui/interface.py: Professional user interface
  - generator.py: Main entry point

Features:
  [OK] Generates only satisfiable instances
  [OK] 10-minute validation timeout per instance
  [OK] Automatic cleanup of failed attempts
  [OK] Comprehensive logging
  [OK] Modular, maintainable design
  [OK] Professional UI

Author: AVISPA Research Team
Version: 3.0.0
Date: April 2026
================================================================================
"""

import sys
from pathlib import Path

# Ensure Generator directory is in Python path
sys.path.insert(0, str(Path(__file__).parent))

from ui.interface import main

if __name__ == '__main__':
    main()
