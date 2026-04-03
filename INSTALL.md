# Installation Guide

Complete guide for installing and setting up the CLP-RCLP MiniZinc Lab Environment.

## Prerequisites

### Minimum System Requirements

- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+, Debian 10+)
- **RAM**: 4GB minimum (8GB recommended)
- **Disk Space**: 2GB for MiniZinc, models, and sample data
- **Python**: 3.8 or higher
- **Internet**: Required for downloading MiniZinc

## Step-by-Step Installation

### 1. Install Python

#### Windows
```bash
# Download from https://www.python.org/downloads/
# Run installer and ensure "Add Python to PATH" is checked
python --version  # Verify (should be 3.8+)
```

#### macOS
```bash
brew install python3
python3 --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip
python3 --version
```

### 2. Install MiniZinc

#### Windows
1. Download from https://www.minizinc.org/software.html
2. Run installer (accepts default installations)
3. Verify installation:
   ```bash
   minizinc --version
   minizinc --solvers  # Should list Chuffed, Gecode, etc.
   ```

#### macOS
```bash
brew install minizinc
minizinc --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt install minizinc
minizinc --version
```

### 3. Clone Repository

```bash
git clone https://github.com/AndreyQuicenoC/CLP-RCLP_Minizinc_Lab_Enviroment.git
cd CLP-RCLP\ Minizinc\ Lab\ Enviroment
```

### 4. Verify Installation

Run the validation script:

```bash
python Scripts/setup/setup_and_validate.py
```

Expected output:
```
✓ Python 3.8+ found
✓ MiniZinc 2.5+ found
✓ Project structure valid
✓ Data directories exist
✓ Ready to use!
```

## Troubleshooting Installation

### MiniZinc Not Found

**Windows**:
- Add MiniZinc to PATH environment variable
- Restart terminal after installation

```bash
# Check PATH
echo %PATH%  # Windows CMD
# Find MiniZinc installation, usually: C:\Program Files\MiniZinc\
```

**macOS/Linux**:
```bash
# Check if MiniZinc is installed
which minizinc

# If not found, install via package manager
brew install minizinc       # macOS
sudo apt install minizinc   # Ubuntu/Debian
```

### Python Version Too Old

```bash
# Check current version
python --version  # or python3 --version

# Update Python
# Windows: Download new version from python.org
# macOS: brew install python@3.10 && brew link python@3.10
# Linux: sudo apt install python3.10
```

### Permission Denied (Linux/macOS)

```bash
# Make scripts executable
chmod +x Scripts/**/*.sh
chmod +x Scripts/**/*.py
```

### Module Not Found Errors

```bash
# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# Install required packages
pip install --upgrade pip
```

## Minimal Setup (Quick Start)

For testing only:

```bash
# 1. Install Python 3.8+
# 2. Install MiniZinc 2.5+
# 3. Clone repository
git clone https://github.com/AndreyQuicenoC/CLP-RCLP_Minizinc_Lab_Enviroment.git

# 4. Test with a simple case
minizinc --solver chuffed Models/clp_model.mzn Data/Battery\ Own/noncity_5buses-8stations.dzn
```

## Development Setup

For contributing to the project:

```bash
# 1. Follow all steps above
# 2. Create development environment
python -m venv venv-dev

# 3. Install development tools
pip install pytest pytest-cov black flake8

# 4. Verify setup
pytest Scripts/testing/test_initial_small_case.py
```

## Environment Variables

Optional configuration via environment variables:

```bash
# Specify MiniZinc solver
export MINIZINC_DEFAULT_SOLVER=chuffed

# Increase verbosity for debugging
export DEBUG=1

# Set data directory location
export CLP_DATA_DIR=./Data
```

## Network Requirements

Some operations require internet connectivity:

- Initial MiniZinc download: ~500MB
- Solver downloads: ~100-200MB each
- GitHub clone: ~50MB

After installation, most operations work offline.

## Uninstallation

### Remove MiniZinc

**Windows**:
- Control Panel → Programs → Uninstall a Program → MiniZinc

**macOS**:
```bash
brew uninstall minizinc
```

**Linux**:
```bash
sudo apt remove minizinc
```

### Remove Project

```bash
rm -rf CLP-RCLP\ Minizinc\ Lab\ Enviroment
```

## Getting Help

If installation fails:

1. Check output of `setup_and_validate.py`
2. Verify MiniZinc with: `minizinc --version`
3. Verify Python with: `python --version`
4. Check [README.md](README.md) for additional context
5. Open an issue on GitHub with error messages

---

**Last Updated**: 2026-03-25
**Tested On**: Python 3.8-3.11, MiniZinc 2.5-2.9
