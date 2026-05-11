# Scripts Directory

Collection of utility scripts for data processing, generation, testing, and verification of the CLP-RCLP optimization framework.

## Directory Structure

```
scripts/
├── data-processing/        # Data conversion and validation
│   ├── convert_json_to_integer_dzn.py
│   ├── validate_integer_dzn.py
│   └── README.md
│
├── generation/             # Instance variant and synthetic generation
│   ├── create_cork_variants.py
│   ├── generate_synthetic_data.py
│   └── README.md
│
├── setup/                  # Environment setup and validation
│   ├── setup_and_validate.py
│   └── README.md
│
├── solvers/                # Solver installation and testing
│   ├── check_solvers.py              # Check available solvers
│   ├── diagnose_solvers.py           # Diagnose solver issues
│   ├── test_gurobi.py
│   ├── test_multiple_solvers.py
│   └── README.md
│
├── testing/                # Test suites and validation
│   ├── test_generator.sh              (MAIN TEST SUITE)
│   ├── test_clp_preliminary.sh
│   ├── run_battery_project_tests.py
│   ├── test_converter.py
│   ├── test_converter_integration.py
│   ├── test_initial_small_case.py
│   └── README.md
│
├── ui-testing/             # UI interface validation
│   ├── test_runner_ui.py
│   ├── test_generator_ui.py
│   └── README.md
│
├── utilities/              # Diagnostic and utility scripts
│   ├── diagnose_cork.sh
│   └── README.md
│
├── verification/           # Converter and model verification
│   ├── analyze_distance_scaling.py
│   ├── test_converter_against_jits2022.py
│   ├── verify_converter_fidelity.py
│   ├── verify_dzn_correctness.py
│   └── (no individual README)
│
└── README.md               # This file
```

## Quick Start

### Launch System Center (Recommended)

```bash
cd core
python start.py
```

Then use the GUI to access all tools.

### From Command Line

```bash
# First time: validate setup
python scripts/setup/setup_and_validate.py

# Check available solvers
python scripts/solvers/check_solvers.py

# Run test suite
bash scripts/testing/test_generator.sh
```

## Module Guide

### Data Processing (`data-processing/`)

Convert and validate data formats.

**Scripts:**
- `convert_json_to_integer_dzn.py` - JSON → DZN conversion
- `validate_integer_dzn.py` - Verify DZN file correctness

**Usage:**
```bash
# Convert JSON to DZN
python data-processing/convert_json_to_integer_dzn.py input.json

# Validate DZN file
python data-processing/validate_integer_dzn.py data.dzn
```

### Generation (`generation/`)

Create test instances and variants.

**Scripts:**
- `create_cork_variants.py` - Extract Cork single-cycle variants
- `generate_synthetic_data.py` - Generate random instances

**Usage:**
```bash
# Generate Cork variants
python generation/create_cork_variants.py

# Generate synthetic data
python generation/generate_synthetic_data.py --buses 10 --stops 5
```

### Setup (`setup/`)

Configure and validate environment.

**Scripts:**
- `setup_and_validate.py` - Validate system requirements

**Usage:**
```bash
python setup/setup_and_validate.py
```

### Solvers (`solvers/`)

Manage and test solver installation.

**Scripts:**
- `check_solvers.py` - List available solvers
- `diagnose_solvers.py` - Diagnose solver issues
- `test_gurobi.py` - Test Gurobi solver
- `test_multiple_solvers.py` - Test all solvers

**Usage:**
```bash
# Check installed solvers
python solvers/check_solvers.py

# Diagnose issues
python solvers/diagnose_solvers.py

# Test specific solver
python solvers/test_gurobi.py
```

### Testing (`testing/`)

Execute test suites.

**Main Scripts:**
- `test_generator.sh` - **MAIN** test suite (recommended)
- `test_clp_preliminary.sh` - Preliminary tests
- `test_converter.py` - Converter unit tests
- `test_converter_integration.py` - Integration tests
- `run_battery_project_tests.py` - Battery project tests
- `test_initial_small_case.py` - Small case validation

**Usage:**
```bash
# Run main test suite
bash testing/test_generator.sh

# Run specific tests
bash testing/test_clp_preliminary.sh
python testing/test_converter.py
```

### UI Testing (`ui-testing/`)

Validate user interface and theme system.

**Scripts:**
- `test_runner_ui.py` - Test Runner interface
- `test_generator_ui.py` - Test Generator interface

**Tests:**
- Theme switching (dark/light)
- Component rendering
- Window positioning
- Responsive layout

### Utilities (`utilities/`)

Diagnostic tools.

**Scripts:**
- `diagnose_cork.sh` - Analyze Cork instance issues

**Usage:**
```bash
bash utilities/diagnose_cork.sh
```

### Verification (`verification/`)

Verify converter and model correctness.

**Scripts:**
- `test_converter_against_jits2022.py` - Verify converter accuracy
- `verify_converter_fidelity.py` - Check conversion fidelity
- `verify_dzn_correctness.py` - Validate DZN output
- `analyze_distance_scaling.py` - Analyze scaling parameters

## Use Cases

### New User Setup

```bash
# 1. Validate environment
python setup/setup_and_validate.py

# 2. Check solvers
python solvers/check_solvers.py

# 3. Launch System Center
cd core && python start.py
```

### Generate Test Data

```bash
# Via GUI (recommended)
cd core && python start.py
# Then use Instance Generator tool

# Via command line
python generation/generate_synthetic_data.py --buses 10 --stops 5 --output test_instance
```

### Run Optimization Tests

```bash
# Via GUI (recommended)
cd core && python start.py
# Then use Test Runner tool

# Via command line
bash testing/test_generator.sh
```

### Convert Data Format

```bash
# Via GUI
cd core && python start.py
# Then use Data Converter tool

# Via command line
python data-processing/convert_json_to_integer_dzn.py data.json
```

### Verify Installation

```bash
# Check all requirements
python setup/setup_and_validate.py

# Test solvers
python solvers/check_solvers.py

# Run verification tests
python verification/test_converter_against_jits2022.py
```

## Data Paths (v2.0.0)

All paths reference the new structure:

```
../experiments/instances/           # Test instances (old: ../Data/)
├── battery-project-integer/
├── battery-project-variant/
├── battery-generated/
└── battery-own/

../experiments/results/             # Results (old: ../Tests/)
└── Diagnostics/

../core/models/                     # Models (old: ../Models/)
├── clp_model.mzn
├── rclp_model.mzn
└── archive/
```

## System Requirements

- **Python**: 3.8+
- **MiniZinc**: 2.6+
- **RAM**: 8GB minimum, 16GB recommended
- **Disk**: 2GB for solvers and test data

## Dependencies

All scripts use only Python standard library and MiniZinc CLI.

Optional Python packages:
- `pytest` (for testing)
- `numpy` (for some analysis scripts)

## Running Tests

### Full Test Suite (Recommended)

```bash
cd scripts
bash testing/test_generator.sh
```

### Individual Tests

```bash
# Data processing
python data-processing/validate_integer_dzn.py ../experiments/instances/*.dzn

# Generation
python generation/generate_synthetic_data.py --test

# Conversion
python testing/test_converter.py

# Solver verification
python solvers/test_multiple_solvers.py
```

## Maintenance

- **Paths**: All scripts use relative paths from `scripts/` directory
- **Python Version**: 3.8+ required
- **Encoding**: UTF-8
- **Cross-platform**: Windows, Linux, macOS compatible

## Contributing

To add new scripts:

1. Choose appropriate category directory
2. Create script file following naming convention
3. Add documentation to category README.md
4. Update relative paths if needed
5. Test with multiple solvers if applicable

## Documentation

For detailed information:

- [data-processing/README.md](data-processing/README.md) - Data tools
- [generation/README.md](generation/README.md) - Generation tools
- [setup/README.md](setup/README.md) - Setup procedures
- [solvers/README.md](solvers/README.md) - Solver management
- [testing/README.md](testing/README.md) - Test procedures
- [ui-testing/README.md](ui-testing/README.md) - UI testing
- [utilities/README.md](utilities/README.md) - Diagnostics

---

**Version**: 2.0.0  
**Last Updated**: April 20, 2026  
**Structure**: clp-rclp-framework pattern
