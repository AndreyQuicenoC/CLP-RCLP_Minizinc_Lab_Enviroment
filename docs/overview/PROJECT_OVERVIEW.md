# CLP-RCLP Project Overview

## What is CLP-RCLP?

CLP-RCLP (Charging Logistics Problem / Recharging Charging Logistics Problem) is a research framework for optimizing battery charging schedules in electric vehicle fleets. The project provides tools for:

- **Data conversion**: JSON → MiniZinc constraint programming models
- **Instance generation**: Creating synthetic test datasets with realistic parameters
- **Optimization**: Solving scheduling problems with multiple constraint solvers
- **Analysis**: Comparing solver performance and solution quality

## Research Goals

This framework addresses the problem of optimally scheduling battery charging for a fleet of electric vehicles under constraints including:
- **Time windows**: Each vehicle has available charging periods
- **Energy limits**: Battery capacity constraints
- **Power limits**: Charging infrastructure capacity
- **Feasibility**: Finding feasible schedules for complex problem instances

## Key Features

### 🔧 Multi-Tool Architecture
- **Converter**: Transform real or synthetic data into optimization models
- **Generator**: Create test instances with controllable parameters
- **Runner**: Execute models with various solvers and collect results
- **System Center**: Unified GUI for accessing all tools

### 🎯 Professional UI
- Dark/Light theme support
- Responsive layout with scroll support
- Intuitive tool navigation
- Real-time execution feedback

### 🔬 Scientific Rigor
- Multiple solver backends (Chuffed, Gecode, COIN-BC, OR-Tools, CPLEX, Gurobi)
- Comprehensive result aggregation and metrics
- Reproducible experimental setup
- Validation against known solutions

### 📊 Complete Toolchain
- Data preprocessing and validation
- Instance generation with realistic parameters
- Parallel solver execution
- Automated result analysis

## Problem Formulation

The CLP/RCLP problem is formulated as a Mixed-Integer Linear Program (MILP) with:

**Variables:**
- `tbi[b,i]`: Time of the i-th charging event for bus b
- `cbi[b,i]`: Energy charged during event i for bus b
- `tau_bi[b,i]`: Duration of charging event i for bus b
- `ebi[b,i]`: Energy level after event i for bus b

**Constraints:**
- Energy balance: Battery level must be non-negative
- Time windows: Charging only during available periods
- Capacity: Battery cannot exceed maximum charge
- Power limits: Charging rate constrained by infrastructure

**Objective:**
Minimize total charging cost or maximize scheduling efficiency

See `docs/model/MathModel.tex` for complete mathematical formulation.

## Project Structure

```
CLP-RCLP/
├── core/                    # Application modules
│   ├── orchestration/       # System Center GUI
│   ├── converter/           # JSON to DZN conversion
│   ├── generator/           # Instance generation
│   ├── runner/              # Optimization execution
│   ├── models/              # MiniZinc formulations
│   └── shared/              # Common utilities
│
├── experiments/             # Experimental data
│   ├── instances/           # Test datasets
│   └── results/             # Solver outputs
│
├── scripts/                 # Utility scripts
│   ├── data-processing/     # Data utilities
│   ├── solvers/             # Solver management
│   ├── testing/             # Test suites
│   └── verification/        # Validation tools
│
├── docs/                    # Documentation
│   ├── guides/              # User guides
│   ├── installation/        # Setup instructions
│   └── model/               # Mathematical docs
│
└── external/                # External dependencies
    └── jits2022/            # JITS 2022 reference
```

## Technology Stack

- **Language**: Python 3.8+
- **Constraint Programming**: MiniZinc 2.6+
- **Solvers**: Chuffed, Gecode, COIN-BC, OR-Tools, CPLEX, Gurobi
- **UI Framework**: Tkinter (Python built-in)
- **Testing**: pytest, shell scripts
- **Version Control**: Git

## Research Applications

This framework supports:

1. **Algorithm Research**: Compare constraint programming approaches
2. **Solver Benchmarking**: Evaluate solver performance on real instances
3. **Parameter Sensitivity**: Study impact of problem parameters
4. **Scalability Analysis**: Test performance on varying problem sizes
5. **Real-World Deployment**: Generate instances from actual EV fleet data

## Supported Problem Variants

### Cork Instances
Special test cases with known infeasibility characteristics for validation.

### Generated Instances
Synthetic datasets created with:
- Configurable number of vehicles and stops
- Realistic battery and charging parameters
- Reproducible random initialization

### Project Instances
Real-world battery project data in standardized format.

## Performance Characteristics

Typical execution times (on multi-core system):
- **Small instances** (5 buses, 3 stops): < 1 second
- **Medium instances** (20 buses, 10 stops): 5-30 seconds
- **Large instances** (50 buses, 20 stops): 60+ seconds

Results vary significantly by solver choice and problem structure.

## Version Roadmap

### v1.0 - Initial Release
- Basic Converter and Runner
- Single solver support
- Command-line interface

### v2.0 - Multi-Tool Framework (Current)
- System Center GUI
- Instance Generator
- Multi-solver support
- Professional theming
- Comprehensive documentation

### Future Versions
- Distributed solving
- Real-time performance monitoring
- Advanced visualization
- Machine learning integration for instance classification

## Research Team

Developed by the AVISPA Research Team at [Institution Name].

**Contributors:**
- Andrey Quiceno (Lead Developer)
- Juan Francesco García (UI/Framework)
- Research team members and collaborators

## Citation

If using this framework in research, please cite:

```
@software{clprclp2026,
  title={CLP-RCLP: Charging Logistics Optimization Framework},
  author={Quiceno, Andrey and García, Juan Francesco},
  year={2026},
  url={https://github.com/AndreyQuicenoC/CLP-RCLP_Minizinc_Lab_Enviroment}
}
```

## License

See LICENSE file in project root.

## Getting Started

New users should start with:
1. `docs/GETTING_STARTED.md` - Installation and basic usage
2. `docs/model/QUICKSTART.md` - Mathematical formulation overview
3. `core/README.md` - Tool architecture and direct usage

## Support & Resources

- **Documentation**: See `docs/` directory
- **Issues**: GitHub issue tracker
- **Discussions**: GitHub discussions forum
- **Troubleshooting**: `docs/guides/TROUBLESHOOTING.md`
