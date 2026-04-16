# Multiple Solver Support Architecture (v1.4.0)

## Overview

Version 1.4.0 introduces comprehensive multi-solver support to the CLP-RCLP environment, allowing users to execute test instances with different constraint and optimization solvers. This document provides technical context for future development and maintenance.

## Architecture

### Core Components

#### 1. Solver Management (`Runner/core/solvers.py`)

- **SolverType Enum**: Defines six solver types
  - CHUFFED (default)
  - GECODE
  - COIN_BC
  - OR_TOOLS (cp-sat)
  - CPLEX (commercial)
  - GUROBI (commercial)

- **SolverInfo Dataclass**: Encapsulates solver metadata
  - Display name, description
  - Strengths and use cases
  - Commercial license information
  - Availability status

- **SolverManager**: Static utility class for solver operations
  - Solver lookup and validation
  - Display name mapping
  - MiniZinc command-line name resolution

#### 2. Execution Engine (`Runner/core/executor.py`)

- **MiniZincExecutor Enhancement**
  - `execute()` method now accepts `solver` parameter
  - Returns tuple: (success, result_dict, execution_time)
  - Tracks execution time with millisecond precision
  - Supports all six solvers transparently

#### 3. Result Management (`Runner/core/result_handler.py`)

- **Result Organization by Solver**
  - Structure: `Tests/Output/{Battery}/{Solver}/`
  - JSON format includes: solver, execution_time, timestamp, solution
  - TXT format human-readable with solver information

- **Diagnostic Storage**
  - Structure: `Tests/Diagnostics/{Solver}/`
  - Support for three statuses: error, unsatisfiable, timeout
  - Detailed error information and execution metrics
  - Both JSON and TXT formats

#### 4. User Interface (`Runner/ui/interface.py`)

- **Solver Selection**
  - Combobox with all available solvers
  - Dynamic population from SolverManager
  - Default to Chuffed

- **Solver Information Modal**
  - Triggered by "?" button
  - Displays description, strengths, use cases
  - Shows commercial license badge if applicable
  - Centered modal window with theme support

- **Tooltip System** (`Runner/ui/tooltip.py`)
  - Professional hover tooltips on all controls
  - Theme-aware styling
  - 500ms default delay
  - Context-sensitive help text

## Data Flow

### Execution Flow

```
User Selection
    ↓
[Directory, Instance, Model, Solver]
    ↓
MiniZincExecutor.execute(instance_path, solver_type)
    ↓
[subprocess: minizinc --solver {solver} ...]
    ↓
Output Parsing
    ↓
[success, result_dict, execution_time]
    ↓
ResultHandler.save_results(instance, result, solver)
    ↓
Tests/Output/{Battery}/{Solver}/results
```

### Result Storage Structure

```
Tests/
├── Output/
│   ├── Battery Own/
│   │   ├── Chuffed/
│   │   │   ├── instance1_result.json
│   │   │   └── instance1_result.txt
│   │   ├── Gecode/
│   │   │   ├── instance1_result.json
│   │   │   └── instance1_result.txt
│   │   └── ...
│   └── Battery Generated/
│       └── ...
└── Diagnostics/
    ├── Chuffed/
    │   ├── instance1_diagnostic.json
    │   └── instance1_diagnostic.txt
    ├── Gecode/
    └── ...
```

## Configuration

### Solver Availability

Solvers are detected at runtime through MiniZinc:

```bash
minizinc --solver {solver_name} --version
```

### Commercial Solvers

- CPLEX and Gurobi marked as commercial in SolverInfo
- UI displays warning badge for commercial solvers
- No functional restrictions; users must have valid licenses

## Testing and Verification

### Solver Verification Script

```bash
python Scripts/solvers/check_solvers.py
```

- Verifies system solver availability
- Generates JSON report
- Outputs formatted console report

### Multi-Solver Testing

```bash
python Scripts/solvers/test_multiple_solvers.py Data/instance.dzn [Model] [Solvers...]
```

- Execute instance with multiple solvers
- Compare performance
- Generate benchmark report

## Key Design Decisions

### 1. Result Organization by Solver

- **Rationale**: Allows easy comparison of solver performance
- **Benefit**: Automatic benchmarking capabilities
- **Implementation**: SolverManager display names used as directory names

### 2. Execution Time Tracking

- **Rationale**: Enable performance analysis
- **Precision**: Millisecond-level (Python `time.time()`)
- **Storage**: Both JSON and TXT formats

### 3. Modal Information Dialog

- **Rationale**: Provide solver context without overwhelming UI
- **UX**: Non-intrusive, optional information access
- **Implementation**: Standard Tkinter Toplevel widget

### 4. Tooltip System

- **Rationale**: Improve discoverability of features
- **Design**: Professional, theme-aware tooltips
- **Behavior**: Hover-activated with configurable delay

## Extension Points

### Adding New Solvers

1. Add enum value to `SolverType` in `solvers.py`
2. Add entry to `SOLVER_DATABASE` with SolverInfo
3. No changes needed to executor or UI (automatic detection)

### Custom Result Formats

Modify `ResultHandler._save_json()` and `_save_txt()` to extend result format

### Additional Diagnostics

Extend `save_diagnostic()` method in ResultHandler to capture additional error details

## Performance Considerations

### Timeout Management

- Default: 300 seconds per test
- MiniZinc timeout: solver_timeout \* 1000 (milliseconds)
- Process timeout: solver_timeout + 10 seconds (Python safety margin)

### Memory Usage

- No solver processes cached in memory
- Each execution spawns new subprocess
- Graceful cleanup via `subprocess.run()` context

## Known Limitations

### Commercial Solvers

- CPLEX and Gurobi require valid system installation
- No built-in license checking
- Installation verification via `minizinc --solver {name} --version`

### Solver Compatibility

- All solvers require MiniZinc 2.5+
- Not all solvers available on all platforms
- Check system with `Scripts/solvers/check_solvers.py`

## Future Enhancements

### Potential Improvements

1. Solver warm-start capabilities (cached solutions)
2. Advanced solver configuration (algorithm selection, parameters)
3. Real-time solver switching during execution
4. Multi-objective optimization solver selection
5. Parallel execution across multiple solvers
6. Result comparison visualization

### Maintenance Tasks

- Regular update of solver version checks
- Monitoring solver availability changes
- Performance regression testing
- Documentation updates for new MiniZinc versions

## Integration Notes

### With Generator

- Generator uses hardcoded Chuffed for validation
- Can be extended to use SolverManager for flexibility
- Current implementation satisfactory for generation validation

### With Test Suite

- Scripts can leverage SolverManager for test automation
- `test_multiple_solvers.py` provides batch testing foundation
- Extensible for benchmarking workflows

## Troubleshooting Guide

### Solver Not Found

```
Error: Solver not available
Solution: Run Scripts/solvers/check_solvers.py
Action: Install missing solver via MiniZinc
```

### Timeout Issues

```
Error: Execution timed out
Solution: Check solver performance with test_multiple_solvers.py
Action: Increase timeout or choose different solver
```

### Result Organization Issues

```
Error: Results not saved to correct directory
Solution: Verify Tests/Output and Tests/Diagnostics exist
Action: Create directories if missing (auto-created by handler)
```

## References

- SolverType: `Runner/core/solvers.py:25`
- SolverInfo: `Runner/core/solvers.py:47`
- SolverManager: `Runner/core/solvers.py:167`
- MiniZincExecutor: `Runner/core/executor.py:24`
- ResultHandler: `Runner/core/result_handler.py:25`
- RunnerInterface: `Runner/ui/interface.py:43`

---

**Version**: 1.4.0  
**Last Updated**: April 2026  
**Authors**: Andrey Quiceno and Juan Francesco García (AVISPA Team)
