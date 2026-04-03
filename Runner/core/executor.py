"""
MiniZinc Executor - Run CLP/RCLP tests

Handles MiniZinc execution with proper timeout management and output parsing.
"""

import subprocess
import json
import re
from pathlib import Path
from typing import Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class MiniZincExecutor:
    """Execute MiniZinc models and parse results."""

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

    def execute(self, dzn_file: str) -> Tuple[bool, Optional[Dict]]:
        """
        Execute MiniZinc with given instance.

        Args:
            dzn_file: Path to .dzn instance file

        Returns:
            (success: bool, result: dict or None)
            Result contains: num_buses, num_stations, charged_stations,
                           charging_locations, time_deviation
        """
        dzn_path = Path(dzn_file)
        if not dzn_path.exists():
            logger.error(f"Instance file not found: {dzn_file}")
            return False, None

        try:
            cmd = [
                "minizinc",
                "--solver", "chuffed",
                "--time-limit", str(self.timeout_seconds * 1000),
                str(self.model_path),
                str(dzn_path)
            ]

            logger.debug(f"Running: {' '.join(cmd)}")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds + 10
            )

            # Parse output
            if result.returncode == 0:
                return self._parse_solution(result.stdout, dzn_path)
            else:
                logger.warning(f"MiniZinc failed: {result.stderr[:200]}")
                return False, None

        except subprocess.TimeoutExpired:
            logger.warning("MiniZinc execution timed out")
            return False, None
        except Exception as e:
            logger.error(f"Execution error: {str(e)}")
            return False, None

    def _parse_solution(self, output: str, dzn_path: Path) -> Tuple[bool, Optional[Dict]]:
        """
        Parse MiniZinc output to extract solution.

        Args:
            output: MiniZinc stdout
            dzn_path: Path to instance file (for metadata extraction)

        Returns:
            (success: bool, result: dict or None)
        """
        try:
            # Check if satisfiable
            if "UNSATISFIABLE" in output or "=====\n\n" in output:
                logger.info("Instance is UNSATISFIABLE")
                return False, None

            # Extract key values from solution
            lines = output.strip().split("\n")
            result = self._extract_values(lines, dzn_path)

            if result is None:
                logger.warning("Could not parse solution values")
                return False, None

            logger.info(f"Solution found: {result['charged_stations']} stations charged")
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
            with open(dzn_path, 'r') as f:
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

        # Extract from solution output
        solution_text = "\n".join(lines)

        # Look for charging locations array
        locations_match = re.search(r'charging_locations\s*=\s*\[(.*?)\]', solution_text)
        if locations_match:
            locations_str = locations_match.group(1)
            try:
                charging_locs = [int(x.strip()) for x in locations_str.split(',') if x.strip()]
                result['charging_locations'] = charging_locs
                result['charged_stations'] = sum(charging_locs)
            except ValueError:
                return None
        else:
            return None

        # Look for time deviation
        deviation_match = re.search(r'total_deviation\s*=\s*(\d+)', solution_text)
        if deviation_match:
            result['time_deviation'] = int(deviation_match.group(1))
        else:
            result['time_deviation'] = 0

        return result
