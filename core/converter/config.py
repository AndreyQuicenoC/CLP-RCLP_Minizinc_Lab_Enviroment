"""
Converter Configuration Module

Centralized configuration for the JSON to DZN converter system.
Manages UI colors, fonts, paths, and model parameters.

Author: AVISPA Research Team
Date: April 2026
"""

# ============================================================================
# SCALING CONFIGURATION
# ============================================================================

# Scaling factor: all floating-point values are multiplied by this
SCALE = 10

# Model parameters (original values)
CMAX_ORIGINAL = 100.0  # Maximum battery capacity (kWh)
CMIN_ORIGINAL = 20.0   # Minimum battery reserve (kWh)
ALPHA_ORIGINAL = 10.0  # Fast charging rate (kWh per minute)
MU_ORIGINAL = 5.0      # Maximum delay allowed (minutes)
SM_ORIGINAL = 1.0      # Safety margin between charging (minutes)
PSI_ORIGINAL = 1.0     # Minimum charging time (minutes)
BETA_ORIGINAL = 10.0   # Maximum charging time per stop (minutes)
M_ORIGINAL = 10000.0   # Big-M constant

# ============================================================================
# UI COLORS - DARK THEME
# ============================================================================

DARK_PALETTE = {
    "bg_base": "#1a1a1a",           # Main background
    "bg_surface": "#2a2a2a",        # Surface elements
    "bg_hover": "#3a3a3a",          # Hover states
    "border": "#404040",             # Borders
    "text_primary": "#e0e0e0",      # Primary text
    "text_secondary": "#a0a0a0",    # Secondary text
    "accent_primary": "#6366f1",    # Primary accent (indigo)
    "accent_secondary": "#8b5cf6",  # Secondary accent (purple)
    "success": "#10b981",            # Success (green)
    "error": "#ef4444",              # Error (red)
    "warning": "#f59e0b",            # Warning (amber)
    "info": "#3b82f6",               # Info (blue)
}

# ============================================================================
# UI COLORS - LIGHT THEME
# ============================================================================

LIGHT_PALETTE = {
    "bg_base": "#f8f9fa",            # Main background
    "bg_surface": "#ffffff",         # Surface elements
    "bg_hover": "#f0f1f3",           # Hover states
    "border": "#d0d0d0",             # Borders
    "text_primary": "#1a1a1a",      # Primary text
    "text_secondary": "#666666",    # Secondary text
    "accent_primary": "#6366f1",    # Primary accent (indigo)
    "accent_secondary": "#8b5cf6",  # Secondary accent (purple)
    "success": "#059669",            # Success (green)
    "error": "#dc2626",              # Error (red)
    "warning": "#d97706",            # Warning (amber)
    "info": "#2563eb",               # Info (blue)
}

# ============================================================================
# FONTS
# ============================================================================

FONTS = {
    "title": ("Arial", 16, "bold"),
    "header": ("Arial", 12, "bold"),
    "normal": ("Arial", 10),
    "small": ("Arial", 9),
    "mono": ("Courier New", 9),
}

# ============================================================================
# WINDOW SETTINGS
# ============================================================================

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
WINDOW_RESIZABLE = False

# ============================================================================
# CONVERSION SETTINGS
# ============================================================================

# Extensions
JSON_EXTENSION = ".json"
DZN_EXTENSION = ".dzn"
JSON_PATTERN = "*_input*.json"  # Pattern for JSON files in JITS2022

# Support files to check
SUPPORT_FILES = {
    "distances_input.csv": "Distance matrix for energy calculation",
    "stations_input.csv": "Station information and coordinates",
    "input_report.txt": "Dataset metadata and statistics",
}

# ============================================================================
# PATHS
# ============================================================================
# Note: These are relative paths resolved from the project root at runtime
# For absolute paths, use Path(__file__).parent.parent.parent for project_root

JITS_BASE_PATH = "external/jits2022/Code/data"  # Default input source
DATA_OUTPUT_BASE = "experiments/instances"      # Default output destination
