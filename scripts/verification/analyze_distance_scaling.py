"""
Distance Scaling Analysis and Validation

Analyzes distances_input.csv to determine optimal SCALE factor
and detect potential precision loss in conversion.

Usage: python analyze_distance_scaling.py <distances_input.csv>
"""

import csv
from pathlib import Path
from typing import List, Tuple
import statistics


def analyze_distances(csv_file: Path) -> Tuple[List[float], dict]:
    """Load and analyze distances from CSV."""
    distances = []

    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header

        for row in reader:
            if len(row) >= 3:
                try:
                    distance_km = float(row[2])
                    distances.append(distance_km)
                except ValueError:
                    pass

    # Remove duplicates (symmetric matrix)
    distances = list(set(distances))
    distances.sort()

    stats = {
        'count': len(distances),
        'min': min(distances),
        'max': max(distances),
        'mean': statistics.mean(distances),
        'median': statistics.median(distances),
        'stdev': statistics.stdev(distances) if len(distances) > 1 else 0,
    }

    return distances, stats


def calculate_optimal_scale(distances: List[float], min_precision: float = 0.01) -> int:
    """
    Calculate optimal SCALE factor to preserve precision.

    Args:
        distances: List of distance values
        min_precision: Minimum desired precision (in km) to preserve

    Returns:
        Recommended SCALE factor
    """
    if not distances:
        return 10

    min_dist = min(d for d in distances if d > 0)

    # We want scaled_value to be at least large enough to maintain precision
    # If min_dist = 0.265 and min_precision = 0.01, then:
    # min_dist / min_precision = 0.265 / 0.01 = 26.5
    # So SCALE should be ~27 to get at least 26-27 as smallest scaled value

    needed_scale = (min_dist / min_precision)
    scale = max(10, int(needed_scale * 1.5))  # Add 50% margin

    # Round to nearest 5 for cleaner values
    scale = ((scale + 2) // 5) * 5

    return scale


def verify_precision_loss(distances: List[float], scale_factor: int) -> List[dict]:
    """
    Verify precision loss when scaling distances.

    Returns list of problem distances (>5% error).
    """
    errors = []

    for original in distances:
        if original == 0:
            continue

        # Scale and round
        scaled = round(original * scale_factor)

        # Unscale
        recovered = scaled / scale_factor

        # Calculate error
        absolute_error = abs(original - recovered)
        relative_error_pct = (absolute_error / original) * 100

        if relative_error_pct > 5:
            errors.append({
                'original': original,
                'scaled': scaled,
                'recovered': recovered,
                'absolute_error_km': absolute_error,
                'relative_error_pct': relative_error_pct,
            })

    return errors


def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python analyze_distance_scaling.py <distances_input.csv>")
        sys.exit(1)

    csv_file = Path(sys.argv[1])

    if not csv_file.exists():
        print(f"Error: {csv_file} not found")
        sys.exit(1)

    print("=" * 80)
    print("DISTANCE SCALING ANALYSIS")
    print("=" * 80)
    print(f"\nAnalyzing: {csv_file.name}\n")

    # Load and analyze
    distances, stats = analyze_distances(csv_file)

    print("Distance Statistics:")
    print(f"  Count: {stats['count']}")
    print(f"  Min: {stats['min']:.6f} km")
    print(f"  Max: {stats['max']:.6f} km")
    print(f"  Mean: {stats['mean']:.6f} km")
    print(f"  Median: {stats['median']:.6f} km")
    print(f"  Stdev: {stats['stdev']:.6f} km")

    # Current scale
    current_scale = 10
    print(f"\n\nCurrent SCALE Factor: {current_scale}")
    print("-" * 80)

    print(f"\nPrecision Analysis with SCALE={current_scale}:")
    errors_current = verify_precision_loss(distances, current_scale)

    if errors_current:
        print(f"\n[!] PRECISION LOSS DETECTED: {len(errors_current)} distances lose >5% accuracy")
        print(f"\nWorst cases (top 5):")
        for i, err in enumerate(sorted(errors_current, key=lambda e: -e['relative_error_pct'])[:5]):
            print(f"  {i+1}. Original: {err['original']:.6f} km")
            print(f"     Scaled: {err['scaled']} -> Recovered: {err['recovered']:.6f} km")
            print(f"     Error: {err['absolute_error_km']:.6f} km ({err['relative_error_pct']:.2f}%)\n")
    else:
        print(f"\n[OK] All distances preserve accuracy within 5%")

    # Recommend optimal scale
    optimal_scale = calculate_optimal_scale(distances, min_precision=0.01)

    print(f"\n{'='*80}")
    print(f"RECOMMENDATION: Use SCALE = {optimal_scale}")
    print(f"{'='*80}")

    print(f"\nPrecision Analysis with SCALE={optimal_scale}:")
    errors_optimal = verify_precision_loss(distances, optimal_scale)

    if errors_optimal:
        print(f"\n[!] {len(errors_optimal)} distances lose >5% accuracy (but less than current)")
        print(f"Worst case: {max(e['relative_error_pct'] for e in errors_optimal):.2f}% error")
    else:
        print(f"\n[OK] All distances preserve accuracy within 5%")

    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    print(f"\nWith SCALE={optimal_scale}:")
    print(f"  - Smallest distance: {stats['min']:.6f} km")
    print(f"    -> Scaled: {round(stats['min'] * optimal_scale)}")
    print(f"  - Largest distance: {stats['max']:.6f} km")
    print(f"    -> Scaled: {round(stats['max'] * optimal_scale)}")
    print(f"  - Average distance: {stats['mean']:.6f} km")
    print(f"    -> Scaled: {round(stats['mean'] * optimal_scale)}")

    print(f"\n\nScale Factor Comparison:")
    for test_scale in [10, 50, 100, optimal_scale]:
        errors = verify_precision_loss(distances, test_scale)
        error_pct = (len(errors) / len(distances) * 100) if distances else 0
        print(f"  SCALE={test_scale:3d}: {error_pct:5.1f}% distances lose >5% accuracy")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
