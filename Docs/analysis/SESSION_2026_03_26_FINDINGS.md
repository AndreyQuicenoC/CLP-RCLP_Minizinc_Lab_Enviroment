# CRITICAL FINDINGS - Session 2026-03-26

## Status Summary
- ✅ Battery Project Integer indexing FIXED (0-indexed → 1-indexed)
- ✅ Model constraints UPDATED for 1-indexing
- ✅ Generator v2.0 SYNTAX FIXED (array2d formatting)
- ❌ Battery Project Integer still UNSATISFIABLE
- ❌ Generated instances still UNSATISFIABLE
- 🔍 Root cause ISOLATED: Temporal or Installation constraints

## Key Discovery
**Model Energy Constraints ONLY**: ✅ SAT
**Model Full (with timing/installation)**: ❌ UNSAT

This means:
- Energy feasibility: WORKS
- Problem: Timing constraints OR Station installation constraints are over-constrained

## Issues Identified

### 1. Model/Data Indexing (FIXED)
- Changed: st_bi from 0-indexed to 1-indexed
- Updated: Removed filters for st_bi==0
- Status: ✅ Applied

### 2. Initial Battery Condition (FIXED)
- Added: `cbi[b,1] = Cmax` to initialize bus with full battery
- Impact: Allows energy evolution to begin properly
- Status: ✅ Applied

### 3. Array2D Formatting (FIXED)
- Changed: Comma placement in array2d formatting
- Was: `[row1,\nrow2,\nrow3]` (commas between rows)
- Now: `[row1,\nrow2\nrow3]` (no comma after last row)
- Status: ✅ Applied

### 4. Temporal Constraints (⚠️ NEEDS INVESTIGATION)
Current constraints:
- Line 83-86: tbi[ b,i] >= tbi[b,i-1] + ctbi[b,i-1] + T[b,i]
- Line 89-93: d_tbi[b,i] constraints with mu limit

Possibility: These constraints conflict with energy constraints

### 5. Station Installation Constraints (⚠️ NEEDS INVESTIGATION)
Expected: xst[st_bi[b,i]] >= xbi[b,i]
Possibility: No station can be installed, forcing all xst=0, making xbi impossible

## Next Steps (Ordered by Impact)

1. **IMMEDIATE**: Test model WITHOUT temporal constraints (like debug_debug version)
   - If SAT: problem is timing
   - If UNSAT: problem is station installation

2. **Test model WITHOUT station constraints ("xst always 1")**
   - If SAT: stations are the issue
   - If UNSAT: timing is the issue

3. **Investigate temporal over-constraint**
   - Maybe mu=50 (5 min) is too restrictive
   - Maybe tau_bi values don't align with T values

4. **Review station-charging relationship**
   - xst[st_bi[b,i]] >= xbi[b,i] might force all xst=0
   - If no station is installed, no charging possible → infeasible

5. **Update generator algorithm to respect constraints**
   - Ensure generated T, tau_bi, D align with CLP assumptions
   - Override battery/consumption if timing requires

---

**Action Plan**:
- Test model variants to isolate constraint causing UNSAT
- Fix root cause in model
- Update generator to respect model assumptions
- Regenerate Battery Project Integer with corrected understanding

---

**Files Created This Session**:
- Docs/analysis/BUG_ANALYSIS_st_bi_indexing.txt (analysis document)
- Models/clp_model.mzn.bak (backup)
- Models/clp_model_debug.mzn (energy-only model)
- Tests/Output/Generator/debug_minimal*.dzn (test instances)
