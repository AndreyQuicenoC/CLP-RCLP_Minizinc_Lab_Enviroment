"""
================================================================================
MiniZinc Exporter Module - Instance Export
================================================================================
Exports generated instances to MiniZinc DZN format with comprehensive
documentation and metadata.
================================================================================
"""

from typing import Dict, List
from datetime import datetime
from pathlib import Path


class MiniZincExporter:
    """Export instances to MiniZinc DZN format"""

    @staticmethod
    def format_array_1d(arr: List) -> str:
        """Format 1D array for MiniZinc"""
        return '[' + ','.join(map(str, arr)) + ']'

    @staticmethod
    def format_array_2d(arr: List[List], num_buses: int) -> str:
        """Format 2D array with comments per bus - MiniZinc syntax compliant"""
        lines = []
        for b in range(num_buses):
            row = ','.join(map(str, arr[b]))
            # Add comma after each row EXCEPT the last one
            if b < num_buses - 1:
                lines.append(f"  {row},  % Bus {b+1}")
            else:
                lines.append(f"  {row}  % Bus {b+1}")

        return '[\n' + '\n'.join(lines) + '\n]'

    @staticmethod
    def export_to_dzn(instance: Dict, output_path: str) -> str:
        """
        Export instance to DZN format with metadata

        Returns:
            Path to created file
        """
        num_buses = instance['num_buses']
        num_stations = instance['num_stations']
        max_stops = instance['max_stops']

        # Calculate metadata
        total_energy = sum(sum(D) for D in instance['D'])
        avg_energy_per_bus = total_energy / num_buses if num_buses > 0 else 0
        overconsumption_factor = (
            avg_energy_per_bus / (instance['Cmax'] - instance['Cmin'])
        )

        content = f"""% =============================================================================
% Generated CLP Test Instance (v2.0)
% =============================================================================
% Generator: AVISPA CLP Instance Generator v2.0.0 (Modular)
% Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
%
% Instance Characteristics:
%   - Buses: {num_buses}
%   - Stations: {num_stations}
%   - Max stops per bus: {max_stops}
%   - Actual stops per bus: {instance['num_stops']}
%   - Total energy consumption: {total_energy} (scaled ×10)
%   - Average per bus: {avg_energy_per_bus:.0f} ({avg_energy_per_bus/10:.1f} kWh)
%   - Usable capacity: {instance['Cmax'] - instance['Cmin']} ({(instance['Cmax'] - instance['Cmin'])/10:.1f} kWh)
%
% Feasibility Analysis:
%   - Overconsumption factor: {overconsumption_factor:.2f}x
%   - Expected charges per bus: {overconsumption_factor - 1:.1f}
%   - Pattern: Designed to force strategic charging
%
% All values scaled ×10 for integer arithmetic.
% Divide by 10 to get original units (kWh, minutes).
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
% Station 1 is the depot (D=0, T=0)
st_bi = array2d(1..{num_buses}, 1..{max_stops}, {MiniZincExporter.format_array_2d(instance['st_bi'], num_buses)});

% --- Energy Consumption (D) ---
% Energy consumed between stops (scaled ×10, divide by 10 for kWh)
D = array2d(1..{num_buses}, 1..{max_stops}, {MiniZincExporter.format_array_2d(instance['D'], num_buses)});

% --- Travel Time (T) ---
% Time between stops (scaled ×10, divide by 10 for minutes)
T = array2d(1..{num_buses}, 1..{max_stops}, {MiniZincExporter.format_array_2d(instance['T'], num_buses)});

% --- Timetable (tau_bi) ---
% Scheduled arrival times (scaled ×10, divide by 10 for minutes since 00:00)
% Buses are staggered to reduce station conflicts
tau_bi = array2d(1..{num_buses}, 1..{max_stops}, {MiniZincExporter.format_array_2d(instance['tau_bi'], num_buses)});
"""

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return output_path
