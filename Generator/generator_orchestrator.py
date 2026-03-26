"""
================================================================================
Generator Orchestrator - Main Generation Workflow
================================================================================
Coordinates the entire generation process: creation, validation, file
management. Implements robust retry logic and cleanup.
================================================================================
"""

from pathlib import Path
from typing import Tuple, Optional, Dict, Callable
import os

from config import Config
from instance_generator import FeasibleInstanceGenerator
from minizinc_exporter import MiniZincExporter
from instance_validator import InstanceValidator
from instance_manager import InstanceManager


class GeneratorOrchestrator:
    """
    Orchestrates the complete instance generation workflow:
    1. Generate instance
    2. Export to DZN
    3. Validate with MiniZinc
    4. Manage files (keep successful, delete failures)
    5. Save metadata
    """

    def __init__(self, project_root: str, log_callback: Callable = None, output_subdir: str = 'Tests/Output/Generator'):
        """
        Initialize orchestrator

        Args:
            project_root: Root directory of CLP-RCLP Minizinc project
            log_callback: Optional function(message, level) for logging
            output_subdir: Subdirectory for output (relative to project_root)
        """
        self.project_root = Path(project_root)
        self.config = Config()
        self.log_callback = log_callback or self._default_log

        # Initialize modules
        self.output_dir = self.project_root / output_subdir
        self.manager = InstanceManager(str(self.output_dir))

        model_path = self.project_root / 'Models' / 'clp_model.mzn'
        if not model_path.exists():
            self.log("MODEL ERROR: Model not found at {model_path}", 'error')
            raise FileNotFoundError(f"Model not found: {model_path}")

        self.validator = InstanceValidator(
            str(model_path),
            timeout_ms=self.config.SOLVER_TIMEOUT
        )

        self.current_dzn_path = None

    def _default_log(self, message: str, level: str = 'info'):
        """Default logging to console"""
        prefix_map = {'info': 'ℹ', 'success': '✓', 'error': '✗',
                     'warning': '⚠'}
        prefix = prefix_map.get(level, '•')
        print(f"[{level.upper()}] {prefix} {message}")

    def log(self, message: str, level: str = 'info'):
        """Log message through callback"""
        self.log_callback(message, level)

    def generate_and_validate(self, num_buses: int,
                             num_stations: int) -> Tuple[bool, str]:
        """
        Main workflow: generate → export → validate → cleanup

        CRITICAL BEHAVIOR: Iterates CONTINUOUSLY until SAT instance found.
        Does NOT stop after fixed attempts - only stops when SAT is achieved.

        Returns:
            (success: bool, dzn_path: str)
        """
        self.log(
            f"Starting generation: {num_buses} buses, {num_stations} stations",
            'info'
        )

        attempt = 0
        failed_attempts = []  # Track all failed attempts for cleanup

        while True:  # Iterate indefinitely until SAT found
            attempt += 1

            # STEP 1: Generate instance
            self.log(
                f"Attempt {attempt}: Generating instance...",
                'info'
            )

            try:
                generator = FeasibleInstanceGenerator(num_buses, num_stations)
                instance = generator.generate_instance()
                max_stops = instance['max_stops']

                self.log(
                    f"Instance generated: {max_stops} max stops per bus",
                    'success'
                )
            except Exception as e:
                self.log(f"Generation failed: {str(e)}", 'error')
                continue

            # STEP 2: Export to DZN
            filename, filepath = self.manager.generate_filename(
                num_buses, num_stations, attempt - 1 if attempt > 1 else 0
            )

            try:
                MiniZincExporter.export_to_dzn(instance, str(filepath))
                self.log(f"Exported to: {filename}", 'success')
                self.current_dzn_path = str(filepath)
                failed_attempts.append(str(filepath))
            except Exception as e:
                self.log(f"Export failed: {str(e)}", 'error')
                continue

            # STEP 3: Validate with MiniZinc
            self.log("Validating with MiniZinc (timeout: 10 min)...", 'info')
            is_sat, solution, msg = self.validator.validate(str(filepath))

            if is_sat:
                self.log(f"✓ Instance is SATISFIABLE!", 'success')
                self.log(
                    f"  Solution: {solution['total_stations']} stations, "
                    f"deviation: {solution['total_deviation']}",
                    'success'
                )

                # STEP 4: Save successful instance
                self.manager.save_instance(str(filepath), instance)
                self.manager.save_solution(str(filepath), solution)
                self.log(f"Instance saved: {filename}", 'success')

                # Clean up ALL failed attempts
                self._cleanup_failed_attempts(failed_attempts, str(filepath))

                self.log("=" * 60, 'info')
                return True, str(filepath)

            else:
                self.log(f"Attempt failed: {msg}", 'warning')
                # Continue to next attempt - no limit!

    def _cleanup_failed_attempts(self, failed_paths: list, success_path: str):
        """Delete all failed attempt files, keeping only the successful one"""
        for fail_path in failed_paths:
            if fail_path != success_path:
                try:
                    path = Path(fail_path)
                    if path.exists():
                        path.unlink()

                        # Also delete metadata
                        meta_path = str(path).replace('.dzn', '_meta.json')
                        if Path(meta_path).exists():
                            Path(meta_path).unlink()
                except Exception:
                    pass
