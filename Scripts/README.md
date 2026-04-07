# Scripts Directory

Collection of scripts for generation, validation, testing, and utilities of the CLP-RCLP MiniZinc project.

## Directory Structure

```
Scripts/
├── data-processing/        # Data conversion and validation
│   ├── convert_json_to_integer_dzn.py
│   ├── validate_integer_dzn.py
│   └── README.md
│
├── generation/            # Instance variant and synthetic generation
│   ├── create_cork_variants.py
│   ├── generate_synthetic_data.py
│   └── README.md
│
├── testing/              # Testing suite and validation
│   ├── test_generator.sh              (MAIN)
│   ├── test_clp_preliminary.sh
│   ├── run_battery_project_tests.py
│   ├── test_initial_small_case.py
│   └── README.md
│
├── setup/               # Initial configuration
│   ├── setup_and_validate.py
│   └── README.md
│
├── ui-testing/         # UI interface validation and theme testing
│   ├── test_runner_ui.py
│   ├── test_generator_ui.py
│   └── README.md
│
├── utilities/           # Diagnostic and utility scripts
│   ├── diagnose_cork.sh
│   └── README.md
│
└── README.md            # This file
```

## Quick Start Workflow

### First Time Using the Project
```bash
# 1. Initial setup
python setup/setup_and_validate.py

# 2. Generate Cork variants (if needed)
python generation/create_cork_variants.py

# 3. Run test suite
bash testing/test_generator.sh
```

### Using the Interactive Generator
```bash
cd .. && python Generator/generator.py
```

### Development and Testing
```bash
# Individual tests
bash testing/test_clp_preliminary.sh
python testing/run_battery_project_tests.py

# Cork diagnostics
bash utilities/diagnose_cork.sh

# Validate existing data
python data-processing/validate_integer_dzn.py ../Data/Battery\ Generated/*.dzn
```

## Modules by Functionality

### Conversion & Validation (data-processing/)
Convert between formats and validate data integrity.
- `convert_json_to_integer_dzn.py` - JSON → .dzn (scaled ×10)
- `validate_integer_dzn.py` - Verify .dzn correctness

**Input**: JSON, unvalidated `.dzn`
**Output**: Validated data, correct `.dzn` files

### Generation (generation/)
Create instance variants and synthetic instances.
- `create_cork_variants.py` - Extract Cork single-cycle from full-day
- `generate_synthetic_data.py` - Generate random synthetic instances

**Input**: Full-day instances, custom parameters
**Output**: Feasible variants (single cycle), synthetic instances

### Testing (testing/)
Validate the complete system.
- `test_generator.sh` (MAIN) - Main suite (7 tests)
- `test_clp_preliminary.sh` - Basic preliminary tests
- `run_battery_project_tests.py` - Battery project tests
- `test_initial_small_case.py` - Small case tests

**Input**: .dzn instances
**Output**: Test report

### UI Testing (ui-testing/)
Validate user interface functionality and theme system.
- `test_runner_ui.py` - Runner interface validation (8 test scenarios)
- `test_generator_ui.py` - Generator interface validation (9 test scenarios)

**Input**: None (tests system directly)
**Output**: Theme system verification, component rendering confirmation
**Features Tested**: Dark/light mode switching, design tokens, component styling, window centering

### Setup (setup/)
Configure the environment.
- `setup_and_validate.py` - Validate requirements and structure

**Input**: System environment
**Output**: Configuration report and suggestions

### Utilities (utilities/)
Diagnostic functions.
- `diagnose_cork.sh` - Analyze Cork instance issues

## Global Dependencies

```bash
# Python 3.8+
python --version

# MiniZinc 2.5+
minizinc --version

# Git (for versioning)
git --version
```

## Runbook: Use Cases

### Case 1: Generate New Cork Variants
```bash
# If variants don't exist:
python generation/create_cork_variants.py

# Verify creation:
ls ../Data/Battery\ Project\ Variant/cork-*_1cycle.dzn
```

### Case 2: Validate Existing Data
```bash
# Validate single .dzn file
python data-processing/validate_integer_dzn.py ../Data/sample.dzn

# Validate all files in directory
for f in ../Data/Battery\ Generated/*.dzn; do
  python data-processing/validate_integer_dzn.py "$f"
done
```

### Case 3: Complete Testing
```bash
# Main suite (recommended)
bash testing/test_generator.sh

# If failed, diagnose
bash utilities/diagnose_cork.sh
```

### Case 4: Develop New Instances
```bash
# 1. Generate synthetic data
python generation/generate_synthetic_data.py --buses 8 --stations 10 --output test.dzn

# 2. Validate
python data-processing/validate_integer_dzn.py test.dzn

# 3. Test with MiniZinc
minizinc --solver chuffed ../Models/clp_model.mzn test.dzn
```

## Documentation

For detailed information about each module:
- [data-processing/README.md](data-processing/README.md)
- [generation/README.md](generation/README.md)
- [testing/README.md](testing/README.md)
- [setup/README.md](setup/README.md)
- [ui-testing/README.md](ui-testing/README.md)
- [utilities/README.md](utilities/README.md)

## Maintenance

- **Paths**: All scripts use relative paths from Scripts/
- **Encoding**: Python scripts use UTF-8 by default
- **Compatibility**: Windows (bash via Git Bash), Linux, macOS

## Contributing

To add new scripts:
1. Determine category (data-processing, generation, testing, setup, utilities)
2. Create file in corresponding subdirectory
3. Add documentation in subdirectory README.md
4. Update relative paths if needed
5. Follow existing naming conventions

**Last Updated**: April 2026
