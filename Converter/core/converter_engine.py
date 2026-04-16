"""
Converter Engine Module

Core conversion logic from JSON to integer DZN format.
Handles bus schedule parsing, energy calculation, and DZN file generation.

Based on: Scripts/data-processing/convert_json_to_integer_dzn.py
Author: AVISPA Research Team
Date: April 2026
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ConverterEngine:
    """Convert JSON bus schedules to integer DZN format."""

    # Scaling factor
    SCALE = 10

    # Model parameters
    CMAX = 1000  # 100.0 * 10
    CMIN = 200   # 20.0 * 10
    ALPHA = 100  # 10.0 * 10
    MU = 50      # 5.0 * 10
    SM = 10      # 1.0 * 10
    PSI = 10     # 1.0 * 10
    BETA = 100   # 10.0 * 10
    M = 100000   # 10000.0 * 10

    @staticmethod
    def parse_time_to_minutes(time_str: str) -> float:
        """
        Convert time string (HH:MM format) to minutes since 00:00.

        Args:
            time_str: Time in "HH:MM" format

        Returns:
            Minutes since midnight as float
        """
        try:
            hours, minutes = map(int, time_str.split(':'))
            return hours * 60 + minutes
        except Exception as e:
            logger.error(f"Error parsing time '{time_str}': {e}")
            return 0.0

    @staticmethod
    def scale_to_integer(value: float) -> int:
        """
        Scale a floating-point value to integer by multiplying by SCALE.

        Args:
            value: Original floating-point value

        Returns:
            Scaled integer value (rounded to nearest int)
        """
        return round(value * ConverterEngine.SCALE)

    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate Euclidean distance between two GPS coordinates.

        Args:
            lat1, lon1: First coordinate
            lat2, lon2: Second coordinate

        Returns:
            Distance in arbitrary units
        """
        return ((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2) ** 0.5

    @staticmethod
    def process_bus_line(line_data: Dict[str, Any]) -> List[Dict[str, List]]:
        """
        Process a single bus line from JSON and extract all buses.

        Args:
            line_data: Dictionary containing line information

        Returns:
            List of processed bus dictionaries
        """
        buses = line_data.get('buses', [])
        processed_buses = []

        for bus_idx, bus in enumerate(buses):
            path = bus.get('path', [])

            if not path:
                logger.warning(f"Bus {bus_idx} has empty path. Skipping.")
                continue

            # Extract station IDs
            station_ids = [stop['station_id'] for stop in path]

            # Extract and convert times to minutes
            times = [ConverterEngine.parse_time_to_minutes(stop['time']) for stop in path]

            # Calculate time deltas (travel time between consecutive stops)
            time_deltas = [0.0]
            for i in range(1, len(times)):
                delta = times[i] - times[i-1]
                time_deltas.append(delta)

            # Calculate distances (energy consumption)
            distances = [0.0]
            for i in range(1, len(path)):
                if 'lat' in path[i] and 'lon' in path[i] and 'lat' in path[i-1] and 'lon' in path[i-1]:
                    dist = ConverterEngine.calculate_distance(
                        path[i-1]['lat'], path[i-1]['lon'],
                        path[i]['lat'], path[i]['lon']
                    )
                    energy = (dist * 0.01) * 10
                else:
                    time_minutes = time_deltas[i]
                    energy = time_minutes * 0.20

                distances.append(energy)

            processed_buses.append({
                'station_ids': station_ids,
                'times': times,
                'time_deltas': time_deltas,
                'energy_consumption': distances
            })

        return processed_buses

    @classmethod
    def convert_json_to_dzn(cls, json_file: Path, output_file: Path,
                           variant_name: str = "") -> Tuple[bool, str]:
        """
        Convert a JSON bus schedule file to integer DZN format.

        Args:
            json_file: Path to input JSON file
            output_file: Path to output DZN file
            variant_name: Name of the variant (e.g., "20_0")

        Returns:
            (success: bool, message: str)
        """
        logger.info(f"Converting {json_file.name} to integer DZN format...")

        try:
            # Read JSON file
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Process all lines and collect buses
            all_buses = []
            for line_data in data:
                buses = cls.process_bus_line(line_data)
                all_buses.extend(buses)

            if not all_buses:
                return False, f"No buses found in {json_file.name}"

            # Collect all unique stations
            all_stations = set()
            for bus in all_buses:
                all_stations.update(bus['station_ids'])

            # Create station mapping (1-indexed)
            station_to_idx = {st: idx + 1 for idx, st in enumerate(sorted(all_stations))}

            # Determine dimensions
            num_buses = len(all_buses)
            num_stations = len(all_stations)
            max_stops = max(len(bus['station_ids']) for bus in all_buses)

            # Prepare arrays with padding
            st_bi = []
            D = []
            T = []
            tau_bi = []
            num_stops = []

            for bus in all_buses:
                num_stops.append(len(bus['station_ids']))

                # Map stations to indices and pad
                stations = [station_to_idx[st] for st in bus['station_ids']]
                stations += [stations[-1]] * (max_stops - len(stations))
                st_bi.extend(stations)

                # Scale and pad energy consumption
                energy = [cls.scale_to_integer(e) for e in bus['energy_consumption']]
                energy += [0] * (max_stops - len(energy))
                D.extend(energy)

                # Scale and pad travel times
                times = [cls.scale_to_integer(t) for t in bus['time_deltas']]
                times += [0] * (max_stops - len(times))
                T.extend(times)

                # Scale and pad schedule times
                schedule = [cls.scale_to_integer(t) for t in bus['times']]
                schedule += [cls.scale_to_integer(bus['times'][-1])] * (max_stops - len(schedule))
                tau_bi.extend(schedule)

            # Generate DZN file
            base_name = json_file.stem.replace('buses_input', '')
            base_name = base_name.strip('_') if base_name else 'default'

            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("% " + "=" * 76 + "\n")
                f.write(f"% CLP Test Case: {base_name} (variant: {variant_name})\n")
                f.write("% " + "=" * 76 + "\n")
                f.write("% Source: JITS2022 Test Battery\n")
                f.write(f"% Original file: {json_file.name}\n")
                f.write("% Converted to INTEGER CLP format with SCALE=10\n")
                f.write("%\n")
                f.write("% CONVERSION DETAILS:\n")
                f.write("% - All floating-point values multiplied by 10 and rounded to integers\n")
                f.write("% - Example: 42.5 minutes -> 425 (integer)\n")
                f.write("%           1.3 kWh -> 13 (integer)\n")
                f.write("%\n")
                f.write("% IMPORTANT: To interpret results, divide integer values by 10:\n")
                f.write("%   - Time: integer_value / 10 = minutes\n")
                f.write("%   - Energy: integer_value / 10 = kWh\n")
                f.write("% " + "=" * 76 + "\n\n")

                # Problem dimensions
                f.write("% --- Problem Dimensions ---\n")
                f.write(f"num_buses = {num_buses};\n")
                f.write(f"num_stations = {num_stations};\n\n")

                # Energy parameters
                f.write("% --- Energy Parameters (CLP Model) ---\n")
                f.write("% All values are INTEGERS scaled by x10 from original floating-point values\n")
                f.write(f"Cmax = {cls.CMAX};  % Maximum battery capacity (original: 100.0 kWh)\n")
                f.write(f"Cmin = {cls.CMIN};   % Minimum reserve (original: 20.0 kWh)\n")
                f.write(f"alpha = {cls.ALPHA};  % Fast charging rate (original: 10.0 kWh per minute)\n\n")

                # Time and schedule parameters
                f.write("% --- Time and Schedule Parameters ---\n")
                f.write("% All values are INTEGERS scaled by x10 from original floating-point values\n")
                f.write(f"mu = {cls.MU};      % Maximum delay allowed (original: 5.0 minutes)\n")
                f.write(f"SM = {cls.SM};      % Safety margin (original: 1.0 minutes)\n")
                f.write(f"psi = {cls.PSI};     % Minimum charging time (original: 1.0 minutes)\n")
                f.write(f"beta = {cls.BETA};   % Maximum charging time per stop (original: 10.0 minutes)\n")
                f.write(f"M = {cls.M};   % Big-M constant (original: 10000.0)\n\n")

                # Route structure
                f.write("% --- Route Structure ---\n")
                f.write(f"max_stops = {max_stops};\n")
                f.write(f"num_stops = {num_stops};\n\n")

                # Station sequence
                f.write("% --- Station Sequence (st_bi) ---\n")
                f.write("% Maps each bus stop to a physical station ID (1-indexed)\n")
                f.write(f"st_bi = array2d(1..{num_buses}, 1..{max_stops}, [\n")
                for i in range(num_buses):
                    start_idx = i * max_stops
                    end_idx = start_idx + max_stops
                    bus_stations = st_bi[start_idx:end_idx]
                    line = "  " + ",".join(map(str, bus_stations))
                    f.write(line + ("," if i < num_buses - 1 else "") + f"  % Bus {i+1}\n")
                f.write("]);\n\n")

                # Energy consumption
                f.write("% --- Energy Consumption (D) ---\n")
                f.write("% Energy consumed between stops (INTEGER values, divide by 10 for kWh)\n")
                f.write("% Original floating-point values have been scaled by x10\n")
                f.write(f"D = array2d(1..{num_buses}, 1..{max_stops}, [\n")
                for i in range(num_buses):
                    start_idx = i * max_stops
                    end_idx = start_idx + max_stops
                    bus_energy = D[start_idx:end_idx]
                    line = "  " + ",".join(map(str, bus_energy))
                    f.write(line + ("," if i < num_buses - 1 else "") + f"  % Bus {i+1}\n")
                f.write("]);\n\n")

                # Travel time
                f.write("% --- Travel Time (T) ---\n")
                f.write("% Time between stops (INTEGER values, divide by 10 for minutes)\n")
                f.write("% Original floating-point values have been scaled by x10\n")
                f.write(f"T = array2d(1..{num_buses}, 1..{max_stops}, [\n")
                for i in range(num_buses):
                    start_idx = i * max_stops
                    end_idx = start_idx + max_stops
                    bus_times = T[start_idx:end_idx]
                    line = "  " + ",".join(map(str, bus_times))
                    f.write(line + ("," if i < num_buses - 1 else "") + f"  % Bus {i+1}\n")
                f.write("]);\n\n")

                # Schedule
                f.write("% --- Original Timetable (tau_bi) ---\n")
                f.write("% Scheduled arrival times (INTEGER values, divide by 10 for minutes since 00:00)\n")
                f.write("% Original floating-point values have been scaled by x10\n")
                f.write(f"tau_bi = array2d(1..{num_buses}, 1..{max_stops}, [\n")
                for i in range(num_buses):
                    start_idx = i * max_stops
                    end_idx = start_idx + max_stops
                    bus_schedule = tau_bi[start_idx:end_idx]
                    line = "  " + ",".join(map(str, bus_schedule))
                    f.write(line + ("," if i < num_buses - 1 else "") + f"  % Bus {i+1}\n")
                f.write("]);\n")

            logger.info(f"Successfully created {output_file.name}")
            logger.info(f"  - Buses: {num_buses}, Stations: {num_stations}, Max stops: {max_stops}")
            return True, f"Converted successfully: {num_buses} buses, {num_stations} stations"

        except Exception as e:
            logger.error(f"Error converting {json_file.name}: {e}", exc_info=True)
            return False, f"Conversion error: {str(e)}"

    @classmethod
    def batch_convert_files(cls, json_files: List[Path], output_dir: Path) -> Tuple[int, int, List[str]]:
        """
        Convert multiple JSON files to DZN format.

        Args:
            json_files: List of JSON file paths
            output_dir: Output directory for DZN files

        Returns:
            (success_count: int, failure_count: int, messages: List[str])
        """
        success_count = 0
        failure_count = 0
        messages = []

        for json_file in json_files:
            # Extract variant name
            parts = json_file.stem.split('_')
            variant = '_'.join(parts[2:]) if len(parts) > 2 else ""

            # Generate output filename
            base_name = json_file.stem.replace('buses_input', '')
            base_name = base_name.strip('_') if base_name else 'default'
            output_file = output_dir / f"{output_dir.name}{base_name}.dzn"

            success, message = cls.convert_json_to_dzn(json_file, output_file, variant)
            if success:
                success_count += 1
                messages.append(f"✓ {json_file.name}: {message}")
            else:
                failure_count += 1
                messages.append(f"✗ {json_file.name}: {message}")

        return success_count, failure_count, messages
