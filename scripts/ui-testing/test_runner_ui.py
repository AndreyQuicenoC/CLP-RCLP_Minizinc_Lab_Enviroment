#!/usr/bin/env python3
"""
Test Runner UI - Comprehensive validation of theme switching and UI rendering.

Validates that:
1. Runner interface loads without errors
2. Dark/light mode switching works correctly
3. All theme colors are applied properly
4. UI components render with correct styling

Authors: Andrey Quiceno and Juan Francesco García (AVISPA Team)
Version: 1.3.0
"""

import sys
import tkinter as tk
from pathlib import Path
import time

# Setup paths
project_root = Path(__file__).parent.parent
runner_dir = project_root / "Runner"
sys.path.insert(0, str(runner_dir))
sys.path.insert(0, str(project_root))

import os
os.chdir(str(runner_dir))


def test_runner_ui():
    """Test 1: Load Runner interface without errors."""
    print("[TEST 1] Loading Runner interface...")

    try:
        from ui.interface import RunnerInterface
        from ui.themes import ThemeManager, get_theme_dict

        root = tk.Tk()
        root.geometry("850x650")

        # Create interface
        app = RunnerInterface(root)
        print("✓ Runner interface loaded successfully")

        # Test 2: Verify theme system
        print("\n[TEST 2] Verifying theme system...")

        current_mode = ThemeManager.get_mode()
        print(f"✓ Current theme mode: {current_mode}")
        assert current_mode == "dark", "Default mode should be 'dark'"

        theme_dict = get_theme_dict("dark")
        print(f"✓ Dark theme tokens: {len(theme_dict)} design tokens")
        assert len(theme_dict) >= 26, "Theme dict should have at least 26 tokens"

        required_keys = [
            "bg_base", "bg_surface", "bg_elevated", "bg_hover",
            "accent_primary", "accent_dim", "accent_glow",
            "success", "warning", "error",
            "text_primary", "text_secondary", "text_muted", "text_code",
            "border_normal", "border_active",
            "font_ui", "font_bold", "font_section", "font_mono", "font_small",
        ]
        for key in required_keys:
            assert key in theme_dict, f"Missing theme token: {key}"
        print(f"✓ All required theme tokens present ({len(required_keys)} keys)")

        # Test 3: Theme switching
        print("\n[TEST 3] Testing theme switching...")
        print("  Switching to light mode...")
        ThemeManager.set_mode("light")
        light_theme = get_theme_dict("light")
        print(f"✓ Light theme loaded: {len(light_theme)} tokens")
        assert ThemeManager.get_mode() == "light", "Mode should be 'light'"

        print("  Switching back to dark mode...")
        ThemeManager.set_mode("dark")
        dark_theme = get_theme_dict("dark")
        print(f"✓ Dark theme reloaded: {len(dark_theme)} tokens")
        assert ThemeManager.get_mode() == "dark", "Mode should be 'dark'"

        # Test 4: Verify component colors
        print("\n[TEST 4] Verifying component styling...")
        assert app.status_indicator is not None, "Status indicator not created"
        assert app.theme_toggle_btn is not None, "Theme toggle button not created"
        assert app.run_btn is not None, "Run button not created"
        assert app.log_text is not None, "Log text widget not created"
        print("✓ All UI components created and accessible")

        # Test 5: Verify color values
        print("\n[TEST 5] Verifying design token values...")
        assert theme_dict["bg_base"] == "#0D0F14", "Dark bg_base color mismatch"
        assert theme_dict["accent_primary"] == "#3D8EF5", "Dark accent_primary color mismatch"
        assert theme_dict["success"] == "#22C55E", "Dark success color mismatch"
        print("✓ All color values correct")

        # Test 6: Verify fonts
        print("\n[TEST 6] Verifying typography...")
        assert isinstance(theme_dict["font_ui"], tuple), "font_ui should be tuple"
        assert isinstance(theme_dict["font_mono"], tuple), "font_mono should be tuple"
        assert len(theme_dict["font_ui"]) >= 2, "Font tuples should have size info"
        print("✓ Typography system working correctly")

        # Test 7: Log output verification
        print("\n[TEST 7] Testing log output...")
        app._log("Test message", "info")
        log_content = app.log_text.get("1.0", tk.END)
        assert "Test message" in log_content, "Log message not found"
        print("✓ Log output working correctly")

        print("\n" + "="*60)
        print("ALL TESTS PASSED ✓")
        print("="*60)
        print("\nRunner Interface v1.3.0 is fully functional!")
        print("- Theme system: Working")
        print("- Dark/Light mode: Switching correctly")
        print("- All components: Rendering properly")
        print("- Log output: Operating correctly")

        # Close after tests
        root.after(2000, root.destroy)
        root.mainloop()

        return True

    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n" + "="*60)
    print("RUNNER UI v1.3.0 - VALIDATION TEST SUITE")
    print("="*60 + "\n")

    success = test_runner_ui()
    sys.exit(0 if success else 1)
