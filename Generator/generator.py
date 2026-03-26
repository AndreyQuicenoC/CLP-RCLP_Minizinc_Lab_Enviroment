"""
=============================================================================
AVISPA CLP Test Instance Generator
=============================================================================
Professional test instance generator for the CLP (Charging Location Problem)
mathematical model. Generates feasible test cases based on analyzed patterns
from validated noncity instances.

Author: AVISPA Research Team
Version: 1.0.0
Date: March 2026
License: MIT
=============================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import os
import sys
import subprocess
import json
from datetime import datetime
from pathlib import Path

# =============================================================================
# CONFIGURATION AND CONSTANTS
# =============================================================================

class Config:
    """Configuration constants based on validated noncity instances"""

    # Battery parameters (scaled ×10)
    CMAX = 1000  # 100 kWh max capacity
    CMIN = 200   # 20 kWh min reserve
    USABLE_CAPACITY = CMAX - CMIN  # 80 kWh usable

    ALPHA = 100  # 10 kWh/min charging rate

    # Time parameters (scaled ×10)
    MU = 50      # 5 min max delay
    SM = 10      # 1 min safety margin
    PSI = 10     # 1 min minimum charging time
    BETA = 100   # 10 min maximum charging time
    M = 10000    # Big-M constant

    # Generation parameters (based on noncity analysis)
    MIN_CONSUMPTION_PER_STOP = 100   # 10 kWh (scaled ×10)
    MAX_CONSUMPTION_PER_STOP = 250   # 25 kWh (scaled ×10)
    OPTIMAL_CONSUMPTION_PER_STOP = 180  # 18 kWh (scaled ×10)

    MIN_TRAVEL_TIME = 80     # 8 min (scaled ×10)
    MAX_TRAVEL_TIME = 200    # 20 min (scaled ×10)
    OPTIMAL_TRAVEL_TIME = 120  # 12 min (scaled ×10)

    # Feasibility constraints
    MAX_STOPS_PER_BUS = 12   # Keep routes manageable
    MIN_STOPS_PER_BUS = 4    #Minimum meaningful route

    # Colors
    COLOR_DARK_BLUE = "#1e3a5f"
    COLOR_LIGHT_BLUE = "#4a90e2"
    COLOR_WHITE = "#ffffff"
    COLOR_LIGHT_GRAY = "#f5f5f5"
    COLOR_GRAY = "#cccccc"
    COLOR_SUCCESS = "#28a745"
    COLOR_ERROR = "#dc3545"

# =============================================================================
# CORE ALGORITHM: FEASIBLE INSTANCE GENERATOR
# =============================================================================

class FeasibleInstanceGenerator:
    """
    Expert algorithm to generate feasible CLP instances based on analysis
    of validated noncity test cases.

    Key Principles (extracted from noncity analysis):
    1. Total consumption must exceed usable capacity but remain solvable
    2. Consumption pattern: force 1-2 strategic charges
    3. Route diversity: minimize station conflicts between buses
    4. Temporal feasibility: ensure mu constraint is satisfiable
    5. Depot at station 1: D[b,1]=0, T[b,1]=0
    """

    def __init__(self, num_buses, num_stations):
        self.num_buses = num_buses
        self.num_stations = num_stations
        self.config = Config()

        # Calculate optimal stops based on feasibility analysis
        self.max_stops = self._calculate_optimal_max_stops()
        self.num_stops = self._generate_num_stops()

        # Pre-allocate station usage for diversity
        self.station_usage = {s: [] for s in range(1, num_stations + 1)}

    def _calculate_optimal_max_stops(self):
        """
        Calculate optimal maximum stops based on energy constraints.

        Logic:
        - Usable capacity: 80 kWh
        - Target: 1.3x overconsumption to force charging
        - Average consumption: 18 kWh/stop
        - Add buffer for randomness: aim for 7-8 stops to ensure feasibility
        """
        target_consumption = self.config.USABLE_CAPACITY * 1.3  # 30% overconsumption
        avg_consumption = self.config.OPTIMAL_CONSUMPTION_PER_STOP
        base_stops = int(target_consumption / avg_consumption)

        # Add buffer (2 stops) to account for randomness
        optimal_stops = base_stops + 2

        # Bound by configuration limits
        return max(
            self.config.MIN_STOPS_PER_BUS,
            min(optimal_stops, self.config.MAX_STOPS_PER_BUS)
        )

    def _generate_num_stops(self):
        """Generate number of stops per bus with slight variation"""
        base_stops = self.max_stops
        num_stops = []

        for b in range(self.num_buses):
            # Allow ±1 stop variation for diversity
            variation = random.choice([-1, 0, 0, 1])  # Bias towards base
            stops = max(
                self.config.MIN_STOPS_PER_BUS,
                min(base_stops + variation, self.max_stops)
            )
            num_stops.append(stops)

        return num_stops

    def _generate_station_sequence(self, bus_id):
        """
        Generate station sequence for a bus ensuring diversity.

        Strategy:
        - Start at depot (station 1)
        - Visit different stations preferring less-used ones
        - Avoid immediate repetition
        - Create route patterns (sequential, reverse, zigzag)
        """
        num_stops_bus = self.num_stops[bus_id]
        sequence = [1]  # Start at depot

        available_stations = list(range(2, self.num_stations + 1))

        # Choose pattern type
        pattern = random.choice(['sequential', 'reverse', 'zigzag', 'random'])

        if pattern == 'sequential':
            # Sequential pattern: 1, 2, 3, 4, ...
            for i in range(1, num_stops_bus):
                next_station = ((i - 1) % (self.num_stations - 1)) + 2
                sequence.append(next_station)

        elif pattern == 'reverse':
            # Reverse pattern: 1, N, N-1, N-2, ...
            for i in range(1, num_stops_bus):
                next_station = self.num_stations - ((i - 1) % (self.num_stations - 1))
                sequence.append(next_station)

        elif pattern == 'zigzag':
            # Zigzag pattern: 1, 3, 5, 7, 2, 4, 6, 8
            odd_stations = [s for s in available_stations if s % 2 == 1]
            even_stations = [s for s in available_stations if s % 2 == 0]
            combined = odd_stations + even_stations

            for i in range(1, num_stops_bus):
                idx = (i - 1) % len(combined)
                sequence.append(combined[idx])

        else:  # random
            # Random with preference for less-used stations
            for i in range(1, num_stops_bus):
                # Weighted selection favoring less-used stations
                weights = [1.0 / (len(self.station_usage[s]) + 1) for s in available_stations]
                total = sum(weights)
                probabilities = [w / total for w in weights]

                chosen = random.choices(available_stations, weights=probabilities)[0]
                sequence.append(chosen)

        # Register usage
        for station in sequence:
            self.station_usage[station].append((bus_id, len(sequence) - 1))

        # Pad to max_stops
        sequence += [sequence[-1]] * (self.max_stops - num_stops_bus)

        return sequence

    def _generate_consumption_pattern(self, bus_id):
        """
        Generate energy consumption pattern ensuring feasibility.

        Target:
        - Total consumption 1.1-1.4x usable capacity
        - Force 1-2 strategic charges
        - Vary consumption to create challenge
        """
        num_stops_bus = self.num_stops[bus_id]

        # Calculate target total consumption
        target_factor = random.uniform(1.1, 1.4)
        target_total = int(self.config.USABLE_CAPACITY * target_factor)

        # Generate consumption per stop
        consumption = [0]  # Depot: no consumption

        # Distribute consumption across stops
        # Reserve at least MIN consumption for last stop
        min_reserved = self.config.MIN_CONSUMPTION_PER_STOP
        available_for_distribution = target_total - min_reserved

        accumulated = 0
        for i in range(1, num_stops_bus):
            if i == num_stops_bus - 1:
                # Last stop: ensure we reach target
                remaining = target_total - accumulated
                value = max(
                    self.config.MIN_CONSUMPTION_PER_STOP,
                    min(remaining, self.config.MAX_CONSUMPTION_PER_STOP)
                )
            else:
                # Random consumption with bias towards optimal
                mean = self.config.OPTIMAL_CONSUMPTION_PER_STOP
                std_dev = 40
                value = int(random.gauss(mean, std_dev))
                value = max(
                    self.config.MIN_CONSUMPTION_PER_STOP,
                    min(value, self.config.MAX_CONSUMPTION_PER_STOP)
                )

            consumption.append(value)
            accumulated += value

        # Pad with zeros
        consumption += [0] * (self.max_stops - num_stops_bus)

        return consumption

    def _generate_travel_times(self, bus_id):
        """Generate travel times ensuring temporal feasibility"""
        num_stops_bus = self.num_stops[bus_id]

        times = [0]  # Depot: no travel time

        for i in range(1, num_stops_bus):
            # Random time with bias towards optimal
            mean = self.config.OPTIMAL_TRAVEL_TIME
            std_dev = 30
            value = int(random.gauss(mean, std_dev))
            value = max(
                self.config.MIN_TRAVEL_TIME,
                min(value, self.config.MAX_TRAVEL_TIME)
            )
            times.append(value)

        # Pad with zeros
        times += [0] * (self.max_stops - num_stops_bus)

        return times

    def _generate_timetable(self, bus_id, travel_times):
        """
        Generate arrival timetable ensuring feasibility.

        Start times are staggered to reduce conflicts.
        Times accumulate based on travel + potential charging buffer.
        """
        # Stagger start times: bus 0 at 7:00, bus 1 at 7:05, etc.
        start_time = 4200 + (bus_id * 50)  # 420.0 min (7:00 AM) + 5 min per bus

        timetable = [start_time]
        accumulated = start_time

        num_stops_bus = self.num_stops[bus_id]

        for i in range(1, num_stops_bus):
            # Add travel time + buffer for potential charging
            accumulated += travel_times[i] + 20  # 2 min buffer
            timetable.append(accumulated)

        # Pad with last value
        timetable += [accumulated] * (self.max_stops - num_stops_bus)

        return timetable

    def generate_instance(self):
        """Generate complete feasible CLP instance"""

        # Generate all matrices
        st_bi = []
        D = []
        T = []
        tau_bi = []

        for b in range(self.num_buses):
            st_bi.append(self._generate_station_sequence(b))
            D.append(self._generate_consumption_pattern(b))
            T.append(self._generate_travel_times(b))
            tau_bi.append(self._generate_timetable(b, T[-1]))

        instance = {
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

        return instance

# =============================================================================
# MiniZinc EXPORTER
# =============================================================================

class MiniZincExporter:
    """Export generated instance to MiniZinc .dzn format"""

    @staticmethod
    def format_array_1d(arr):
        """Format 1D array for MiniZinc"""
        return '[' + ','.join(map(str, arr)) + ']'

    @staticmethod
    def format_array_2d(arr, num_buses, max_stops):
        """Format 2D array for MiniZinc with proper line breaks"""
        lines = []
        for b in range(num_buses):
            row = ','.join(map(str, arr[b]))
            comment = f"  % Bus {b+1}"
            lines.append(f"  {row}{comment if b < num_buses - 1 else comment}")

        return '[\n' + ',\n'.join(lines) + '\n]'

    @staticmethod
    def export_to_dzn(instance, filename):
        """Export instance to .dzn file"""

        num_buses = instance['num_buses']
        num_stations = instance['num_stations']
        max_stops = instance['max_stops']

        # Calculate metadata
        total_consumption = sum(sum(D) for D in instance['D'])
        avg_consumption_per_bus = total_consumption / num_buses if num_buses > 0 else 0

        content = f"""% =============================================================================
% Generated CLP Test Instance
% =============================================================================
% Generator: AVISPA CLP Instance Generator v1.0.0
% Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
%
% Instance Characteristics:
%   - Buses: {num_buses}
%   - Stations: {num_stations}
%   - Max stops per bus: {max_stops}
%   - Total energy consumption: {total_consumption} ({total_consumption/10:.1f} kWh)
%   - Average per bus: {avg_consumption_per_bus:.1f} ({avg_consumption_per_bus/10:.1f} kWh)
%   - Usable capacity: {instance['Cmax'] - instance['Cmin']} ({(instance['Cmax'] - instance['Cmin'])/10:.1f} kWh)
%
% Feasibility Analysis:
%   - Overconsumption factor: {avg_consumption_per_bus / (instance['Cmax'] - instance['Cmin']):.2f}x
%   - Expected charges per bus: {avg_consumption_per_bus / (instance['Cmax'] - instance['Cmin']):.1f}
%   - Pattern: Designed to force strategic charging
%
% All values scaled ×10 for integer arithmetic
% =============================================================================

% --- Problem Dimensions ---
num_buses = {num_buses};
num_stations = {num_stations};

% --- Energy Parameters (CLP Model) ---
% All values scaled ×10 from kWh
Cmax = {instance['Cmax']};  % {instance['Cmax']/10:.1f} kWh maximum capacity
Cmin = {instance['Cmin']};  % {instance['Cmin']/10:.1f} kWh minimum reserve
alpha = {instance['alpha']};  % {instance['alpha']/10:.1f} kWh/min charging rate

% --- Time and Schedule Parameters ---
% All values scaled ×10 from minutes
mu = {instance['mu']};      % {instance['mu']/10:.1f} min maximum delay
SM = {instance['SM']};      % {instance['SM']/10:.1f} min safety margin
psi = {instance['psi']};     % {instance['psi']/10:.1f} min minimum charging time
beta = {instance['beta']};   % {instance['beta']/10:.1f} min maximum charging time
M = {instance['M']};      % Big-M constant

% --- Route Structure ---
max_stops = {max_stops};
num_stops = {MiniZincExporter.format_array_1d(instance['num_stops'])};

% --- Station Sequence (st_bi) ---
% Maps each bus stop to a physical station ID (1-indexed)
% Station 1 is depot (D=0, T=0)
st_bi = array2d(1..{num_buses}, 1..{max_stops}, {MiniZincExporter.format_array_2d(instance['st_bi'], num_buses, max_stops)});

% --- Energy Consumption (D) ---
% Energy consumed between stops (scaled ×10, divide by 10 for kWh)
D = array2d(1..{num_buses}, 1..{max_stops}, {MiniZincExporter.format_array_2d(instance['D'], num_buses, max_stops)});

% --- Travel Time (T) ---
% Time between stops (scaled ×10, divide by 10 for minutes)
T = array2d(1..{num_buses}, 1..{max_stops}, {MiniZincExporter.format_array_2d(instance['T'], num_buses, max_stops)});

% --- Timetable (tau_bi) ---
% Scheduled arrival times (scaled ×10, divide by 10 for minutes since 00:00)
% Starting times staggered to reduce conflicts
tau_bi = array2d(1..{num_buses}, 1..{max_stops}, {MiniZincExporter.format_array_2d(instance['tau_bi'], num_buses, max_stops)});
"""

        with open(filename, 'w') as f:
            f.write(content)

        return filename

# =============================================================================
# VALIDATOR: Test instance with MiniZinc
# =============================================================================

class InstanceValidator:
    """Validate generated instances using MiniZinc"""

    def __init__(self, model_path, timeout=60):
        self.model_path = model_path
        self.timeout = timeout

    def validate_instance(self, dzn_path):
        """
        Validate instance by running MiniZinc.

        Returns:
            tuple: (is_satisfiable, solution_dict, error_message)
        """
        try:
            cmd = [
                'minizinc',
                '--solver', 'chuffed',
                '--time-limit', str(self.timeout * 1000),  # milliseconds
                self.model_path,
                dzn_path
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout + 5
            )

            output = result.stdout

            # Check for UNSATISFIABLE
            if 'UNSATISFIABLE' in output:
                return False, None, "Instance is UNSATISFIABLE"

            # Check for solution
            if 'Total estaciones:' in output:
                # Parse solution
                solution = {}
                for line in output.split('\n'):
                    if 'Total estaciones:' in line:
                        solution['total_stations'] = int(line.split(':')[-1].strip())
                    if 'Desviacion total:' in line:
                        solution['total_deviation'] = int(line.split(':')[-1].strip())
                    if 'Estaciones instaladas:' in line:
                        solution['stations_installed'] = line.split(':')[-1].strip()

                return True, solution, None

            # Timeout or other issue
            return False, None, "No solution found within timeout"

        except subprocess.TimeoutExpired:
            return False, None, "Timeout expired"
        except FileNotFoundError:
            return False, None, "MiniZinc not found. Please install MiniZinc."
        except Exception as e:
            return False, None, f"Error: {str(e)}"

# =============================================================================
# GUI APPLICATION
# =============================================================================

class GeneratorGUI:
    """Professional GUI for CLP instance generator"""

    def __init__(self, root):
        self.root = root
        self.root.title("AVISPA CLP Test Instance Generator")
        self.root.geometry("800x700")
        self.root.resizable(False, False)

        # Set color scheme
        self.colors = {
            'bg': Config.COLOR_LIGHT_GRAY,
            'dark_blue': Config.COLOR_DARK_BLUE,
            'light_blue': Config.COLOR_LIGHT_BLUE,
            'white': Config.COLOR_WHITE,
            'gray': Config.COLOR_GRAY,
            'success': Config.COLOR_SUCCESS,
            'error': Config.COLOR_ERROR
        }

        self.root.configure(bg=self.colors['bg'])

        # Find project root
        self.project_root = self._find_project_root()
        self.output_dir = os.path.join(self.project_root, 'Data', 'Battery Generated')
        self.expected_dir = os.path.join(self.output_dir, 'Expected Results')
        self.model_path = os.path.join(self.project_root, 'Models', 'clp_model.mzn')

        self._create_widgets()

    def _find_project_root(self):
        """Find CLP-RCLP Minizinc project root"""
        current = Path(__file__).parent.absolute()

        # Search upwards for project root
        while current.name != 'CLP-RCLP Minizinc' and current.parent != current:
            current = current.parent

        if current.name == 'CLP-RCLP Minizinc':
            return str(current)

        # Fallback to parent of Generator
        return str(Path(__file__).parent.parent.absolute())

    def _create_widgets(self):
        """Create all GUI widgets"""

        # Header
        header_frame = tk.Frame(self.root, bg=self.colors['dark_blue'], height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="AVISPA CLP Instance Generator",
            font=('Arial', 20, 'bold'),
            bg=self.colors['dark_blue'],
            fg=self.colors['white']
        )
        title_label.pack(pady=20)

        subtitle_label = tk.Label(
            header_frame,
            text="Professional Test Instance Generator for Charging Location Problem",
            font=('Arial', 10),
            bg=self.colors['dark_blue'],
            fg=self.colors['light_blue']
        )
        subtitle_label.pack()

        # Main content frame
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Input parameters section
        params_frame = tk.LabelFrame(
            main_frame,
            text=" Instance Parameters ",
            font=('Arial', 12, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['dark_blue'],
            padx=20,
            pady=20
        )
        params_frame.pack(fill='x', pady=(0, 15))

        # Number of buses
        buses_frame = tk.Frame(params_frame, bg=self.colors['white'])
        buses_frame.pack(fill='x', pady=10)

        tk.Label(
            buses_frame,
            text="Number of Buses:",
            font=('Arial', 11),
            bg=self.colors['white'],
            anchor='w'
        ).pack(side='left', padx=(0, 20))

        self.buses_var = tk.IntVar(value=5)
        buses_spinbox = tk.Spinbox(
            buses_frame,
            from_=2,
            to=25,
            textvariable=self.buses_var,
            font=('Arial', 11),
            width=10,
            state='readonly'
        )
        buses_spinbox.pack(side='left')

        tk.Label(
            buses_frame,
            text="(2-25)",
            font=('Arial', 9),
            bg=self.colors['white'],
            fg=self.colors['gray']
        ).pack(side='left', padx=(10, 0))

        # Number of stations
        stations_frame = tk.Frame(params_frame, bg=self.colors['white'])
        stations_frame.pack(fill='x', pady=10)

        tk.Label(
            stations_frame,
            text="Number of Stations:",
            font=('Arial', 11),
            bg=self.colors['white'],
            anchor='w'
        ).pack(side='left', padx=(0, 20))

        self.stations_var = tk.IntVar(value=8)
        stations_spinbox = tk.Spinbox(
            stations_frame,
            from_=4,
            to=25,
            textvariable=self.stations_var,
            font=('Arial', 11),
            width=10,
            state='readonly'
        )
        stations_spinbox.pack(side='left')

        tk.Label(
            stations_frame,
            text="(4-25)",
            font=('Arial', 9),
            bg=self.colors['white'],
            fg=self.colors['gray']
        ).pack(side='left', padx=(10, 0))

        # Validation toggle
        self.validate_var = tk.BooleanVar(value=True)
        validate_check = tk.Checkbutton(
            params_frame,
            text="Validate with MiniZinc (automatically fix if UNSAT)",
            variable=self.validate_var,
            font=('Arial', 10),
            bg=self.colors['white'],
            activebackground=self.colors['white']
        )
        validate_check.pack(pady=(15, 5))

        # Action buttons
        button_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        button_frame.pack(fill='x', pady=15)

        generate_btn = tk.Button(
            button_frame,
            text="Generate Instance",
            command=self._generate_instance,
            font=('Arial', 12, 'bold'),
            bg=self.colors['light_blue'],
            fg=self.colors['white'],
            activebackground=self.colors['dark_blue'],
            activeforeground=self.colors['white'],
            padx=30,
            pady=10,
            cursor='hand2',
            relief='raised',
            bd=2
        )
        generate_btn.pack(side='left', expand=True, padx=5)

        clear_btn = tk.Button(
            button_frame,
            text="Clear Log",
            command=self._clear_log,
            font=('Arial', 11),
            bg=self.colors['gray'],
            fg=self.colors['white'],
            activebackground=self.colors['dark_blue'],
            activeforeground=self.colors['white'],
            padx=20,
            pady=10,
            cursor='hand2'
        )
        clear_btn.pack(side='left', expand=True, padx=5)

        # Log section
        log_frame = tk.LabelFrame(
            main_frame,
            text=" Generation Log ",
            font=('Arial', 11, 'bold'),
            bg=self.colors['white'],
            fg=self.colors['dark_blue'],
            padx=10,
            pady=10
        )
        log_frame.pack(fill='both', expand=True)

        # Log text with scrollbar
        log_scroll = tk.Scrollbar(log_frame)
        log_scroll.pack(side='right', fill='y')

        self.log_text = tk.Text(
            log_frame,
            font=('Consolas', 9),
            bg='#fafafa',
            fg='#333',
            yscrollcommand=log_scroll.set,
            wrap='word',
            state='disabled'
        )
        self.log_text.pack(fill='both', expand=True)
        log_scroll.config(command=self.log_text.yview)

        # Footer
        footer_frame = tk.Frame(self.root, bg=self.colors['dark_blue'], height=40)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)

        footer_label = tk.Label(
            footer_frame,
            text="AVISPA Research Team © 2026  |  Version 1.0.0",
            font=('Arial', 9),
            bg=self.colors['dark_blue'],
            fg=self.colors['white']
        )
        footer_label.pack(pady=10)

        # Initial log message
        self._log("Ready to generate CLP test instances.", 'info')
        self._log(f"Output directory: {self.output_dir}", 'info')

    def _log(self, message, level='info'):
        """Add message to log"""
        self.log_text.config(state='normal')

        timestamp = datetime.now().strftime('%H:%M:%S')

        if level == 'success':
            prefix = "✓"
            color_tag = 'success'
        elif level == 'error':
            prefix = "✗"
            color_tag = 'error'
        elif level == 'warning':
            prefix = "⚠"
            color_tag = 'warning'
        else:
            prefix = "ℹ"
            color_tag = 'info'

        self.log_text.insert('end', f"[{timestamp}] {prefix} {message}\n")

        # Configure tags
        self.log_text.tag_config('success', foreground='#28a745')
        self.log_text.tag_config('error', foreground='#dc3545')
        self.log_text.tag_config('warning', foreground='#ffc107')
        self.log_text.tag_config('info', foreground='#17a2b8')

        self.log_text.see('end')
        self.log_text.config(state='disabled')
        self.root.update()

    def _clear_log(self):
        """Clear log text"""
        self.log_text.config(state='normal')
        self.log_text.delete('1.0', 'end')
        self.log_text.config(state='disabled')
        self._log("Log cleared.", 'info')

    def _generate_instance(self):
        """Main instance generation workflow"""
        num_buses = self.buses_var.get()
        num_stations = self.stations_var.get()

        self._log(f"Starting generation: {num_buses} buses, {num_stations} stations", 'info')

        try:
            # Generate instance
            self._log("Generating instance with expert algorithm...", 'info')
            generator = FeasibleInstanceGenerator(num_buses, num_stations)
            instance = generator.generate_instance()
            self._log(f"Instance generated: {instance['max_stops']} max stops per bus", 'success')

            # Generate filename
            counter = 1
            while True:
                filename = f"generated_{counter}_{num_buses}buses_{num_stations}stations.dzn"
                filepath = os.path.join(self.output_dir, filename)
                if not os.path.exists(filepath):
                    break
                counter += 1

            # Export to .dzn
            self._log(f"Exporting to: {filename}", 'info')
            MiniZincExporter.export_to_dzn(instance, filepath)
            self._log(f"File created: {filepath}", 'success')

            # Validate if requested
            if self.validate_var.get():
                self._log("Validating instance with MiniZinc...", 'info')
                self._validate_and_fix(filepath, instance, num_buses, num_stations, counter)
            else:
                self._log("Skipping validation (disabled by user)", 'warning')
                self._log("=" * 60, 'info')

        except Exception as e:
            self._log(f"Error during generation: {str(e)}", 'error')
            messagebox.showerror("Generation Error", f"An error occurred:\n{str(e)}")

    def _validate_and_fix(self, filepath, instance, num_buses, num_stations, counter):
        """Validate instance and fix if UNSAT"""
        validator = InstanceValidator(self.model_path, timeout=60)

        max_attempts = 5
        attempt = 1

        while attempt <= max_attempts:
            is_sat, solution, error = validator.validate_instance(filepath)

            if is_sat:
                self._log(f"✓ Instance is SATISFIABLE!", 'success')
                self._log(f"  Solution: {solution['total_stations']} stations optimal", 'success')

                # Save expected result
                self._save_expected_result(filepath, solution)

                self._log("=" * 60, 'info')
                messagebox.showinfo(
                    "Success",
                    f"Instance generated successfully!\n\n"
                    f"File: {os.path.basename(filepath)}\n"
                    f"Solution: {solution['total_stations']} stations\n"
                    f"Deviation: {solution['total_deviation']}"
                )
                return

            else:
                self._log(f"✗ Attempt {attempt}/{max_attempts}: {error}", 'warning')

                if attempt < max_attempts:
                    self._log(f"Regenerating instance (attempt {attempt + 1})...", 'info')

                    # Regenerate
                    generator = FeasibleInstanceGenerator(num_buses, num_stations)
                    instance = generator.generate_instance()

                    # Update filepath
                    filename = f"generated_{counter}_{num_buses}buses_{num_stations}stations_v{attempt}.dzn"
                    filepath = os.path.join(self.output_dir, filename)

                    MiniZincExporter.export_to_dzn(instance, filepath)
                    self._log(f"New file: {filename}", 'info')

                    attempt += 1
                else:
                    self._log("Maximum attempts reached. Instance may be too constrained.", 'error')
                    self._log("=" * 60, 'info')
                    messagebox.showerror(
                        "Validation Failed",
                        f"Could not generate satisfiable instance after {max_attempts} attempts.\n\n"
                        f"Try adjusting parameters or contact support."
                    )
                    return

    def _save_expected_result(self, dzn_path, solution):
        """Save expected result to Expected Results directory"""
        basename = os.path.basename(dzn_path).replace('.dzn', '')
        result_filename = f"{basename}_expected.json"
        result_path = os.path.join(self.expected_dir, result_filename)

        result_data = {
            'instance': basename,
            'generated': datetime.now().isoformat(),
            'solver': 'chuffed',
            'satisfiable': True,
            'solution': solution,
            'dzn_path': dzn_path
        }

        with open(result_path, 'w') as f:
            json.dump(result_data, f, indent=2)

        self._log(f"Expected result saved: {result_filename}", 'success')

# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = GeneratorGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
