"""
================================================================================
Instance Manager Module - File Management
================================================================================
Manages generated instance files: creation, deletion, and organization.
Ensures only successful instances are kept.
================================================================================
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple


class InstanceManager:
    """Manages instance files and metadata"""

    def __init__(self, output_dir: str):
        """
        Initialize manager

        Args:
            output_dir: Directory for generated instances
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.expected_dir = self.output_dir / "Expected Results"
        self.expected_dir.mkdir(parents=True, exist_ok=True)

    def generate_filename(self, num_buses: int, num_stations: int,
                         attempt: int = 0) -> Tuple[str, Path]:
        """
        Generate unique instance filename

        Returns:
            (filename, full_path)
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        suffix = f"_v{attempt}" if attempt > 0 else ""
        filename = (
            f"clp_generated_{timestamp}_{num_buses}b_{num_stations}s{suffix}.dzn"
        )
        filepath = self.output_dir / filename

        return filename, filepath

    def save_instance(self, filepath: str, instance: Dict) -> None:
        """Save instance metadata to JSON"""
        metadata = {
            'instance': Path(filepath).stem,
            'generated': datetime.now().isoformat(),
            'num_buses': instance['num_buses'],
            'num_stations': instance['num_stations'],
            'max_stops': instance['max_stops'],
            'dzn_path': str(filepath),
            'parameters': {
                'Cmax': instance['Cmax'],
                'Cmin': instance['Cmin'],
                'alpha': instance['alpha'],
                'mu': instance['mu'],
                'SM': instance['SM'],
                'psi': instance['psi'],
                'beta': instance['beta'],
                'M': instance['M']
            }
        }

        meta_path = str(filepath).replace('.dzn', '_meta.json')
        with open(meta_path, 'w') as f:
            json.dump(metadata, f, indent=2)

    def save_solution(self, dzn_path: str, solution: Dict) -> None:
        """Save expected solution to Expected Results"""
        basename = Path(dzn_path).stem
        result_file = self.expected_dir / f"{basename}_expected.json"

        result_data = {
            'instance': basename,
            'generated': datetime.now().isoformat(),
            'solver': 'chuffed',
            'satisfiable': True,
            'solution': solution,
            'dzn_path': str(dzn_path)
        }

        with open(result_file, 'w') as f:
            json.dump(result_data, f, indent=2)

    def cleanup_temporary_files(self, prefix: str) -> int:
        """
        Clean up temporary/failed instance files

        Args:
            prefix: Prefix of files to clean (for this session)

        Returns:
            Number of files deleted
        """
        deleted = 0
        for f in self.output_dir.glob("*.dzn"):
            if '_v' in f.name:  # Failed attempt versions
                try:
                    f.unlink()
                    deleted += 1
                except Exception:
                    pass

        return deleted

    def get_latest_instance(self) -> Path:
        """Get most recently generated instance"""
        instances = list(self.output_dir.glob("clp_generated_*.dzn"))
        if not instances:
            return None
        instances_without_v = [i for i in instances if '_v' not in i.name]
        return max(instances_without_v, key=lambda p: p.stat().st_mtime) \
            if instances_without_v else None
