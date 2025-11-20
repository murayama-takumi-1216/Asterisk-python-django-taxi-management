- ## 1.4 Critical Issues Found

#### Issue #1: Inconsistent Day-of-Week Conversion (CRITICAL)

**Location:** `apps/core_operador/utils.py`, Line 169

**Problem:**
```python
def generar_fechas_semana(...):
    dia_semana = fecha.isoweekday() - 1  # BUG: Converts 1-7 to 0-6
    fecha_inicio = fecha - timedelta(days=dia_semana)
```

**Impact:**
- Creates inconsistency with the rest of the system (which uses 1-7)
- Fails for Monday (returns same day instead of Monday)
- Violates the ISO 8601 standard used throughout the application


#### Issue #2: Mixed Day-of-Week Extraction Methods (HIGH)

**Locations:**
- `apps/core_operador/views.py:17` - Uses `strftime("%u")`
- `apps/core_operador/utils.py:195` - Uses `isoweekday()`
- `apps/core_operador/utils.py:169` - Uses `isoweekday() - 1`

**Impact:**
- Inconsistent coding practices
- Confusion for developers
- Risk of bugs when "fixing" one method

**Severity:** HIGH
**Fix Required:** Standardize on `isoweekday()` throughout



please modify this error