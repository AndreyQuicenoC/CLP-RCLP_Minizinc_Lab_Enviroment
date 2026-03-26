"""
================================================================================
Configuration Module - CLP Instance Generator
================================================================================
Central configuration for the entire generator system.
Author: AVISPA Research Team
Version: 2.0.0
================================================================================
"""

class Config:
    """Centralized configuration for instance generation"""

    # =========================================================================
    # BATTERY PARAMETERS (scaled ×10)
    # =========================================================================
    CMAX = 1000   # 100 kWh max capacity
    CMIN = 200    # 20 kWh min reserve
    USABLE_CAPACITY = CMAX - CMIN  # 80 kWh usable

    ALPHA = 100   # 10 kWh/min charging rate

    # =========================================================================
    # TIME PARAMETERS (scaled ×10)
    # =========================================================================
    MU = 50       # 5 min max delay
    SM = 10       # 1 min safety margin
    PSI = 10      # 1 min minimum charging time
    BETA = 100    # 10 min maximum charging time
    M = 10000     # Big-M constant

    # =========================================================================
    # GENERATION PARAMETERS (derived from constraint analysis)
    # =========================================================================

    # Energy consumption bounds (scaled ×10)
    MIN_CONSUMPTION_PER_STOP = 100    # 10 kWh
    MAX_CONSUMPTION_PER_STOP = 300    # 30 kWh
    OPTIMAL_CONSUMPTION_PER_STOP = 180  # 18 kWh

    # Travel times (scaled ×10)
    MIN_TRAVEL_TIME = 60      # 6 min
    MAX_TRAVEL_TIME = 300     # 30 min
    OPTIMAL_TRAVEL_TIME = 120 # 12 min

    # Route constraints
    MIN_STOPS_PER_BUS = 4
    MAX_STOPS_PER_BUS = 10

    # Generation strategy
    TARGET_CONSUMPTION_FACTOR_MIN = 1.2  # Ensure charging is needed
    TARGET_CONSUMPTION_FACTOR_MAX = 1.5  # Feasibility bound

    # =========================================================================
    # VALIDATION PARAMETERS
    # =========================================================================
    SOLVER_TIMEOUT = 600000  # 600 seconds = 10 minutes (milliseconds)
    VALIDATION_ATTEMPTS = 1000  # Iterate until SAT instance found (1000 = "infinite" for practical purposes)

    # =========================================================================
    # UI COLORS
    # =========================================================================
    COLOR_DARK_BLUE = "#1e3a5f"
    COLOR_LIGHT_BLUE = "#4a90e2"
    COLOR_WHITE = "#ffffff"
    COLOR_LIGHT_GRAY = "#f5f5f5"
    COLOR_GRAY = "#cccccc"
    COLOR_SUCCESS = "#28a745"
    COLOR_ERROR = "#dc3545"
    COLOR_WARNING = "#ffc107"
    COLOR_INFO = "#17a2b8"
