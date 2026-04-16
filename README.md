# CLP-RCLP MiniZinc Lab Environment

[![Version](https://img.shields.io/badge/version-1.4.0-brightgreen?style=flat-square)](.)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](.)
[![Python](https://img.shields.io/badge/python-3.8+-yellow?style=flat-square)](.)
[![MiniZinc](https://img.shields.io/badge/minizinc-2.5+-ff69b4?style=flat-square)](.)

## Overview

Professional lab environment for research and optimization of the **Charging Location Problem (CLP)** and its robust extension **(RCLP)** for electric bus fleets.

This project includes:

- Mathematical models in MiniZinc (CLP and RCLP)
- Professional instance generation system (v3.0 - Working Pattern Replication)
- Complete automated testing suite with **multi-solver support**
- Enhanced test execution interface (Runner v1.4.0)
- Exhaustive technical documentation
- Varied datasets (Cork, synthetic, validated)

## Key Features

### 1. Mathematical Models

- **CLP**: Optimal charging station location under normal conditions
- **RCLP**: Robust version with resilience against failures

### 2. Automatic Generation System (v3.0 - Production Ready)

- Working Pattern Replication: Each bus visits every station exactly once
- 5 Route Patterns: Sequential, Reverse, Alternate-Odd/Even, Diagonal
- Smart Overconsumption: 1.5-1.8x for small networks, forcing strategic charging
- Guaranteed SAT: All test cases generate satisfiable instances instantly
- Automatic validation with MiniZinc (chuffed solver)

### 3. Test Runner Interface (v1.4.0 - Multi-Solver Support)

- Professional Tkinter GUI with dark/light theme support
- **Multiple solver selection** (chuffed, gecode, coin-bc, globalizer, cplex, gurobi)
- Solver information modal with capabilities and use cases
- Directory and file selectors for test instances
- Model selection (CLP/RCLP)
- Real-time execution monitoring
- Automatic result formatting (JSON and TXT)
- **Results organized by solver** for easy comparison
- Comprehensive tooltips for improved UX
- Centered window positioning on all screens
- Complete theme system with 27 design tokens

### 4. Datasets

- Cork City (Real): Irish case instances
- Noncity (Validated): Manually validated test cases
- Synthetic (Scalable): Procedurally generated instances
- Cork Variants (Single-cycle): Reduced Cork instances
- Battery Generated (User-created): Generated via Generator v3.0

## Quick Start

### Prerequisites

```bash
# Python 3.8+
python --version

# MiniZinc 2.5+
minizinc --version

# Download from https://www.minizinc.org/ if needed
```

### Initial Setup

```bash
# Validate configuration
python Scripts/setup/setup_and_validate.py

# Generate Cork variants (if necessary)
python Scripts/generation/create_cork_variants.py

# Run tests
bash Scripts/testing/test_generator.sh
```

### Generate New Instances

```bash
# Interactive GUI (recommended)
python Generator/generator.py

# Expected: SAT instance in ~1 second
```

### Run Tests with Runner

```bash
# Launch test execution interface
python Runner/runner.py

# Workflow:
# 1. Select test directory
# 2. Choose test instance (.dzn file)
# 3. Select model (CLP or RCLP)
# 4. Click "Run Test"
# 5. View results in JSON/TXT formats
```

### Execute Models Directly

```bash
# Quick test with validated instance
minizinc --solver chuffed Models/clp_model.mzn Data/Battery\ Own/noncity_5buses-8stations.dzn

# With generated instance
minizinc --solver chuffed Models/clp_model.mzn Data/Battery\ Generated/*.dzn
```

## Project Structure

```
CLP-RCLP Minizinc/
│
├── Models/                      # Mathematical models
│   ├── clp_model.mzn            # CLP Model (primary)
│   ├── rclp_model.mzn           # RCLP Model (robust)
│   └── archive/                 # Backup and experimental variants
│
├── Data/                        # Datasets
│   ├── Battery Project Integer/ # Cork (real instances)
│   ├── Battery Project Variant/ # Cork single-cycle variants
│   ├── Battery Generated/       # Generated instances
│   └── Battery Own/             # Noncity + synthetic
│
├── Scripts/                     # Organized scripts
│   ├── data-processing/         # Conversion and validation
│   ├── generation/              # Variant generation
│   ├── testing/                 # Test suite
│   ├── setup/                   # Setup and initialization
│   ├── utilities/               # Tools and diagnostics
│   └── README.md                # Scripts guide
│
├── Generator/                   # Generation system (v3.0)
│   ├── generator.py             # Interactive GUI
│   ├── config.py                # Configuration module
│   ├── core/                    # Core generation logic
│   ├── ui/                      # User interface components
│   ├── orchestrator.py          # Workflow coordinator
│   └── README.md                # Documentation
│
├── Runner/                      # Test execution interface (NEW)
│   ├── runner.py                # Entry point
│   ├── config.py                # UI colors and settings
│   ├── core/                    # Executor and result handler
│   ├── ui/                      # Tkinter interface
│   └── README.md                # Documentation
│
├── Docs/                        # Documentation
│   ├── generated-system/        # Generation system docs
│   ├── model/                   # Model documentation
│   ├── analysis/                # Analysis and diagnostics
│   └── README.md                # Documentation index
│
├── Tests/                       # Test results and output
│
├── README.md                    # This file
├── LICENSE                      # MIT License
├── CONTRIBUTING.md              # Contribution guide
├── CHANGELOG.md                 # Change history
├── VERSION                      # Version number
└── .gitignore                   # Git configuration
```

## Documentation

### Getting Started

- **[Generator/README.md](Generator/README.md)** - Generator v3.0 documentation
- **[Runner/README.md](Runner/README.md)** - Test Runner interface guide
- **[Scripts/README.md](Scripts/README.md)** - Scripts and utilities guide
- **[Docs/README.md](Docs/README.md)** - Central documentation index

### Technical Documentation

- **[Docs/model/](Docs/model/)** - Mathematical formulation
- **[Docs/model/PROJECT_SUMMARY.md](Docs/model/PROJECT_SUMMARY.md)** - Project summary
- **[Docs/analysis/](Docs/analysis/)** - Detailed analysis

## Typical Workflows

### Generate New Instances

```bash
python Generator/generator.py          # Interactive GUI
# or
python Scripts/generation/create_cork_variants.py  # Cork variants
```

### Validate Existing Instances

```bash
python Scripts/data-processing/validate_integer_dzn.py Data/Battery\ Generated/*.dzn
```

### Run Tests

```bash
bash Scripts/testing/test_generator.sh    # Main suite (recommended)
python Scripts/testing/run_battery_project_tests.py  # Battery tests
python Runner/runner.py                   # GUI test runner (v1.4.0)
```

### Check Available Solvers

```bash
python Scripts/solvers/check_solvers.py    # System solver verification
```

### Test Multiple Solvers

```bash
python Scripts/solvers/test_multiple_solvers.py Data/Battery\ Own/instance.dzn CLP
```

### Diagnose Issues

```bash
python Scripts/setup/setup_and_validate.py  # Validate environment
bash Scripts/utilities/diagnose_cork.sh    # Diagnose Cork
```

## Datasets

| Dataset       | Origin         | Instances | Status   | Usage                 |
| ------------- | -------------- | --------- | -------- | --------------------- |
| Cork          | Real (Ireland) | 182+      | Complex  | RCLP or single cycles |
| Cork Variants | Reduced        | 5         | Feasible | Testing               |
| Noncity       | Validated      | 10+       | Feasible | Recommended           |
| Synthetic     | Generated      | Variable  | Feasible | Recommended           |
| Generated     | Gen. System    | 3+        | Feasible | Recommended           |

## Testing Status

Generator v3.0 Results:

- 2 buses, 4 stations: SAT in attempt 1 [PASS]
- 3 buses, 5 stations: SAT in attempt 1 [PASS]
- 5 buses, 8 stations: SAT in attempt 1 [PASS]

System Performance:

- Success Rate: 100%
- Average Time to SAT: <1 second
- Average Attempts: 1.0

## Tools and Dependencies

| Tool     | Version     | Purpose                    |
| -------- | ----------- | -------------------------- |
| MiniZinc | 2.5+        | Constraint modeling        |
| Python   | 3.8+        | Utility scripts and Runner |
| Bash     | Linux/macOS | Automation scripts         |
| Git      | Any         | Version control            |

### Supported Solvers

- **Chuffed** (Default) - Fast constraint solver, recommended
- **Gecode** - General-purpose constraint programming
- **COIN-BC** - Linear/mixed-integer programming
- **OR-Tools CP-SAT** - Google's modern CP solver
- **CPLEX** (Commercial) - Industry-leading optimizer
- **Gurobi** (Commercial) - Requires valid license

## Key Concepts

### CLP (Charging Location Problem)

Base constraint programming problem that determines optimal charging station location, minimizing station count while guaranteeing operational feasibility.

### RCLP (Robust CLP)

Robust extension that adds resilience against potential system failures.

### Scaling (x10)

All values are scaled by 10 to use integer arithmetic in MiniZinc, improving numerical precision and reliability.

### Feasibility

An instance is "feasible" if a valid solution exists where all buses complete their routes respecting all constraints.

## FAQ

### Where do I start?

1. Run `bash Scripts/testing/test_generator.sh` first
2. Review [Docs/README.md](Docs/README.md) for documentation
3. Use `python Generator/generator.py` to create instances
4. Execute tests with `python Runner/runner.py`

### Why is Cork infeasible?

Cork contains 13-14 daily cycles (~400-500 stops) with ~1700 kWh consumption vs 80 kWh usable capacity. Requires 3+ RCLP models or reduction to single cycles.

### How do I generate custom instances?

Use `python Generator/generator.py` (GUI) or modify `Scripts/generation/` for automation.

### How do I run tests?

Use `python Runner/runner.py` for GUI interface or `minizinc --solver chuffed Models/clp_model.mzn Data/.../*.dzn` for command line.

### Where are results stored?

Test results auto-save to `Tests/Output/{DirectoryName}/` in JSON and TXT formats.

## Contributing

Contributions are welcome! Please:

1. Read [CONTRIBUTING.md](CONTRIBUTING.md)
2. Fork the repository
3. Create a branch: `git checkout -b feature/your-feature`
4. Make descriptive commits
5. Submit a Pull Request with clear description

## License

This project is licensed under MIT. See [LICENSE](LICENSE) for details.

## Authors

- **AVISPA Research Team** - Main research
- **Andrey Quiceño** - Development and maintenance

## Support

- Report Bugs: [GitHub Issues](../../issues)
- Questions: See [Docs/README.md](Docs/README.md)
- Documentation: [Docs/](Docs/)

## Roadmap

- [ ] Batch generation mode
- [ ] Custom parameter profiles
- [ ] Improved CLI mode
- [ ] Real-time visualization
- [ ] Benchmark suite integration
- [ ] REST API

## Project Statistics

- Lines of Code: 2500+
- Documentation: 3500+ lines
- Automated Tests: 7 test suites
- Datasets: 200+ instances
- Validated Instances: 18+

---

Version: 1.4.0
Last Updated: April 2026
Status: Production Ready - Multi-Solver Support & Enhanced UI v1.4.0

## Technical Note

All numeric parameters are scaled x10 to use integer arithmetic:

- Time: `4200` = 420.0 minutes = 7:00 AM
- Energy: `250` = 25.0 kWh
- Capacity: `1000` = 100.0 kWh

For more details, see [Docs/](Docs/) and [Runner/README.md](Runner/README.md).
