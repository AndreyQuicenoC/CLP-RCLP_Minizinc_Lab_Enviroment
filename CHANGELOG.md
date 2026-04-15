# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.0] - 2026-04-15

### Added

- **Multi-Solver Support**
  - Six solver options: Chuffed, Gecode, COIN-BC, Globalizer, CPLEX, Gurobi
  - New `solvers.py` module with SolverType enum and SolverManager class
  - Solver information database with capabilities and use cases
  - Solver selection combobox in Runner UI
  - Solver information modal dialog with detailed descriptions
  - Support for commercial solvers (CPLEX and Gurobi)

- **Result Organization by Solver**
  - Results automatically organized in `Tests/Output/{Battery}/{Solver}/`
  - Diagnostics organized in `Tests/Diagnostics/{Solver}/`
  - Execution time tracking for all solvers
  - Solver information in result JSON and TXT files
  - Support for unsatisfiable and error diagnostics

- **Enhanced Execution Engine**
  - MiniZincExecutor updated to support solver parameter
  - Execution time measurement (millisecond precision)
  - Improved error handling and diagnostics
  - Status tracking for different execution outcomes

- **User Experience Improvements**
  - Comprehensive tooltip system in `tooltip.py`
  - Tooltips on all configuration controls
  - Solver information button with "?" icon
  - Modal dialog for solver capabilities information
  - Window size increased to 950x650 for new controls
  - Enhanced logging with solver information

- **Solver Verification Scripts**
  - `Scripts/solvers/check_solvers.py`: System solver availability checker
  - `Scripts/solvers/test_multiple_solvers.py`: Multi-solver performance comparison
  - JSON reports for solver status and test results
  - Comprehensive solver documentation in `Scripts/solvers/README.md`

### Changed

- Runner version updated to 1.4.0
- Updated project version to 1.4.0
- ResultHandler refactored to organize results by solver
- MiniZincExecutor.execute() now returns (success, result, execution_time) tuple
- Enhanced error diagnostics with more detailed reporting

### Documentation

- Updated README.md with multi-solver features
- Added comprehensive solver documentation
- Updated all feature descriptions and examples
- Added usage examples for new solver features
- Updated project status and version badges

### Technical Details

**Solver Integration:**
- All solvers compatible with MiniZinc 2.5+
- Graceful fallback to Chuffed if solver unavailable
- Commercial solver license handling
- Timeout management per solver

**Result Storage:**
- JSON format includes: solver, execution time, timestamp, solution data
- TXT format human-readable with clear sections
- Diagnostic files contain error information and timestamps
- Support for both successful and failed execution tracking

## [1.3.0] - 2026-04-07

### Added

- **Modular Theme System**
  - Complete dark/light theme support for all interfaces
  - ThemeManager singleton for global theme state management
  - 27 design tokens per theme (colors, typography, spacing)
  - Theme observer pattern for real-time UI updates
  - Professional color palettes (dark default, light alternative)
  - Consistent design language across Generator and Runner

- **UI Improvements**
  - Window centering on screen startup (both Runner and Generator)
  - Improved window sizing for better display (850x650 Runner, 750x600 Generator)
  - Fixed FlatButton theme switching widget accessibility
  - Enhanced component styling with theme-aware rendering

- **Script Organization**
  - Created `Scripts/ui-testing/` subdirectory for UI validation tests
  - Added `/test_runner_ui.py` with 8 comprehensive test scenarios
  - Added `test_generator_ui.py` with 9 comprehensive test scenarios
  - Created `Scripts/ui-testing/README.md` with complete documentation
  - Updated `Scripts/README.md` with ui-testing reference

- **Documentation Updates**
  - Updated README.md to v1.3.0 with theme system features
  - Comprehensive CHANGELOG entry documenting all changes
  - Professional authorship attribution (Andrey Quiceno and Juan Francesco García)

### Fixed

- **Runner Execution Error**
  - Fixed TypeError in MiniZincExecutor initialization
  - Changed from passing RunnerConfig object to model path string
  - Proper model file path mapping (CLP/RCLP → .mzn files)
  - Instances now execute without PathLike argument errors

- **Generator Theme Switching**
  - Fixed unknown option "-text" error during theme toggle
  - Proper FlatButton internal Label widget access
  - Theme observer now correctly updates UI components

- **Minor Issues**
  - Updated authorship to include student developer names
  - Synchronized VERSION file (1.3.0) with documentation

## [1.2.0] - 2026-04-03

### Added

- **Generator Directory Reorganization**
  - Create modular `core/` subdirectory for generation and export logic
  - Create modular `ui/` subdirectory for user interface components
  - Rename configuration modules to follow consistent patterns
  - Improved code organization with clear separation of concerns
  - Architecture documentation added

- **Output Path Consolidation**
  - Consolidate all generated instances to `Data/Battery Generated/`
  - Remove fragmented output directories
  - Centralized management of test results
  - Automatic directory creation based on source directory names

- **Scripts Documentation Translation**
  - Translate all README.md files in Scripts/ to English
  - Translate data-processing, generation, testing, setup, and utilities content
  - Professional, concise documentation without emojis
  - Clear usage instructions and examples

- **Test Runner Interface (NEW)**
  - Create `Runner/` module for professional test execution
  - Professional Tkinter GUI for running CLP/RCLP tests
  - Directory selector supporting Battery Own, Battery Project Integer/Variant, Battery Generated
  - File selector for .dzn test instances with refresh capability
  - Model selector (CLP/RCLP radio buttons)
  - Real-time status display and execution monitoring
  - Automatic result generation in JSON and TXT formats
  - Automatic `Tests/Output/{DirectoryName}/` creation
  - Senior-level code with exception handling and logging
  - Professional color palette: Gray (#CCCCCC), Dark Blue (#1E3A5F), Black (#000000)

- **Root Documentation Updates**
  - Update README.md to v1.2.0 with new Runner section
  - Remove all emojis for professional documentation
  - Add Test Runner workflow documentation
  - Update project structure to include Runner module
  - Update documentation references

- **Version Bump**
  - Update VERSION file to 1.2.0
  - Update documentation headers to reflect v1.2.0

### Changed

- **Generator Module Structure**
  - `Generator/orchestrator.py`: Renamed from `generator_orchestrator.py`
  - Output default path: `Tests/Output/Generator/` → `Data/Battery Generated/`
  - All imports updated for new modular structure

- **Documentation Style**
  - Remove emojis throughout all markdown files
  - Standardize professional documentation format
  - Maintain technical clarity with concise language
  - English-only documentation

### Removed

- `Generator/generator_old.py` - Obsolete v2.0 implementation

### Technical Details

- **New Modules**:
  - `Runner/core/executor.py` - MiniZinc execution management
  - `Runner/core/result_handler.py` - JSON/TXT result formatting
  - `Runner/ui/interface.py` - Professional Tkinter GUI

- **Output Format**:
  - JSON: Structured result data with num_buses, num_stations, charged_stations, charging_locations, time_deviation
  - TXT: Human-readable formatted results

- **Backward Compatibility**:
  - All existing functionality preserved
  - Generator v3.0 continues to work as production ready
  - All test suites remain functional

### Quality Metrics

- Lines of Code: 2500+
- New UI Module: 500+ lines
- Documentation: 3500+ lines (updated)
- Test Coverage: Maintained at 7 test suites
- Code Organization: Improved modular structure

---

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
  - Organized Scripts into 5 functional categories
  - Organized Docs into 3 technical categories
  - Professional .gitignore
  - LICENSE (MIT)
  - CONTRIBUTING.md guidelines

### Technical Details

- Overconsumption Factor: 1.1-1.4x forcing strategic charging
- Route Diversity: Multiple strategies (sequential, reverse, zigzag, weighted-random)
- Consumption Model: Gaussian(18kWh, σ=4kWh) per stop, scaled x10 for integer arithmetic
- Temporal Feasibility: Staggered start times (7:00 AM + 5 min/bus)
- Auto-Validation: MiniZinc integration with subprocess control
- Encoding: UTF-8 support with Windows/Linux/macOS compatibility

### Test Results

- 7/7 system tests passing (100% success rate)
- All instances validated as SATISFIABLE or properly flagged
- Cork variants successfully extracted and reduced
- Generated instances use expert algorithm patterns

### Quality Metrics

- Lines of Code: 1500+
- Documentation: 600+ lines
- Test Coverage: 7 test cases covering all major components
- Code Organization: 5 script categories + 3 doc categories
- Compatibility: Windows, Linux, macOS

---

**Version**: 1.2.0
**Release Date**: April 2026
**Status**: Production Ready - Generator v3.0 with Professional Test Runner
