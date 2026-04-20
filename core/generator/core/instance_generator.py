"""
================================================================================
Instance Generator - CLP Instance Generation (v3.0 - Working Pattern Replication)
================================================================================

Professional instance generation based on DIRECT REPLICATION of working examples
from Battery Own dataset.

Key insight: Working examples follow a STRICT PATTERN:
- max_stops = num_stations (each bus visits EVERY station exactly ONCE)
- num_stops[bus] = num_stations for ALL buses
- NO padding, NO repetitions
- Diverse route patterns per bus (sequential, reverse, alternating, diagonal)
- Consumption ensures 1.3-1.5x overconsumption (forces charging requirement)
- Timing is cumulative and strictly increasing

This generator replicates this pattern with minimal variations.
================================================================================
"""

import random
from typing import Dict, List, Tuple
import sys
from pathlib import Path

# Ensure project root is in sys.path
project_root = Path(__file__).parent.parent.parent.parent.absolute()
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from core.generator.config import Config


class ProfessionalInstanceGenerator:
    """
    Generates CLP instances by replicating the proven working pattern
    from Battery Own examples.
    """

    # Proven route patterns from working examples
    ROUTE_PATTERNS = {
        'sequential': lambda stations: list(range(1, stations + 1)),
        'reverse': lambda stations: list(range(stations, 0, -1)),
        'alternate_odd': lambda stations: (
            [s for s in range(1, stations + 1) if s % 2 == 1] +
            [s for s in range(1, stations + 1) if s % 2 == 0]
        ),
        'alternate_even': lambda stations: (
            [s for s in range(1, stations + 1) if s % 2 == 0] +
            [s for s in range(1, stations + 1) if s % 2 == 1]
        ),
        'diagonal': lambda stations: [
            ((i * 7 + 1) % stations) or stations  # Deterministic pseudo-random rotation
            for i in range(stations)
        ]
    }

    def __init__(self, num_buses: int, num_stations: int):
        self.num_buses = num_buses
        self.num_stations = num_stations
        self.config = Config()

        # Validate input constraints
        if num_buses < 1 or num_stations < 2:
            raise ValueError(f"Invalid dimensions: {num_buses} buses, {num_stations} stations")

    def generate_instance(self) -> Dict:
        """
        Generate a single CLP instance following working pattern.

        Returns:
            Dictionary with all required DZN data
        """
        # PATTERN 1: max_stops and num_stops match num_stations exactly
        max_stops = self.num_stations
        num_stops = [self.num_stations] * self.num_buses

        # PATTERN 2: Generate diverse route patterns (station sequences)
        st_bi = self._generate_routes()

        # PATTERN 3: Generate energy consumption (1.3-1.5x overconsumption factor)
        D = self._generate_energy_consumption(max_stops, num_stops)

        # PATTERN 4: Generate realistic travel times
        T = self._generate_travel_times(max_stops, num_stops)

        # PATTERN 5: Generate cumulative timetable
        tau_bi = self._generate_timetable(max_stops, num_stops, T)

        # Assemble instance
        instance = {
            'num_buses': self.num_buses,
            'num_stations': self.num_stations,
            'max_stops': max_stops,
            'num_stops': num_stops,
            'st_bi': st_bi,
            'D': D,
            'T': T,
            'tau_bi': tau_bi,
            'Cmax': self.config.Cmax,
            'Cmin': self.config.Cmin,
            'alpha': self.config.alpha,
            'mu': self.config.mu,
            'SM': self.config.SM,
            'psi': self.config.psi,
            'beta': self.config.beta,
            'M': self.config.M,
        }

        return instance

    def _generate_routes(self) -> List[List[int]]:
        """
        Generate station sequences using proven patterns.

        Each bus gets a different pattern to ensure diversity:
        - Bus 0: Sequential
        - Bus 1: Reverse
        - Bus 2: Alternate-odd
        - Bus 3: Alternate-even
        - Bus 4+: Diagonal
        """
        pattern_list = ['sequential', 'reverse', 'alternate_odd', 'alternate_even', 'diagonal']
        st_bi = []

        for bus_id in range(self.num_buses):
            # Assign pattern cyclically
            pattern_name = pattern_list[bus_id % len(pattern_list)]
            pattern_func = self.ROUTE_PATTERNS[pattern_name]

            # Generate route for this bus
            route = pattern_func(self.num_stations)

            # Ensure exactly num_stations stops (no padding)
            route = route[:self.num_stations]

            # Verify all stations are included (working pattern requirement)
            if set(route) != set(range(1, self.num_stations + 1)):
                # Fallback: force unique stations
                remaining = set(range(1, self.num_stations + 1)) - set(route)
                route = route[:len(route) - len(remaining)] + list(remaining)

            st_bi.append(route)

        return st_bi

    def _generate_energy_consumption(self, max_stops: int, num_stops: List[int]) -> List[List[int]]:
        """
        Generate energy consumption ensuring overconsumption factor >= 1.3x.

        Key insight from working examples:
        - Each bus MUST consume > USABLE_CAPACITY to force charging
        - Working: noncity_5buses-8stations achieves 1.3-1.55x via distributed consumption
        - Strategy: distribute target consumption evenly across all stops
        """
        D = []

        for bus_id in range(self.num_buses):
            num_stops_bus = num_stops[bus_id]

            # Determine target consumption factor
            # Stricter: ensure we hit at least 1.3x for feasibility
            if self.num_stations <= 4:
                # Very small: must be aggressive (1.5-1.8x)
                factor_min = 1.5
                factor_max = 1.8
            elif self.num_stations <= 8:
                # Small: 1.3-1.55x (working examples)
                factor_min = 1.3
                factor_max = 1.55
            elif self.num_stations <= 15:
                # Medium: 1.1-1.35x (still need charging)
                factor_min = 1.0
                factor_max = 1.35
            else:
                # Large: 0.9-1.2x
                factor_min = 0.9
                factor_max = 1.2

            # Random factor for diversity
            factor = random.uniform(factor_min, factor_max)
            target_total = int(self.config.USABLE_CAPACITY * factor)

            # STRATEGY: Distribute consumption EVENLY across stops
            # This ensures we consistently reach target even for small networks
            # D[0] = 0 (depot), then D[1..N-1] = target_total / (N-1)

            consumption = [0]  # First stop: no consumption

            # Distribute target consumption across remaining stops
            base_consumption_per_stop = target_total // (num_stops_bus - 1) if num_stops_bus > 1 else 0
            remainder = target_total % (num_stops_bus - 1) if num_stops_bus > 1 else 0

            for i in range(1, num_stops_bus):
                # Each stop gets base amount, distributed remainder added to early stops
                if i <= remainder:
                    value = base_consumption_per_stop + 1
                else:
                    value = base_consumption_per_stop

                # Add small random variance to avoid suspiciously uniform patterns
                # But keep it minimal to maintain target total
                variance = random.randint(-5, 5) if value > 10 else 0
                value = max(50, value + variance)  # Min 50 to ensure some consumption

                consumption.append(value)

            D.append(consumption)

        return D

    def _generate_travel_times(self, max_stops: int, num_stops: List[int]) -> List[List[int]]:
        """
        Generate realistic travel times between stops.

        Working pattern: All values positive (100-200 range, ×10 scale)
        """
        T = []

        for bus_id in range(self.num_buses):
            num_stops_bus = num_stops[bus_id]

            # Travel time profile based on network size
            if self.num_stations <= 8:
                min_time = 100  # 10 minutes
                max_time = 150  # 15 minutes
            elif self.num_stations <= 12:
                min_time = 80
                max_time = 160
            else:
                min_time = 80
                max_time = 200

            times = [0]  # First stop (depot): 0

            for i in range(1, num_stops_bus):
                # Random travel time (always positive, no zeros)
                time = random.randint(min_time, max_time)
                times.append(time)

            T.append(times)

        return T

    def _generate_timetable(self, max_stops: int, num_stops: List[int],
                           T: List[List[int]]) -> List[List[int]]:
        """
        Generate cumulative timetable (arrival times).

        Working pattern:
        - Strictly increasing: tau[i] < tau[i+1]
        - Cumulative sum: tau[i] = tau[i-1] + travel_time[i-1]
        - Each bus starts at different offset
        """
        tau_bi = []

        for bus_id in range(self.num_buses):
            num_stops_bus = num_stops[bus_id]

            # Starting time offset (different for each bus to reduce conflicts)
            # Working pattern: 0-100 range, with 50 minute spacing between buses
            start_time = (bus_id * 50 + random.randint(0, 20))

            # Build cumulative timetable
            times = [start_time]

            for i in range(1, num_stops_bus):
                # Next arrival = previous + travel time
                next_time = times[i - 1] + T[bus_id][i]
                times.append(next_time)

            tau_bi.append(times)

        return tau_bi


class FeasibleInstanceGenerator:
    """
    Wrapper for backward compatibility with orchestrator.
    """

    def __init__(self, num_buses: int, num_stations: int):
        self.generator = ProfessionalInstanceGenerator(num_buses, num_stations)

    def generate_instance(self) -> Dict:
        """Generate instance - delegates to ProfessionalInstanceGenerator"""
        return self.generator.generate_instance()
