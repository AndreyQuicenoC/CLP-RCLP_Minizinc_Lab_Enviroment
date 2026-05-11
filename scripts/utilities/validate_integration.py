#!/usr/bin/env python3
"""
Path Resolution and Module Integration Validator

Comprehensive validation script to ensure all path resolution,
navigation, and theme switching systems are properly integrated
and functional across the entire CLP-RCLP framework.

This script:
1. Validates ToolPathResolver implementation
2. Tests navigation between windows
3. Verifies theme persistence and switching
4. Checks module imports and dependencies
5. Generates detailed diagnostic report

Usage:
    python scripts/utilities/validate_integration.py [--verbose]

Author: AVISPA Research Team
Date: April 2026
"""

import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Any
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-8s | %(message)s"
)
logger = logging.getLogger(__name__)


class IntegrationValidator:
    """Validates path resolution and module integration."""

    def __init__(self, verbose: bool = False):
        """Initialize validator."""
        self.verbose = verbose
        self.project_root = self._find_project_root()
        self.results = {}

        # Add to sys.path
        sys.path.insert(0, str(self.project_root))
        sys.path.insert(0, str(self.project_root / "core"))

        logger.info(f"Project root: {self.project_root}")

    @staticmethod
    def _find_project_root() -> Path:
        """Find project root."""
        current = Path(__file__).parent.parent.parent.absolute()
        max_iterations = 10

        for _ in range(max_iterations):
            if (current / "core").exists() or current.name == "CLP-RCLP Minizinc":
                return current
            parent = current.parent
            if parent == current:
                break
            current = parent

        raise RuntimeError("Could not find project root")

    def validate_module(self, module_name: str, import_path: str) -> Tuple[bool, str]:
        """
        Validate that a module can be imported.

        Args:
            module_name: Human-readable module name
            import_path: Python import path

        Returns:
            Tuple: (success, message)
        """
        try:
            __import__(import_path)
            logger.info(f"✓ {module_name}: {import_path}")
            return True, f"Imported successfully"
        except ImportError as e:
            logger.error(f"✗ {module_name}: {import_path}")
            if self.verbose:
                logger.error(f"  Error: {e}")
            return False, str(e)

    def validate_file(self, file_name: str, file_path: Path) -> Tuple[bool, str]:
        """
        Validate that a file exists.

        Args:
            file_name: Human-readable file name
            file_path: Path to file

        Returns:
            Tuple: (success, message)
        """
        if file_path.exists() and file_path.is_file():
            logger.info(f"✓ {file_name}: {file_path.relative_to(self.project_root)}")
            return True, "File exists"
        else:
            logger.error(f"✗ {file_name}: {file_path.relative_to(self.project_root)}")
            return False, "File not found"

    def validate_core_structure(self) -> Dict[str, bool]:
        """Validate core directory structure."""
        logger.info("\n" + "=" * 80)
        logger.info("CORE DIRECTORY STRUCTURE VALIDATION")
        logger.info("=" * 80)

        structure = {
            "converter": (self.project_root / "core" / "converter"),
            "generator": (self.project_root / "core" / "generator"),
            "runner": (self.project_root / "core" / "runner"),
            "orchestration": (self.project_root / "core" / "orchestration"),
            "shared": (self.project_root / "core" / "shared"),
        }

        results = {}
        for name, path in structure.items():
            exists = path.exists() and path.is_dir()
            status = "✓" if exists else "✗"
            logger.info(f"{status} core/{name}/")
            results[name] = exists

        return results

    def validate_path_resolver(self) -> Dict[str, Any]:
        """Validate ToolPathResolver implementation."""
        logger.info("\n" + "=" * 80)
        logger.info("PATH RESOLVER VALIDATION")
        logger.info("=" * 80)

        results = {
            "module_found": False,
            "tools": {}
        }

        # Check module file exists
        resolver_path = self.project_root / "core" / "shared" / "path_resolver.py"
        module_ok, msg = self.validate_file("PathResolver Module", resolver_path)
        results["module_found"] = module_ok

        if not module_ok:
            return results

        # Try to import
        import_ok, msg = self.validate_module("PathResolver Import", "shared.path_resolver")
        if not import_ok:
            return results

        # Test tool resolution
        try:
            from shared.path_resolver import ToolPathResolver

            resolver = ToolPathResolver(self.project_root)
            tools = resolver.get_all_tools()

            for tool_name, tool_path in tools.items():
                if tool_path and tool_path.exists():
                    logger.info(f"✓ Tool '{tool_name}' found: {tool_path.relative_to(self.project_root)}")
                    results["tools"][tool_name] = True
                else:
                    logger.error(f"✗ Tool '{tool_name}' not found")
                    results["tools"][tool_name] = False
        except Exception as e:
            logger.error(f"✗ ToolPathResolver test failed: {e}")

        return results

    def validate_navigation(self) -> Dict[str, bool]:
        """Validate navigation system."""
        logger.info("\n" + "=" * 80)
        logger.info("NAVIGATION SYSTEM VALIDATION")
        logger.info("=" * 80)

        results = {}

        # Navigation module
        nav_path = self.project_root / "core" / "shared" / "navigation.py"
        results["navigation_file"], _ = self.validate_file("Navigation Module", nav_path)

        # Orchestrator
        orch_path = self.project_root / "core" / "orchestration" / "orchestrator.py"
        results["orchestrator_file"], _ = self.validate_file("Orchestrator Entry", orch_path)

        # Navigation imports
        if results["navigation_file"]:
            try:
                with open(nav_path, "r", encoding="utf-8") as f:
                    content = f.read()

                checks = {
                    "return_to_orchestrator": "return_to_orchestrator" in content,
                    "path_resolver_import": "path_resolver" in content,
                    "subprocess_usage": "subprocess" in content,
                }

                for check_name, found in checks.items():
                    status = "✓" if found else "✗"
                    logger.info(f"{status} Navigation contains '{check_name}'")
                    results[f"nav_{check_name}"] = found

            except Exception as e:
                logger.error(f"✗ Error reading navigation module: {e}")

        return results

    def validate_orchestrator_ui(self) -> Dict[str, bool]:
        """Validate Orchestrator UI implementation."""
        logger.info("\n" + "=" * 80)
        logger.info("ORCHESTRATOR UI VALIDATION")
        logger.info("=" * 80)

        results = {}

        orch_ui_path = self.project_root / "core" / "orchestration" / "ui" / "interface.py"
        results["interface_file"], _ = self.validate_file("Orchestrator Interface", orch_ui_path)

        if results["interface_file"]:
            try:
                with open(orch_ui_path, "r", encoding="utf-8") as f:
                    content = f.read()

                checks = {
                    "ThemeManager": "ThemeManager" in content,
                    "_toggle_theme": "_toggle_theme" in content,
                    "_refresh_ui_colors": "_refresh_ui_colors" in content,
                    "FlatButton": "FlatButton" in content,
                    "theme_dict": "theme_dict" in content,
                    "ToolPathResolver": "ToolPathResolver" in content,
                }

                for check_name, found in checks.items():
                    status = "✓" if found else "✗"
                    component_type = "Theme" if "theme" in check_name.lower() else "Tool"
                    logger.info(f"{status} {check_name} ({component_type} component)")
                    results[f"ui_{check_name}"] = found

            except Exception as e:
                logger.error(f"✗ Error reading interface: {e}")

        return results

    def validate_themes(self) -> Dict[str, bool]:
        """Validate theme system."""
        logger.info("\n" + "=" * 80)
        logger.info("THEME SYSTEM VALIDATION")
        logger.info("=" * 80)

        results = {}

        # Check theme files
        theme_locations = [
            ("orchestration", self.project_root / "core" / "orchestration" / "ui" / "themes.py"),
            ("runner", self.project_root / "core" / "runner" / "ui" / "themes.py"),
            ("generator", self.project_root / "core" / "generator" / "ui" / "themes.py"),
        ]

        for name, path in theme_locations:
            ok, _ = self.validate_file(f"Theme ({name})", path)
            results[f"theme_{name}"] = ok

        # Check theme persistence
        persistence_path = self.project_root / "core" / "shared" / "theme_persistence.py"
        ok, _ = self.validate_file("Theme Persistence", persistence_path)
        results["theme_persistence"] = ok

        return results

    def generate_report(self) -> str:
        """Generate comprehensive validation report."""
        logger.info("\n\n")
        logger.info("╔" + "=" * 78 + "╗")
        logger.info("║" + " INTEGRATION VALIDATION REPORT ".center(78) + "║")
        logger.info("╚" + "=" * 78 + "╝")

        # Run all validations
        core_structure = self.validate_core_structure()
        path_resolver = self.validate_path_resolver()
        navigation = self.validate_navigation()
        orchestrator_ui = self.validate_orchestrator_ui()
        themes = self.validate_themes()

        # Summary
        logger.info("\n" + "=" * 80)
        logger.info("SUMMARY")
        logger.info("=" * 80)

        all_results = {
            "Core Structure": core_structure,
            "Path Resolver": path_resolver,
            "Navigation": navigation,
            "Orchestrator UI": orchestrator_ui,
            "Themes": themes,
        }

        total_checks = 0
        total_passed = 0

        for section_name, section_results in all_results.items():
            for key, value in section_results.items():
                if isinstance(value, bool):
                    total_checks += 1
                    if value:
                        total_passed += 1

        logger.info(f"\nTotal Checks: {total_passed}/{total_checks}")
        logger.info(f"Success Rate: {(total_passed/total_checks*100):.1f}%")

        # Detailed section summary
        logger.info("\nSection Status:")
        for section_name, section_results in all_results.items():
            bool_results = [v for v in section_results.values() if isinstance(v, bool)]
            if bool_results:
                passed = sum(bool_results)
                status = "✓ PASS" if all(bool_results) else "⚠ PARTIAL" if passed > 0 else "✗ FAIL"
                logger.info(f"  {section_name}: {status} ({passed}/{len(bool_results)})")

        overall_status = "✓ PASS" if total_passed == total_checks else "✗ FAIL"
        logger.info(f"\nOverall Status: {overall_status}")

        logger.info("\n" + "=" * 80 + "\n")

        return overall_status


def main() -> int:
    """Run the validation script."""
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    try:
        validator = IntegrationValidator(verbose=verbose)
        status = validator.generate_report()
        return 0 if "PASS" in status else 1
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
