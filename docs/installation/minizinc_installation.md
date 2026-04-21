# MiniZinc Installation Guide

MiniZinc is the constraint modeling language and solver platform required for all functionality in the CLP-RCLP environment.

## System Requirements

### Minimum Specifications
- **OS**: Windows 10/11, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Disk Space**: 500 MB
- **RAM**: 2 GB minimum (4 GB recommended)
- **Internet**: Required for download and validation

### Supported Platforms
- Windows (64-bit recommended)
- macOS (Intel and Apple Silicon M1+)
- Linux (Ubuntu, Debian, Fedora, etc.)

## Installation

### Windows

#### Method 1: Installer (Recommended)
1. Download MiniZinc from https://www.minizinc.org/download.html
2. Select version: **Latest Stable Release** (2.5.0 or higher)
3. Run installer: `MiniZincIDE-<version>-bundled.exe`
4. Follow installation wizard
5. Choose "Add MiniZinc to PATH" when prompted
6. Click "Finish"

#### Method 2: Portable/Standalone
1. Download portable version from https://www.minizinc.org/download.html
2. Extract ZIP file to desired location (e.g., `C:\Program Files\MiniZinc`)
3. Add to PATH manually:
   - Right-click "This PC" → Properties
   - Advanced system settings → Environment variables
   - Edit PATH and add MiniZinc `bin` directory

### macOS

#### Using Homebrew (Easiest)
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install MiniZinc
brew install minizinc
```

#### Direct Installation
1. Download `.dmg` file from https://www.minizinc.org/download.html
2. Open DMG and drag MiniZinc to Applications folder
3. Open Terminal and verify: `minizinc --version`

### Linux (Ubuntu/Debian)

```bash
# Add repository
sudo apt-add-repository ppa:minizinc/minizinc-releases

# Update package list
sudo apt update

# Install MiniZinc
sudo apt install minizinc

# Verify installation
minizinc --version
```

### Linux (Fedora/RHEL)

```bash
# Download latest RPM from https://www.minizinc.org/download.html
# Then install
sudo dnf install minizinc-<version>.x86_64.rpm

# Verify installation
minizinc --version
```

## Verification

### Step 1: Check Version
```bash
minizinc --version
```

Expected output:
```
MiniZinc to FlatZinc converter, version 2.9.4 (or higher)
Copyright (C) 2014-2025 Monash University
```

### Step 2: Check Included Solvers
```bash
minizinc -h | grep -i solver
```

Expected output should list:
- Chuffed
- Gecode
- COIN-BC
- OR-Tools CP-SAT

### Step 3: Test Execution
```bash
# From project root directory
minizinc --solver chuffed Models/clp_model.mzn Data/Battery\ Own/noncity_5buses-8stations.dzn
```

Expected output:
```
Estaciones instaladas: [...]
Total estaciones: N
Desviacion total: N
```

## Configuration

### PATH Setup (If Needed)

#### Windows
```powershell
# Open PowerShell as Administrator
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\MiniZinc\bin", "User")

# Restart your terminal/IDE
```

#### macOS/Linux
```bash
# Add to ~/.bash_profile or ~/.zshrc
export PATH="/path/to/minizinc/bin:$PATH"

# Reload shell
source ~/.bash_profile  # or source ~/.zshrc
```

## Verify CLP-RCLP Setup

From project root:

```bash
# Verify all solvers available
python Scripts/solvers/check_solvers.py

# Run system diagnostics
python Scripts/solvers/diagnose_solvers.py Data/Battery\ Own/noncity_5buses-8stations.dzn

# Launch Runner
python Runner/runner.py
```

## Troubleshooting

### Issue: "minizinc command not found"
**Cause**: MiniZinc not in PATH

**Solution**:
1. Verify installation: Check if MiniZinc exists in Program Files
2. Add to PATH: Follow PATH Setup section above
3. Restart terminal/IDE
4. Test: `minizinc --version`

### Issue: "Solver not available"
**Cause**: Installed version missing solvers

**Solution**:
1. Ensure version >= 2.5.0: `minizinc --version`
2. Download latest from https://www.minizinc.org/download.html
3. Reinstall with all bundled solvers

### Issue: Slow execution on first run
**Cause**: MiniZinc compiling solvers on first use

**Solution**: Normal behavior. Subsequent runs are faster.

## Optional: Commercial Solvers

### Next Steps

After verifying MiniZinc, optionally configure:
- [Gurobi Installation Guide](./gurobi_installation.md)
- [CPLEX Installation Guide](./cplex_installation.md)

## Support

### Documentation
- Official: https://www.minizinc.org/documentation.html
- CLP-RCLP: See `Docs/` directory

### Getting Help
```bash
# Check command options
minizinc --help

# Check solver options
minizinc --solver chuffed --help
```

---

**Last Updated**: April 2026  
**MiniZinc Version**: 2.5.0+  
**Authors**: Andrey Quiceno and Juan Francesco García (AVISPA Team)
