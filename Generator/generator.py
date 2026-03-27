"""
================================================================================
AVISPA CLP Test Instance Generator v2.0
================================================================================
Professional test instance generator with integrated MiniZinc validation.

Architecture:
  - config.py: Centralized configuration
  - instance_generator.py: Expert algorithm for feasible instances
  - minizinc_exporter.py: DZN export with metadata
  - instance_validator.py: MiniZinc validation with robust timeout
  - instance_manager.py: File management and cleanup
  - generator_orchestrator.py: Workflow coordination
  - generator_gui.py: Professional user interface
  - generator.py: Main entry point

Features:
  [OK] Generates only satisfiable instances
  [OK] 10-minute validation timeout per instance
  [OK] Automatic cleanup of failed attempts
  [OK] Comprehensive logging
  [OK] Modular, maintainable design
  [OK] Professional UI

Author: AVISPA Research Team
Version: 2.0.0
Date: March 2026
================================================================================
"""

from generator_gui import main

if __name__ == '__main__':
    main()
