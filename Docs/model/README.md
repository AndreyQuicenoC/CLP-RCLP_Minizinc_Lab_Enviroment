# Mathematical Model Documentation

Technical documentation and mathematical formulation of the CLP-RCLP model.

## 📁 Contents

### Main Files

- **MathModel.tex** - Complete mathematical formulation in LaTeX
  - Variable definitions
  - Objective function
  - Constraints
  - Parameters

- **PROJECT_SUMMARY.md** - Executive project summary
  - Objectives
  - Scope
  - Results

- **QUICKSTART.md** - Quick start guide
  - Installation
  - First test
  - Basic examples

## 🔬 Model Structure

### Main Parameters

| Parameter | Value | Meaning |
|-----------|-------|---------|
| Cmax | 1000 | Maximum capacity (100 kWh) |
| Cmin | 200 | Minimum reserve (20 kWh) |
| alpha | 100 | Charging rate (10 kWh/min) |
| mu | 50 | Maximum delay (5 min) |

### Decision Variables

- `x_bi` - Binary: Is charging performed at stop (b,i)?
- `e_bi` - Continuous: Energy at end of stop (b,i)
- `ct_bi` - Continuous: Charging time at stop (b,i)

## 📊 Typical Results

For instance noncity_5buses-8stations:
- **Total stations**: 3/8 installed
- **Total deviation**: ~1564
- **Resolution time**: < 1 second

## 🔗 Related Links

- [Generation System](../generated-system/)
- [Detailed Analysis](../analysis/)
- [MiniZinc Model](../../Models/)

## 📚 For More Information

See the complete formulation in MathModel.tex (compile with LaTeX).

**Last Updated**: 2026-03-26
