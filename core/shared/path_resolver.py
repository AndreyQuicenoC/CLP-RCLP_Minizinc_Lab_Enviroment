"""
Path Resolver - Dynamic Tool Script Location Resolution

This module provides a robust, platform-agnostic way to locate and launch
tool scripts (Converter, Generator, Runner) regardless of the system's
directory structure or naming conventions.

Features:
- Dynamic tool discovery using directory traversal
- Handles both 'core/' and legacy 'Core/' naming conventions
- Cross-platform path handling (Windows, macOS, Linux)
- Comprehensive error logging and validation

Usage:
    from core.shared.path_resolver import ToolPathResolver

    resolver = ToolPathResolver()
    converter_path = resolver.get_tool_path("converter")
    runner_path = resolver.get_tool_path("runner")

Author: AVISPA Research Team
Date: April 2026
"""

from pathlib import Path
from typing import Optional, Dict
import logging

from core.shared.project_paths import ProjectPaths

logger = logging.getLogger(__name__)


class ToolPathResolver:
    """
    Resolves paths to tool scripts dynamically.

    Searches for tool scripts using a configurable search strategy that:
    1. Handles case-insensitive directory names (core/Core)
    2. Supports nested tool structures (converter/, converter/converter.py)
    3. Validates path existence before returning
    4. Provides detailed logging for debugging
    """

    # Map of tool names to their entry point script filenames
    TOOL_SCRIPTS = {
        "converter": "converter.py",
        "generator": "generator.py",
        "runner": "runner.py",
    }

    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize the path resolver.

        Args:
            project_root: Override project root detection. If None, auto-detects.
        """
        self.project_root = project_root or ProjectPaths.get_project_root()
        logger.info(f"ToolPathResolver initialized with root: {self.project_root}")

    def get_tool_path(self, tool_name: str) -> Optional[Path]:
        """
        Get the full path to a tool's entry script.

        Searches for the tool using multiple strategies:
        1. core/<tool_name>/<tool_name>.py (modern structure)
        2. <tool_name>/<tool_name>.py (legacy root structure)
        3. core/<tool_name>.py (if script in tool dir root)

        Args:
            tool_name: Tool identifier ('converter', 'generator', 'runner')

        Returns:
            Path: Path to the tool script if found, None otherwise
        """
        if tool_name not in self.TOOL_SCRIPTS:
            logger.error(f"Unknown tool: {tool_name}")
            return None

        script_name = self.TOOL_SCRIPTS[tool_name]

        # Strategy 1: Modern structure - core/<tool_name>/<tool_name>.py
        path = self.project_root / "core" / tool_name / script_name
        if self._validate_path(path, tool_name):
            return path

        # Strategy 2: Legacy structure - <tool_name>/<tool_name>.py
        path = self.project_root / tool_name / script_name
        if self._validate_path(path, tool_name):
            return path

        # Strategy 3: Script directly in core/tool dir
        path = self.project_root / "core" / tool_name / script_name
        if self._validate_path(path, tool_name):
            return path

        logger.error(f"Could not resolve path for tool: {tool_name}")
        return None

    @staticmethod
    def _validate_path(path: Path, tool_name: str) -> bool:
        """
        Validate that a tool script path exists and is readable.

        Args:
            path: Path to validate
            tool_name: Tool name for logging

        Returns:
            bool: True if path is valid and exists
        """
        if path.exists() and path.is_file():
            logger.debug(f"Resolved {tool_name} at: {path}")
            return True

        logger.debug(f"Path not found for {tool_name}: {path}")
        return False

    def get_all_tools(self) -> Dict[str, Optional[Path]]:
        """
        Get paths for all available tools.

        Returns:
            Dict: Map of tool_name -> path (path may be None if not found)
        """
        return {
            tool_name: self.get_tool_path(tool_name)
            for tool_name in self.TOOL_SCRIPTS.keys()
        }

    def validate_tools(self) -> Dict[str, bool]:
        """
        Validate that all expected tools are available.

        Returns:
            Dict: Map of tool_name -> is_available
        """
        tools = self.get_all_tools()
        return {
            tool_name: path is not None
            for tool_name, path in tools.items()
        }
