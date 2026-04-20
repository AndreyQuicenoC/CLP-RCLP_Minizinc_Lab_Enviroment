#!/usr/bin/env python3
"""
Quick test script to validate Generator works with improved algorithm.
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from generator_orchestrator import GeneratorOrchestrator

def test_generator():
    """Test generator with small instance"""
    project_root = Path(__file__).parent.parent

    orchestrator = GeneratorOrchestrator(str(project_root))

    # Test case 1: 2 buses, 4 stations (small, quick)
    print("\n" + "="*60)
    print("TEST 1: 2 buses, 4 stations")
    print("="*60)
    success, dzn_path = orchestrator.generate_and_validate(2, 4)

    if success:
        print(f"[OK] SUCCESS: Generated {Path(dzn_path).name}")
        return True
    else:
        print("[X] FAILED after many attempts")
        return False

if __name__ == '__main__':
    success = test_generator()
    sys.exit(0 if success else 1)
