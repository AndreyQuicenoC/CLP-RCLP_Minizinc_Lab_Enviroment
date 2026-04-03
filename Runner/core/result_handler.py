"""
Result Handler - Save test results in JSON and TXT formats

Manages output file generation and formatting.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Optional, Tuple

logger = logging.getLogger(__name__)


class ResultHandler:
    """Handle result file generation and storage."""

    def __init__(self, output_dir: str):
        """
        Initialize result handler.

        Args:
            output_dir: Directory to save results
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_results(self, filename: str, result: Dict) -> Tuple[bool, str, str]:
        """
        Save results in JSON and TXT formats.

        Args:
            filename: Base filename (without extension)
            result: Result dictionary

        Returns:
            (success: bool, json_path: str, txt_path: str)
        """
        try:
            # Save JSON
            json_path = self.output_dir / f"{filename}_result.json"
            self._save_json(json_path, result)

            # Save TXT
            txt_path = self.output_dir / f"{filename}_result.txt"
            self._save_txt(txt_path, result)

            logger.info(f"Results saved: {json_path}, {txt_path}")
            return True, str(json_path), str(txt_path)

        except Exception as e:
            logger.error(f"Save error: {str(e)}")
            return False, "", ""

    def _save_json(self, path: Path, result: Dict) -> None:
        """Save result as JSON with proper formatting."""
        json_data = {
            "num_buses": result.get('num_buses', 0),
            "num_stations": result.get('num_stations', 0),
            "charged_stations": result.get('charged_stations', 0),
            "charging_locations": result.get('charging_locations', []),
            "time_deviation": result.get('time_deviation', 0)
        }

        with open(path, 'w') as f:
            json.dump(json_data, f, indent=2)

    def _save_txt(self, path: Path, result: Dict) -> None:
        """Save result as human-readable TXT format."""
        num_buses = result.get('num_buses', 0)
        num_stations = result.get('num_stations', 0)
        charged = result.get('charged_stations', 0)
        locations = result.get('charging_locations', [])
        deviation = result.get('time_deviation', 0)

        # Format charging locations as binary array
        locations_str = "[" + ",".join(str(x) for x in locations) + "]"

        lines = [
            "=" * 60,
            "CLP-RCLP Test Execution Result",
            "=" * 60,
            "",
            f"Number of Buses:        {num_buses}",
            f"Number of Stations:     {num_stations}",
            f"Charged Stations:       {charged}",
            f"Charging Locations:     {locations_str}",
            f"Time Deviation:         {deviation} minutes",
            "",
            "=" * 60
        ]

        with open(path, 'w') as f:
            f.write("\n".join(lines))
