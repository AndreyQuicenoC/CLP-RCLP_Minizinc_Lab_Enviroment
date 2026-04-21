# UI Testing Suite

Automated validation scripts for theme system and UI rendering.

## Overview

This directory contains comprehensive test scripts for validating the CLP-RCLP interfaces are functioning correctly. The tests verify dark/light theme switching, component rendering, and design token application.

## Test Scripts

### test_runner_ui.py

Validates the CLP-RCLP Runner interface:

- Interface loads without errors
- Dark/light mode switching works correctly
- All 26+ theme design tokens are present and properly configured
- Component styling renders with correct colors
- Log output functionality operates correctly
- Theme observer pattern notifies on mode changes

**Run**: `python test_runner_ui.py`

**Test Coverage**: 8 comprehensive test scenarios

### test_generator_ui.py

Validates the CLP-RCLP Generator interface:

- Interface loads without errors
- Dark/light mode switching works correctly
- Parameter controls (buses, stations spinboxes) function properly
- Boundary validation for parameter ranges
- Theme token colors match expected palettes
- Log clearing and output operations work correctly

**Run**: `python test_generator_ui.py`

**Test Coverage**: 9 comprehensive test scenarios

## Features Tested

✓ **Theme System**

- Default dark mode activation
- Light mode switching and activation
- Theme design tokens (colors, fonts, spacing)

✓ **Component Rendering**

- All UI component creation and accessibility
- Theme-aware styling application
- Component visib ility and functionality

✓ **User Interactions**

- Window startup and centering
- Mode toggle functionality
- Parameter value modification

✓ **Design System**

- 27 design tokens available per theme
- Typography coverage (ui, bold, section, mono, small)
- Color palette consistency (dark and light modes)

## Architecture

### Tests Verify These Components

- **ThemeManager**: Singleton pattern for global theme state
- **get_theme_dict()**: Returns complete design token dictionary
- **Theme Palettes**: Dark (default) and Light color palettes
- **Observer Pattern**: Theme change notifications to subscribers
- **UI Components**: SectionLabel, FlatButton, Divider, StatusIndicator

## Design Tokens Validated

**Color Palette** (16 tokens):

- Backgrounds: base, surface, elevated, hover
- Accents: primary, dim, glow
- Status: success, warning, error
- Text: primary, secondary, muted, code
- Borders: normal, active

**Typography** (5 tokens):

- font_ui, font_bold, font_section, font_mono, font_small

**Spacing** (5+ tokens):

- padding_large, padding_medium, padding_small, padding_tiny, header_height

## Running Tests

### Single Test

```bash
python test_runner_ui.py
python test_generator_ui.py
```

### All Tests

```bash
python test_runner_ui.py && python test_generator_ui.py
```

### With Logging

The test scripts provide detailed output showing:

- Component checks ✓
- Theme token validation ✓
- Mode switching tests ✓
- Color value verification ✓
- Typography verification ✓

## Test Results

Successful tests output:

```
===============================================================
ALL TESTS PASSED ✓
===============================================================
Runner Interface v1.3.0 is fully functional!
```

## Authors

Andrey Quiceno and Juan Francesco García (AVISPA Team)

**Version**: 1.3.0
**Date**: April 2026
**Framework**: Tkinter theme system
**Test Framework**: Python unittest patterns
