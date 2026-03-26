"""
================================================================================
Instance Generator Module - CLP Instance Generation
================================================================================
Expert algorithm for generating feasible CLP instances based on constraint
analysis of the CLP model.

Key Principles:
1. Force needed charging: consumption > usable capacity
2. Strategic placement: 1-2 forced charge points per route
3. Temporal feasibility: ensure deviation constraints are satisfiable
4. Diversity: minimize station conflicts between buses
================================================================================
"""

import random
from typing import Dict, List, Tuple
from config import Config


class ConstraintAnalyzer:
    """Analyzes CLP constraints to guide instance generation"""

    def __init__(self, num_buses: int, num_stations: int):
        self.num_buses = num_buses
        self.num_stations = num_stations
        self.config = Config()

    def estimate_optimal_stops(self) -> int:
        """
        Estimate optimal number of stops to force exactly 1-2 charges.

        Logic:
        - Usable capacity: 80 kWh
        - Target overconsumption: 1.2-1.5x to force charging
        - Average consumption: ~18 kWh/stop
        - Result: need ~6-8 stops to trigger charging

        CRITICAL: Limit by number of stations to avoid excessive padding/repetition.
        With N stations, can realistically have max N unique stops (including depot).
        """
        target = self.config.USABLE_CAPACITY * 1.3
        avg = self.config.OPTIMAL_CONSUMPTION_PER_STOP
        base_stops = int(target / avg)

        # Maximum stops limited by number of stations
        # With N stations: max = N (unique stations) + padding allowed by config
        # For small station counts, reduce aggressively
        max_by_stations = min(
            max(self.num_stations - 1, 3),  # At least 3, but not more than stations-1
            self.config.MAX_STOPS_PER_BUS
        )

        # Bound by configuration AND station count
        optimal = max(
            self.config.MIN_STOPS_PER_BUS,
            min(base_stops + 1, max_by_stations)
        )

        return optimal


class RouteGenerator:
    """Generates bus routes with diversity constraints"""

    def __init__(self, num_buses: int, num_stations: int, max_stops: int):
        self.num_buses = num_buses
        self.num_stations = num_stations
        self.max_stops = max_stops
        self.config = Config()
        self.station_usage = {s: [] for s in range(1, num_stations + 1)}

    def generate_station_sequence(self, bus_id: int, num_stops: int) -> List[int]:
        """
        Generate station sequence for a bus, PADDED to max_stops.

        Strategy:
        - Start at depot (station 1)
        - Visit diverse stations
        - Minimize station reuse conflicts
        - Create varied patterns
        - Pad to max_stops
        """
        sequence = [1]  # Depot

        pattern = random.choice(['sequential', 'reverse', 'zigzag', 'random'])
        available = list(range(2, self.num_stations + 1))

        if pattern == 'sequential':
            for i in range(1, num_stops):
                idx = ((i - 1) % (self.num_stations - 1)) + 2
                sequence.append(idx)

        elif pattern == 'reverse':
            for i in range(1, num_stops):
                idx = self.num_stations - ((i - 1) % (self.num_stations - 1))
                sequence.append(idx)

        elif pattern == 'zigzag':
            odds = [s for s in available if s % 2 == 1]
            evens = [s for s in available if s % 2 == 0]
            combined = odds + evens

            for i in range(1, num_stops):
                idx = (i - 1) % len(combined)
                sequence.append(combined[idx])

        else:  # random with preference for less-used
            for i in range(1, num_stops):
                weights = [1.0 / (len(self.station_usage[s]) + 1)
                           for s in available]
                total = sum(weights)
                probs = [w / total for w in weights]
                chosen = random.choices(available, weights=probs)[0]
                sequence.append(chosen)

        # Register usage
        for station in sequence:
            self.station_usage[station].append((bus_id, len(sequence)))

        # Pad to max_stops with last station
        sequence += [sequence[-1]] * (self.max_stops - num_stops)

        return sequence


class ConsumptionGenerator:
    """Generates energy consumption patterns ensuring feasibility"""

    def __init__(self, max_stops: int):
        self.config = Config()
        self.max_stops = max_stops

    def generate_consumption(self, num_stops: int, bus_id: int) -> List[int]:
        """
        Generate energy consumption ensuring:
        - Total exceeds usable capacity
        - Varied pattern
        - Realistic bounds
        - Padded to max_stops
        """
        consumption = [0]  # Depot: no consumption

        # Randomly set overconsumption factor
        factor = random.uniform(
            self.config.TARGET_CONSUMPTION_FACTOR_MIN,
            self.config.TARGET_CONSUMPTION_FACTOR_MAX
        )
        target_total = int(self.config.USABLE_CAPACITY * factor)

        accumulated = 0
        for i in range(1, num_stops):
            if i == num_stops - 1:
                # Last stop: close to target
                remaining = target_total - accumulated
                value = max(
                    self.config.MIN_CONSUMPTION_PER_STOP,
                    min(remaining, self.config.MAX_CONSUMPTION_PER_STOP)
                )
            else:
                # Random with bias toward optimal
                mean = self.config.OPTIMAL_CONSUMPTION_PER_STOP
                std = 50
                value = int(random.gauss(mean, std))
                value = max(
                    self.config.MIN_CONSUMPTION_PER_STOP,
                    min(value, self.config.MAX_CONSUMPTION_PER_STOP)
                )

            consumption.append(value)
            accumulated += value

        # Pad to max_stops with zeros
        consumption += [0] * (self.max_stops - num_stops)

        return consumption


class TimingGenerator:
    """Generates travel times and timetables respecting CLP constraints"""

    def __init__(self, max_stops: int):
        self.config = Config()
        self.max_stops = max_stops

    def generate_travel_times(self, num_stops: int) -> List[int]:
        """Generate travel times with realistic distribution, padded to max_stops"""
        times = [0]  # Depot: no travel

        for i in range(1, num_stops):
            mean = self.config.OPTIMAL_TRAVEL_TIME
            std = 40
            value = int(random.gauss(mean, std))
            value = max(
                self.config.MIN_TRAVEL_TIME,
                min(value, self.config.MAX_TRAVEL_TIME)
            )
            times.append(value)

        # Pad to max_stops with zeros
        times += [0] * (self.max_stops - num_stops)

        return times

    def generate_timetable(self, bus_id: int, travel_times: List[int]) -> List[int]:
        """
        Generate arrival timetable respecting CLP timing constraints.

        CRITICAL: Ensures that tau_bi allows time for both travel AND charging:
        tau_bi[i] >= tau_bi[i-1] + T[i] + PSI * (charge chance)

        Also ensures mu constraint is satisfiable by creating schedule with margin.
        """
        num_stops = len(travel_times)
        # Stagger buses to reduce charging conflicts: bus 0 at 7:00, bus 1 at 7:05, etc.
        start_time = 4200 + (bus_id * 50)

        timetable = [start_time]
        accumulated = start_time

        for i in range(1, num_stops):
            # CONSTRAINT-RESPECTING TIMING:
            # Previous stop + travel time + buffer for charging (if needed)
            # Buffer = PSI (minimum charge time) to allow option to charge
            travel_time = travel_times[i]

            # Minimum time needed: only travel
            min_next_time = accumulated + travel_time

            # Add buffer for potential charging to remain feasible
            # Use half the mu value to leave deviation margin
            charge_buffer = int(self.config.PSI * 1.5)  # 1.5× minimum charge time
            desired_next_time = min_next_time + charge_buffer

            # Add small variance (±10 units = ±1 min) to create realistic schedules
            variance = random.randint(-10, 10)
            next_time = desired_next_time + variance

            accumulated = next_time
            timetable.append(accumulated)

        # Ensure length = max_stops
        if len(timetable) < self.max_stops:
            # Pad with last value
            timetable += [accumulated] * (self.max_stops - len(timetable))

        return timetable


class FeasibleInstanceGenerator:
    """
    Expert generator producing highly feasible CLP instances.

    Combines constraint analysis, route diversity, and temporal feasibility
    to maximize SAT probability.
    """

    def __init__(self, num_buses: int, num_stations: int):
        self.num_buses = num_buses
        self.num_stations = num_stations
        self.config = Config()

        self.analyzer = ConstraintAnalyzer(num_buses, num_stations)

        # Calculate optimal stops FIRST
        self.max_stops = self.analyzer.estimate_optimal_stops()

        # THEN pass max_stops to all generators
        self.route_gen = RouteGenerator(num_buses, num_stations, self.max_stops)
        self.consumption_gen = ConsumptionGenerator(self.max_stops)
        self.timing_gen = TimingGenerator(self.max_stops)

        self.num_stops = self._generate_num_stops()

    def _generate_num_stops(self) -> List[int]:
        """Generate varied stops per bus around optimal"""
        base = self.max_stops
        stops = []

        for b in range(self.num_buses):
            # ±1 variation
            variation = random.choice([-1, 0, 0, 1])
            value = max(
                self.config.MIN_STOPS_PER_BUS,
                min(base + variation, self.max_stops)
            )
            stops.append(value)

        return stops

    def generate_instance(self) -> Dict:
        """Generate complete feasible instance"""

        st_bi = []
        D = []
        T = []
        tau_bi = []

        for b in range(self.num_buses):
            nb = self.num_stops[b]

            # Generate components
            stations = self.route_gen.generate_station_sequence(b, nb)
            energy = self.consumption_gen.generate_consumption(nb, b)
            times = self.timing_gen.generate_travel_times(nb)
            timetable = self.timing_gen.generate_timetable(b, times)

            st_bi.append(stations)
            D.append(energy)
            T.append(times)
            tau_bi.append(timetable)

        return {
            'num_buses': self.num_buses,
            'num_stations': self.num_stations,
            'max_stops': self.max_stops,
            'num_stops': self.num_stops,
            'st_bi': st_bi,
            'D': D,
            'T': T,
            'tau_bi': tau_bi,
            'Cmax': self.config.CMAX,
            'Cmin': self.config.CMIN,
            'alpha': self.config.ALPHA,
            'mu': self.config.MU,
            'SM': self.config.SM,
            'psi': self.config.PSI,
            'beta': self.config.BETA,
            'M': self.config.M
        }
