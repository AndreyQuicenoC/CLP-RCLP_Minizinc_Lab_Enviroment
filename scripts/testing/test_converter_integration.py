#!/usr/bin/env python3
"""
Converter Integration Test Script

Tests file management, directory structure creation, and batch conversion.

Usage:
    python Scripts/testing/test_converter_integration.py

Author: AVISPA Research Team
Date: April 2026
"""

import sys
import shutil
import logging
from pathlib import Path
from typing import Tuple

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def get_project_root() -> Path:
    """Find project root directory."""
    # Scripts/testing/test_converter_integration.py -> project root is 3 levels up
    current = Path(__file__).parent.parent.parent.absolute()
    return current


def test_integration() -> Tuple[bool, str]:
    """
    Test full converter integration: file management and batch conversion.

    Returns:
        (success: bool, message: str)
    """
    try:
        import importlib.util

        project_root = get_project_root()

        # Load converter modules
        converter_engine_path = project_root / "Converter" / "core" / "converter_engine.py"
        file_manager_path = project_root / "Converter" / "core" / "file_manager.py"
        jits_analyzer_path = project_root / "Converter" / "core" / "jits_analyzer.py"

        # Load converter_engine
        spec = importlib.util.spec_from_file_location("converter_engine", converter_engine_path)
        converter_engine_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(converter_engine_module)
        ConverterEngine = converter_engine_module.ConverterEngine

        # Load file_manager
        spec = importlib.util.spec_from_file_location("file_manager", file_manager_path)
        file_manager_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(file_manager_module)
        FileManager = file_manager_module.FileManager

        # Load jits_analyzer
        spec = importlib.util.spec_from_file_location("jits_analyzer", jits_analyzer_path)
        jits_analyzer_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(jits_analyzer_module)
        JITSAnalyzer = jits_analyzer_module.JITSAnalyzer

        logger.info("=" * 80)
        logger.info("CONVERTER INTEGRATION TEST")
        logger.info("=" * 80)

        # Create test output directory
        test_battery = project_root / "Data" / "_Test_Converter_Integration"
        if test_battery.exists():
            shutil.rmtree(test_battery)

        logger.info(f"Testing output structure creation...")

        # Setup
        jits_path = project_root / "JITS2022" / "Code" / "Data"
        directories = JITSAnalyzer.get_test_directories(jits_path)

        if not directories:
            return False, "No test directories found in JITS2022"

        test_dir_name = directories[0]
        test_dir = jits_path / test_dir_name

        # Test 1: Create output structure
        logger.info(f"Test 1: Creating output structure for {test_dir_name}...")

        success, output_path = FileManager.create_output_structure(
            test_battery,
            test_dir_name,
            test_dir
        )

        if not success:
            return False, "Failed to create output structure"

        if not output_path.exists():
            return False, "Output path does not exist after creation"

        logger.info(f"✓ Output structure created: {output_path}")

        # Check support files were copied
        support_files_found = 0
        for filename in ["distances_input.csv", "stations_input.csv", "input_report.txt"]:
            if (output_path / filename).exists():
                support_files_found += 1
                logger.info(f"✓ Support file copied: {filename}")

        if support_files_found > 0:
            logger.info(f"✓ {support_files_found} support files copied")

        # Test 2: Batch conversion
        logger.info(f"Test 2: Batch converting JSON files...")

        json_files = JITSAnalyzer.get_json_files(test_dir, "buses_input_*.json")
        if not json_files:
            return False, "No JSON files found to convert"

        logger.info(f"Found {len(json_files)} JSON files to convert")

        success_count, failure_count, messages = ConverterEngine.batch_convert_files(
            json_files[:3],  # Test with first 3 files
            output_path
        )

        logger.info(f"Conversion results:")
        logger.info(f"  - Successful: {success_count}")
        logger.info(f"  - Failed: {failure_count}")

        for msg in messages[:5]:  # Show first 5 messages
            logger.info(f"  {msg}")

        if success_count == 0:
            return False, "No files were converted successfully"

        # Test 3: Verify output files
        logger.info(f"Test 3: Verifying output files...")

        dzn_files = list(output_path.glob("*.dzn"))
        logger.info(f"✓ Found {len(dzn_files)} DZN files")

        for dzn_file in dzn_files[:3]:  # Check first 3
            size = dzn_file.stat().st_size
            logger.info(f"  - {dzn_file.name}: {size} bytes")

            if size < 1000:
                return False, f"DZN file too small: {dzn_file.name}"

        # Test 4: Validate path operations
        logger.info(f"Test 4: Testing path operations...")

        # Test solver directory
        solver_dir = FileManager.ensure_solver_dir(output_path, "Chuffed")
        if not solver_dir.exists():
            return False, "Solver directory creation failed"

        logger.info(f"✓ Solver directory created: {solver_dir.name}")

        # Test path validation
        is_writable = FileManager.validate_output_path(output_path)
        if not is_writable:
            return False, "Output path validation failed"

        logger.info(f"✓ Output path is writable")

        # Cleanup
        logger.info(f"Cleaning up test data...")
        shutil.rmtree(test_battery)

        logger.info("=" * 80)
        logger.info("ALL INTEGRATION TESTS PASSED ✓")
        logger.info("=" * 80)

        return True, "Integration test successful"

    except Exception as e:
        logger.error(f"Integration test failed: {e}", exc_info=True)
        return False, f"Exception: {str(e)}"


def main():
    """Run integration test."""
    success, message = test_integration()

    if success:
        logger.info(message)
        sys.exit(0)
    else:
        logger.error(message)
        sys.exit(1)


if __name__ == "__main__":
    main()
