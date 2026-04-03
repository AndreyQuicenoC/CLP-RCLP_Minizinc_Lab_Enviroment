# Runner - CLP/RCLP Test Interface

Professional GUI interface for executing CLP and RCLP tests on generated or existing instances.

## Overview

Runner provides a clean, user-friendly interface to:

- Select test instances from Data directories
- Choose between CLP and RCLP models
- Execute tests with MiniZinc solver
- Save results in JSON and TXT formats
- View real-time execution status

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

4. **Run Test**: Click "Run Test" button to execute

5. **View Results**: Monitor progress in the results panel

### Result Output

Results are automatically saved to `Tests/Output/{DirectoryName}/` in two formats:

#### JSON Format (`{filename}_result.json`)

```json
{
  "num_buses": 5,
  "num_stations": 8,
  "charged_stations": 2,
  "charging_locations": [0, 1, 0, 0, 1, 0, 0, 0],
  "time_deviation": 45
}
```

#### TXT Format (`{filename}_result.txt`)

```
============================================================
CLP-RCLP Test Execution Result
============================================================

Number of Buses:        5
Number of Stations:     8
Charged Stations:       2
Charging Locations:     [0,1,0,0,1,0,0,0]
Time Deviation:         45 minutes

============================================================
```

## Architecture

```
Runner/
├── runner.py              (Entry point)
├── config.py              (UI colors and constants)
├── __init__.py
│
├── core/
│   ├── __init__.py
│   ├── executor.py        (MiniZinc execution)
│   └── result_handler.py  (Output file generation)
│
├── ui/
│   ├── __init__.py
│   └── interface.py       (Tkinter GUI)
│
└── README.md              (This file)
```

## Components

### core/executor.py

Handles MiniZinc model execution with:

- Process management and timeout handling
- Output parsing and solution extraction
- Error handling and logging

### core/result_handler.py

Manages result file generation:

- JSON export with structured data
- Human-readable TXT format
- Directory creation and file management

### ui/interface.py

Professional Tkinter interface featuring:

- Directory and file selection dropdowns
- Model selector (radio buttons)
- Real-time status display
- Run/Stop controls
- Color scheme: Gray, Dark Blue, Black

### config.py

Centralized configuration with:

- UI color palette
- Font settings
- Data directory mapping
- MiniZinc solver settings

## Requirements

- Python 3.8+
- MiniZinc 2.5+ with Chuffed solver
- tkinter (usually included with Python)

## Color Scheme

Professional palette selected for clarity and aesthetics:

- **Background**: Light Gray (#CCCCCC)
- **Accents**: Dark Blue (#1E3A5F)
- **Text**: Black (#000000)
- **Highlights**: White (#FFFFFF)

## Status Indicators

- **[OK]**: Test passed - instance is satisfiable
- **[ERROR]**: Test failed - instance not satisfiable
- **[WARN]**: Warning messages during execution

## Limitations

- Timeout: 5 minutes per test (configurable)
- Supports CLP and RCLP models only
- Results directory auto-created based on source directory name

## Development Notes

To modify colors or settings, edit `config.py`:

```python
class RunnerConfig:
    COLOR_GRAY = "#CCCCCC"
    COLOR_DARK_BLUE = "#1E3A5F"
    # ... etc
```

All imports use absolute paths from Runner root for compatibility.

## Version

Runner v1.2.0 - Part of CLP-RCLP MiniZinc Lab Environment
