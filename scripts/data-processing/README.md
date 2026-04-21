# Data Processing Scripts

Scripts for processing, validating, and converting data files between different formats.

## Contents

### `convert_json_to_integer_dzn.py`
Converts JSON files with instance data to MiniZinc format (.dzn) with scaled integer values.

**Usage**:
```bash
python convert_json_to_integer_dzn.py <input.json> <output.dzn>
```

**Features**:
- Convert decimal values to integers (scaled ×10)
- Validate value ranges
- Generate descriptive comments in .dzn file
- Compatible with CLP model

### `validate_integer_dzn.py`
Verify that generated .dzn files meet CLP model requirements.

**Usage**:
```bash
python validate_integer_dzn.py <file.dzn>
```

**Validations**:
- Correct array structure
- Correct data types (integers)
- Values within allowed ranges
- Parameter coherence

## Dependencies
- Python 3.8+
- numpy (optional for analysis)

## Related Scripts
- Generation: `../generation/create_cork_variants.py` (produces data for this module)
- Testing: `../testing/run_battery_project_tests.py` (validates output)
