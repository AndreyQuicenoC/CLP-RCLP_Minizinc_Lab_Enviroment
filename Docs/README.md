# CLP-RCLP MiniZinc Documentation

Central documentation directory for technical documentation, analysis and project guides.

## 📁 Structure

```
Docs/
├── generated-system/       # Instance generation system
│   ├── README.md          # Complete generator guide
│   └── INDEX.md           # Navigation index
│
├── model/                 # Mathematical model documentation
│   ├── MathModel.tex      # LaTeX formulation
│   ├── PROJECT_SUMMARY.md # Executive summary
│   ├── QUICKSTART.md      # Quick start guide
│   └── README.md          # Model index
│
├── analysis/              # Analysis and diagnostics
│   ├── Cork_Infeasibility_Analysis.md
│   ├── DataCorrections.md
│   ├── ModelModificationJustification.md
│   ├── CHECKLIST_FINAL.md
│   ├── SESSION_2026_03_26_*.md # Session notes
│   └── README.md          # Analysis index
│
├── ARCHITECTURE_v1_4_0.md # v1.4.0 multi-solver architecture
│
└── README.md              # This file
```

## 🎯 Quick Start by User Type

### 👨‍💼 Executive / Project Manager

1. Read: `generated-system/README.md` (Overview section)
2. View: `model/PROJECT_SUMMARY.md`
3. Check: `analysis/CHECKLIST_FINAL.md`

### 👨‍💻 Developer / Researcher

1. Start: `generated-system/README.md` (Quick Start)
2. Understand: `model/MathModel.tex`
3. Analyze: `analysis/Cork_Infeasibility_Analysis.md`
4. Implement: Scripts in `../Scripts/`

### 🔬 Scientist / Data Analyst

1. Review: `model/MathModel.tex`
2. Study: `analysis/DataCorrections.md`
3. Investigate: `analysis/ModelModificationJustification.md`
4. Execute: Scripts in `../Scripts/testing/`

## 📚 Documents by Functionality

### Generation System

**Main File**: `generated-system/README.md`

Contains:

- System overview
- How to generate instances
- Expert algorithm
- Troubleshooting
- Performance metrics

### Mathematical Model

**Main File**: `model/MathModel.tex`

Contains:

- Complete formulation
- Variables and constraints
- Parameters
- Examples

Executive summary: `model/PROJECT_SUMMARY.md`
Quick reference: `model/QUICKSTART.md`

### Technical Analysis

**Main File**: `analysis/README.md`

Contains:

- Cork problems
- Data corrections
- Model modifications
- Key findings

## 🔍 Quick Search by Topic

### Cork Instances

- **Problem**: `analysis/Cork_Infeasibility_Analysis.md`
- **Solution**: `generated-system/README.md` (Cork Variants)

### Data Issues

- **Corrections**: `analysis/DataCorrections.md`
- **Validation**: `generated-system/README.md` (Validation)

### Model Questions

- **Formulation**: `model/MathModel.tex`
- **Changes**: `analysis/ModelModificationJustification.md`

### Generation System

- **Complete Guide**: `generated-system/README.md`
- **Algorithm**: `generated-system/README.md` (Algorithm Design)

### First Time Setup

- **Steps**: `model/QUICKSTART.md`
- **Checklist**: `analysis/CHECKLIST_FINAL.md`

### Multi-Solver Architecture (v1.4.0)

- **Architecture Guide**: `ARCHITECTURE_v1_4_0.md`
- **Solver Scripts**: `../Scripts/solvers/README.md`

## 📋 Documents by Format

### Markdown (.md)

- `**/README.md` - Main guides
- `**/INDEX.md` - Navigation indices
- `analysis/*.md` - Detailed analysis

### LaTeX (.tex)

- `model/MathModel.tex` - Mathematical formulation

### Text (.txt)

- `analysis/INSTALLATION_SUCCESS.txt` - Installation log

## 🔗 Related Links

- [Project Scripts](../Scripts/README.md)
- [Generator GUI](../Generator/README.md)
- [MiniZinc Models](../Models/)
- [Datasets](../Data/)

## 🤝 Contributing

To add documentation:

1. Determine category (generated-system, model, analysis)
2. Create Markdown file with descriptive name
3. Add index in corresponding README.md
4. Update this file if necessary

## 📊 Documentation Status

| Section               | Complete | Updated          |
| --------------------- | -------- | ---------------- |
| generated-system/     | ✓        | Yes (2026-03-26) |
| model/                | ✓        | Yes (2026-03-25) |
| analysis/             | ✓        | Yes (2026-03-26) |
| Navigation            | ✓        | Yes (2026-03-26) |
| Architecture (v1.4.0) | ✓        | Yes (2026-04-15) |

## 📝 Change History

- **2026-04-15**: Multi-Solver Architecture (v1.4.0)
  - Added ARCHITECTURE_v1_4_0.md with comprehensive technical documentation
  - Documented solver management and result organization
  - Added troubleshooting guide for multi-solver setup
  - Updated navigation and status table

- **2026-03-26**: Generator enhancements and documentation updates
  - Fixed st_bi indexing in Battery Project data
  - Enhanced Generator v2.0 with infinite iteration
  - Organized Models directory
  - Translated all docs to English

- **2026-03-25**: Professional documentation restructuring
  - Organized into 3 main categories
  - Added navigation indices
  - Updated reference paths

**Last Updated**: 2026-04-15
