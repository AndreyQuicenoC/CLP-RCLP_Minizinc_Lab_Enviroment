"""
Solver Configuration and Management

Defines available solvers, their properties, and execution parameters.
Provides solver selection and validation logic.

Supported Solvers:
- chuffed: Default constraint solver (fast, good for most problems)
- gecode: General-purpose constraint programming solver
- coin-bc: Linear/mixed-integer programming solver
- globalizer: Global optimization solver
- cplex: IBM CPLEX (commercial, high-performance)
- gurobi: Gurobi optimization engine (commercial, high-performance)

Authors: Andrey Quiceno and Juan Francesco García (AVISPA Team)
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum


class SolverType(Enum):
    """Available solver types."""
    CHUFFED = "chuffed"
    GECODE = "gecode"
    COIN_BC = "coin-bc"
    GLOBALIZER = "globalizer"
    CPLEX = "cplex"
    GUROBI = "gurobi"


@dataclass
class SolverInfo:
    """Comprehensive solver information and metadata."""
    type: SolverType
    display_name: str
    description: str
    strengths: List[str]
    use_cases: List[str]
    commercial: bool
    availability_status: str  # 'available', 'not_installed', 'checking'


# Solver information database for UI tooltips and information dialogs
SOLVER_DATABASE: Dict[SolverType, SolverInfo] = {
    SolverType.CHUFFED: SolverInfo(
        type=SolverType.CHUFFED,
        display_name="Chuffed",
        description="Default constraint solver optimized for satisfaction problems",
        strengths=[
            "Fast constraint solving",
            "Excellent for CLP/RCLP problems",
            "Low memory footprint",
            "Minimal configuration needed"
        ],
        use_cases=[
            "Constraint satisfaction problems (CSP)",
            "Combinatorial optimization",
            "Feasibility checking",
            "Rapid prototyping"
        ],
        commercial=False,
        availability_status="available"
    ),
    SolverType.GECODE: SolverInfo(
        type=SolverType.GECODE,
        display_name="Gecode",
        description="General-purpose constraint programming solver with strong optimization capabilities",
        strengths=[
            "Robust constraint propagation",
            "Good for medium-sized problems",
            "Excellent documentation",
            "Active development community"
        ],
        use_cases=[
            "Constraint programming problems",
            "Scheduling problems",
            "Resource allocation",
            "N-queens and related combinatorial problems"
        ],
        commercial=False,
        availability_status="available"
    ),
    SolverType.COIN_BC: SolverInfo(
        type=SolverType.COIN_BC,
        display_name="COIN-BC",
        description="Linear and Mixed-Integer Programming solver",
        strengths=[
            "Efficient for linear/MIP problems",
            "Good branch-and-cut implementation",
            "Open-source and reliable",
            "Well-established in academic use"
        ],
        use_cases=[
            "Linear programming (LP)",
            "Mixed-integer programming (MIP)",
            "Network flow problems",
            "Production planning problems"
        ],
        commercial=False,
        availability_status="available"
    ),
    SolverType.GLOBALIZER: SolverInfo(
        type=SolverType.GLOBALIZER,
        display_name="Globalizer",
        description="Global optimization solver for non-convex problems",
        strengths=[
            "Global optimization capability",
            "Handles non-convex problems",
            "Deterministic search algorithms",
            "Rigorous bounds computation"
        ],
        use_cases=[
            "Global optimization",
            "Non-convex optimization",
            "Problems requiring global optimality certificates",
            "Bound-tight optimization"
        ],
        commercial=False,
        availability_status="available"
    ),
    SolverType.CPLEX: SolverInfo(
        type=SolverType.CPLEX,
        display_name="CPLEX",
        description="IBM CPLEX - Industry-leading commercial optimization solver",
        strengths=[
            "Highest performance on large-scale problems",
            "Advanced presolve and heuristics",
            "MIP callback functionality",
            "Enterprise support available"
        ],
        use_cases=[
            "Large-scale optimization",
            "Enterprise production systems",
            "Time-sensitive optimization",
            "Complex constraint problems requiring maximum performance"
        ],
        commercial=True,
        availability_status="not_installed"
    ),
    SolverType.GUROBI: SolverInfo(
        type=SolverType.GUROBI,
        display_name="Gurobi",
        description="Gurobi - Cutting-edge commercial optimization engine",
        strengths=[
            "State-of-the-art performance",
            "Multi-threading support",
            "Advanced warm-start capabilities",
            "Responsive commercial support"
        ],
        use_cases=[
            "Cutting-edge optimization",
            "Problems requiring latest algorithms",
            "Multi-threaded computation",
            "High-performance enterprise optimization"
        ],
        commercial=True,
        availability_status="not_installed"
    ),
}


class SolverManager:
    """Manage solver selection and validation."""

    # Default solver if not specified
    DEFAULT_SOLVER = SolverType.CHUFFED

    # Solvers compatible with MiniZinc
    MINIZINC_COMPATIBLE = {
        SolverType.CHUFFED,
        SolverType.GECODE,
        SolverType.COIN_BC,
        SolverType.GLOBALIZER,
        SolverType.CPLEX,
        SolverType.GUROBI
    }

    @staticmethod
    def get_solver_info(solver: SolverType) -> SolverInfo:
        """Get detailed information about a solver."""
        return SOLVER_DATABASE[solver]

    @staticmethod
    def get_display_name(solver: SolverType) -> str:
        """Get display name for a solver."""
        return SOLVER_DATABASE[solver].display_name

    @staticmethod
    def get_available_solvers() -> List[SolverType]:
        """Get list of all available solver types."""
        return list(SOLVER_DATABASE.keys())

    @staticmethod
    def get_solver_by_name(name: str) -> Optional[SolverType]:
        """Get solver type from string name."""
        try:
            return SolverType(name)
        except ValueError:
            return None

    @staticmethod
    def is_commercial(solver: SolverType) -> bool:
        """Check if solver is commercial."""
        return SOLVER_DATABASE[solver].commercial

    @staticmethod
    def get_minizinc_solver_name(solver: SolverType) -> str:
        """Get the MiniZinc command-line solver name for a given solver."""
        return solver.value  # The enum values are already the MiniZinc names
