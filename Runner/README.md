# Runner - CLP/RCLP Test Interface (v1.4.0 - Multi-Solver Edition)

Professional GUI interface for executing CLP and RCLP tests on generated or existing instances with support for multiple constraint solvers.

## Overview

Runner provides a clean, user-friendly interface to:

- Select test instances from Data directories
- Choose between CLP and RCLP models
- **Select from 6 solvers** (Chuffed, Gecode, COIN-BC, Globalizer, CPLEX, Gurobi)
- View solver information and capabilities
- Execute tests with chosen solver
- Save results organized by solver in JSON and TXT formats
- View real-time execution status and diagnostics

## Usage

### Launch the Interface

```bash
python Runner/runner.py
```

### Workflow

1. **Select Directory**: Choose from available data directories
   - Battery Own
   - Battery Project Integer
   - Battery Project Variant
   - Battery Generated

2. **Select Instance**: Pick a .dzn test file from the directory

3. **Choose Model**: Select either CLP or RCLP model

4. **Select Solver**: Pick from 6 available solvers
   - **Chuffed** (Default) - Fast constraint solver
   - **Gecode** - General-purpose constraint programming
   - **COIN-BC** - Linear/mixed-integer programming
   - **Globalizer** - Global optimization
   - **CPLEX** (Commercial) - High-performance optimizer
   - **Gurobi** (Commercial) - Cutting-edge optimization

5. **Get Solver Info**: Click the "?" button to learn about the selected solver

6. **Run Test**: Click "Run Test" button to execute

7. **View Results**: Monitor progress in the results panel

### Result Output

Results are automatically organized by solver in `Tests/Output/{DirectoryName}/{Solver}/` in two formats:

#### JSON Format (`{filename}_result.json`)

```json
{
  "solver": "Chuffed",
  "execution_time_seconds": 0.234,
  "num_buses": 5,
  "num_stations": 8,
  "charged_stations": 2,
  "charging_locations": [0, 1, 0, 0, 1, 0, 0, 0],
  "time_deviation_minutes": 45,
  "timestamp": "2026-04-15T10:30:45.123456"
}
```

#### TXT Format (`{filename}_result.txt`)

```
======================================================================
CLP-RCLP Test Execution Result
======================================================================

Solver:                 Chuffed
Execution Time:         0.234 seconds
Timestamp:              2026-04-15T10:30:45.123456

Number of Buses:        5
Number of Stations:     8
Charged Stations:       2
Charging Locations:     [0,1,0,0,1,0,0,0]
Time Deviation:         45 minutes

======================================================================
```

### Diagnostics

Failed or unsatisfiable runs are stored in `Tests/Diagnostics/{Solver}/` with detailed error information in both JSON and TXT formats.

## Architecture

```
Runner/
├── runner.py              (Entry point)
├── config.py              (UI colors and constants)
├── __init__.py
│
├── core/
│   ├── __init__.py
│   ├── executor.py        (MiniZinc execution with solver support)
│   ├── result_handler.py  (Result organization and file generation)
│   └── solvers.py         (Solver management and metadata)
│
├── ui/
│   ├── __init__.py
│   ├── interface.py       (Tkinter GUI with solver selection)
│   ├── themes.py          (Theme system - dark/light)
│   ├── components.py      (Reusable UI components)
│   ├── layouts.py         (Layout builders)
│   ├── tooltip.py         (Tooltip component)
│   └── ...
│
└── README.md              (This file)
```

## Components

### core/executor.py

Handles MiniZinc model execution with:

- **Multi-solver support** (6 solvers)
- Process management and timeout handling
- Execution time measurement (millisecond precision)
- Output parsing and solution extraction
- Error handling and logging
- Support for all available solvers via SolverType parameter

### core/result_handler.py

Manages result file generation with:

- **Solver-specific result organization** (Tests/Output/{Battery}/{Solver}/)
- **Diagnostic storage** (Tests/Diagnostics/{Solver}/)
- JSON export with solver information and execution time
- Human-readable TXT format with solver details
- Support for success, unsatisfiable, and error statuses
- Directory creation and file management

### core/solvers.py

Solver management and metadata:

- SolverType enum (6 solvers)
- SolverInfo dataclass with descriptions and capabilities
- SolverManager utility class for solver operations
- Solver information database for UI tooltips

### ui/interface.py

Professional Tkinter interface featuring:

- **Solver selection dropdown** with all 6 solvers
- **Solver information modal** (triggered by "?" button)
- Directory and file selection dropdowns
- Model selector (radio buttons)
- Comprehensive tooltips on all controls
- Real-time status display
- Run/Stop controls
- Dark/Light theme support
- Professional window centering

### config.py

Centralized configuration with:

- UI color palette
- Font settings
- Data directory mapping
- MiniZinc solver settings

## Requirements

- Python 3.8+
- MiniZinc 2.5+ with at least one solver installed
- tkinter (usually included with Python)
- Supported solvers:
  - Chuffed (included with MiniZinc)
  - Gecode (included with MiniZinc)
  - COIN-BC (included with MiniZinc)
  - Globalizer (included with MiniZinc)
  - CPLEX (requires license)
  - Gurobi (requires license)

## Theme Support

Runner features a professional theme system with:

- **Dark Mode** (Default) - Optimized for extended use
- **Light Mode** - High contrast alternative
- 27 design tokens per theme
- Real-time theme switching
- Dynamic UI updates

Theme toggle available in header bar (☀ Light / 🌙 Dark)

## Solver Verification

Check available solvers on your system:

```bash
python Scripts/solvers/check_solvers.py
```

This generates a report in `Tests/solver_check_report.json` listing which solvers are installed.

## Multi-Solver Testing

Run a single instance with multiple solvers to compare performance:

```bash
python Scripts/solvers/test_multiple_solvers.py Data/Battery\ Own/instance.dzn CLP
```

Results are saved to `Tests/solver_tests/` with detailed timing information.

## Architecture Documentation

For detailed technical information about the v1.4.0 multi-solver implementation, see:
- `Docs/ARCHITECTURE_v1_4_0.md` - Complete technical architecture
- `Scripts/solvers/README.md` - Solver scripts documentation
