# JSON to DZN Conversion Process - Technical Documentation

## Overview

The JSON to DZN converter transforms JITS2022 test instances into MiniZinc-compatible `.dzn` format files. This document explains the step-by-step conversion process, parameter scaling, and precision considerations.

**Target Audience:** Developers, model analysts, and users who need to understand data transformation and verify conversion accuracy.

---

## 1. Input Data Structure

### Required Files

#### 1.1 Bus Schedules: `buses_input_<SPEED>_<REST>.json`

**Format:** JSON array of line objects

```json
[
  {
    "buses": [
      {
        "path": [
          {"station_id": "S1", "time": "08:00", "rest": false},
          {"station_id": "S5", "time": "08:15", "rest": false},
          {"station_id": "S3", "time": "08:30", "rest": true}
        ]
      }
    ]
  }
]
```

**What it contains:**
- Bus routes (sequence of station IDs)
- Scheduled arrival times (HH:MM format)
- Rest flags (whether driver rests at stop)

#### 1.2 Stations: `stations_input.csv`

**Format:** Comma-separated values

```csv
station_id,station_name,latitude,longitude
S1,Downtown Station,40.7128,-74.0060
S2,Transit Hub,40.7580,-73.9855
S3,North Terminal,40.7849,-73.9680
```

**What it contains:**
- Unique station identifiers
- Station names
- GPS coordinates (for distance verification)

#### 1.3 Distance Matrix: `distances_input.csv`

**Format:** Comma-separated origin-destination-distance

```csv
from_station_id,to_station_id,distance_meters
S1,S2,4000
S1,S3,5200
S2,S3,2000
```

**What it contains:**
- Pairwise distances between all stations (in meters)
- Used to calculate energy consumption per arc
- Must be symmetric (S1→S2 ≈ S2→S1)

---

## 2. Conversion Pipeline

### Step 1: Parse Schedule Times

**Input:** JSON bus paths with time strings (HH:MM)

**Process:**
```
"HH:MM" → minutes_since_midnight = HH × 60 + MM
```

**Example:**
```
"08:15" → 8 × 60 + 15 = 495 minutes
```

**Output:** Integer minutes (0..1440)

---

### Step 2: Calculate Travel Times (T Array)

**Input:** Schedule times for consecutive stops

**Process:**
```
T[i] = time[i] - time[i-1] + rest_contribution

rest_contribution = config.rest_time if rest_flag[i-1] else 0
```

**Example:**
```
Stop 1: 08:00 (480 min)
Stop 2: 08:15 (495 min)
Travel time: 495 - 480 = 15 minutes
Rest time: 10 minutes (if rest flag = true)
T[2] = 15 + 10 = 25 minutes
```

**Key Detail:** Travel times derive from the schedule directly, NOT from distance/speed.

**Output:** Integer minutes (no scaling)

---

### Step 3: Calculate Energy Consumption (D Array)

**Input:** Distance matrix + consumption rate constant

**Process:**
```
distance_km = distance_m / 1000
consumption_kwh = distance_km × CONSUMPTION_RATE
D_scaled = round(consumption_kwh × SCALE_ENERGY)
```

**Constants:**
```
CONSUMPTION_RATE = 0.25 kWh/km  (typical electric bus)
SCALE_ENERGY = 1000            (precision factor)
```

**Example:**
```
Distance: 4000 meters = 4.0 km
Consumption: 4.0 × 0.25 = 1.0 kWh
Scaled: round(1.0 × 1000) = 1000 units
```

**Precision Analysis:**
```
1 unit = 0.001 kWh = 0.1% precision
Error: ≤ 0.5 units = 0.05% relative error
```

This is significantly better than the previous scale of 50 (which gave ~10% error).

---

### Step 4: Create Station Mapping

**Input:** All unique station IDs from all buses

**Process:**
```
Sort station_ids alphabetically
Create mapping: station_id → 1-indexed number
```

**Example:**
```
Unique stations: {S1, S3, S5, S2}
Sorted: [S1, S2, S3, S5]
Mapping:
  S1 → 1
  S2 → 2
  S3 → 3
  S5 → 4
```

---

### Step 5: Build Output Arrays

#### st_bi (Station Sequence)
```
st_bi[b, i] = station_index for bus b at stop i
```

Padded with last station if bus has fewer stops than max_stops.

#### T (Travel Times)
```
T[b, i] = time_delta[b, i] in minutes
```

Padded with 0.

#### D (Energy Consumption)
```
D[b, i] = scaled energy consumed from stop i-1 to i
```

First stop has D=0 (no travel before starting point).

#### tau_bi (Schedule Times)
```
tau_bi[b, i] = scheduled arrival time in minutes since 00:00
```

Padded with last time.

---

## 3. Scaling Strategy

### Energy Scaling (SCALE_ENERGY = 1000)

**Why 1000?**

Previous scale of 50 had issues:
```
Example: 0.268 km × 0.25 = 0.067 kWh
With SCALE_ENERGY=50:
  0.067 × 50 = 3.35 → round(3.35) = 3
  Error: 3.35 - 3 = 0.35 units = 10.4% relative error
  
With SCALE_ENERGY=1000:
  0.067 × 1000 = 67 → round(67) = 67
  Error: 67 - 67 = 0 units = 0% relative error
```

**Cumulative Error Propagation:**
```
- 100 buses × 20 stops = 2000 arcs
- With 10% error per arc: 2000 × 0.1 = 200 units of accumulated error
- With 0.1% error per arc: 2000 × 0.001 = 2 units of accumulated error

Conclusion: Higher scale prevents constraint infeasibility from truncation.
```

### Time Scaling (SCALE_TIME = 1)

**Why no scaling?**

- Schedule times must match MiniZinc variable range: `var 0..3000: tbi`
- Travel times are short (minutes), already precise enough
- Scaling would inflate Big-M constants unnecessarily

---

## 4. Parameter Mapping to MiniZinc

### Battery Capacity Parameters

| Original | Value | Scaled | Unit |
|----------|-------|--------|------|
| Cmax | 100 kWh | 100000 | × 0.001 kWh |
| Cmin | 20 kWh | 20000 | × 0.001 kWh |
| alpha | 10 kWh/min | 10000 | × 0.001 kWh/min |

### Time Parameters (Unscaled)

| Parameter | Value | Range | Unit |
|-----------|-------|-------|------|
| mu | 5 | 0..100 | minutes |
| SM | 1 | 0..30 | minutes |
| psi | 1 | 0..30 | minutes |
| beta | 10 | 0..60 | minutes |

### Big-M Constant

```
M = 5000

Rationale:
- Maximum scheduling horizon: ~480 min × 8-10 hour day = ~3000 min
- Buffer for delays and charging: +2000 min
- Used in disjunctive constraints, not inflated by global scale
```

---

## 5. Output File Format (.dzn)

The output `.dzn` file contains:

### Structure

```minizinc
% Header with problem metadata
num_buses = 5;
num_stations = 12;
max_stops = 8;

% Scaling documentation (for reproducibility)
Cmax = 100000;        % Scaled by 1000
Cmin = 20000;
alpha = 10000;

% Arrays
st_bi = array2d(1..5, 1..8, [...]);
D = array2d(1..5, 1..8, [...]);
T = array2d(1..5, 1..8, [...]);
tau_bi = array2d(1..5, 1..8, [...]);
```

### Verification Checklist

- [ ] All D values divided by 1000 match original energy consumption
- [ ] All T values match schedule time differences
- [ ] tau_bi values fall within 0..1440 range (minutes in day)
- [ ] st_bi indices match station_to_idx mapping
- [ ] Problem dimensions match: |buses| × max_stops = array size

---

## 6. Precision & Error Analysis

### Energy Precision

```
Scaling: 1000 (1 unit = 0.001 kWh = 0.1% precision)

Per-arc error:
  Max error: ±0.5 units = ±0.0005 kWh = 0.05%

Total error for 100 buses, 20 stops each (2000 arcs):
  Worst case: 2000 × 0.0005 = 1 kWh (out of ~2000 total)
  Accumulated relative error: < 0.05% ✓
```

### Time Precision

```
No scaling: exact minutes

Example verification:
  Schedule: 09:30 = 570 minutes
  Stored as: 570 (exact match)
  Error: 0%
```

---

## 7. How to Verify Conversion Accuracy

### Manual Verification

1. **Pick a specific bus and arc**
   ```
   Bus 1, Stop 2 → Stop 3
   Original distance: 4000 m
   Expected energy: 4.0 km × 0.25 = 1.0 kWh
   Scaled: 1000 units
   ```

2. **Find in DZN file**
   ```minizinc
   D[1, 3] should = 1000
   ```

3. **Check schedule times**
   ```
   tau_bi[1, 1] should = time1_in_minutes
   tau_bi[1, 3] should = time3_in_minutes
   T[1, 3] should ≈ time3 - time2 + rest
   ```

### Programmatic Verification

```python
# Load DZN
D_scaled = 1000  # Example value
D_actual_kwh = D_scaled / 1000  # = 1.0 kWh

# Verify against distance
distance_km = 4.0
expected_kwh = distance_km * 0.25  # = 1.0 kWh

assert abs(D_actual_kwh - expected_kwh) < 0.001
```

---

## 8. Known Constraints & Limitations

### File Requirements

- **Distances must be positive:** All distance_meters > 0
- **Times must be monotonic:** Scheduled times strictly increasing per bus
- **Station IDs must match:** Same format across JSON, CSV, and distances file
- **Distances must be symmetric:** distance(A→B) ≈ distance(B→A)

### Conversion Limits

- **Max buses:** Limited by system memory (typically 10,000+)
- **Max stops per bus:** Configurable (typically 50-100)
- **Max stations:** Scales with problem size

---

## 9. Configuration Parameters

Located in `Converter/config` or `experiment_config.py`:

```python
CONSUMPTION_RATE = 0.25  # kWh/km (configurable per vehicle type)
SCALE_ENERGY = 1000      # Precision factor
SCALE_TIME = 1           # Time units (minutes)
M = 5000                 # Big-M constant
```

---

## 10. Troubleshooting

### Common Issues

**Issue:** Model becomes infeasible after conversion

**Check:**
1. Verify D values: divide by 1000 and compare to input distances
2. Verify T values: must equal time differences plus rest time
3. Verify Cmax/Cmin: should be 100000/20000, not 1000/200
4. Check that no truncation errors accumulated

**Issue:** Output DZN has very large or very small numbers

**Check:**
1. Energy values >> 100000? Something scaled wrongly
2. Energy values << 100? Check if dividing instead of multiplying
3. Time values >> 3000? These should be minutes in range 0..1440

---

## 11. References

- **JITS2022 Format:** Original test battery specification
- **MiniZinc DZN:** MiniZinc language data file format
- **Consumption Rate:** Based on typical 40-ton electric bus specification
- **Scaling Strategy:** Optimized for MIP solver precision requirements

---

## Summary

| Step | Input | Process | Output | Precision |
|------|-------|---------|--------|-----------|
| 1 | Time strings | Parse HH:MM | Minutes 0..1440 | Exact |
| 2 | Schedule times | T = time[i] - time[i-1] | Travel times | Exact |
| 3 | Distances | E = dist × 0.25 × 1000 | Scaled energy | ±0.0005 kWh |
| 4 | Station IDs | Create 1-indexed map | st indices | Exact |
| 5 | All data | Build arrays 2D | DZN arrays | Within bounds |

**Result:** Accurate, precise, MiniZinc-compatible data files ready for optimization.

---

*Document Version: 1.0*  
*Updated: April 2026*  
*Author: AVISPA Research Team*
