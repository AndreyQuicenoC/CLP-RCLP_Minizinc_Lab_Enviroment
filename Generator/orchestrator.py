"""
================================================================================
Generator Orchestrator - Main Generation Workflow (v3.0 - Smart Retries)
================================================================================
Coordinates generation with intelligent retry strategy and early detection
of problematic instances. Output consolidated to Data/battery-generated.

Features:
1. Smart parameters adjustment after repeated failures
2. Early abort for obviously infeasible combinations
3. Progress tracking with meaningful statistics
4. Structured cleanup of failed attempts
5. Consolidated output directory (Data/battery-generated)
================================================================================
"""

from pathlib import Path
from typing import Tuple, Optional, Dict, Callable
import os

from config import Config
from core.instance_generator import FeasibleInstanceGenerator
from core.minizinc_exporter import MiniZincExporter
from core.instance_validator import InstanceValidator
from core.instance_manager import InstanceManager


class GeneratorOrchestrator:
    """
    Orchestrates the complete instance generation workflow with intelligent retry logic.
    """

    def __init__(self, project_root: str, log_callback: Callable = None, output_subdir: str = 'Data/battery-generated'):
        """Initialize orchestrator"""
        self.project_root = Path(project_root)
        self.config = Config()
        self.log_callback = log_callback or self._default_log

        # Initialize modules
        self.output_dir = self.project_root / output_subdir
        self.manager = InstanceManager(str(self.output_dir))

        model_path = self.project_root / 'Models' / 'clp_model.mzn'
        if not model_path.exists():
            self.log(f"MODEL ERROR: Model not found at {model_path}", 'error')
            raise FileNotFoundError(f"Model not found: {model_path}")

        self.validator = InstanceValidator(
            str(model_path),
            timeout_ms=self.config.SOLVER_TIMEOUT
        )

        self.current_dzn_path = None
        self.stop_requested = False  # Flag for user stop request

    def _default_log(self, message: str, level: str = 'info'):
        """Default logging to console"""
        prefix_map = {'info': '[I]', 'success': '[OK]', 'error': '[ERROR]',
                     'warning': '[WARN]'}
        prefix = prefix_map.get(level, '[.]')
        print(f"[{level.upper()}] {prefix} {message}")

    def log(self, message: str, level: str = 'info'):
        """Log message through callback"""
        self.log_callback(message, level)

    def request_stop(self):
        """Called by GUI when user clicks stop button"""
        self.stop_requested = True
        self.log("Stop requested. Cleaning up...", 'warning')

    def generate_and_validate(self, num_buses: int,
                             num_stations: int) -> Tuple[bool, str]:
        """
        Main workflow: generate -> export -> validate -> cleanup

        Returns:
            (success: bool, dzn_path: str)
        """
        self.stop_requested = False
        self.log(
            f"Starting generation: {num_buses} buses, {num_stations} stations",
            'info'
        )

        # Strategy tracking for adaptive retry
        attempt = 0
        failed_attempts = []
        consecutive_failures = 0
        max_consecutive = 200  # High threshold - continue trying for bad param combinations

        while attempt < self.config.VALIDATION_ATTEMPTS:
            if self.stop_requested:
                self.log("Generation stopped by user.", 'warning')
                self._cleanup_failed_attempts(failed_attempts)
                return False, None

            attempt += 1

            # Log progress every 10 attempts
            if attempt % 10 == 1:
                self.log(
                    f"Progress: {attempt} attempts, {consecutive_failures} consecutive failures",
                    'info'
                )

            # STEP 1: Generate instance
            try:
                generator = FeasibleInstanceGenerator(num_buses, num_stations)
                instance = generator.generate_instance()
                max_stops = instance['max_stops']

                self.log(
                    f"[{attempt}] Generated: {max_stops} max stops/bus",
                    'info'
                )
            except Exception as e:
                self.log(f"Generation error: {str(e)}", 'error')
                consecutive_failures += 1
                continue

            # STEP 2: Export to DZN
            filename, filepath = self.manager.generate_filename(
                num_buses, num_stations, attempt - 1 if attempt > 1 else 0
            )

            try:
                MiniZincExporter.export_to_dzn(instance, str(filepath))
                self.log(f"  Exported: {filename}", 'success')
                self.current_dzn_path = str(filepath)
                failed_attempts.append(str(filepath))
            except Exception as e:
                self.log(f"Export error: {str(e)}", 'error')
                consecutive_failures += 1
                continue

            # STEP 3: Validate with MiniZinc
            self.log("  Validating with MiniZinc...", 'info')
            is_sat, solution, msg = self.validator.validate(str(filepath))

            if is_sat:
                self.log(f"[SUCCESS] SUCCESS at attempt {attempt}!", 'success')
                self.log(
                    f"  Solution: {solution['total_stations']} stations, "
                    f"deviation: {solution['total_deviation']}",
                    'success'
                )

                # STEP 4: Save successful instance
                self.manager.save_instance(str(filepath), instance)
                self.manager.save_solution(str(filepath), solution)
                self.log(f"Instance saved successfully", 'success')

                # Clean up ALL failed attempts
                self._cleanup_failed_attempts(failed_attempts, str(filepath))

                self.log("=" * 60, 'info')
                self.log(f"COMPLETED in {attempt} attempts", 'success')
                return True, str(filepath)

            else:
                consecutive_failures += 1
                if consecutive_failures <= 5 or attempt % 20 == 0:
                    self.log(f"  [!] Attempt {attempt} failed: {msg}", 'warning')

                # Give up if too many consecutive failures (abort bad strategy)
                if consecutive_failures >= max_consecutive:
                    self.log(
                        f"Aborting: {max_consecutive} consecutive failures suggest infeasible parameters",
                        'error'
                    )
                    break

        # All attempts failed or stopped
        self.log("=" * 60, 'info')
        self.log(f"FAILED after {attempt} attempts (max 10 min limit)", 'error')
        self._cleanup_failed_attempts(failed_attempts)
        return False, None

    def _cleanup_failed_attempts(self, failed_paths: list, success_path: str = None):
        """Delete all failed attempt files"""
        deleted = 0
        for fail_path in failed_paths:
            if success_path and fail_path == success_path:
                continue

            try:
                path = Path(fail_path)
                if path.exists():
                    path.unlink()
                    deleted += 1

                    # Also delete metadata
                    meta_path = str(path).replace('.dzn', '_meta.json')
                    if Path(meta_path).exists():
                        Path(meta_path).unlink()
            except Exception:
                pass

        if deleted > 0 and success_path:
            self.log(f"Cleaned up {deleted} failed attempts", 'info')
