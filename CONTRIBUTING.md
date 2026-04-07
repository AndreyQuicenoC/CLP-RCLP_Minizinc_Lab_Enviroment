# Contributing to CLP-RCLP MiniZinc Lab Environment

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

Before creating a bug report, check if the issue already exists. When creating a bug report, include:

- **Clear description** of what the bug is
- **Steps to reproduce** the behavior
- **Expected behavior** vs actual behavior
- **Environment details**: OS, Python version, MiniZinc version
- **Screenshots** if applicable
- **Log files** if available

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When suggesting an enhancement:

- Use a **clear and descriptive title**
- Provide **detailed description** of the suggested enhancement
- Explain **why this enhancement would be useful**
- List **examples** of how it would work

### Pull Requests

1. **Fork** the repository
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Make your changes**
4. **Test your changes** thoroughly
5. **Commit with clear messages** (see Commit Guidelines below)
6. **Push to your fork** (`git push origin feature/AmazingFeature`)
7. **Submit a Pull Request**

## Development Setup

### Prerequisites

```bash
# Python 3.8+
python --version

# MiniZinc 2.6+
minizinc --version

# Git
git --version
```

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/AndreyQuicenoC/CLP-RCLP_Minizinc_Lab_Enviroment.git
cd CLP-RCLP\ Minizinc\ Lab\ Enviroment

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install MiniZinc if not already installed
# https://www.minizinc.org/software.html
```

### Project Structure

- `Models/` - MiniZinc model files (.mzn)
- `Data/` - Test instances (.dzn files)
- `Scripts/` - Python and shell scripts (organized by function)
- `Docs/` - Documentation and technical guides
- `Tests/` - Test results and benchmarks
- `Generator/` - Instance generator with modular architecture (v3.0)
- `Runner/` - Test execution interface with theme system (v1.3.0)

### Testing

Run the test suite:

```bash
# Test entire system
bash Scripts/testing/test_generator.sh

# Run specific tests
python Scripts/testing/test_initial_small_case.py
python Scripts/testing/run_battery_project_tests.py
```

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that don't affect code meaning (formatting, etc)
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Code change that improves performance
- **test**: Adding or updating tests
- **chore**: Changes to build process, CI/CD, dependencies

### Scope

Scope should specify what is affected:

- `generator` - Instance generator GUI and core modules
- `runner` - Test execution interface with dark/light theme (v1.3.0)
- `scripts` - Python/shell scripts
- `models` - MiniZinc model files
- `data` - Data processing or test instances
- `docs` - Documentation

### Subject

- Use imperative mood ("add feature" not "added feature")
- Don't capitalize first letter
- No period at the end
- Limit to 50 characters

### Body

- Explain **what** and **why**, not **how**
- Wrap at 72 characters
- Separate from subject with blank line

### Footer

Reference issues with keywords:

- `Closes #123`
- `Fixes #456`
- `Resolves #789`

### Example

```
feat(generator): implement expert algorithm for instance generation

Add intelligent instance generation based on noncity analysis patterns.
Implements overconsumption factor (1.1-1.4x) with route diversity and
temporal feasibility. Includes auto-validation with MiniZinc integration.

Closes #42
Resolves #55
```

## Code Style

### Python

- Follow PEP 8 style guide
- Use 4-space indentation
- Keep lines under 100 characters
- Add docstrings to functions and classes

```python
def validate_instance(dzn_file):
    """
    Validate a DZN instance file for correctness.

    Args:
        dzn_file (str): Path to the .dzn file

    Returns:
        tuple: (is_valid, error_message)
    """
    pass
```

### Shell Scripts

- Use bash (#!/bin/bash)
- Quote variables: `"$variable"`
- Use meaningful variable names
- Add comments for complex logic

### Documentation

- Use Markdown for documentation
- Include code examples where helpful
- Keep documentation up-to-date with code changes
- Add links to related documentation

## Reporting Security Issues

**Do not** open a public issue for security vulnerabilities. Email security concerns to the project maintainers instead.

## Recognition

Contributors will be recognized in:

- README.md contributors section
- GitHub contributors page
- Project releases

## Questions?

Feel free to open an issue with the `question` label for any clarification.

---

**Last Updated**: April 2026
