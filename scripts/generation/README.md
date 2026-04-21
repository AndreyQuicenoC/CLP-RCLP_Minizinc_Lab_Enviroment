# Generation Scripts

Scripts for generating instance variants and creating new test instances.

## Contents

### `create_cork_variants.py`
Extract individual cycles from complete Cork project instances, transforming them into feasible single-cycle variants.

**Description**:
The Cork project contains multi-cycle instances (378-568 stops) that are infeasible for the standard CLP model. This script extracts the first operational cycle (~42 stops) creating more manageable instances.

**Usage**:
```bash
python create_cork_variants.py
```

**Input**: `Data/Battery Project Integer/cork-*.dzn`
**Output**: `Data/Battery Project Variant/cork-*_1cycle.dzn`

**Features**:
- Extract exactly 42 stops from first cycle
- Maintain coherent time and consumption structure
- Create well-formatted .dzn files with comments
- Handle UTF-8 encoding for Windows/Linux compatibility

---

### `generate_synthetic_data.py`
Generate synthetic CLP instances for testing and development.

**Usage**:
```bash
python generate_synthetic_data.py [options]
```

**Features**:
- Generate configurable random instances
- Export to MiniZinc format (.dzn)
- Valid and testable structure
- Automatic value scaling

**Main Parameters**:
- `--buses N`: Number of buses
- `--stations M`: Number of stations
- `--output FILE`: Output directory/file

**Example**:
```bash
python generate_synthetic_data.py --buses 10 --stations 15
```

## Related Scripts
- Data Processing: `../data-processing/` (to validate generated data)
- Testing: `../testing/test_generator.sh` (to verify variants)
- Utilities: `../utilities/diagnose_cork.sh` (to diagnose issues)
- GUI: `../../Generator/generator.py` (interactive instance generator)

## Dependencies
- Python 3.8+
- Standard library: re, sys, pathlib

## Architecture
```
Cork Original (378-568 stops)
    ↓
create_cork_variants.py
    ↓
Cork Variant (1 cycle, ~42 stops) ✓ FEASIBLE
```

## Troubleshooting
- **UTF-8 Encoding**: Script auto-configures encoding on Windows
- **Missing Files**: Verify that `Data/Battery Project Integer/` exists
- **Invalid Format**: Ensure Cork files have "% Bus X" comments
