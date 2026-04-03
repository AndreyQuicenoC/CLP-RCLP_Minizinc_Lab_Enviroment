# Troubleshooting Guide

Common issues and solutions for the CLP-RCLP MiniZinc Lab Environment.

## Installation Issues

### "minizinc: command not found"

**Cause**: MiniZinc is not installed or not in PATH

**Solutions**:

#### Windows
```bash
# Option 1: Add to PATH manually
# Control Panel → System → Environment Variables → Path → Add MiniZinc folder
# Usually: C:\Program Files\MiniZinc

# Option 2: Reinstall with "Add to PATH" option checked
# Download from https://www.minizinc.org/software.html
```

#### macOS
```bash
# Check if installed
which minizinc

# If not found, install
brew install minizinc

# Verify
minizinc --version
```

#### Linux
```bash
# Install
sudo apt update && sudo apt install minizinc

# Verify
minizinc --version
```

### "Python 3.8+ not found"

**Cause**: Python is not installed or older version

**Solutions**:

```bash
# Check version
python --version
python3 --version

# Update Python
# Windows: Download from python.org
# macOS: brew install python@3.10
# Linux: sudo apt install python3

# Use specific version
python3.10 --version
```

## Runtime Issues

### "No module named 'minizinc'"

**Cause**: Python MiniZinc bindings not installed

**Solution**:
```bash
# Install optional dependency (if needed)
pip install minizinc

# Or use system MiniZinc directly
minizinc --solver chuffed model.mzn data.dzn
```

### Timeout During Solving

**Cause**: Instance is too complex for default time limit

**Solutions**:

```bash
# Increase timeout (milliseconds)
minizinc --time-limit 600000 model.mzn data.dzn  # 10 minutes

# Use faster solver
minizinc --solver gecode model.mzn data.dzn

# Or use test script with custom limit
python Scripts/testing/run_battery_project_tests.py --time-limit 600000
```

## Debugging Steps

### General Approach

1. **Isolate the problem**:
   - Does setup work? Run `setup_and_validate.py`
   - Do tests pass? Run `test_initial_small_case.py`
   - Can model compile? Run `minizinc --compile-only`

2. **Check basics**:
   - Python version: `python --version`
   - MiniZinc version: `minizinc --version`
   - Available solvers: `minizinc --solvers`

3. **Common Fixes**:
   - Reinstall MiniZinc with PATH configuration
   - Update Python to 3.8+
   - Make scripts executable: `chmod +x *.sh`
   - Clear cache: `find . -type d -name __pycache__ -exec rm -r {} +`

## Getting Additional Help

- **Docs**: See [README.md](README.md) and [Docs/README.md](Docs/README.md)
- **GitHub Issues**: Report bugs with detailed error traces
- **Installation**: See [INSTALL.md](INSTALL.md)
- **Development**: See [DEVELOPMENT.md](DEVELOPMENT.md)

---

**Last Updated**: 2026-03-25
