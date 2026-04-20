# ⚡ Quick Start Guide - 5 Minutes to Testing

## 🎯 Goal
Get the integer battery testing system running in 5 minutes.

## ✅ Prerequisites
- Python 3.7+
- MiniZinc 2.6+ with chuffed solver
- Terminal/Command Prompt

## 🚀 Steps

### 1. Verify Installation (30 seconds)
```bash
cd "CLP-RCLP Minizinc"

# Check MiniZinc
minizinc --version
# Expected: MiniZinc 2.6.x or higher

# Check Python
python --version
# Expected: Python 3.7 or higher
```

### 2. Validate Data (30 seconds)
```bash
python Scripts/validate_integer_dzn.py
```

**Expected output:**
```
Validating 182 DZN files...
✓ All files valid
```

### 3. Run Quick Test (2 minutes)
```bash
python Scripts/test_initial_small_case.py
```

**Expected output:**
```
Testing: noncity_5buses-8stations
✓ Test PASSED
Solution Found: OPTIMAL
Stations: 4
```

### 4. Run Small Batch (2 minutes)
```bash
python Scripts/run_battery_project_tests.py --limit 3 --time-limit 60000
```

**Expected output:**
```
[1/3] Testing: cork-1-line20_0
✓ cork-1-line20_0: 23.45s
  Solution: OPTIMAL
  Stations: 8

...

✓ ALL TESTS PASSED!
Results saved to: Tests/Battery Project/Run_1/
```

---

## 📊 What You Get

After running, check:
```bash
# View summary
cat "Tests/Battery Project/Run_1/SUMMARY.txt"

# View first result
cat "Tests/Battery Project/Run_1/cork-1-line20_0.txt"

# List all results
ls "Tests/Battery Project/Run_1/"
```

---

## 🎉 Success Indicators

✅ **All validations pass**
✅ **Small test completes in < 60s**
✅ **Results saved to Run_1/ directory**
✅ **SUMMARY.txt file exists**
✅ **No errors in execution.log**

---

## 🔧 Troubleshooting

### "minizinc: command not found"
```bash
# Install MiniZinc from https://www.minizinc.org/software.html
# Add to PATH (Windows/Mac/Linux instructions in download)
```

### "No DZN files found"
```bash
# Re-run converter
python Scripts/convert_json_to_integer_dzn.py
```

### "Test timeout"
```bash
# Use shorter timeout
python Scripts/run_battery_project_tests.py --time-limit 30000 --limit 1
```

---

## 🏃 Next Steps

Once everything works:

1. **Run Full Battery** (takes hours):
   ```bash
   python Scripts/run_battery_project_tests.py
   ```

2. **Generate Synthetic Data**:
   ```bash
   python Scripts/generate_synthetic_data.py
   ```

3. **Run Custom Tests**:
   ```bash
   python Scripts/run_battery_project_tests.py --pattern "cork-1-line*.dzn"
   ```

---

## 📚 Documentation

- `PROJECT_SUMMARY.md` - Complete project overview
- `Data/Battery Project Integer/README.md` - Data format details
- `Scripts/README.md` - Script documentation
- `Models/clp_model.mzn` - Model file (with comments)

---

## 🆘 Need Help?

1. Check `Tests/Battery Project/Run_N/execution.log`
2. Run setup script: `python Scripts/setup_and_validate.py`
3. Read error messages carefully
4. Verify file paths are correct

---

## 🎯 Most Common Commands

```bash
# Quick validation
python Scripts/validate_integer_dzn.py

# Quick test
python Scripts/test_initial_small_case.py

# Small batch
python Scripts/run_battery_project_tests.py --limit 5

# Full run (hours!)
python Scripts/run_battery_project_tests.py
```

---

**Time to Complete**: 5 minutes
**Difficulty**: Easy
**Status**: Ready to Go! 🚀
