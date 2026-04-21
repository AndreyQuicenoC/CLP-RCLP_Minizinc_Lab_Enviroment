# Installation and Configuration Guide

Complete guides for setting up MiniZinc, Gurobi, and CPLEX solvers for the CLP-RCLP environment.

## Quick Start

### 1. MiniZinc (Required)
MiniZinc is required for all solver functionality.

**Installation**: 5 minutes  
**Configuration**: 2 minutes  
**Status**: [MiniZinc Installation Guide](./minizinc_installation.md)

### 2. Gurobi (Optional - Commercial)
Gurobi provides cutting-edge optimization performance.

**Installation**: 10 minutes  
**Configuration**: 5 minutes  
**License Setup**: 10-30 minutes  
**Status**: [Gurobi Installation Guide](./gurobi_installation.md)

### 3. CPLEX (Optional - Commercial)
IBM's CPLEX is an industry-leading optimizer.

**Installation**: 10 minutes  
**Configuration**: 5 minutes  
**License Setup**: 10-30 minutes  
**Status**: [CPLEX Installation Guide](./cplex_installation.md)

## Solver Status Summary

| Solver | Type | Status | Installation Time |
|--------|------|--------|-------------------|
| Chuffed | Open-source | Included with MiniZinc | Built-in |
| Gecode | Open-source | Included with MiniZinc | Built-in |
| COIN-BC | Open-source | Included with MiniZinc | Built-in |
| OR-Tools CP-SAT | Open-source | Included with MiniZinc | Built-in |
| CPLEX | Commercial | Optional, requires license | 10 min + license |
| Gurobi | Commercial | Optional, requires license | 10 min + license |

## Verification

After installation, verify your setup:

```bash
# Check MiniZinc
minizinc --version

# Check available solvers
python Scripts/solvers/check_solvers.py

# Run diagnostics
python Scripts/solvers/diagnose_solvers.py Data/Battery\ Own/noncity_5buses-8stations.dzn
```

## Troubleshooting

### Common Issues

**1. MiniZinc not found**
```
Error: command 'minizinc' not found
Solution: Ensure MiniZinc is in PATH
```
→ See [MiniZinc Installation Guide](./minizinc_installation.md)

**2. Gurobi DLL error**
```
Error: cannot load gurobi dll, specify --gurobi-dll
Solution: Set GUROBI_HOME or install valid license
```
→ See [Gurobi Installation Guide](./gurobi_installation.md)

**3. Gurobi no license found**
```
Error: No Gurobi license found
Solution: Install academic or commercial license
```
→ See [Gurobi License Setup](./gurobi_installation.md#license-setup)

**4. CPLEX not recognized**
```
Error: CPLEX solver not found
Solution: Install CPLEX or add to PATH
```
→ See [CPLEX Installation Guide](./cplex_installation.md)

## Next Steps

1. Start with [MiniZinc Installation](./minizinc_installation.md)
2. Optionally configure [Gurobi](./gurobi_installation.md) or [CPLEX](./cplex_installation.md)
3. Verify installation with verification commands above
4. Start using the Runner: `python Runner/runner.py`

---

**Last Updated**: April 2026  
**Version**: 1.4.0
