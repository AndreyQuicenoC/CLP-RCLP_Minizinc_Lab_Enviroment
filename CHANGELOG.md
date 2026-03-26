# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-25

### Added

- **GUI Instance Generator** (`Generator/generator.py`)
  - Tkinter-based professional interface
  - Supports 2-25 buses and 4-25 stations
  - Expert algorithm with overconsumption factor adjustment
  - Automatic MiniZinc validation
  - Self-correction: regenerates up to 5 times if UNSAT
  - JSON-based expected results storage
  - Dark blue/white/gray professional theme

- **Data Processing Scripts**
  - `Scripts/data-processing/convert_json_to_integer_dzn.py` - Convert JSON to MiniZinc format
  - `Scripts/data-processing/validate_integer_dzn.py` - Validate DZN files for correctness

- **Generator Scripts**
  - `Scripts/generation/create_cork_variants.py` - Extract single cycles from Cork instances
  - `Scripts/generation/generate_synthetic_data.py` - Generate synthetic test cases

- **Testing Suite**
  - `Scripts/testing/test_generator.sh` - Comprehensive system validation (7 tests)
  - `Scripts/testing/test_clp_preliminary.sh` - Preliminary CLP tests
  - `Scripts/testing/run_battery_project_tests.py` - Full battery test suite
  - `Scripts/testing/test_initial_small_case.py` - Small case validation

- **Setup & Utilities**
  - `Scripts/setup/setup_and_validate.py` - Initial environment validation
  - `Scripts/utilities/diagnose_cork.sh` - Cork instance diagnostics

- **Documentation**
  - Comprehensive README files in all directories
  - Generated System documentation (600+ lines)
  - Model documentation (mathematical formulation)
  - Analysis reports (Cork feasibility, data corrections, model modifications)

- **Data**
  - 5 Cork single-cycle variants in `Data/Battery Project Variant/`
  - 3 generated test instances in `Data/Battery Generated/`
  - Expected results for regression testing
  - Original validated instances in `Data/Battery Own/`

- **Professional Organization**
  - Organized Scripts into 5 functional categories (data-processing, generation, testing, setup, utilities)
  - Organized Docs into 3 technical categories (generated-system, model, analysis)
  - Professional .gitignore
  - LICENSE (MIT)
  - CONTRIBUTING.md guidelines

### Technical Details

- **Overconsumption Factor**: 1.1-1.4x forcing strategic charging
- **Route Diversity**: Multiple strategies (sequential, reverse, zigzag, weighted-random)
- **Consumption Model**: Gaussian(18kWh, σ=4kWh) per stop, scaled ×10 for integer arithmetic
- **Temporal Feasibility**: Staggered start times (7:00 AM + 5 min/bus)
- **Auto-Validation**: MiniZinc integration with subprocess control and 5-attempt self-correction
- **Encoding**: UTF-8 support with Windows/Linux/macOS compatibility

### Test Results

- 7/7 system tests passing (100% success rate)
- All instances validated as SATISFIABLE or properly flagged
- Cork variants successfully extracted and reduced from ~378 stops to ~42 stops
- Generated instances use expert algorithm patterns
- Performance verified with Chuffed solver (v2.9.4)

### Test Instances Available

- 5 Cork variants (from full-day multi-cycle to single-cycle)
- 3 generated test instances (5 buses/8 stations, variable complexity)
- 2 noncity original instances
- All instances with complete documentation and expected results

### Quality Metrics

- Lines of Code: 1500+ (generator.py)
- Documentation: 600+ lines (README.md)
- Test Coverage: 7 test cases covering all major components
- Code Organization: 5 script categories + 3 doc categories
- Compatibility: Windows, Linux, macOS

### Known Limitations

- Cork single-cycle variants are structurally complex (expected WARN on tests)
- Large instances (>20 buses) may timeout with default 5-minute limit
- GUI requires tkinter (included in standard Python installation)

### Dependencies

- Python 3.8+
- MiniZinc 2.6+
- Chuffed solver (recommended)
- Standard library modules

### Files Overview

```
CLP-RCLP Minizinc/
├── Generator/                          # GUI application
│   ├── generator.py (1500+ lines)
│   └── README_BUILD.md
├── Scripts/
│   ├── data-processing/ (2 scripts)
│   ├── generation/ (2 scripts)
│   ├── testing/ (4 scripts)
│   ├── setup/ (1 script)
│   └── utilities/ (1 script)
├── Docs/
│   ├── generated-system/ (600+ lines)
│   ├── model/
│   └── analysis/
├── Data/
│   ├── Battery Project Integer/        # Cork instances
│   ├── Battery Project Variant/        # Generated Cork variants
│   ├── Battery Generated/              # User-generated instances
│   └── Battery Own/                    # Original validated instances
├── Models/                             # MiniZinc model files
├── Tests/                              # Execution results
├── README.md                           # Main documentation
├── LICENSE                             # MIT License
├── CONTRIBUTING.md                     # Contributing guidelines
├── CHANGELOG.md                        # This file
└── .gitignore                          # Git ignore rules
```

---

## Future Roadmap

### Planned for v1.1
- Build .exe executable with PyInstaller
- Batch instance generation
- Advanced visualization of solutions
- CLI mode for automated generation

### Planned for v1.2
- RCLP model integration
- Constraint relaxation tools
- Performance profiling subsystem
- Parallel solver support

### Long-term Vision
- Web interface for remote access
- Cloud-based instance generation
- Integration with other optimization toolkits
- Academic paper generation from results
- Advanced analytics dashboard

---

**Version**: 1.0.0
**Release Date**: 2026-03-25
**Status**: Stable
