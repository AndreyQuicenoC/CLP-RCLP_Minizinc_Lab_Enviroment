# CLP-RCLP Documentation

Complete documentation for the CLP-RCLP optimization framework.

## Quick Navigation

### Getting Started
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Installation and first steps (start here!)
- **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** - What is CLP-RCLP and how it works
- **[VERSION_HISTORY.md](VERSION_HISTORY.md)** - Version history and migration guides

### Using the Tools
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Detailed guide for each tool (GUI and CLI)
- **guides/TROUBLESHOOTING.md** - Solutions to common problems
- **guides/** - Additional user guides

### Technical Documentation
- **model/QUICKSTART.md** - Quick mathematical overview
- **model/MathModel.tex** - Complete mathematical formulation
- **model/README.md** - Model documentation index

### Installation & Setup
- **installation/minizinc_installation.md** - MiniZinc setup
- **installation/gurobi_installation.md** - Gurobi solver (optional)
- **installation/cplex_installation.md** - CPLEX solver (optional)
- **installation/README.md** - Installation index

## For Different Users

### First-Time Users
1. Read: [GETTING_STARTED.md](GETTING_STARTED.md)
2. Launch: `python core/start.py`
3. Explore: System Center GUI
4. Learn: [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)

### Researchers
1. Review: [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)
2. Study: model/MathModel.tex
3. Use: [USAGE_GUIDE.md](USAGE_GUIDE.md)
4. Benchmark: Compare solvers with Runner tool

### Developers
1. Setup: [GETTING_STARTED.md](GETTING_STARTED.md)
2. Understand: core/README.md
3. Reference: model/MathModel.tex
4. Debug: guides/TROUBLESHOOTING.md

### System Administrators
1. Install: [GETTING_STARTED.md](GETTING_STARTED.md) + installation/
2. Verify: Run `python scripts/solvers/check_solvers.py`
3. Configure: core/*/config.py files
4. Monitor: Check experiments/results/

## Documentation Structure

```
docs/
├── GETTING_STARTED.md          # Installation and first steps
├── PROJECT_OVERVIEW.md         # Project description and features
├── USAGE_GUIDE.md              # How to use each tool
├── VERSION_HISTORY.md          # Version information and roadmap
│
├── guides/                     # User guides
│   └── TROUBLESHOOTING.md     # Problem solutions
│
├── installation/               # Setup instructions
│   ├── minizinc_installation.md
│   ├── gurobi_installation.md
│   ├── cplex_installation.md
│   └── README.md
│
└── model/                      # Mathematical documentation
    ├── QUICKSTART.md
    ├── MathModel.tex
    └── README.md
```

## Finding What You Need

### By Topic

**Getting Started**
→ [GETTING_STARTED.md](GETTING_STARTED.md)

**How to Use Tools**
→ [USAGE_GUIDE.md](USAGE_GUIDE.md)

**Understanding the Project**
→ [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)

**Mathematical Model**
→ model/MathModel.tex or model/QUICKSTART.md

**Installation Issues**
→ installation/ directory

**Solver Problems**
→ guides/TROUBLESHOOTING.md

**Previous Versions**
→ [VERSION_HISTORY.md](VERSION_HISTORY.md)

### By User Type

| Type | Start Here |
|------|-----------|
| New User | [GETTING_STARTED.md](GETTING_STARTED.md) |
| Researcher | [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) |
| Developer | core/README.md |
| Admin | installation/ |
| Troubleshooting | guides/TROUBLESHOOTING.md |

## Common Tasks

### Generate and Run Optimization
→ See [USAGE_GUIDE.md](USAGE_GUIDE.md#batch-workflow-example)

### Install Additional Solvers
→ See installation/

### Compare Solver Performance
→ See [USAGE_GUIDE.md](USAGE_GUIDE.md#test-runner)

### Convert Data to MiniZinc
→ See [USAGE_GUIDE.md](USAGE_GUIDE.md#data-converter)

### Generate Test Instances
→ See [USAGE_GUIDE.md](USAGE_GUIDE.md#instance-generator)

### Understand the Model
→ See model/QUICKSTART.md or model/MathModel.tex

## System Requirements

- Python 3.8+
- MiniZinc 2.6+
- 2GB disk space for solvers
- 8GB RAM minimum
- Multi-core CPU recommended

See [GETTING_STARTED.md](GETTING_STARTED.md#system-requirements) for details.

## Key Features

✓ Multi-tool framework (Generator, Converter, Runner)
✓ Professional GUI (System Center)
✓ Multiple solvers (6 supported)
✓ Complete documentation
✓ Real-world data support
✓ Scalable to large instances

See [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md#key-features) for more.

## Version Information

**Current Version**: 2.0.0 (April 2026)

Major update with:
- New System Center GUI
- Multi-solver support
- Professional documentation
- Complete project restructuring

See [VERSION_HISTORY.md](VERSION_HISTORY.md) for upgrade guides.

## Support

- **Installation Issues**: See installation/
- **Tool Usage**: See [USAGE_GUIDE.md](USAGE_GUIDE.md)
- **Problems**: See guides/TROUBLESHOOTING.md
- **General Questions**: See [GETTING_STARTED.md](GETTING_STARTED.md)
- **GitHub**: See main README.md for links

## Contributing

Documentation improvements welcome! See main README.md for contribution guidelines.

---

**Last Updated**: April 20, 2026
**Version**: 2.0.0
