# Gurobi Installation and Configuration Guide

Complete guide for installing and configuring Gurobi optimization solver with MiniZinc.

## System Requirements

### Prerequisites
- **MiniZinc**: 2.5.0+ (see [MiniZinc Installation Guide](./minizinc_installation.md))
- **Disk Space**: 1.5 GB
- **RAM**: 2 GB minimum
- **License**: Academic or Commercial (see License Setup section)

### Supported Platforms
- Windows (64-bit)
- macOS (Intel and Apple Silicon)
- Linux (Ubuntu, CentOS, etc.)

## Installation Steps

### Step 1: Download Gurobi

1. Visit https://www.gurobi.com/download/gurobi-software/
2. Select your platform and version (latest stable)
3. Download installer for your OS

**Note**: Installation requires registration or login

### Step 2: Install Gurobi

#### Windows

1. Run installer: `Gurobi-<version>-win64.exe`
2. Choose installation directory (recommended: `C:\gurobi<version>\win64`)
3. Note the installation path (needed for GUROBI_HOME)
4. Complete installation

#### macOS

```bash
# Download the .pkg file
# Run installer
open Gurobi-<version>-macos_universal2.pkg

# Or install via terminal
sudo installer -pkg Gurobi-<version>-macos_universal2.pkg -target /
```

#### Linux (Ubuntu/Debian)

```bash
# Download and extract
tar xvfz gurobi<version>_linux64.tar.gz

# Move to /opt or preferred location
sudo mv gurobi<version>/linux64 /opt/gurobi

# Set permissions
sudo chown -R $USER:$USER /opt/gurobi
```

### Step 3: Set Environment Variable

#### Windows PowerShell (Admin)

```powershell
# Set GUROBI_HOME
[Environment]::SetEnvironmentVariable("GUROBI_HOME", "C:\gurobi<version>\win64", "User")

# Verify
$env:GUROBI_HOME

# Restart terminal/IDE
```

#### macOS/Linux Bash

```bash
# Add to ~/.bash_profile or ~/.zshrc
export GUROBI_HOME="/opt/gurobi/linux64"
# Or for macOS
export GUROBI_HOME="/Library/gurobi<version>/macos_universal2"

# Reload shell
source ~/.bash_profile  # or ~/.zshrc

# Verify
echo $GUROBI_HOME
```

### Step 4: Verify Installation

```bash
# Check Gurobi CLI
gurobi_cl --version

# Check binary location
which gurobi  # macOS/Linux
where gurobi  # Windows
```

## License Setup

### Option 1: Free Academic License (Recommended)

**Eligibility**: Faculty and students at academic institutions

1. Visit https://www.gurobi.com/academia/academic-program-and-licenses/
2. Click "Request Academic License"
3. Select institution and agree to terms
4. Download license file (`gurobi.lic`)
5. Place in home directory:
   - Windows: `C:\Users\<username>\gurobi.lic`
   - macOS/Linux: `~/.gurobi/gurobi.lic`

6. Verify:
   ```bash
   gurobi_cl --version
   ```

### Option 2: Free Trial License

**Validity**: 14 days

1. Visit https://www.gurobi.com/free-trial/
2. Register account
3. Download trial license
4. Place license file in home directory (same as Academic)

### Option 3: Commercial License

1. Purchase license from https://www.gurobi.com/pricing/
2. Receive license file via email
3. Place in home directory as described above
4. Or use Cloud license with access keys

## Configuration with MiniZinc

### Automatic Detection

Once Gurobi is installed and licensed, MiniZinc should detect it automatically:

```bash
# Check if Gurobi is recognized
minizinc -h | grep -i gurobi

# Expected output:
# Gurobi <version> (...)
```

### Manual DLL Specification (Windows)

If automatic detection fails:

```bash
minizinc --gurobi-dll "C:\gurobi<version>\win64\bin\gurobi<major_version>.dll" --solver gurobi Models/clp_model.mzn Data/instance.dzn
```

**Find your DLL**:
```bash
# Windows PowerShell
Get-ChildItem -Path "C:\gurobi*" -Recurse -Include "gurobi*.dll" | Select-Object FullName

# macOS/Linux
find ~/gurobi* -name "libgurobi*.so"
```

## Verification

### Test 1: Check License

```bash
gurobi_cl --version
```

Expected:
```
Gurobi 11.x.x (or higher)
Gurobi Interactive Shell (...)
License ID: XXXXX (yours)
```

### Test 2: MiniZinc Integration

```bash
# Check if Gurobi shows in solvers
python Scripts/solvers/check_solvers.py

# Expected: Gurobi should show as available
```

### Test 3: Actual Execution

```bash
# Run diagnostics
python Scripts/solvers/test_gurobi.py Data/Battery\ Own/noncity_5buses-8stations.dzn

# Expected output:
# [GUROBI FOUND] Gurobi installation found and license valid
# Status: working
```

### Test 4: Performance Test

```bash
# Compare with other solvers
python Scripts/solvers/diagnose_solvers.py Data/Battery\ Own/noncity_5buses-8stations.dzn

# Gurobi should appear in working solvers list
```

## Troubleshooting

### Issue: "Cannot load gurobi dll"

**Cause**: DLL path not found

**Solution**:
```bash
# Find the correct DLL path
# Windows:
dir C:\gurobi* /s /b | findstr "\.dll"

# macOS/Linux:
find ~ -name "gurobi*.so" 2>/dev/null
```

Then use explicit path:
```bash
minizinc --gurobi-dll "C:\gurobi1301\win64\bin\gurobi130.dll" --solver gurobi Models/clp_model.mzn Data/instance.dzn
```

### Issue: "No Gurobi license found"

**Cause**: License file not in expected location or expired

**Solution**:
1. Verify license file location:
   - Windows: `C:\Users\<username>\gurobi.lic`
   - macOS/Linux: `~/.gurobi/gurobi.lic` or `~/gurobi.lic`

2. Check license validity:
   ```bash
   gurobi_cl --version
   ```

3. If expired or invalid:
   - Renew at https://www.gurobi.com/
   - Request new academic license
   - Download and place new license file

### Issue: "Gurobi not in PATH"

**Cause**: Installation directory not in system PATH

**Solution**:
1. Set GUROBI_HOME (see Step 3 above)
2. Ensure bin directory is in PATH
3. Restart terminal/IDE

### Issue: MiniZinc doesn't recognize Gurobi

**Cause**: MiniZinc needs rebuild after Gurobi installation

**Solution**:
```bash
# Reinstall MiniZinc or update environment variables
# Then restart IDE/terminal completely
# Test again
```

## Using Gurobi in Runner

### Via GUI

1. Launch Runner: `python Runner/runner.py`
2. Select test instance and model
3. Choose **Gurobi** from solver dropdown
4. Results automatically organized in `Tests/Output/{Battery}/Gurobi/`

### Via Command Line

```bash
python Scripts/solvers/test_multiple_solvers.py Data/Battery\ Own/instance.dzn CLP gurobi
```

## Performance Optimization

### For Large Problems

Gurobi configuration parameters (advanced):

```bash
# Time limit (seconds)
minizinc --gurobi-flags "TimeLimit=300" --solver gurobi ...

# Thread count
minizinc --gurobi-flags "Threads=4" --solver gurobi ...

# MIP focus (optimality vs finding solutions)
minizinc --gurobi-flags "MIPFocus=2" --solver gurobi ...
```

## Support

### Official Resources
- Documentation: https://www.gurobi.com/documentation/
- Licensing: https://www.gurobi.com/support/
- Community: https://groups.google.com/forum/#!forum/gurobi

### CLP-RCLP Specific

```bash
# Diagnose Gurobi-specific issues
python Scripts/solvers/test_gurobi.py Data/Battery\ Own/instance.dzn

# Check all solvers
python Scripts/solvers/diagnose_solvers.py Data/Battery\ Own/instance.dzn
```

---

**Last Updated**: April 2026  
**Gurobi Version**: 11.0+  
**MiniZinc Version**: 2.5.0+  
**Authors**: Andrey Quiceno and Juan Francesco García (AVISPA Team)
