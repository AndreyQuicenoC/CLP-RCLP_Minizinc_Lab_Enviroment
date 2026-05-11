# CPLEX Installation and Configuration Guide

Complete guide for installing and configuring IBM CPLEX optimization solver with MiniZinc.

## System Requirements

### Prerequisites
- **MiniZinc**: 2.5.0+ (see [MiniZinc Installation Guide](./minizinc_installation.md))
- **Disk Space**: 2.5 GB
- **RAM**: 4 GB minimum
- **License**: Academic or Commercial (see License Setup section)

### Supported Platforms
- Windows (64-bit)
- macOS (Intel and Apple Silicon)
- Linux (Ubuntu, CentOS, etc.)

### Note
CPLEX is a large optimization suite; installation requires 2.5 GB disk space and a valid IBM account.

## Installation Steps

### Step 1: Obtain CPLEX

1. Visit https://www.ibm.com/products/ilog-cplex-optimization-studio
2. For **Academic License**:
   - Visit https://www.ibm.com/academic/topic/cplex
   - Register with academic email (.edu, .org, etc.)
   - Download CPLEX Optimization Studio
3. For **Commercial License**:
   - Contact IBM sales
   - Receive download link and license key via email

### Step 2: Install CPLEX

#### Windows

1. Run installer: `CPLEX_Studio<version>.exe`
2. Select installation directory (recommended: `C:\Program Files\IBM\ILOG\CPLEX_Studio<version>`)
3. Note the installation path (needed for CPLEX_HOME)
4. Select installation type: **Full installation** (includes all components)
5. Complete installation wizard
6. Restart Windows

#### macOS

```bash
# Download the installer
# Navigate to Downloads and run
cd ~/Downloads

# Run installer (replace with actual version)
./CPLEX_Studio<version>_osx.bin

# Follow the graphical installer
# Default installation: /Applications/CPLEX_Studio<version>
```

#### Linux (Ubuntu/Debian)

```bash
# Download the installer
# Make executable
chmod +x CPLEX_Studio<version>_linux-x86-64.bin

# Run installer
./CPLEX_Studio<version>_linux-x86-64.bin

# Follow the installer wizard
# Recommended installation: /opt/ibm/CPLEX_Studio<version>

# Or use package manager if available
# Add IBM repository and install via apt
```

### Step 3: Set Environment Variable

#### Windows PowerShell (Admin)

```powershell
# Set CPLEX_HOME
[Environment]::SetEnvironmentVariable("CPLEX_HOME", "C:\Program Files\IBM\ILOG\CPLEX_Studio<version>\cplex", "User")

# Verify
$env:CPLEX_HOME

# Restart terminal/IDE
```

#### macOS/Linux Bash

```bash
# Add to ~/.bash_profile or ~/.zshrc
export CPLEX_HOME="/Applications/CPLEX_Studio<version>/cplex"
# Or for Linux:
export CPLEX_HOME="/opt/ibm/CPLEX_Studio<version>/cplex"

# Add CPLEX bin directory to PATH
export PATH="$CPLEX_HOME/bin/x86-64_linux:$PATH"

# Reload shell
source ~/.bash_profile  # or source ~/.zshrc

# Verify
echo $CPLEX_HOME
```

### Step 4: Verify Installation

```bash
# Check CPLEX executable
cplex -c "quit"

# Check library location
which cplex  # macOS/Linux
where cplex  # Windows

# Should return path to CPLEX executable
```

## License Setup

### Option 1: Free Academic License (Recommended)

**Eligibility**: Faculty and students at accredited academic institutions

1. Visit https://www.ibm.com/academic/topic/cplex
2. Sign in with IBM account (create if needed)
3. Select your academic institution
4. Verify affiliation
5. Download CPLEX Studio installer and license file
6. Place license file in home directory:
   - Windows: `C:\Users\<username>\.cplex\cplex.license`
   - macOS/Linux: `~/.cplex/cplex.license`

7. Create directory if needed:
   ```bash
   # macOS/Linux
   mkdir -p ~/.cplex
   
   # Windows PowerShell
   New-Item -ItemType Directory -Path $env:USERPROFILE\.cplex -Force
   ```

8. Verify:
   ```bash
   cplex -c "quit"
   ```

### Option 2: Free Trial License

**Validity**: 90 days

1. Visit https://www.ibm.com/cloud/cplex/free-trial
2. Register account
3. Download installer and trial license
4. Place license file in home directory (same as Academic)

### Option 3: Commercial License

1. Purchase license from IBM Sales
2. Receive license file via email
3. Place in home directory as described above
4. Or use Online Licensing with access key

## Configuration with MiniZinc

### Automatic Detection

Once CPLEX is installed and licensed, MiniZinc should detect it automatically:

```bash
# Check if CPLEX is recognized
minizinc -h | grep -i cplex

# Expected output:
# CPLEX <version> (...)
```

### Manual DLL Specification (Windows)

If automatic detection fails:

```bash
# Find CPLEX libraries
Get-ChildItem -Path "C:\Program Files\IBM\ILOG\CPLEX_Studio*" -Recurse -Include "cplex*.dll" | Select-Object FullName

# Run with explicit path
minizinc --cplex-dll "C:\Program Files\IBM\ILOG\CPLEX_Studio<version>\cplex\bin\x64_win64\cplex.dll" --solver cplex Models/clp_model.mzn Data/instance.dzn
```

## Verification

### Test 1: Check License

```bash
cplex -c "quit"
```

Expected output:
```
CPLEX Interactive Optimizer
Version <version>
...
Academic License
```

### Test 2: MiniZinc Integration

```bash
# Check if CPLEX shows in solvers
python Scripts/solvers/check_solvers.py

# Expected: CPLEX should show as available
```

### Test 3: Actual Execution

```bash
# Run diagnostics
python Scripts/solvers/test_cplex.py Data/Battery\ Own/noncity_5buses-8stations.dzn

# Expected output:
# [CPLEX FOUND] CPLEX installation found and license valid
# Status: working
```

### Test 4: Performance Test

```bash
# Compare with other solvers
python Scripts/solvers/diagnose_solvers.py Data/Battery\ Own/noncity_5buses-8stations.dzn

# CPLEX should appear in working solvers list
```

## Troubleshooting

### Issue: "Cannot find CPLEX"

**Cause**: CPLEX not in PATH or CPLEX_HOME not set

**Solution**:
```bash
# Verify CPLEX_HOME
echo $CPLEX_HOME  # macOS/Linux
echo %CPLEX_HOME%  # Windows

# If empty, set environment variable (see Step 3)
# Restart terminal/IDE
# Verify again with: cplex -c "quit"
```

### Issue: "CPLEX license not found"

**Cause**: License file not in expected location or expired

**Solution**:
1. Verify license file location:
   - Windows: `C:\Users\<username>\.cplex\cplex.license`
   - macOS/Linux: `~/.cplex/cplex.license`

2. Check license validity:
   ```bash
   cplex -c "quit"
   ```

3. If expired or invalid:
   - Renew at https://www.ibm.com/academic/topic/cplex
   - Request new academic license
   - Download and place new license file

### Issue: "CPLEX DLL error" (Windows)

**Cause**: DLL path incorrect or CPLEX bin directory not in PATH

**Solution**:
```bash
# Find the correct DLL
dir "C:\Program Files\IBM\ILOG\CPLEX_Studio*" /s /b | findstr "\.dll"

# Add bin directory to PATH
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Program Files\IBM\ILOG\CPLEX_Studio<version>\cplex\bin\x64_win64", "User")

# Restart terminal
```

### Issue: MiniZinc doesn't recognize CPLEX

**Cause**: MiniZinc needs rebuild after CPLEX installation

**Solution**:
```bash
# Reinstall MiniZinc or update environment variables
# Then restart IDE/terminal completely
# Verify with: minizinc -h | grep cplex
```

### Issue: "Academic license expired"

**Cause**: Annual license renewal required

**Solution**:
1. Visit https://www.ibm.com/academic/topic/cplex
2. Login and renew license
3. Download new license file
4. Replace old license file in ~/.cplex/ or C:\Users\<username>\.cplex\
5. No reinstallation needed

## Using CPLEX in Runner

### Via GUI

1. Launch Runner: `python Runner/runner.py`
2. Select test instance and model
3. Choose **CPLEX** from solver dropdown
4. Results automatically organized in `Tests/Output/{Battery}/CPLEX/`

### Via Command Line

```bash
python Scripts/solvers/test_multiple_solvers.py Data/Battery\ Own/instance.dzn CLP cplex
```

## Performance Optimization

### For Large Problems

CPLEX configuration parameters (advanced):

```bash
# Time limit (seconds)
minizinc --cplex-flags "timelimit=300" --solver cplex ...

# Thread count
minizinc --cplex-flags "threads=4" --solver cplex ...

# Node limit (branch-and-bound exploration)
minizinc --cplex-flags "nodelim=100000" --solver cplex ...

# Optimality tolerance (gap in percentage)
minizinc --cplex-flags "epgap=0.01" --solver cplex ...

# Focus on finding good solutions vs. proving optimality
minizinc --cplex-flags "workdir=/tmp/cplex" --solver cplex ...
```

### Memory Management

For very large problems with limited memory:

```bash
# Reduce workarea (memory limit in MB)
minizinc --cplex-flags "workarea=1000" --solver cplex ...

# Use disk for node file instead of memory
minizinc --cplex-flags "treememory=500" --solver cplex ...
```

## Support

### Official Resources
- Documentation: https://www.ibm.com/docs/en/icos
- Academic Program: https://www.ibm.com/academic/topic/cplex
- Community: https://www.ibm.com/community/cplex
- IBM Support: https://www.ibm.com/support/

### CLP-RCLP Specific

```bash
# Diagnose CPLEX-specific issues
python Scripts/solvers/test_cplex.py Data/Battery\ Own/instance.dzn

# Check all solvers
python Scripts/solvers/diagnose_solvers.py Data/Battery\ Own/instance.dzn
```

## Common Questions

### Q: Is CPLEX free for academic use?
**A**: Yes. Qualified students and faculty can use CPLEX free of charge through the IBM Academic Initiative. Register at https://www.ibm.com/academic/topic/cplex

### Q: Can I use CPLEX without a license?
**A**: No. CPLEX requires a valid license (academic, trial, or commercial). The solver will not run without one.

### Q: How long does installation take?
**A**: Typically 10-15 minutes for installation, plus 10-30 minutes for license setup (acquiring and placing the license file).

### Q: Can I use CPLEX on Linux?
**A**: Yes. CPLEX is fully supported on Linux. Follow the Linux installation steps above.

### Q: What's the difference between CPLEX and Gurobi?
**A**: Both are commercial MIP/LP solvers. CPLEX is IBM's offering with broad industry adoption. Gurobi is newer with good performance. For academic use, both are free. Test both with your instances to see which performs better.

---

**Last Updated**: April 2026  
**CPLEX Version**: 22.1+  
**MiniZinc Version**: 2.5.0+  
**Authors**: Andrey Quiceno and Juan Francesco García (AVISPA Team)
