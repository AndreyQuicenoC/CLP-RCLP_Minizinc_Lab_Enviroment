"""
Converter Fidelity Verification Script

Compares DZN output from Converter against reference values from JITS2022.
Validates that D, T, and schedule parameters match within tolerance.

Author: AVISPA Research Team
Date: April 2026
"""

import re
import logging
from pathlib import Path
from typing import Dict, Tuple, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class DZNMetrics:
    """Extracted metrics from a DZN file."""
    num_buses: int
    num_stations: int
    max_stops: int
    D: List[List[int]]
    T: List[List[int]]
    tau_bi: List[List[int]]
    st_bi: List[List[int]]


class DZNParser:
    """Parse MiniZinc DZN files and extract metrics."""

    @staticmethod
    def parse_array2d(content: str, pattern: str) -> List[List[int]]:
        """
        Parse an array2d declaration from DZN.

        Args:
            content: Full DZN content
            pattern: Pattern name (e.g., 'D', 'T', 'tau_bi')

        Returns:
            2D list of integers
        """
        # Find the array declaration
        regex = rf"{pattern}\s*=\s*array2d\(1\.\.(\d+),\s*1\.\.(\d+),\s*\[(.*?)\]\);"
        match = re.search(regex, content, re.DOTALL)

        if not match:
            logger.warning(f"Could not find array {pattern} in DZN")
            return []

        rows = int(match.group(1))
        cols = int(match.group(2))
        values_str = match.group(3)

        # Extract numbers
        numbers = re.findall(r'[-]?\d+', values_str)
        numbers = [int(n) for n in numbers]

        # Reshape into 2D array
        if len(numbers) != rows * cols:
            logger.warning(f"Expected {rows * cols} values for {pattern}, got {len(numbers)}")

        result = []
        for i in range(rows):
            row = numbers[i * cols:(i + 1) * cols]
            result.append(row)

        return result

    @staticmethod
    def parse_scalar(content: str, name: str) -> int:
        """
        Parse a scalar value from DZN.

        Args:
            content: Full DZN content
            name: Variable name (e.g., 'num_buses', 'Cmax')

        Returns:
            Integer value
        """
        regex = rf"{name}\s*=\s*([-]?\d+)\s*;"
        match = re.search(regex, content)

        if not match:
            logger.warning(f"Could not find {name} in DZN")
            return 0

        return int(match.group(1))

    @staticmethod
    def parse_dzn(dzn_file: Path) -> Optional[DZNMetrics]:
        """
        Parse a DZN file and extract all metrics.

        Args:
            dzn_file: Path to .dzn file

        Returns:
            DZNMetrics or None if parsing failed
        """
        try:
            with open(dzn_file, 'r', encoding='utf-8') as f:
                content = f.read()

            num_buses = DZNParser.parse_scalar(content, 'num_buses')
            num_stations = DZNParser.parse_scalar(content, 'num_stations')
            max_stops = DZNParser.parse_scalar(content, 'max_stops')

            D = DZNParser.parse_array2d(content, 'D')
            T = DZNParser.parse_array2d(content, 'T')
            tau_bi = DZNParser.parse_array2d(content, 'tau_bi')
            st_bi = DZNParser.parse_array2d(content, 'st_bi')

            return DZNMetrics(
                num_buses=num_buses,
                num_stations=num_stations,
                max_stops=max_stops,
                D=D,
                T=T,
                tau_bi=tau_bi,
                st_bi=st_bi
            )

        except Exception as e:
            logger.error(f"Error parsing {dzn_file}: {e}")
            return None


class VerifyConverterFidelity:
    """Verify converter output against reference DZN."""

    # Tolerance for numeric comparisons (±1%)
    TOLERANCE_PERCENT = 1.0

    @staticmethod
    def compare_scalars(name: str, ref_value: int, gen_value: int, tolerance_pct: float = 1.0) -> Tuple[bool, str]:
        """
        Compare two scalar values with tolerance.

        Args:
            name: Field name
            ref_value: Reference value
            gen_value: Generated value
            tolerance_pct: Tolerance percentage

        Returns:
            (matches: bool, message: str)
        """
        if ref_value == 0:
            match = ref_value == gen_value
            return match, f"{name}: {gen_value} (expected {ref_value})" + (" ✓" if match else " ✗")

        tolerance = max(1, int(ref_value * tolerance_pct / 100))
        diff = abs(ref_value - gen_value)
        match = diff <= tolerance

        return match, f"{name}: {gen_value} (expected {ref_value}, diff={diff})" + (" ✓" if match else " ✗")

    @staticmethod
    def compare_arrays(name: str, ref_array: List[List[int]], gen_array: List[List[int]],
                      tolerance_pct: float = 1.0) -> Tuple[bool, str, List[str]]:
        """
        Compare two 2D arrays with tolerance.

        Args:
            name: Field name
            ref_array: Reference array
            gen_array: Generated array
            tolerance_pct: Tolerance percentage

        Returns:
            (matches: bool, summary: str, mismatches: List[str])
        """
        mismatches = []

        if len(ref_array) != len(gen_array):
            return False, f"{name}: Bus count mismatch ({len(gen_array)} vs {len(ref_array)})", mismatches

        if not ref_array:
            return True, f"{name}: Empty array ✓", []

        for bus_idx, (ref_row, gen_row) in enumerate(zip(ref_array, gen_array)):
            if len(ref_row) != len(gen_row):
                mismatches.append(f"Bus {bus_idx}: Column count mismatch ({len(gen_row)} vs {len(ref_row)})")
                continue

            for stop_idx, (ref_val, gen_val) in enumerate(zip(ref_row, gen_row)):
                if ref_val == 0 and gen_val == 0:
                    continue

                if ref_val == 0:
                    # Expected 0 but got non-zero
                    mismatches.append(f"{name}[{bus_idx},{stop_idx}]: {gen_val} (expected 0)")
                    continue

                tolerance = max(1, int(ref_val * tolerance_pct / 100))
                diff = abs(ref_val - gen_val)

                if diff > tolerance:
                    mismatches.append(f"{name}[{bus_idx},{stop_idx}]: {gen_val} (expected {ref_val}, diff={diff})")

        match = len(mismatches) == 0
        summary = f"{name}: {len(mismatches)} mismatches" + (" ✓" if match else f" ✗ ({len(mismatches)} errors)")

        return match, summary, mismatches

    @staticmethod
    def verify(ref_dzn: Path, gen_dzn: Path, tolerance_pct: float = 1.0) -> Tuple[bool, Dict]:
        """
        Verify that generated DZN matches reference DZN.

        Args:
            ref_dzn: Path to reference DZN file
            gen_dzn: Path to generated DZN file
            tolerance_pct: Tolerance percentage for numeric comparisons

        Returns:
            (all_match: bool, report: Dict with detailed results)
        """
        report = {
            'passed': False,
            'ref_file': str(ref_dzn),
            'gen_file': str(gen_dzn),
            'results': {},
            'mismatches': []
        }

        # Parse DZN files
        ref_metrics = DZNParser.parse_dzn(ref_dzn)
        gen_metrics = DZNParser.parse_dzn(gen_dzn)

        if not ref_metrics or not gen_metrics:
            logger.error("Failed to parse DZN files")
            return False, report

        all_match = True

        # Compare scalars
        for name in ['num_buses', 'num_stations', 'max_stops']:
            ref_val = getattr(ref_metrics, name)
            gen_val = getattr(gen_metrics, name)
            match, msg = VerifyConverterFidelity.compare_scalars(name, ref_val, gen_val, tolerance_pct)
            report['results'][name] = {'match': match, 'message': msg}
            all_match = all_match and match

        # Compare arrays
        for array_name in ['D', 'T', 'tau_bi', 'st_bi']:
            ref_array = getattr(ref_metrics, array_name)
            gen_array = getattr(gen_metrics, array_name)
            match, summary, mismatches = VerifyConverterFidelity.compare_arrays(
                array_name, ref_array, gen_array, tolerance_pct
            )
            report['results'][array_name] = {
                'match': match,
                'message': summary,
                'mismatch_count': len(mismatches)
            }
            if mismatches:
                report['mismatches'].extend(mismatches[:10])  # Show first 10 mismatches
            all_match = all_match and match

        report['passed'] = all_match
        return all_match, report

    @staticmethod
    def print_report(report: Dict) -> None:
        """
        Print verification report to console.

        Args:
            report: Report dictionary from verify()
        """
        print("\n" + "=" * 80)
        print("CONVERTER FIDELITY VERIFICATION REPORT")
        print("=" * 80)

        print(f"\nReference: {report['ref_file']}")
        print(f"Generated: {report['gen_file']}")

        print("\n--- RESULTS ---")
        for name, result in report['results'].items():
            status = "✓ PASS" if result.get('match') else "✗ FAIL"
            print(f"  {status}: {result['message']}")

        if report['mismatches']:
            print("\n--- MISMATCHES (first 10) ---")
            for mismatch in report['mismatches']:
                print(f"  {mismatch}")

        print("\n" + "=" * 80)
        if report['passed']:
            print("OVERALL: ✓ ALL CHECKS PASSED")
        else:
            print("OVERALL: ✗ SOME CHECKS FAILED")
        print("=" * 80 + "\n")


if __name__ == "__main__":
    # Example usage
    import sys

    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) < 3:
        print("Usage: python verify_converter_fidelity.py <ref_dzn> <gen_dzn> [tolerance_pct]")
        print("Example: python verify_converter_fidelity.py ref.dzn generated.dzn 1.0")
        sys.exit(1)

    ref_file = Path(sys.argv[1])
    gen_file = Path(sys.argv[2])
    tolerance = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0

    passed, report = VerifyConverterFidelity.verify(ref_file, gen_file, tolerance)
    VerifyConverterFidelity.print_report(report)

    sys.exit(0 if passed else 1)
