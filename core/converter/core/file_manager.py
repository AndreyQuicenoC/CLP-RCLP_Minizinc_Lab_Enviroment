"""
File Manager Module

Manages file operations for the converter including output directory creation,
data file copying, and cleanup operations.

Author: AVISPA Research Team
Date: April 2026
"""

import logging
import shutil
from pathlib import Path
from typing import List, Tuple

logger = logging.getLogger(__name__)


class FileManager:
    """Handle file operations for conversion process."""

    @staticmethod
    def create_output_structure(battery_dir: Path, test_name: str, source_dir: Path) -> Tuple[bool, Path]:
        """
        Create output directory structure and copy data files.

        Creates: battery_dir/test_name/
        Copies required data files if they exist in source directory.

        Args:
            battery_dir: Base battery directory (e.g., Data/Battery Own)
            test_name: Name of the test (directory name)
            source_dir: Source directory containing data files

        Returns:
            (success: bool, output_path: Path)
        """
        try:
            # Create test directory
            output_path = battery_dir / test_name
            output_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created output directory: {output_path}")

            # Copy required data files if they exist
            data_files = ["distances_input.csv", "stations_input.csv", "input_report.txt"]
            for filename in data_files:
                source_file = source_dir / filename
                if source_file.exists():
                    dest_file = output_path / filename
                    shutil.copy2(source_file, dest_file)
                    logger.info(f"Copied data file: {filename}")

            return True, output_path

        except Exception as e:
            logger.error(f"Error creating output structure: {e}")
            return False, Path()

    @staticmethod
    def ensure_solver_dir(output_path: Path, solver_name: str = "") -> Path:
        """
        Ensure solver subdirectory exists in output path.

        Args:
            output_path: Output directory path
            solver_name: Optional solver subdirectory name

        Returns:
            Path to solver directory (or output_path if solver_name is empty)
        """
        if solver_name:
            solver_dir = output_path / solver_name
            solver_dir.mkdir(parents=True, exist_ok=True)
            return solver_dir
        return output_path

    @staticmethod
    def validate_output_path(output_path: Path) -> bool:
        """
        Validate that output path is writable.

        Args:
            output_path: Path to validate

        Returns:
            True if path is writable, False otherwise
        """
        try:
            test_file = output_path / ".test_write"
            test_file.write_text("test")
            test_file.unlink()
            return True
        except Exception as e:
            logger.error(f"Output path not writable: {e}")
            return False

    @staticmethod
    def get_existing_dzn_files(output_path: Path) -> List[Path]:
        """
        Get list of existing DZN files in output path.

        Args:
            output_path: Directory to search

        Returns:
            List of existing DZN file paths
        """
        if not output_path.exists():
            return []

        return sorted(output_path.glob("*.dzn"))

    @staticmethod
    def cleanup_failed_conversion(output_path: Path, dzn_filename: str) -> bool:
        """
        Remove DZN file if conversion fails (cleanup).

        Args:
            output_path: Directory containing DZN file
            dzn_filename: Name of DZN file to remove

        Returns:
            True if cleanup successful, False otherwise
        """
        try:
            dzn_file = output_path / dzn_filename
            if dzn_file.exists():
                dzn_file.unlink()
                logger.info(f"Cleaned up failed conversion: {dzn_filename}")
            return True
        except Exception as e:
            logger.error(f"Error cleaning up file: {e}")
            return False
