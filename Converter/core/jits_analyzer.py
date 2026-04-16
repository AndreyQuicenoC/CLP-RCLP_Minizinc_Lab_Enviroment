"""
JITS2022 Analyzer Module

Analyzes JITS2022 dataset structure to extract test directories and JSON files.
Handles validation of directory structure and support files.

Author: AVISPA Research Team
Date: April 2026
"""

import logging
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import json as json_module

logger = logging.getLogger(__name__)


class JITSAnalyzer:
    """Analyze and manage JITS2022 dataset structure."""

    @staticmethod
    def get_test_directories(jits_base: Path) -> List[str]:
        """
        Get all test directories in JITS2022/Code/Data.

        Args:
            jits_base: Path to JITS2022/Code/Data directory

        Returns:
            List of directory names (sorted)
        """
        if not jits_base.exists():
            logger.warning(f"JITS base path not found: {jits_base}")
            return []

        directories = [d.name for d in jits_base.iterdir() if d.is_dir()]
        return sorted(directories)

    @staticmethod
    def get_json_files(test_dir: Path, json_pattern: str = "*_input.json") -> List[Path]:
        """
        Get all JSON files matching pattern in a test directory.

        Args:
            test_dir: Path to test directory (e.g., cork-1-line)
            json_pattern: Glob pattern for JSON files

        Returns:
            List of JSON file paths (sorted)
        """
        if not test_dir.exists():
            logger.warning(f"Test directory not found: {test_dir}")
            return []

        json_files = sorted(test_dir.glob(json_pattern))
        return json_files

    @staticmethod
    def check_support_files(test_dir: Path) -> Dict[str, bool]:
        """
        Check which support files exist in test directory.

        Args:
            test_dir: Path to test directory

        Returns:
            Dictionary mapping filename to existence boolean
        """
        support_files = {
            "distances_input.csv": False,
            "stations_input.csv": False,
            "input_report.txt": False,
        }

        for filename in support_files:
            file_path = test_dir / filename
            support_files[filename] = file_path.exists()

        return support_files

    @staticmethod
    def validate_json_file(json_path: Path) -> Tuple[bool, str]:
        """
        Validate JSON file structure.

        Args:
            json_path: Path to JSON file

        Returns:
            (is_valid: bool, error_message: str)
        """
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json_module.load(f)

            # Check if it's a list (array of line objects)
            if not isinstance(data, list):
                return False, "JSON must be an array of line objects"

            if len(data) == 0:
                return False, "JSON array is empty"

            # Check first item structure
            first_item = data[0]
            if 'buses' not in first_item or not isinstance(first_item['buses'], list):
                return False, "JSON items must have 'buses' array"

            return True, ""

        except json_module.JSONDecodeError as e:
            return False, f"Invalid JSON: {str(e)}"
        except Exception as e:
            return False, f"Error validating JSON: {str(e)}"

    @staticmethod
    def get_json_metadata(json_path: Path) -> Dict[str, any]:
        """
        Extract metadata from JSON file.

        Args:
            json_path: Path to JSON file

        Returns:
            Dictionary with metadata (num_buses, num_stations, num_lines, etc.)
        """
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json_module.load(f)

            all_stations = set()
            total_buses = 0
            num_lines = len(data)

            for line_obj in data:
                buses = line_obj.get('buses', [])
                total_buses += len(buses)

                for bus in buses:
                    path = bus.get('path', [])
                    for stop in path:
                        station_id = stop.get('station_id')
                        if station_id is not None:
                            all_stations.add(station_id)

            return {
                "num_buses": total_buses,
                "num_stations": len(all_stations),
                "num_lines": num_lines,
                "file_size_kb": json_path.stat().st_size / 1024,
                "filename": json_path.name,
            }

        except Exception as e:
            logger.error(f"Error extracting metadata from {json_path}: {e}")
            return {}
