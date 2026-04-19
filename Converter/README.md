# Converter - JSON to DZN Conversion Tool

Professional interface for converting JITS2022 test batteries from JSON format to MiniZinc integer DZN format.

## Overview

The Converter tool provides an intuitive GUI to transform JSON bus schedule files from the JITS2022 dataset into integer-scaled DZN format compatible with the CLP and RCLP models.

## Features

- **Directory Selection**: Browse and select from JITS2022 test directories
- **Batch Conversion**: Convert one or all tests from a selected directory
- **Data-Driven Conversion**: Reads actual instance data (stations, distances, speeds)
- **JITS2022 Algorithm**: Calculates travel times (T) using JITS2022 speed/distance formula
- **Flexible Output**: Create new battery directories or use existing ones
- **Real-time Progress**: Monitor conversion status with live logging
- **Dark/Light Themes**: Professional UI with theme switching
- **Tooltips**: Context help on all major controls
- **Integer Scaling**: All values scaled by 10x for MiniZinc integer arithmetic

## Usage

### Launch the Interface

```bash
python Converter/converter.py
```

### Workflow

1. **Select Test Directory**
   - Choose a directory from JITS2022/Code/Data
   - Directories like `cork-1-line`, `cork-2-lines`, etc.

2. **Select Tests to Convert**
   - Option 1: Convert all JSON files in the directory
   - Option 2: Select specific test files

3. **Choose Output Battery**
   - Select an existing battery: Battery Own, Battery Project Integer, etc.
   - Files automatically organized by test name and solver subdirectories

4. **Start Conversion**
   - Click "Convert" to begin
   - Monitor progress in the log panel
   - Click "Stop" to cancel at any time

### Output Structure

Converted files are organized as:

```
Data/
├── Battery Own/
│   ├── cork-1-line/           # Test name directory
│   │   ├── cork-1-line_20.dzn
│   │   ├── cork-1-line_30.dzn
│   │   ├── distances_input.csv
│   │   ├── stations_input.csv
│   │   └── input_report.txt
│   └── ...
```

## Architecture

```
Converter/
├── converter.py              (Entry point)
├── config.py                 (Configuration)
├── __init__.py
│
├── core/
│   ├── __init__.py
│   ├── converter_engine.py   (JSON->DZN conversion logic)
│   ├── file_manager.py       (Directory and file operations)
│   └── jits_analyzer.py      (JITS2022 dataset analysis)
│
├── ui/
│   ├── __init__.py
│   ├── interface.py          (Main Tkinter interface)
│   ├── themes.py             (Dark/light theme system)
│   ├── components.py         (Reusable UI widgets)
│   └── tooltip.py            (Hover tooltips)
│
└── README.md                 (This file)
```

## Components

### converter_engine.py

Core conversion logic:

- Parse JSON bus schedules with JITS2022 format
- Load stations and distance matrix from CSV files
- Calculate travel times (T) using JITS2022 algorithm:
  - T = distance / speed (constrained by speed limits)
  - Includes rest time adjustments when applicable
- Generate integer DZN files with proper formatting
- Batch conversion support with configurable parameters

### file_manager.py

File operations:

- Create output directory structure
- Copy required data files (distances, stations data)
- Validate output paths
- Cleanup on conversion failures

### jits_analyzer.py

JITS2022 dataset utilities:

- List available test directories
- Validate JSON file structure
- Extract test metadata
- Check required data file availability

### ui/interface.py

Professional Tkinter GUI:

- Directory and test selection
- Output configuration
- Real-time conversion monitoring
- Status indicators and logging

## Conversion Details

### Integer Scaling

All floating-point values are multiplied by 50 and rounded to integers:

- **Time**: 42.5 minutes → 2125 (divide by 50 for minutes)
- **Energy**: 1.3 kWh → 65 (divide by 50 for kWh)
- **Distance**: 0.265 km → 13 (divide by 50 for km)

The SCALE factor was increased from 10 to 50 to minimize precision loss in distance values. Analysis shows this reduces the percentage of distances losing >5% accuracy from 1.2% to 0.1%, particularly important for small distances (< 0.01 km) that would otherwise round to zero.

### Model Parameters

Configurable parameters for CLP model (from experiment_config.py):

- **Cmax**: 100.0 kWh (battery capacity)
- **Cmin**: 20.0 kWh (minimum reserve)
- **alpha**: 10.0 kWh/min (fast charging rate)
- **mu**: 5.0 min (maximum delay allowed)
- **model_speed**: 30 km/h (minimum speed constraint)
- **rest_time**: 10 min (rest duration at stops)

All parameters are scaled by factor SCALE (default: 50) for integer arithmetic.
Configuration can be modified via experiment_config.py or config files.

### Required Data Files

The converter requires the following files for correct operation:

- **buses*input*<speed>\_<rest>.json**: Bus routes, stops, and schedules
  - REQUIRED for all conversions
  - Filename pattern determines speed and rest parameters

- **distances_input.csv**: Distance matrix between stations
  - REQUIRED for calculating travel times (T)
  - Used with actual speeds to compute journey durations
  - Values in kilometers (converted to meters internally)

- **stations_input.csv**: Station names and identifiers
  - REQUIRED for mapping station references
  - Defines num_stations and station names

Optional/Legacy Files:

- **input_report.txt**: Dataset statistics
  - Currently not used by converter
  - Kept for reference but does not affect conversion

## Theme Support

Toggle between Dark and Light modes using the button in the header:

- **Dark Mode** (default): Optimized for extended use
- **Light Mode**: High contrast alternative

## Tooltips

Hover over [?] icons to get context-specific help:

- Which directory to select
- How conversion works
- What JSON and DZN formats are
- Support file information

## Requirements

- Python 3.8+
- tkinter (usually included with Python)
- pathlib, json, logging (standard library)

## Related Tools

- **Generator**: Create new test instances
- **Runner**: Execute tests with multiple solvers
- Scripts/data-processing/convert_json_to_integer_dzn.py: CLI conversion script

## Troubleshooting

### "No JSON files found"

- Verify the selected directory contains JSON files
- Check file names match `buses_input_*.json` pattern

### "Loading stations and distance data..." error

- Ensure distances_input.csv exists in the directory
- Ensure stations_input.csv exists in the directory
- These files are now REQUIRED (not optional)
- Check file names are exactly: `distances_input.csv`, `stations_input.csv`

### Conversion failed

- Check output directory is writable
- Ensure JSON files are valid
- Verify required CSV files are present and readable
- Check available disk space

### "Zero or negative time delta" warnings

- These are normal for JITS2022 instances with consecutive duplicate stations
- Indicates a stop where bus stays at same location (rest)
- Converter handles this gracefully by using default 1-minute delta

## Technical Notes

- Conversion is performed in a separate thread to keep UI responsive
- Failed conversions are cleaned up automatically
- All paths are cross-platform compatible (Windows/Linux/macOS)
- Logging with timestamps for debugging

## Author

AVISPA Research Team
Date: April 2026
Version: 1.5.1 (JITS2022 Algorithm Implementation)
