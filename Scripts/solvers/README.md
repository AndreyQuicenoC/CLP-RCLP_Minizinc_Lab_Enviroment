# Solver Management Scripts

Professional scripts for managing and testing multiple solvers in the CLP-RCLP environment.

## Available Scripts

### 1. check_solvers.py
Check which solvers are available in your system and verify installation.

**Usage:**
```bash
python Scripts/solvers/check_solvers.py
```

**Output:**
- Console report with availability status
- JSON report saved to `Tests/solver_check_report.json`
- Version information for each solver

**Example Output:**
```
======================================================================
SOLVER AVAILABILITY REPORT
======================================================================

Summary: 3/6 solvers available

----------------------------------------------------------------------
✓ AVAILABLE SOLVERS
----------------------------------------------------------------------

  CHUFFED
    Status: Ready
    Info: MiniZinc solver chuffed 0.12.8

  GECODE
    Status: Ready
    Info: MiniZinc solver gecode 6.3.0

----------------------------------------------------------------------
✗ UNAVAILABLE SOLVERS
----------------------------------------------------------------------

  CPLEX
    Status: Not found
    Details: Solver not available
```

### 2. test_multiple_solvers.py
Execute a test instance with multiple solvers and compare performance.

**Usage:**
```bash
# Test with all available solvers
python Scripts/solvers/test_multiple_solvers.py Data/Battery\ Own/instance.dzn

# Test with specific model
python Scripts/solvers/test_multiple_solvers.py Data/Battery\ Own/instance.dzn RCLP

# Test with specific solvers
python Scripts/solvers/test_multiple_solvers.py Data/Battery\ Own/instance.dzn CLP chuffed gecode coin-bc
```

**Output:**
- Console summary with results
- JSON results saved to `Tests/solver_tests/instance_multi_solver_results.json`

**Example Output:**
```
Testing instance: instance.dzn
Model: CLP
Solvers: chuffed, gecode, coin-bc

Testing chuffed... ✓ (0.123s)
Testing gecode... ✓ (0.456s)
Testing coin-bc... ✗ (5.000s)

================================================================================
MULTI-SOLVER TEST RESULTS
================================================================================
Instance: instance.dzn
Model: CLP
--------------------------------------------------------------------------------

Successful: 2/3 solvers

SUCCESSFUL SOLVERS (sorted by execution time):
--------------------------------------------------------------------------------
  chuffed          - 0.123s
  gecode           - 0.456s

FAILED SOLVERS:
--------------------------------------------------------------------------------
  coin-bc          - Execution timed out
```

## Solver Information

### Available Solvers

1. **Chuffed** (Default)
   - Fast constraint solver
   - Best for CLP/RCLP problems
   - Recommended for quick testing

2. **Gecode**
   - General-purpose constraint solver
   - Good optimization capabilities
   - Stable and well-documented

3. **COIN-BC**
   - Linear/mixed-integer programming
   - Efficient branch-and-cut
   - Good for LP problems

4. **Globalizer**
   - Global optimization solver
   - Non-convex problem support
   - Rigorous bounds computation

5. **CPLEX** (Commercial)
   - Industry-leading optimizer
   - Highest performance
   - Requires valid license

6. **Gurobi** (Commercial)
   - Cutting-edge optimization
   - Multi-threading support
   - Requires valid license

## Installation

### Check Solver Installation
```bash
python Scripts/solvers/check_solvers.py
```

### Install via MiniZinc (Recommended)
```bash
# Most solvers are included with MiniZinc
# Download from: https://www.minizinc.org/

# Verify MiniZinc is in PATH
minizinc --version
```

### Commercial Solver Licenses
- **CPLEX**: IBM official website
- **Gurobi**: Gurobi official website
- Academic licenses often available free

## Integration with Runner

The Runner UI automatically:
- Detects available solvers
- Allows solver selection per test
- Organizes results by solver
- Stores diagnostics for failures

## Output Organization

### Successful Results
- Location: `Tests/Output/{Battery}/{Solver}/`
- Formats: JSON and TXT
- Contains: instance data, solution, execution time

### Diagnostics (Failures/Unsatisfiable)
- Location: `Tests/Diagnostics/{Solver}/`
- Formats: JSON and TXT
- Contains: error information, stderr, execution time

## Troubleshooting

### Solver Not Found
```bash
# Check if MiniZinc is installed
minizinc --version

# Check solver availability
python Scripts/solvers/check_solvers.py

# Verify PATH
echo $PATH
```

### Timeout Issues
- Increase timeout in Runner UI
- Check system resources
- Try different solver

### Performance Comparison
Use `test_multiple_solvers.py` to identify fastest solver for your instances.

## Authors

Andrey Quiceno and Juan Francesco García (AVISPA Team)

Last Updated: April 2026
Version: 1.4.0
