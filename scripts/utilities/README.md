# Utility Scripts

Scripts for general utilities, diagnostics, and auxiliary functions.

## Contents

### `validate_integration.py`

**Purpose**: Comprehensive validation of path resolution, navigation, and theme integration systems.

**What it validates**:
- ✓ Core directory structure (converter, generator, runner, orchestration, shared)
- ✓ ToolPathResolver implementation and functionality
- ✓ Navigation system between windows
- ✓ Orchestrator UI theme switching components
- ✓ Theme system integration across all modules
- ✓ Module imports and dependencies

**Usage**:

```bash
# Basic validation
python scripts/utilities/validate_integration.py

# Verbose output with detailed error messages
python scripts/utilities/validate_integration.py --verbose
python scripts/utilities/validate_integration.py -v
```

**Exit Codes**:
- `0`: All validations passed ✓
- `1`: One or more validations failed ✗

**Example Output**:

```
CORE DIRECTORY STRUCTURE VALIDATION
========================
✓ core/converter/
✓ core/generator/
✓ core/runner/
✓ core/orchestration/
✓ core/shared/

PATH RESOLVER VALIDATION
========================
✓ PathResolver Module
✓ PathResolver Import
✓ Tool 'converter' found: core/converter/converter.py
✓ Tool 'generator' found: core/generator/generator.py
✓ Tool 'runner' found: core/runner/runner.py

NAVIGATION SYSTEM VALIDATION
========================
✓ Navigation Module
✓ Orchestrator Entry
✓ Navigation contains 'return_to_orchestrator'
✓ Navigation contains 'path_resolver_import'

ORCHESTRATOR UI VALIDATION
========================
✓ Orchestrator Interface
✓ ThemeManager (Theme component)
✓ _toggle_theme (Theme component)
✓ _refresh_ui_colors (Theme component)
✓ FlatButton (UI component)
✓ ToolPathResolver (Navigation component)

SUMMARY
========================
Total Checks: 23/23
Success Rate: 100.0%

Overall Status: ✓ PASS
```

### `diagnose_cork.sh`

Diagnostic script for analyzing and resolving Cork instance issues.

**Usage**:
```bash
bash diagnose_cork.sh
```

**Functionality**:
- Check Cork file format
- Analyze size and structure
- Report main parameters
- Suggest corrective actions
- Validate data integrity

## Utilities Module

This module can be expanded with useful auxiliary functions:
- Format conversion
- Instance analysis
- Visualization
- Post-processing

## Related Scripts

- Generation: `../generation/` (Cork variant generation)
- Data Processing: `../data-processing/` (validation and processing)
- Testing: `../testing/` (output verification)
- Verification: `../verification/` (window transitions and integration)

## Dependencies

**Python Scripts**:
- Python 3.8+
- pathlib (standard library)
- logging (standard library)

**Shell Scripts**:
- bash 4.0+

## Development Notes

To add new utility scripts:
1. Create file in this directory
2. Add documentation to "Contents" section
3. Update this README
4. Include comprehensive module docstring
5. Add logging for debugging support

