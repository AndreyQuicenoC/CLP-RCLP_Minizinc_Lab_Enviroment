"""
================================================================================
Instance Validator Module - MiniZinc Validation
================================================================================
Validates generated instances by running the CLP model with the chuffed solver.
Implements robust timeout handling and solution parsing.
================================================================================
"""

import subprocess
import re
from typing import Tuple, Optional, Dict
from pathlib import Path


class InstanceValidator:
    """Validates instances using MiniZinc solver"""

    def __init__(self, model_path: str, timeout_ms: int = 600000):
        """
        Initialize validator

        Args:
            model_path: Path to MiniZinc model file
            timeout_ms: Timeout in milliseconds (default 600s = 10 min)
        """
        self.model_path = model_path
        self.timeout_ms = timeout_ms
        self.timeout_sec = timeout_ms / 1000

    def validate(self, dzn_path: str) -> Tuple[bool, Optional[Dict], str]:
        """
        Validate instance by running MiniZinc

        Returns:
            (is_satisfiable, solution_dict, status_message)
        """
        if not Path(self.model_path).exists():
            return False, None, f"Model not found: {self.model_path}"

        if not Path(dzn_path).exists():
            return False, None, f"Instance not found: {dzn_path}"

        try:
            cmd = [
                'minizinc',
                '--solver', 'chuffed',
                '--time-limit', str(self.timeout_ms),
                self.model_path,
                dzn_path
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout_sec + 10
            )

            output = result.stdout + result.stderr

            # Check for satisfiability
            if 'UNSATISFIABLE' in output:
                return False, None, "Instance is UNSATISFIABLE"

            if 'UNKNOWN' in output:
                return False, None, "Solver returned UNKNOWN (timeout or complexity)"

            # Try to parse solution
            if 'Total estaciones:' in output:
                solution = self._parse_solution(output)
                return True, solution, "SATISFIABLE"

            # No clear result
            if 'error' in output.lower():
                error_line = [line for line in output.split('\n')
                             if 'error' in line.lower()][0]
                return False, None, f"Solver error: {error_line}"

            return False, None, "No solution found"

        except subprocess.TimeoutExpired:
            return False, None, f"Timeout expired ({self.timeout_sec:.0f}s)"
        except FileNotFoundError:
            return False, None, "MiniZinc not found. Install MiniZinc first."
        except Exception as e:
            return False, None, f"Validation error: {str(e)}"

    @staticmethod
    def _parse_solution(output: str) -> Optional[Dict]:
        """Parse solution from MiniZinc output"""
        try:
            solution = {}

            # Extract total stations
            match = re.search(r'Total estaciones:\s*(\d+)', output)
            if match:
                solution['total_stations'] = int(match.group(1))

            # Extract total deviation
            match = re.search(r'Desviacion total:\s*(\d+)', output)
            if match:
                solution['total_deviation'] = int(match.group(1))

            return solution if solution else None

        except Exception:
            return None
