# Core Module - CLP-RCLP Application Modules

This directory contains all the core application modules for the CLP-RCLP MiniZinc Lab Environment.

## Module Structure

```
core/
├── start.py               # Python entry point for System Center
├── start.sh               # Bash entry point for System Center
│
├── orchestration/          # System Center (main entry point)
│   ├── orchestrator.py    # Orchestrator launcher
│   ├── config.py          # Configuration
│   ├── __init__.py
│   ├── README.md
│   └── ui/                # User interface components
│
├── converter/             # JSON to DZN converter
│   ├── converter.py       # Entry point
│   ├── config.py
│   ├── core/              # Conversion engine
│   └── ui/                # Tkinter interface
│
├── generator/             # Instance generation system
│   ├── generator.py       # Entry point
│   ├── config.py
│   ├── core/              # Generation logic
│   ├── orchestrator.py    # Workflow coordinator
│   └── ui/                # User interface
│
├── runner/                # Test execution interface
│   ├── runner.py          # Entry point
│   ├── config.py
│   ├── core/              # Execution engine
│   └── ui/                # Tkinter interface
│
├── models/                # MiniZinc models
│   ├── clp_model.mzn      # CLP model
│   ├── rclp_model.mzn     # RCLP model
│   └── archive/           # Archived versions
│
└── shared/                # Shared utilities
    └── navigation.py      # Tool integration
```

## Quick Start

### Launch System Center (Recommended)

From the `core/` directory:

```bash
python start.py
```

Or use the bash wrapper:

```bash
bash start.sh
```

Or launch directly:

```bash
python orchestration/orchestrator.py
```

### Direct Module Access

From the `core/` directory:

- **Generator**: `python generator/generator.py`
- **Runner**: `python runner/runner.py`
- **Converter**: `python converter/converter.py`

## Module Details

- **Orchestration**: Central entry point providing unified interface to all tools
- **Converter**: Converts JSON schedules to MiniZinc DZN format
- **Generator**: Creates test instances with configurable parameters
- **Runner**: Executes optimization tests with multiple solvers
- **Models**: MiniZinc constraint programming models
- **Shared**: Common utilities for inter-module communication

## Architecture

All modules follow a consistent architecture pattern:

- `config.py` - Configuration and constants
- `{module}.py` - Entry point script
- `core/` - Core business logic
- `ui/` - Tkinter user interface components

## Theme System

All UI modules support dark/light theme switching with:

- Professional color palettes
- Dynamic theme switching
- Persistent theme state
- 27 design tokens per theme

## See Also

- `../docs/` - Technical documentation
- `../scripts/` - Utility scripts and testing
- `../experiments/` - Data and results
