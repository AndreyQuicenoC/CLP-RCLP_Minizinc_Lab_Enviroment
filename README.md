# CLP-RCLP MiniZinc Lab Environment

![Version](https://img.shields.io/badge/version-3.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![MiniZinc](https://img.shields.io/badge/minizinc-2.5+-blue)
![Generator](https://img.shields.io/badge/generator-v3.0_working_pattern-brightgreen)

## 📋 Overview

Professional lab environment for research and optimization of the **Charging Location Problem (CLP)** and its robust extension **(RCLP)** for electric bus fleets.

This project includes:
- ✅ Mathematical models in MiniZinc (CLP and RCLP)
- ✅ Professional instance generation system
- ✅ Complete automated testing suite
- ✅ Exhaustive technical documentation
- ✅ Varied datasets (Cork, synthetic, validated)

## 🎯 Key Features

### 1. Mathematical Models
- **CLP**: Optimal charging station location under normal conditions
- **RCLP**: Robust version with resilience against failures

### 2. Automatic Generation System (v3.0 - Production Ready)
- **Working Pattern Replication**: Each bus visits every station exactly once
- **5 Route Patterns**: Sequential, Reverse, Alternate-Odd/Even, Diagonal
- **Smart Overconsumption**: 1.5-1.8x for small networks, forcing strategic charging
- **Instant SAT**: All test cases generate satisfiable instances in 1 attempt
- **Automatic validation** with MiniZinc (chuffed solver)

### 3. Datasets
- **Cork City** (Real): Irish case instances
- **Noncity** (Validated): Manually validated test cases
- **Synthetic** (Scalable): Procedurally generated instances
- **Cork Variants** (Single-cycle): Reduced Cork instances

### 4. Testing Suite
- 7 system-wide tests
- Preliminary and validation tests
- Detailed reports with statistics
- 100% pass rate in release

## 🚀 Quick Start

### 1️⃣ Prerequisites

```bash
# Python 3.8+
python --version

# MiniZinc 2.5+
minizinc --version

# If not installed, download from https://www.minizinc.org/
```

### 2️⃣ Initial Setup

```bash
# Validate configuration
python Scripts/setup/setup_and_validate.py

# Generate Cork variants (if necessary)
python Scripts/generation/create_cork_variants.py

# Run tests
bash Scripts/testing/test_generator.sh
```

### 2️⃣ Use the Generator (v3.0)

```bash
# Interactive GUI (recommended)
python Generator/generator.py

# Expected: SAT instance in ~1 second
# Input: 2 buses, 4 stations -> Output: SAT in attempt 1
```

### 4️⃣ Run Model

```bash
# Quick test with validated instance
minizinc --solver chuffed Models/clp_model.mzn Data/Battery\ Own/noncity_5buses-8stations.dzn

# With generated instance (from v3.0 Generator)
minizinc --solver chuffed Models/clp_model.mzn Tests/Output/Generator/*.dzn
```

## 📁 Project Structure

```
CLP-RCLP Minizinc/
│
├── 📂 Models/                      # Mathematical models
│   ├── clp_model.mzn              # CLP Model (primary)
│   ├── rclp_model.mzn             # RCLP Model (robust)
│   └── archive/                   # Backup and experimental variants
│
├── 📂 Data/                        # Datasets
│   ├── Battery Project Integer/   # Cork (real instances)
│   ├── Battery Project Variant/   # Cork single-cycle
│   ├── Battery Generated/         # Generated instances
│   └── Battery Own/               # Noncity + synthetic
│
├── 📂 Scripts/                     # Organized scripts
│   ├── data-processing/           # Conversion and validation
│   ├── generation/                # Variant generation
│   ├── testing/                   # Test suite
│   ├── setup/                     # Setup and initialization
│   ├── utilities/                 # Tools and diagnostics
│   └── README.md                  # Scripts guide
│
├── 📂 Generator/                   # Generation system
│   ├── generator.py               # Interactive GUI
│   ├── config.py                  # Configuration module
│   ├── instance_generator.py       # Expert algorithm
│   ├── generator_orchestrator.py   # Workflow coordinator
│   └── README.md                  # Build instructions
│
├── 📂 Docs/                        # Documentation
│   ├── generated-system/          # Generation system docs
│   ├── model/                     # Model documentation
│   ├── analysis/                  # Analysis and diagnostics
│   └── README.md                  # Documentation index
│
├── 📂 Tests/                       # Test results
│
├── 📄 README.md                    # This file
├── 📄 LICENSE                      # MIT License
├── 📄 CONTRIBUTING.md              # Contribution guide
├── 📄 CHANGELOG.md                 # Change history
└── 📄 .gitignore                   # Git configuration
```

All guides moved to `Docs/` for better organization:
- Installation: `Docs/setup/INSTALL.md`
- Development: `Docs/development/DEVELOPMENT.md`
- Troubleshooting: `Docs/guides/TROUBLESHOOTING.md`

## 📚 Documentation

### Quick Start
- **[Generator/README.md](Generator/README.md)** - Generator v3.0 documentation
- **[Docs/README.md](Docs/README.md)** - Central documentation index
- **[Docs/setup/INSTALL.md](Docs/setup/INSTALL.md)** - Installation instructions
- **[Docs/development/DEVELOPMENT.md](Docs/development/DEVELOPMENT.md)** - Development guide
- **[Docs/guides/TROUBLESHOOTING.md](Docs/guides/TROUBLESHOOTING.md)** - Common issues

### Technical Documentation
- **[Docs/model/MathModel.tex](Docs/model/MathModel.tex)** - Mathematical formulation
- **[Docs/model/PROJECT_SUMMARY.md](Docs/model/PROJECT_SUMMARY.md)** - Project summary
- **[Docs/analysis/](Docs/analysis/)** - Detailed analysis

### Specific Guides
- **[Generator/README.md](Generator/README.md)** - Generator v3.0 details
- **[Docs/model/PROJECT_SUMMARY.md](Docs/model/PROJECT_SUMMARY.md)** - Project overview
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

## 🔄 Typical Workflows

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

### Run Complete Tests
```bash
bash Scripts/testing/test_generator.sh    # Main suite (recommended)
python Scripts/testing/run_battery_project_tests.py  # Battery tests
```

### Diagnose Issues
```bash
python Scripts/setup/setup_and_validate.py  # Validate environment
bash Scripts/utilities/diagnose_cork.sh    # Diagnose Cork
```

## 📊 Datasets

| Dataset | Origin | Instances | Status | Recommendation |
|---------|--------|-----------|--------|-----------------|
| **Cork** | Real (Ireland) | 182+ | Infeasible* | RCLP or single cycles |
| **Cork Variants** | Reduced | 5 | Feasible | Testing, Research |
| **Noncity** | Validated | 10+ | Feasible✅ | **Recommended** |
| **Synthetic** | Generated | Variable | Feasible✅ | **Recommended** |
| **Generated** | Gen. System | 3+ | Feasible✅ | **Recommended** |

*Cork is infeasible for basic CLP. See [analysis](Docs/analysis/Cork_Infeasibility_Analysis.md)*

## 🧪 Testing Status

```
Generator v3.0 Test Results (Current):
  2 buses, 4 stations:   SAT in attempt 1  [PASS]
  3 buses, 5 stations:   SAT in attempt 1  [PASS]
  5 buses, 8 stations:   SAT in attempt 1  [PASS]

System Performance:
  Success Rate:         100%
  Average Time to SAT:  <1 second
  Average Attempts:     1.0

Validated Instances:
  - Noncity (Working):   10+ (SATISFIABLE)
  - Generated (v3.0):     3+ (SATISFIABLE)
  - Cork (Real):         Requires RCLP or single-cycle reduction
```

## 🛠️ Tools Used

| Tool | Version | Purpose |
|------|---------|---------|
| MiniZinc | 2.5+ | Constraint modeling |
| Python | 3.8+ | Utility scripts |
| Bash | Linux/macOS | Automation scripts |
| Git | Any | Version control |

### Supported Solvers
- ✅ Chuffed (recommended)
- ✅ Gecode
- ✅ COIN-BC

## 📖 Key Concepts

### CLP (Charging Location Problem)
Base constraint programming problem that determines optimal charging station location, minimizing station count while guaranteeing operational feasibility.

### RCLP (Robust CLP)
Robust extension that adds resilience against potential system failures.

### Scaling (×10)
All values are scaled by 10 to use integer arithmetic in MiniZinc, improving numerical precision.

### Feasibility
An instance is "feasible" if a valid solution exists where all buses complete their routes respecting constraints.

## ❓ FAQ

### Where do I start?
1. Run `bash Scripts/testing/test_generator.sh` first
2. Review [Docs/README.md](Docs/README.md) for documentation
3. Use `python Generator/generator.py` to create instances

### Why is Cork infeasible?
Cork contains 13-14 daily cycles (~400-500 stops) with ~1700 kWh consumption vs 80 kWh usable capacity. Requires 3+ RCLP models or reduction to single cycles.

### How do I generate custom instances?
Use `python Generator/generator.py` (GUI) or modify `Scripts/generation/` for automation.

### Where can I see expected results?
See `Data/Battery Generated/Expected Results/*.json`

## 🤝 Contributing

Contributions are welcome! Please:

1. Read [CONTRIBUTING.md](CONTRIBUTING.md)
2. Fork the repository
3. Create a branch: `git checkout -b feature/your-feature`
4. Make descriptive commits
5. Submit a Pull Request with clear description

## 📄 License

This project is licensed under MIT. See [LICENSE](LICENSE) for details.

## 👥 Authors

- **AVISPA Research Team** - Main research
- **Andrey Quiceño** - Development and maintenance

## 📞 Support

- 🐛 **Report Bugs**: [GitHub Issues](../../issues)
- 💬 **Questions**: See [Docs/README.md](Docs/README.md)
- 📚 **Documentation**: [Docs/](Docs/)

## 🎯 Future Roadmap

- [ ] Batch generation mode
- [ ] Custom parameter profiles
- [ ] Improved CLI mode
- [ ] Real-time visualization
- [ ] Benchmark suite integration
- [ ] REST API

## 📊 Project Statistics

- **Lines of Code**: 2000+
- **Documentation**: 3000+ lines
- **Automated Tests**: 7 test suites
- **Datasets**: 200+ instances
- **Validated Instances**: 18+

---

**Version**: 3.0.0
**Last Updated**: 2026-03-26 21:30 UTC
**Status**: [OK] Production Ready - Generator v3.0 "Working Pattern Replication"

## 📝 Technical Note

All numeric parameters are scaled ×10 to use integer arithmetic:

- **Time**: `4200` = 420.0 minutes = 7:00 AM
- **Energy**: `250` = 25.0 kWh
- **Capacity**: `1000` = 100.0 kWh

For more details, see [Docs/](Docs/) and [Generator/README.md](Generator/README.md).
