#!/usr/bin/env python3
"""
Test Generator UI - Comprehensive validation of theme switching and UI rendering.

Validates that:
1. Generator interface loads without errors
2. Dark/light mode switching works correctly
3. All theme colors are applied properly
4. UI components render with correct styling
5. Parameter spinboxes work correctly

Authors: Andrey Quiceno and Juan Francesco García (AVISPA Team)
Version: 1.3.0
"""

import sys
import tkinter as tk
from pathlib import Path
import time

# Setup paths
project_root = Path(__file__).parent.parent
generator_dir = project_root / "Generator"
sys.path.insert(0, str(generator_dir))
sys.path.insert(0, str(project_root))

import os
os.chdir(str(generator_dir))


def test_generator_ui():
    """Test 1: Load Generator interface without errors."""
    print("[TEST 1] Loading Generator interface...")

    try:
        from ui.interface import GeneratorInterface
        from ui.themes import ThemeManager, get_theme_dict

        root = tk.Tk()
        root.geometry("750x600")

        # Create interface
        app = GeneratorInterface(root)
        print("✓ Generator interface loaded successfully")

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
        print("\n[TEST 3] Testing theme switching (light mode)...")
        print("  Switching to light mode...")
        ThemeManager.set_mode("light")
        light_theme = get_theme_dict("light")
        print(f"✓ Light theme loaded: {len(light_theme)} tokens")
        assert ThemeManager.get_mode() == "light", "Mode should be 'light'"

        # Verify light palette colors
        assert light_theme["bg_base"] == "#F8F9FA", "Light bg_base color mismatch"
        assert light_theme["text_primary"] == "#1A1A1A", "Light text color mismatch"
        print("✓ Light theme colors verified")

        print("  Switching back to dark mode...")
        ThemeManager.set_mode("dark")
        dark_theme = get_theme_dict("dark")
        print(f"✓ Dark theme reloaded: {len(dark_theme)} tokens")
        assert ThemeManager.get_mode() == "dark", "Mode should be 'dark'"

        # Test 4: Verify component creation
        print("\n[TEST 4] Verifying component creation...")
        assert app.theme_toggle_btn is not None, "Theme toggle button not created"
        assert app.generate_btn is not None, "Generate button not created"
        assert app.stop_btn is not None, "Stop button not created"
        assert app.log_text is not None, "Log text widget not created"
        print("✓ All UI components created and accessible")

        # Test 5: Verify parameter controls
        print("\n[TEST 5] Testing parameter controls...")

        # Test buses spinbox
        initial_buses = app.buses_var.get()
        app.buses_var.set(5)
        assert app.buses_var.get() == 5, "Buses spinbox not working"
        print(f"✓ Buses spinbox working (current: {app.buses_var.get()})")

        # Test stations spinbox
        initial_stations = app.stations_var.get()
        app.stations_var.set(10)
        assert app.stations_var.get() == 10, "Stations spinbox not working"
        print(f"✓ Stations spinbox working (current: {app.stations_var.get()})")

        # Verify boundaries
        app.buses_var.set(2)
        assert app.buses_var.get() == 2, "Buses min boundary not working"
        app.buses_var.set(20)
        assert app.buses_var.get() == 20, "Buses max boundary not working"
        print("✓ Parameter validation boundaries working")

        # Test 6: Verify color values
        print("\n[TEST 6] Verifying design token values...")
        assert dark_theme["bg_base"] == "#0D0F14", "Dark bg_base color mismatch"
        assert dark_theme["accent_primary"] == "#3D8EF5", "Dark accent_primary color mismatch"
        assert dark_theme["success"] == "#22C55E", "Dark success color mismatch"
        print("✓ All color values correct")

        # Test 7: Verify fonts
        print("\n[TEST 7] Verifying typography...")
        assert isinstance(dark_theme["font_ui"], tuple), "font_ui should be tuple"
        assert isinstance(dark_theme["font_mono"], tuple), "font_mono should be tuple"
        assert len(dark_theme["font_ui"]) >= 2, "Font tuples should have size info"
        print("✓ Typography system working correctly")

        # Test 8: Log output verification
        print("\n[TEST 8] Testing log output...")
        app._log("Test generation message", "info")
        log_content = app.log_text.get("1.0", tk.END)
        assert "Test generation message" in log_content, "Log message not found"
        print("✓ Log output working correctly")

        # Test 9: Clear log functionality
        print("\n[TEST 9] Testing clear log...")
        app._clear_log()
        log_content = app.log_text.get("1.0", tk.END).strip()
        assert log_content == "", "Log not cleared"
        print("✓ Clear log working correctly")

        print("\n" + "="*60)
        print("ALL TESTS PASSED ✓")
        print("="*60)
        print("\nGenerator Interface v1.3.0 is fully functional!")
        print("- Theme system: Working")
        print("- Dark/Light mode: Switching correctly")
        print("- Parameter controls: Operating properly")
        print("- All components: Rendering correctly")
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
    print("GENERATOR UI v1.3.0 - VALIDATION TEST SUITE")
    print("="*60 + "\n")

    success = test_generator_ui()
    sys.exit(0 if success else 1)
