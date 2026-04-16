# Converter - JSON to DZN Conversion Tool

Professional interface for converting JITS2022 test batteries from JSON format to MiniZinc integer DZN format.

## Overview

The Converter tool provides an intuitive GUI to transform JSON bus schedule files from the JITS2022 dataset into integer-scaled DZN format compatible with the CLP and RCLP models.

## Features

- **Directory Selection**: Browse and select from JITS2022 test directories
- **Batch Conversion**: Convert one or all tests from a selected directory
- **Support File Handling**: Automatically copies required CSV and metadata files
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

- Parse JSON bus schedules
- Calculate energy consumption
- Generate integer DZN files with proper formatting
- Batch conversion support

### file_manager.py

File operations:

- Create output directory structure
- Copy support files (distances, stations data)
- Validate output paths
- Cleanup on conversion failures

### jits_analyzer.py

JITS2022 dataset utilities:

- List available test directories
- Validate JSON file structure
- Extract test metadata
- Check support file availability

### ui/interface.py

Professional Tkinter GUI:

- Directory and test selection
- Output configuration
- Real-time conversion monitoring
- Status indicators and logging

## Conversion Details

### Integer Scaling

All floating-point values are multiplied by 10 and rounded to integers:

- **Time**: 42.5 minutes → 425 (divide by 10 for minutes)
- **Energy**: 1.3 kWh → 13 (divide by 10 for kWh)
- **Schedule times**: Stored as minutes since 00:00, scaled x10

### Model Parameters

Hardcoded scaled values for CLP model:

- Cmax = 1000 (100.0 kWh)
- Cmin = 200 (20.0 kWh)
- alpha = 100 (10.0 kWh/min)
- mu = 50 (5.0 min)
- And others...

### Support Files

If available, the following files are copied to output directory:

- **distances_input.csv**: Distance matrix between stations
- **stations_input.csv**: Station coordinates and metadata
- **input_report.txt**: Dataset statistics and information

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
- Check file names match `*_input.json` pattern

### Conversion failed

- Check output directory is writable
- Ensure JSON files are valid
- Check available disk space

### Missing support files

- Conversion works without them
- Warnings are logged but don't prevent conversion

## Technical Notes

- Conversion is performed in a separate thread to keep UI responsive
- Failed conversions are cleaned up automatically
- All paths are cross-platform compatible (Windows/Linux/macOS)
- Logging with timestamps for debugging

## Author

AVISPA Research Team
Date: April 2026
Version: 1.0.0
