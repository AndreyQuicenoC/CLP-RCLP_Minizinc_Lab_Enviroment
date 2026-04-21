# Getting Started with CLP-RCLP

This guide walks you through launching and using the CLP-RCLP optimization framework for the first time.

## Quick Start (60 seconds)

1. **Navigate to the core directory:**
   ```bash
   cd core
   ```

2. **Launch System Center:**
   ```bash
   python start.py
   ```
   Or on Unix/Linux:
   ```bash
   bash start.sh
   ```

3. **Choose your tool from the interface:**
   - **Data Converter**: Convert JSON schedules to MiniZinc format
   - **Instance Generator**: Create test instances with custom parameters
   - **Test Runner**: Execute optimization and compare solvers

## System Requirements

### Required Software
- Python 3.8+
- MiniZinc 2.6+ (with bundle of solvers)

### Supported Solvers
- **Included**: Chuffed, Gecode, COIN-BC, OR-Tools
- **Optional**: CPLEX, Gurobi (requires separate licenses)

### Recommended System Specs
- **RAM**: 8GB minimum, 16GB recommended
- **Disk Space**: 2GB for solvers and instances
- **CPU**: Multi-core recommended for parallel solving

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/AndreyQuicenoC/CLP-RCLP_Minizinc_Lab_Enviroment.git
cd "CLP-RCLP_Minizinc_Lab_Enviroment"
```

### Step 2: Install MiniZinc
- **Windows**: Download installer from [minizinc.org](https://www.minizinc.org/)
- **macOS**: `brew install minizinc`
- **Linux**: Follow [official guide](https://www.minizinc.org/doc-latest/en/installation_linux.html)

See `docs/installation/minizinc_installation.md` for detailed instructions.

### Step 3: (Optional) Install Additional Solvers
```bash
# CPLEX (requires license)
bash scripts/setup/setup_and_validate.py

# Gurobi (requires license)
See docs/installation/gurobi_installation.md
```

### Step 4: Verify Installation
```bash
python scripts/solvers/check_solvers.py
```

## Core Tools

### Data Converter
Converts JSON-formatted battery schedules to MiniZinc DZN format.

**Quick Example:**
```bash
cd core
python converter/converter.py --input data.json --output data.dzn
```

**Features:**
- Automatic scaling and validation
- Support for Cork instances
- Energy balance verification
- Detailed error reporting

### Instance Generator
Creates synthetic test instances with configurable parameters.

**Quick Example:**
```bash
cd core
python generator/generator.py --buses 5 --stops 3 --output my_instance.dzn
```

**Features:**
- Parameterizable instance generation
- Cork variant creation
- Realistic battery characteristics
- Reproducible random seeds

### Test Runner
Executes optimization models and compares solver performance.

**Quick Example:**
```bash
cd core
python runner/runner.py --instances battery-project --solvers chuffed gecode
```

**Features:**
- Multi-solver comparison
- Automated result aggregation
- Performance metrics (time, optimality)
- HTML report generation

## Directory Structure

```
core/
├── start.py              # Main entry point
├── converter/            # JSON → DZN conversion
├── generator/            # Instance generation
├── runner/               # Optimization execution
├── models/               # MiniZinc constraint models
└── orchestration/        # System Center GUI

experiments/
├── instances/            # Test data and generated instances
└── results/              # Solver results and diagnostics

scripts/
├── data-processing/      # Data utilities
├── solvers/              # Solver installation/testing
├── testing/              # Test suites
└── verification/         # Converter validation

docs/
├── guides/               # User guides
├── installation/         # Solver setup guides
└── model/                # Mathematical formulation
```

## Common Workflows

### Generate and Test an Instance

1. **Generate instance:**
   ```bash
   cd core
   python generator/generator.py --buses 10 --stops 5
   ```

2. **Convert to MiniZinc format:**
   ```bash
   python converter/converter.py --input generated.json --output generated.dzn
   ```

3. **Run optimization:**
   ```bash
   python runner/runner.py --instances generated --solvers chuffed
   ```

### Compare Solver Performance

```bash
cd core
python runner/runner.py \
  --instances battery-project \
  --solvers chuffed gecode "COIN-BC" \
  --timeout 300
```

Results will be saved to `experiments/results/`.

## Troubleshooting

### Issue: "MiniZinc not found"
**Solution**: Install MiniZinc and ensure it's in your PATH.
- Check: `minizinc --version`
- See: `docs/guides/TROUBLESHOOTING.md`

### Issue: "No solver available"
**Solution**: Install solvers with MiniZinc bundle or configure manually.
- Check: `python scripts/solvers/check_solvers.py`
- See: `docs/installation/`

### Issue: Conversion errors
**Solution**: Validate your input JSON format.
- Run: `python scripts/data-processing/validate_integer_dzn.py`
- See: `docs/guides/TROUBLESHOOTING.md`

## Next Steps

- **Learn the model**: Read `docs/model/QUICKSTART.md`
- **Understand formulation**: See `docs/model/MathModel.tex`
- **Advanced usage**: Check tool-specific READMEs in `core/*/`
- **Development**: See main `README.md`

## Getting Help

- **Issues**: GitHub issue tracker
- **Documentation**: `docs/` directory
- **Quick reference**: Run tools with `--help` flag
- **Community**: See main README for contribution guidelines

## System Center Features

The System Center GUI provides:
- ✓ Unified access to all tools
- ✓ Dark/Light theme switching
- ✓ Quick launch buttons
- ✓ Direct documentation links
- ✓ One-click GitHub repository access

Launch it with: `python core/start.py`
