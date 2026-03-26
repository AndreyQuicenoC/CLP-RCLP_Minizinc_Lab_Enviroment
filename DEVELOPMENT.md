# Development Guide

Guidelines for contributing code and developing features for the CLP-RCLP project.

## Development Environment

### Setup

```bash
# Clone repository
git clone https://github.com/AndreyQuicenoC/CLP-RCLP_Minizinc_Lab_Enviroment.git
cd CLP-RCLP\ Minizinc\ Lab\ Enviroment

# Create development environment
python -m venv venv-dev
source venv-dev/bin/activate  # Linux/macOS
# or venv-dev\Scripts\activate on Windows

# Install development dependencies
pip install -r requirements-dev.txt
```

### Project Structure

```
Scripts/
├── data-processing/    # Data format conversions and validation
├── generation/         # Instance generation algorithms
├── testing/           # Test suites and validators
├── setup/            # Environment setup and diagnostics
└── utilities/        # Diagnostic and helper tools

Docs/
├── generated-system/  # Instance generation documentation
├── model/            # Mathematical model documentation
└── analysis/         # Technical analysis and research

Generator/            # GUI application (1500+ lines)
Models/              # MiniZinc models (.mzn files)
Data/                # Test instances and benchmarks
```

## Architecture Overview

### Core Components

1. **MiniZinc Models** (`Models/`)
   - `clp_model.mzn` - Base charging location problem
   - `rclp_model.mzn` - Robust variant with resilience

2. **Python Generator** (`Generator/generator.py`)
   - Tkinter GUI with expert algorithm
   - MiniZinc integration for validation
   - JSON result storage

3. **Scripts Ecosystem** (`Scripts/`)
   - Data processing pipeline
   - Instance generation tools
   - Comprehensive test suite
   - Installation validation

### Data Pipeline

```
JSON Input (JITS2022)
         ↓
convert_json_to_integer_dzn.py
         ↓
Integer .dzn (scaled ×10)
         ↓
validate_integer_dzn.py
         ↓
Validated Instance
         ↓
MiniZinc Solver → Solution
```

## Coding Standards

### Python

Follow PEP 8 with these additions:

```python
# Function documentation
def generate_instance(buses, stations):
    """
    Generate a test instance.
    
    Args:
        buses (int): Number of buses (2-25)
        stations (int): Number of stations (4-25)
        
    Returns:
        dict: Instance data with all parameters
        
    Raises:
        ValueError: If parameters out of range
    """
    if not (2 <= buses <= 25):
        raise ValueError(f"Buses must be 2-25, got {buses}")
```

- Use 4-space indentation
- Keep lines under 100 characters
- Add docstrings to all functions/classes
- Use type hints where possible

### Shell Scripts

```bash
#!/bin/bash
# Use bash not sh

# Quote all variables
RESULT="$variable"

# Meaningful names
INSTANCE_COUNT=5
TIMEOUT_SECONDS=300

# Add comments for complex logic
```

### Documentation

- Use Markdown for all documentation
- Include code examples
- Keep README files up-to-date
- Link to related docs

## Testing

### Run Tests

```bash
# Full test suite
bash Scripts/testing/test_generator.sh

# Specific tests
python Scripts/testing/test_initial_small_case.py
python Scripts/testing/run_battery_project_tests.py

# Data validation
python Scripts/data-processing/validate_integer_dzn.py test.dzn
```

### Writing Tests

Create test functions following this pattern:

```python
def test_instance_generation():
    """Test that generated instances are valid."""
    instance = generate_instance(5, 8)
    assert instance is not None
    assert instance['num_buses'] == 5
    assert len(instance['times']) > 0
```

## Git Workflow

### Branching

```bash
# Create feature branch
git checkout -b feature/new-feature

# Create bugfix branch
git checkout -b bugfix/issue-123

# Create doc branch
git checkout -b docs/update-readme
```

### Commits

Follow conventional commit format:

```
<type>(<scope>): <subject>

<body>

Closes #<issue-number>
```

**Types**: feat, fix, docs, style, refactor, perf, test, chore

**Scopes**: generator, scripts, models, data, docs

**Example**:
```
feat(generator): implement expert overconsumption algorithm

Add intelligent overconsumption factor calculation based on
route analysis. Implements 1.1-1.4x multiplier with dynamic
adjustment. Includes validation against MiniZinc solver output.

Closes #42
```

### Pull Request Process

1. Update branch: `git pull origin main`
2. Create descriptive PR title
3. Include:
   - What problem does it solve?
   - How does it solve it?
   - Test results
   - Breaking changes (if any)
4. Request review from maintainers
5. Address feedback
6. Squash commits if needed: `git rebase -i`

## Performance Profiling

### Python

```python
import cProfile
import pstats

cProfile.run('generate_instance(10, 15)', 'stats')
stats = pstats.Stats('stats')
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 functions
```

### MiniZinc

Monitor solver performance:

```bash
# With timing information
minizinc --solver chuffed --time-limit 60000 --verbose \
  Models/clp_model.mzn Data/test.dzn

# Check solver capabilities
minizinc --solvers
```

## Adding New Features

### Feature Checklist

- [ ] Create feature branch
- [ ] Implement feature with tests
- [ ] Update relevant README files
- [ ] Add to CHANGELOG.md
- [ ] Run full test suite
- [ ] Update documentation
- [ ] Create pull request
- [ ] Address review comments
- [ ] Merge to main

### Example: Adding New Script

1. Create file in appropriate Scripts/ subdirectory
2. Add docstring and usage examples
3. Create or update README.md in that directory
4. Update Scripts/README.md if needed
5. Add tests in Scripts/testing/
6. Document in Docs/ if needed
7. Commit with appropriate message

## Debugging

### Python Debugging

```python
# In your script
import pdb

def problematic_function():
    x = 5
    pdb.set_trace()  # Debugger stops here
    return x * 2
```

### Check MiniZinc Compilation

```bash
minizinc --version
minizinc --solvers

# Compile without solving
minizinc --compile-only Models/clp_model.mzn Data/test.dzn
```

### Enable Debug Mode

```bash
export DEBUG=1
python Scripts/generation/create_cork_variants.py
```

## Common Tasks

### Update Dependencies

```bash
pip install --upgrade pip
pip freeze > requirements-dev.txt
```

### Format Code

```bash
# Python formatting
black Scripts/

# Check style
flake8 Scripts/
```

### Generate Documentation

```bash
# Python docstrings help
pydoc Scripts/generation/create_cork_variants.py

# Create HTML docs (if Sphinx configured)
# cd Docs && make html
```

## Release Process

1. Update CHANGELOG.md with release notes
2. Update version numbers if needed
3. Create release branch: `git checkout -b release/v1.1.0`
4. Tag release: `git tag -a v1.1.0 -m "Release v1.1.0"`
5. Push: `git push origin release/v1.1.0 && git push --tags`
6. Merge to main: `git checkout main && git merge release/v1.1.0`

## Resources

- [Python 3 Docs](https://docs.python.org/3/)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [MiniZinc Handbook](https://www.minizinc.org/doc-latest/en/)
- [Git Documentation](https://git-scm.com/doc)
- [Conventional Commits](https://www.conventionalcommits.org/)

## Getting Help

- Check existing issues: GitHub Issues
- Read documentation: Docs/
- Ask in PR comments or discussions
- Review similar implementations

---

**Last Updated**: 2026-03-25
**Maintained By**: AVISPA Research Team
