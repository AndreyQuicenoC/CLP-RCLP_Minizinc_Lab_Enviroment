# Electric Bus Charging Station Optimization - Integer Test Battery

This directory contains a comprehensive testing framework for the CLP-based electric bus charging station optimization model. All data files use **INTEGER values** (scaled by ×10) for compatibility with the `chuffed` solver.

## 📁 Directory Structure

```
CLP-RCLP Minizinc/
├── Models/
│   ├── clp_model.mzn           # Integer-based CLP model (SCALE=10)
│   └── rclp_model.mzn          # RCLP model (floating-point)
│
├── Data/
│   ├── Battery Project Integer/  # ✨ INTEGER test battery (NEW)
│   │   ├── cork-1-line20_0.dzn
│   │   ├── cork-1-line20_10.dzn
│   │   └── ... (180+ test cases)
│   │
│   ├── Battery Project/          # Original floating-point tests
│   └── Battery Own/              # Manually created & synthetic tests
│
├── Scripts/
│   ├── convert_json_to_integer_dzn.py      # JSON → Integer DZN converter
│   ├── validate_integer_dzn.py             # Data validation
│   ├── test_initial_small_case.py          # Quick sanity test
│   ├── generate_synthetic_data.py          # Synthetic data generator
│   └── run_battery_project_tests.py        # Full test suite runner
│
└── Tests/
    └── Battery Project/
        ├── Run_1/              # First execution results
        ├── Run_2/              # Second execution results
        └── ...
```

## 🔧 Key Features

### 1. Integer Scaling System
All floating-point values are multiplied by **10** and converted to integers:
- `420.0` minutes → `4200` (42.0 minutes actual)
- `1.3` kWh → `13` (1.3 kWh actual)
- `100.0` kWh (Cmax) → `1000`

This ensures compatibility with `chuffed` solver's integer-only constraint solving.

### 2. Professional Test Management
- **Automatic run numbering**: Each execution creates `Run_N/` directory
- **Graceful interruption**: Ctrl+C saves progress and generates reports
- **Comprehensive logging**: Both console and file logs
- **Individual result files**: One `.txt` per test case
- **Summary reports**: Aggregate statistics and detailed results

### 3. Data Validation
Built-in validation ensures:
- No floating-point values in DZN files
- Consistent scaling across all parameters
- Valid array dimensions and station IDs
- Reasonable energy/time values

## 🚀 Quick Start

### Step 1: Validate Existing Integer Data
```bash
cd "CLP-RCLP Minizinc"
python Scripts/validate_integer_dzn.py
```

### Step 2: Run Initial Small Test
```bash
python Scripts/test_initial_small_case.py
```

### Step 3: Generate Additional Synthetic Data
```bash
python Scripts/generate_synthetic_data.py
```

### Step 4: Run Full Test Battery
```bash
python Scripts/run_battery_project_tests.py
```

**Advanced options:**
```bash
# Limit time per test to 2 minutes
python Scripts/run_battery_project_tests.py --time-limit 120000

# Run only cork-1-line tests
python Scripts/run_battery_project_tests.py --pattern "cork-1-line*.dzn"

# Run first 10 tests only
python Scripts/run_battery_project_tests.py --limit 10
```

## 📊 Understanding Results

### Test Output Format
Each test generates a result file (`<test_name>.txt`) with:
```
================================================================================
Test Case: cork-1-line20_0
Timestamp: 2026-03-25T10:30:15
================================================================================

Status: SUCCESS
Elapsed Time: 45.23s
Timed Out: No
Return Code: 0

SOLUTION FOUND:
  Optimal: Yes
  Stations Installed: 8
  Total Deviation: 120
  Solve Time: 42.15s
  Nodes Explored: 15234

================================================================================
STANDARD OUTPUT:
================================================================================
Estaciones instaladas: [1,0,1,0,1,0,1,0...]
...
```

### Summary Report
The `SUMMARY.txt` file provides:
- Execution metadata (run number, timestamps, duration)
- Statistics (success rate, solutions found, timeouts)
- Detailed results table for all tests

## 🔄 Data Conversion Workflow

If you need to convert new JSON test files:

```bash
# Single file conversion
python Scripts/convert_json_to_integer_dzn.py input.json output.dzn

# Batch conversion (all JITS2022 data)
python Scripts/convert_json_to_integer_dzn.py
```

The converter:
1. Reads JSON bus schedules
2. Extracts routes, times, and energy consumption
3. Scales all values by ×10
4. Generates well-commented DZN files with integers
5. Ensures compatibility with `clp_model.mzn`

## 📝 Important Notes

### Integer Interpretation
When viewing results, **divide integer values by 10**:
- Time: `4250` → `425.0` minutes (7h 5min)
- Energy: `135` → `13.5` kWh
- Deviation: `50` → `5.0` minutes

### Model Parameters (Integer Values)
```minizinc
Cmax = 1000;    % 100.0 kWh battery capacity
Cmin = 200;     % 20.0 kWh minimum reserve
alpha = 100;    % 10.0 kWh/min charging rate
mu = 50;        % 5.0 minutes max delay
SM = 10;        % 1.0 minute safety margin
psi = 10;       % 1.0 minute min charging time
beta = 100;     % 10.0 minutes max charging time
M = 100000;     % 10000.0 Big-M constant
```

### Solver Configuration
- **Solver**: `chuffed` (integer constraint programming)
- **Default timeout**: 5 minutes (300,000 ms)
- **Output mode**: JSON stream (for structured parsing)
- **Statistics**: Enabled (nodes, solve time, etc.)

## 🛠️ Troubleshooting

### "No DZN files found"
- Run `convert_json_to_integer_dzn.py` first
- Check that `Data/Battery Project Integer/` exists

### "Model file not found"
- Ensure you're in the `CLP-RCLP Minizinc` directory
- Verify `Models/clp_model.mzn` exists

### Tests timing out
- Reduce time limit: `--time-limit 120000` (2 minutes)
- Run smaller subset: `--limit 10`
- Use simpler test patterns: `--pattern "cork-1-line*"`

### Validation errors
- Check the detailed error messages
- Verify JSON files are correctly formatted
- Ensure no manual edits introduced floating-point values

## 📚 File Naming Convention

Test files follow this pattern:
```
<dataset>_<buses>_<variation>.dzn

Examples:
- cork-1-line20_0.dzn       # Cork 1 line, 20 buses, variation 0
- galway-6-lines30_10.dzn   # Galway 6 lines, 30 buses, variation 10
- synthetic_5buses-10stations-8stops.dzn  # Synthetic test
```

## 🎯 Best Practices

1. **Always validate after conversion**: Run `validate_integer_dzn.py`
2. **Test small cases first**: Use `test_initial_small_case.py`
3. **Monitor disk space**: Test results can accumulate
4. **Keep logs**: Don't delete `Run_N` directories until analyzed
5. **Document changes**: Update this README if adding new scripts

## 📈 Future Enhancements

- [ ] Parallel test execution
- [ ] Result visualization (graphs, charts)
- [ ] Comparison tools between runs
- [ ] Performance regression detection
- [ ] Export to CSV/Excel format
- [ ] Web dashboard for results

## 👥 Authors

- EV-CLP Battery Project Team
- Date: March 2026

## 📄 License

Internal research use only.

---

**Last Updated**: 2026-03-25
**Version**: 1.0.0
**Status**: Production Ready ✅
