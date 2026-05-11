"""
MiniZinc Executor - Run CLP/RCLP tests with multiple solvers

Handles MiniZinc execution with proper timeout management, output parsing,
and support for multiple solvers (chuffed, gecode, coin-bc, cp-sat, cplex, gurobi).

Authors: Andrey Quiceno and Juan Francesco García (AVISPA Team)
"""

import subprocess
import json
import re
from pathlib import Path
from typing import Dict, Tuple, Optional
import logging
import time

from .solvers import SolverType, SolverManager

logger = logging.getLogger(__name__)


class MiniZincExecutor:
    """Execute MiniZinc models with multiple solver support."""

    def __init__(self, model_path: str, timeout_seconds: int = 300):
        """
        Initialize executor.

        Args:
            model_path: Path to .mzn model file
            timeout_seconds: Execution timeout in seconds
        """
        self.model_path = Path(model_path)
        self.timeout_seconds = timeout_seconds

        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")

    def execute(self, dzn_file: str, solver: SolverType = SolverType.CHUFFED) -> Tuple[bool, Optional[Dict], Optional[float]]:
        """
        Execute MiniZinc with given instance and solver.

        Args:
            dzn_file: Path to .dzn instance file
            solver: Solver to use (default: chuffed)

        Returns:
            (success: bool, result: dict or None, execution_time: float or None)
            Result contains: num_buses, num_stations, charged_stations,
                           charging_locations, time_deviation, solver, execution_time
        """
        dzn_path = Path(dzn_file)
        if not dzn_path.exists():
            logger.error(f"Instance file not found: {dzn_file}")
            return False, None, None

        try:
            solver_name = SolverManager.get_minizinc_solver_name(solver)

            cmd = [
                "minizinc",
                "--solver", solver_name,
                "--time-limit", str(self.timeout_seconds * 1000),
                str(self.model_path),
                str(dzn_path)
            ]

            logger.debug(f"Running: {' '.join(cmd)}")

            # Measure execution time
            start_time = time.time()

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds + 10
            )

            execution_time = time.time() - start_time

            # Parse output
            if result.returncode == 0:
                success, parsed_result = self._parse_solution(result.stdout, dzn_path, solver)
                if success and parsed_result:
                    parsed_result['execution_time'] = execution_time
                    parsed_result['solver'] = SolverManager.get_display_name(solver)
                return success, parsed_result, execution_time
            else:
                logger.warning(f"MiniZinc failed with {solver_name}: {result.stderr[:200]}")
                return False, None, execution_time

        except subprocess.TimeoutExpired:
            logger.warning(f"MiniZinc execution timed out with {SolverManager.get_minizinc_solver_name(solver)}")
            return False, None, self.timeout_seconds
        except Exception as e:
            logger.error(f"Execution error: {str(e)}")
            return False, None, None

    def _parse_solution(self, output: str, dzn_path: Path, solver: SolverType) -> Tuple[bool, Optional[Dict]]:
        """
        Parse MiniZinc output to extract solution.

        Args:
            output: MiniZinc stdout
            dzn_path: Path to instance file (for metadata extraction)
            solver: Solver used for this execution

        Returns:
            (success: bool, result: dict or None)
        """
        try:
            # Check if satisfiable - look for actual "UNSATISFIABLE" marker
            if output.strip().startswith("UNSATISFIABLE") or "% UNSATISFIABLE" in output:
                logger.info(f"Instance is UNSATISFIABLE with {SolverManager.get_display_name(solver)}")
                return False, None

            # Extract key values from solution
            lines = output.strip().split("\n")
            result = self._extract_values(lines, dzn_path)

            if result is None:
                logger.warning(f"Could not parse solution values for {SolverManager.get_display_name(solver)}")
                return False, None

            logger.info(f"Solution found with {SolverManager.get_display_name(solver)}: {result.get('charged_stations', 0)} stations charged")
            return True, result

        except Exception as e:
            logger.error(f"Parse error: {str(e)}")
            return False, None

    def _extract_values(self, lines: list, dzn_path: Path) -> Optional[Dict]:
        """
        Extract solution values from MiniZinc output.

        Returns extracted values or None if parse fails.
        """
        result = {}

        # Extract num_buses and num_stations from DZN file
        try:
            with open(dzn_path, 'r', encoding='utf-8') as f:
                content = f.read()
                buses_match = re.search(r'num_buses\s*=\s*(\d+)', content)
                stations_match = re.search(r'num_stations\s*=\s*(\d+)', content)

                if buses_match and stations_match:
                    result['num_buses'] = int(buses_match.group(1))
                    result['num_stations'] = int(stations_match.group(1))
                else:
                    return None
        except Exception:
            return None

        # Extract from solution output (MiniZinc outputs in Spanish)
        solution_text = "\n".join(lines)

        # Look for "Estaciones instaladas: [...]" (Spanish for charging locations)
        estaciones_match = re.search(r'Estaciones instaladas:\s*\[(.*?)\]', solution_text, re.DOTALL)
        if estaciones_match:
            locations_str = estaciones_match.group(1)
            try:
                # Parse the array
                charging_locs = [int(x.strip()) for x in locations_str.split(',') if x.strip()]
                result['charging_locations'] = charging_locs
                result['charged_stations'] = sum(charging_locs)
            except ValueError:
                logger.warning(f"Failed to parse charging locations: {locations_str}")
                return None
        else:
            logger.warning("Could not find 'Estaciones instaladas' in output")
            return None

        # Look for "Desviacion total: N" (Spanish for time deviation)
        desviacion_match = re.search(r'Desviacion total:\s*(\d+)', solution_text)
        if desviacion_match:
            result['time_deviation'] = int(desviacion_match.group(1))
        else:
            logger.warning("Could not find 'Desviacion total' in output")
            result['time_deviation'] = 0

        return result
