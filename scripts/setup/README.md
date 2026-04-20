# Setup & Diagnosis Scripts

Scripts for initial configuration, diagnostics, and troubleshooting of the CLP-RCLP project.

## Contents

### `setup_and_validate.py`
Initial configuration script that verifies all requirements and prepares the environment.

**Usage**:
```bash
python setup_and_validate.py
```

**Validations**:
- Correct directory structure
- Python 3.8+ installation
- MiniZinc availability
- Model files present
- Base data available

**Output**: Configuration report with steps to resolve issues

## Setup Workflow

1. **First Time**:
   ```bash
   python setup_and_validate.py    # Validate requirements
   ```

2. **If Cork Issues**:
   ```bash
   bash ../utilities/diagnose_cork.sh           # Diagnose
   python ../generation/create_cork_variants.py  # Regenerate
   ```

3. **Verify Everything Works**:
   ```bash
   bash ../testing/test_generator.sh  # Complete test
   ```

## Dependencies
- Python 3.8+
- bash (for .sh scripts)
- MiniZinc 2.5+ (https://www.minizinc.org)
- git (for cloning/updating)

## Troubleshooting

### MiniZinc not found
```bash
# Linux (Debian/Ubuntu)
sudo apt install minizinc

# macOS
brew install minizinc

# Windows
# Download from https://www.minizinc.org/software.html
```

### Python version too old
```bash
python3 --version  # Must be 3.8+
pip install --upgrade pip
```

### Directory structure issues
```bash
# Regenerate directories
python setup_and_validate.py --fix
```

## Related Documentation
- Quick Start Guide: `../../README.md`
- Model Documentation: `../../Docs/model/README.md`
