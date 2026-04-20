# CLP-RCLP Usage Guide

Comprehensive guide for using each tool in the CLP-RCLP framework.

## System Center (GUI)

The easiest way to use all tools.

### Launch
```bash
cd core
python start.py
```
Or: `bash start.sh` (Unix/Linux/macOS)

### Features
- **System Features**: Display framework capabilities
- **Available Tools**: Quick access to Converter, Generator, Runner
- **Join Community**: Link to GitHub repository
- **Theme Toggle**: Switch between dark and light mode

### Workflow
1. Select a tool from the "Available Tools" section
2. Click "Launch" to open the tool's interface
3. Use the tool's dedicated GUI
4. Tools automatically save results to `experiments/results/`

---

## Data Converter

Converts JSON-formatted battery schedules to MiniZinc DZN format.

### GUI Usage
```bash
cd core
python converter/converter.py
```

Then:
1. Select input JSON file
2. Specify output path (default: same name, .dzn extension)
3. Click "Convert" or "Batch Convert"
4. View validation results
5. Results saved to `experiments/results/`

### Command-Line Usage

**Basic conversion:**
```bash
cd core
python converter/converter.py \
  --input ../experiments/instances/data.json \
  --output ../experiments/instances/data.dzn
```

**Batch conversion:**
```bash
python converter/converter.py \
  --batch \
  --input-dir ../experiments/instances/ \
  --output-dir ../experiments/instances/ \
  --pattern "*.json"
```

**With validation:**
```bash
python converter/converter.py \
  --input data.json \
  --output data.dzn \
  --validate
```

### Options
- `--input`: Input JSON file path
- `--output`: Output DZN file path
- `--batch`: Enable batch mode
- `--input-dir`: Batch input directory
- `--output-dir`: Batch output directory
- `--pattern`: File pattern for batch (default: "*.json")
- `--validate`: Validate output against model
- `--verbose`: Show detailed conversion steps

### Output Format

DZN (Data in MiniZinc) format with:
```minizinc
% Data parameters
int: n_buses;
int: n_stops;
array[1..n_buses, 1..n_stops] of int: cbi;  % Charge at event
array[1..n_buses, 1..n_stops] of int: tbi;  % Time of event
% ... additional parameters
```

### Common Issues

**Issue**: "Invalid JSON format"
- **Check**: Ensure JSON structure matches expected schema
- **Validate**: Use `python ../scripts/data-processing/validate_integer_dzn.py`

**Issue**: "Energy balance failed"
- **Check**: Initial and final battery levels
- **Verify**: Sum of charges matches energy requirements

**Issue**: "Time window violation"
- **Check**: Event times within allowed windows
- **Review**: Charging period constraints in your data

---

## Instance Generator

Creates synthetic test datasets with configurable parameters.

### GUI Usage
```bash
cd core
python generator/generator.py
```

Then:
1. Set generator parameters (buses, stops, seed, etc.)
2. Choose instance type (Random, Project-based, Cork variant)
3. Click "Generate" or "Generate Multiple"
4. Review generation report
5. Instances saved to `experiments/instances/`

### Command-Line Usage

**Generate single instance:**
```bash
cd core
python generator/generator.py \
  --buses 10 \
  --stops 5 \
  --seed 42 \
  --output battery-custom
```

**Generate multiple instances:**
```bash
python generator/generator.py \
  --batch \
  --buses 5 10 15 20 \
  --stops 3 5 7 \
  --seed 42 \
  --output battery-sweep
```

**Generate Cork variants:**
```bash
python generator/generator.py \
  --cork \
  --variants 1-line 2-lines 3-lines \
  --seed 42
```

**With custom parameters:**
```bash
python generator/generator.py \
  --buses 15 \
  --stops 8 \
  --min-battery 50 \
  --max-battery 200 \
  --min-charge-rate 20 \
  --max-charge-rate 100 \
  --output custom-instance
```

### Options
- `--buses`: Number of buses (default: 5)
- `--stops`: Number of stops per route (default: 3)
- `--seed`: Random seed for reproducibility
- `--batch`: Enable batch generation
- `--cork`: Generate Cork variants
- `--variants`: Which Cork variants (1-line, 2-lines, 3-lines)
- `--output`: Output directory/prefix
- `--min-battery`: Minimum battery capacity (kWh)
- `--max-battery`: Maximum battery capacity (kWh)
- `--min-charge-rate`: Minimum charge rate (kW)
- `--max-charge-rate`: Maximum charge rate (kW)
- `--verbose`: Show generation steps

### Instance Types

**Random Instances**
- Completely synthetic
- Controllable problem size
- Random parameter initialization
- Best for scalability testing

**Project-Based Instances**
- Based on real battery project data
- Realistic bus routes and timing
- Historical charging patterns
- Best for real-world validation

**Cork Variants**
- Special test cases
- Known characteristics
- Three difficulty levels: 1-line, 2-lines, 3-lines
- Best for algorithm validation

### Output
JSON file with structure:
```json
{
  "metadata": {
    "instance_type": "random",
    "n_buses": 10,
    "n_stops": 5,
    "generated": "2026-04-20T10:30:00Z"
  },
  "parameters": {
    "Cmax": [100, 120, ...],
    "Cmin": [10, 15, ...],
    "tbi": [[420, 480, ...], ...],
    ...
  }
}
```

---

## Test Runner

Executes optimization models and compares solver performance.

### GUI Usage
```bash
cd core
python runner/runner.py
```

Then:
1. Select instances from `experiments/instances/`
2. Choose solvers (Chuffed, Gecode, COIN-BC, OR-Tools, CPLEX, Gurobi)
3. Set timeout (seconds)
4. Click "Run Tests"
5. View results in real-time
6. Results saved to `experiments/results/`

### Command-Line Usage

**Run with Chuffed:**
```bash
cd core
python runner/runner.py \
  --instances battery-project \
  --solvers chuffed \
  --timeout 300
```

**Compare multiple solvers:**
```bash
python runner/runner.py \
  --instances battery-project battery-generated \
  --solvers chuffed gecode "COIN-BC" \
  --timeout 300 \
  --output comparison.csv
```

**With specific instances:**
```bash
python runner/runner.py \
  --instance-files \
    ../experiments/instances/data1.dzn \
    ../experiments/instances/data2.dzn \
  --solvers chuffed gecode \
  --timeout 600
```

**Generate HTML report:**
```bash
python runner/runner.py \
  --instances battery-project \
  --solvers chuffed gecode \
  --generate-report \
  --report-name "Solver Comparison"
```

### Options
- `--instances`: Instance directory (can specify multiple)
- `--instance-files`: Specific DZN files
- `--solvers`: Solver names (space-separated)
- `--timeout`: Timeout per instance in seconds (default: 300)
- `--output`: Output file for results (CSV, JSON)
- `--generate-report`: Create HTML report
- `--report-name`: Title for HTML report
- `--parallel`: Run solvers in parallel (default: true)
- `--verbose`: Show detailed execution

### Supported Solvers

| Solver | Status | License | Speed | Notes |
|--------|--------|---------|-------|-------|
| Chuffed | ✓ Available | Open | ⚡⚡⚡ | Default, best for CLP |
| Gecode | ✓ Available | Open | ⚡⚡ | Reliable, consistent |
| COIN-BC | ✓ Available | Open | ⚡ | MILP solver |
| OR-Tools | ✓ Available | Open | ⚡⚡ | Google solver |
| CPLEX | Optional | Proprietary | ⚡⚡⚡ | Requires license |
| Gurobi | Optional | Proprietary | ⚡⚡⚡ | Requires license |

**Check available solvers:**
```bash
python ../scripts/solvers/check_solvers.py
```

### Result Output

**CSV Format:**
```
instance,solver,status,optimal_value,solve_time_ms,nodes_explored
data1.dzn,chuffed,OPTIMAL,45250,1234,5678
data1.dzn,gecode,OPTIMAL,45250,2345,8901
```

**HTML Report includes:**
- Summary statistics
- Solver comparison charts
- Instance difficulty analysis
- Detailed result table
- Execution logs

### Interpreting Results

**Status values:**
- `OPTIMAL`: Optimal solution found
- `SATISFIABLE`: Feasible solution found (not proven optimal)
- `UNSATISFIABLE`: No solution exists
- `UNKNOWN`: Timeout or solver error

**Metrics:**
- **Optimal Value**: Objective function value
- **Solve Time**: Wall-clock time in milliseconds
- **Nodes Explored**: Search tree nodes examined
- **Gap**: Optimality gap (%) for incomplete solutions

---

## Batch Workflow Example

Complete workflow for generating, converting, and testing instances:

### Step 1: Generate Instances
```bash
cd core
python generator/generator.py \
  --batch \
  --buses 5 10 15 \
  --stops 3 5 \
  --output battery-test \
  --seed 42
```

### Step 2: Convert to DZN
```bash
python converter/converter.py \
  --batch \
  --input-dir ../experiments/instances/ \
  --output-dir ../experiments/instances/
```

### Step 3: Run Optimization
```bash
python runner/runner.py \
  --instances battery-test \
  --solvers chuffed gecode \
  --timeout 600 \
  --generate-report \
  --report-name "Batch Test Results"
```

### Step 4: Analyze Results
```bash
# View results summary
cat ../experiments/results/summary.csv

# Open HTML report in browser
# File: ../experiments/results/report.html
```

---

## Performance Tips

### For Large Instances
1. Increase timeout: `--timeout 1200` (20 minutes)
2. Use faster solvers: Chuffed, OR-Tools
3. Enable parallel execution (default)
4. Run on multi-core system

### For Scalability Testing
1. Generate instances with varying sizes
2. Use batch mode for efficiency
3. Compare solvers on same instances
4. Look for performance inflection points

### For Accuracy
1. Use Chuffed or Gurobi for proven optimality
2. Increase timeout if unsure
3. Validate results with multiple solvers
4. Check instance feasibility before running

---

## Troubleshooting

### Solver Issues

**Problem**: Solver not found
```bash
# Check installed solvers
python ../scripts/solvers/check_solvers.py

# See installation guides
# docs/installation/minizinc_installation.md
# docs/installation/gurobi_installation.md
# docs/installation/cplex_installation.md
```

**Problem**: Timeout too short
- Increase with `--timeout` parameter
- Check system resources while running
- Consider solver choice (Chuffed is fastest for CLP)

### Data Issues

**Problem**: Conversion fails
```bash
# Validate JSON format
python ../scripts/data-processing/validate_integer_dzn.py input.json

# Check schema
# See docs/guides/TROUBLESHOOTING.md
```

**Problem**: Instance unsatisfiable
- Verify data correctness
- Check battery capacity constraints
- Review time window feasibility
- See troubleshooting guide

### Performance Issues

**Problem**: Slow execution
- Use Chuffed solver (fastest for CLP)
- Reduce instance size
- Check system load
- Enable parallel execution

**Problem**: High memory usage
- Run smaller instances
- Use streaming result output
- Disable parallel execution if needed
- Monitor with system tools

---

## Integration with Scripts

Run utility scripts for data processing and validation:

```bash
# Validate DZN correctness
python ../scripts/data-processing/validate_integer_dzn.py data.dzn

# Generate synthetic data
python ../scripts/generation/generate_synthetic_data.py

# Test converter fidelity
python ../scripts/verification/test_converter_against_jits2022.py

# Run comprehensive tests
bash ../scripts/testing/test_converter.py
```

See `scripts/README.md` for complete script documentation.
