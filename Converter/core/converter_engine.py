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

    def __init__(self, config=None, distances_dict=None):
        """
        Initialize converter engine with configuration and data.

        Args:
            config: ExperimentConfig instance (or None for defaults)
            distances_dict: Dict[(from_id, to_id)] -> distance_meters (or None to use fallback)
        """
        from .experiment_config import ExperimentConfig

        self.config = config or ExperimentConfig()
        self.distances_dict = distances_dict or {}

        # Get scaled parameters from config
        scaled = self.config.to_scaled_dict()
        self.SCALE = self.config.scale
        self.CMAX = scaled['cmax']
        self.CMIN = scaled['cmin']
        self.ALPHA = scaled['alpha']
        self.MU = scaled['mu']
        self.SM = scaled['sm']
        self.PSI = scaled['psi']
        self.BETA = scaled['beta']
        self.M = 100000 * self.SCALE  # Big-M constant

        # Speed bounds (in km/h)
        self.MIN_SPEED_KMH = self.config.model_speed
        self.MAX_SPEED_KMH = 60

        # Rest time (converted to seconds)
        self.REST_TIME_SECONDS = self.config.rest_time * 60

    @staticmethod
    def parse_time_to_minutes(time_str: str) -> int:
        """
        Convert time string (HH:MM format) to minutes since 00:00.

        Args:
            time_str: Time in "HH:MM" format

        Returns:
            Minutes since midnight as integer
        """
        try:
            hours, minutes = map(int, time_str.split(':'))
            return hours * 60 + minutes
        except Exception as e:
            logger.error(f"Error parsing time '{time_str}': {e}")
            return 0

    def scale_to_integer(self, value: float) -> int:
        """
        Scale a floating-point value to integer by multiplying by SCALE.

        Args:
            value: Original floating-point value

        Returns:
            Scaled integer value (rounded to nearest int)
        """
        return round(value * self.SCALE)

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

    def process_bus_line(self, line_data: Dict[str, Any], distances_dict: Dict = None) -> List[Dict[str, List]]:
        """
        Process a single bus line from JSON and calculate T using JITS2022 algorithm.

        Replicates JITS2022 InstanceMTD.readBuses() and T calculation logic.

        Args:
            line_data: Dictionary containing line information
            distances_dict: Optional dict of (from_id, to_id) -> distance_meters

        Returns:
            List of processed bus dictionaries with properly calculated T values
        """
        buses = line_data.get('buses', [])
        processed_buses = []
        distances_dict = distances_dict or self.distances_dict

        for bus_idx, bus in enumerate(buses):
            path = bus.get('path', [])

            if not path:
                logger.warning(f"Bus {bus_idx} has empty path. Skipping.")
                continue

            # Extract station IDs, times, and rest flags
            station_ids = [stop['station_id'] for stop in path]
            times = [self.parse_time_to_minutes(stop['time']) for stop in path]
            rest_flags = [stop.get('rest', False) for stop in path]

            # Calculate T using JITS2022 algorithm
            T_values = [0]  # First segment has no travel time

            for i in range(1, len(path)):
                prev_station_id = station_ids[i - 1]
                curr_station_id = station_ids[i]

                # Get actual distance from distances_dict if available
                distance_m = 0
                if distances_dict:
                    distance_m = distances_dict.get((prev_station_id, curr_station_id), 0)

                # Calculate time delta between stops (in minutes)
                time_delta_minutes = times[i] - times[i - 1]

                # If no time delta (shouldn't happen in valid data), use default
                if time_delta_minutes <= 0:
                    time_delta_minutes = 1
                    logger.warning(f"Bus {bus_idx}: Zero or negative time delta at stop {i}. Using default.")

                # Calculate required speed (km/h)
                time_delta_hours = time_delta_minutes / 60.0
                if distance_m > 0:
                    # Distance in km, time in hours -> speed in km/h
                    required_speed_kmh = (distance_m / 1000.0) / time_delta_hours
                else:
                    # Fallback: estimate speed from time
                    required_speed_kmh = self.MAX_SPEED_KMH

                # Constrain speed to model limits
                actual_speed_kmh = max(self.MIN_SPEED_KMH, min(required_speed_kmh, self.MAX_SPEED_KMH))

                # Convert speed to m/s
                actual_speed_m_per_sec = (actual_speed_kmh * 1000) / 3600

                # Calculate T: time = distance / speed (in seconds)
                if distance_m > 0 and actual_speed_m_per_sec > 0:
                    travel_time_seconds = distance_m / actual_speed_m_per_sec
                else:
                    # Fallback: use time delta
                    travel_time_seconds = time_delta_minutes * 60

                travel_time_minutes = travel_time_seconds / 60.0

                # Add rest time if previous stop has rest flag
                if rest_flags[i - 1]:
                    travel_time_minutes += self.config.rest_time

                T_values.append(travel_time_minutes)

            processed_buses.append({
                'station_ids': station_ids,
                'times': times,
                'time_deltas': T_values,
                'rest_flags': rest_flags,
            })

        return processed_buses

    @classmethod
    def convert_json_to_dzn(cls, json_file: Path, output_file: Path,
                           variant_name: str = "", config=None, distances_dict=None) -> Tuple[bool, str]:
        """
        Convert a JSON bus schedule file to integer DZN format.

        Args:
            json_file: Path to input JSON file
            output_file: Path to output DZN file
            variant_name: Name of the variant (e.g., "20_0")
            config: ExperimentConfig instance (or None for defaults)
            distances_dict: Optional dict of (from_id, to_id) -> distance_meters

        Returns:
            (success: bool, message: str)
        """
        # Create converter instance with config and data
        converter = cls(config=config, distances_dict=distances_dict or {})

        logger.info(f"Converting {json_file.name} to integer DZN format...")
        logger.info(f"  Using model speed: {converter.MIN_SPEED_KMH} km/h, rest time: {converter.config.rest_time} min")

        try:
            # Read JSON file
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Process all lines and collect buses
            all_buses = []
            for line_data in data:
                buses = converter.process_bus_line(line_data)
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

                # For D: use time-based energy approximation for now
                # (real distance matrix would require stations_input.csv + distances_input.csv)
                energy = [0]  # First segment (at first station)
                for i in range(1, len(bus['time_deltas'])):
                    # Energy ≈ time * 0.20 (default approximation)
                    # This will be more accurate once distances_dict is populated
                    time_delta_minutes = bus['time_deltas'][i]
                    energy_val = time_delta_minutes * 0.20
                    energy.append(energy_val)

                energy_scaled = [converter.scale_to_integer(e) for e in energy]
                energy_scaled += [0] * (max_stops - len(energy_scaled))
                D.extend(energy_scaled)

                # Scale and pad travel times (now correctly calculated with speed/distance)
                times = [converter.scale_to_integer(t) for t in bus['time_deltas']]
                times += [0] * (max_stops - len(times))
                T.extend(times)

                # Scale and pad schedule times
                schedule = [converter.scale_to_integer(t) for t in bus['times']]
                schedule += [converter.scale_to_integer(bus['times'][-1])] * (max_stops - len(schedule))
                tau_bi.extend(schedule)

            # Generate DZN file
            base_name = json_file.stem.replace('buses_input', '')
            base_name = base_name.strip('_') if base_name else 'default'

            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("% " + "=" * 76 + "\n")
                f.write(f"% CLP Test Case: {base_name} (variant: {variant_name})\n")
                f.write("% " + "=" * 76 + "\n")
                f.write("% Source: JITS2022 Test Battery (Converted)\n")
                f.write(f"% Original file: {json_file.name}\n")
                f.write("% Converted to INTEGER CLP format with SCALE=" + str(converter.SCALE) + "\n")
                f.write("%\n")
                f.write("% CONVERSION DETAILS:\n")
                f.write("% - All floating-point values multiplied by SCALE and rounded to integers\n")
                f.write("% - Travel times (T) calculated using JITS2022 algorithm:\n")
                f.write("%   T = distance / speed (constrained by model speed limits)\n")
                f.write("%   Rest times added when previous stop has rest flag\n")
                f.write("% - Example: 42.5 minutes -> " + str(converter.scale_to_integer(42.5)) + " (integer)\n")
                f.write("%           1.3 kWh -> " + str(converter.scale_to_integer(1.3)) + " (integer)\n")
                f.write("%\n")
                f.write("% IMPORTANT: To interpret results, divide integer values by SCALE:\n")
                f.write(f"%   - Time: integer_value / {converter.SCALE} = minutes\n")
                f.write(f"%   - Energy: integer_value / {converter.SCALE} = kWh\n")
                f.write("% " + "=" * 76 + "\n\n")

                # Problem dimensions
                f.write("% --- Problem Dimensions ---\n")
                f.write(f"num_buses = {num_buses};\n")
                f.write(f"num_stations = {num_stations};\n\n")

                # Energy parameters (from config)
                f.write("% --- Energy Parameters (CLP Model) ---\n")
                f.write(f"% Values are INTEGERS scaled by {converter.SCALE} from original values\n")
                f.write(f"Cmax = {converter.CMAX};  % Maximum battery capacity (original: {converter.config.cmax} kWh)\n")
                f.write(f"Cmin = {converter.CMIN};   % Minimum reserve (original: {converter.config.cmin} kWh)\n")
                f.write(f"alpha = {converter.ALPHA};  % Fast charging rate (original: {converter.config.alpha} kWh/min)\n\n")

                # Time and schedule parameters
                f.write("% --- Time and Schedule Parameters ---\n")
                f.write(f"% Values are INTEGERS scaled by {converter.SCALE} from original values\n")
                f.write(f"mu = {converter.MU};      % Maximum delay (original: {converter.config.mu} min)\n")
                f.write(f"SM = {converter.SM};      % Safety margin (original: {converter.config.sm} min)\n")
                f.write(f"psi = {converter.PSI};     % Minimum charging time (original: {converter.config.psi} min)\n")
                f.write(f"beta = {converter.BETA};   % Maximum charging time (original: {converter.config.beta} min)\n")
                f.write(f"M = {converter.M};   % Big-M constant (original: 10000.0)\n\n")

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
                f.write("% Energy consumed between stops (INTEGER values, divide by SCALE for kWh)\n")
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
                f.write("% Time between stops (INTEGER values, divide by SCALE for minutes)\n")
                f.write("% Calculated using JITS2022 algorithm with speed constraints\n")
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
                f.write("% Scheduled arrival times (INTEGER values, divide by SCALE for minutes since 00:00)\n")
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
    def batch_convert_files(cls, json_files: List[Path], output_dir: Path, source_dir_name: str = "",
                           config=None, distances_dict=None) -> Tuple[int, int, List[str]]:
        """
        Convert multiple JSON files to DZN format.

        Args:
            json_files: List of JSON file paths
            output_dir: Output base directory for DZN files
            source_dir_name: Name of the source directory (e.g., 'cork-1-line')
            config: ExperimentConfig instance (or None for defaults)
            distances_dict: Optional dict of (from_id, to_id) -> distance_meters

        Returns:
            (success_count: int, failure_count: int, messages: List[str])
        """
        success_count = 0
        failure_count = 0
        messages = []

        # Create subdirectory with source directory name
        if source_dir_name:
            target_dir = output_dir / source_dir_name
        else:
            target_dir = output_dir

        target_dir.mkdir(parents=True, exist_ok=True)

        for json_file in json_files:
            # Extract variant name
            parts = json_file.stem.split('_')
            variant = '_'.join(parts[2:]) if len(parts) > 2 else ""

            # Generate output filename with source directory prefix
            base_name = json_file.stem.replace('buses_input', '')
            base_name = base_name.strip('_') if base_name else 'default'

            if source_dir_name:
                filename = f"{source_dir_name}_{output_dir.name}{base_name}.dzn"
            else:
                filename = f"{output_dir.name}{base_name}.dzn"

            output_file = target_dir / filename

            success, message = cls.convert_json_to_dzn(json_file, output_file, variant, config, distances_dict)
            if success:
                success_count += 1
                messages.append(f"✓ {json_file.name}: {message}")
            else:
                failure_count += 1
                messages.append(f"✗ {json_file.name}: {message}")

        return success_count, failure_count, messages
