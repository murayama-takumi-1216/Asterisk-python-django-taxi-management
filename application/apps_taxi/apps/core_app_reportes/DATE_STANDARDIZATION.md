# Date Range Standardization for Reports

## Problem

**Issue #16**: Inconsistent date range defaults across different report types caused confusion:
- Most reports defaulted to 7-day lookback
- Operator reports required manual date selection (no defaults)
- Confusing behavior across different report types

## Solution

Implemented standardized date configuration module (`reporte_date_config.js`) that provides:
- **Consistent 7-day default lookback** across all reports
- **Standardized maximum lookback** of 120 days
- **Centralized configuration** to avoid code duplication
- **Utility functions** for easy integration

## Configuration Constants

```javascript
const ReporteDateConfig = {
  DEFAULT_LOOKBACK_DAYS: 7,    // All reports default to last 7 days
  MAX_LOOKBACK_DAYS: 120,       // Maximum queryable history
  ...
};
```

## Usage

### Include the Configuration Script

Add to your HTML template **before** the report-specific JavaScript:

```html
<script src="{% static 'js/core_app_reporte/reporte_date_config.js' %}"></script>
<script src="{% static 'js/core_app_reporte/reporte_driver_vigentes.js' %}"></script>
```

### For Reports with Date Ranges (Driver/Conductor Reports)

**Before** (Inconsistent, no defaults):
```javascript
const fechaDPActual = new Date();
const fechaDPMinima = new Date();
fechaDPMinima.setDate(fechaDPMinima.getDate() - 120);

$("#id_turncond_fecha_inicio").bootstrapMaterialDatePicker({
  format: "YYYY-MM-DD",
  time: false,
  date: true,
  lang: "es-us",
  clearButton: true,
  shortTime: false,
  clearText: "Limpiar",
  cancelText: "Cancelar",
  currentDate: fechaDPActual,
  minDate: fechaDPMinima,
  maxDate: fechaDPActual
});

$("#id_turncond_fecha_fin").bootstrapMaterialDatePicker({
  // ... same config ...
});

// NO DEFAULT VALUES SET - User must manually select dates
```

**After** (Standardized with 7-day defaults):
```javascript
// Use standardized date configuration (7-day default lookback)
ReporteDateConfig.initDatePicker("#id_turncond_fecha_inicio").change(function () {
  let fechaCampo = moment($("#id_turncond_fecha_inicio").val());
  $("#id_turncond_fecha_fin").bootstrapMaterialDatePicker("setMinDate", fechaCampo.format("YYYY-MM-DD"))
});

ReporteDateConfig.initDatePicker("#id_turncond_fecha_fin").change(function () {
  let fechaCampo = moment($("#id_turncond_fecha_fin").val());
  $("#id_turncond_fecha_inicio").bootstrapMaterialDatePicker("setMaxDate", fechaCampo.format("YYYY-MM-DD"))
});

// Set default 7-day date range (today - 7 days to today)
ReporteDateConfig.setDefaultDateRange("#id_turncond_fecha_inicio", "#id_turncond_fecha_fin");
```

### For Reports with Single Date (Operator Reports)

**Before** (No default, requires manual selection):
```javascript
$("#id_turncond_fecha_actual").bootstrapMaterialDatePicker({
  format: "YYYY-MM-DD",
  time: false,
  date: true,
  lang: "es-us",
  clearButton: true,
  shortTime: false,
  clearText: "Limpiar",
  cancelText: "Cancelar",
  currentDate: new Date(),
  minDate: fechaDPMinima,
  maxDate: fechaDPActual
});

// NO DEFAULT VALUE - Empty field
```

**After** (Standardized with today as default):
```javascript
// Use standardized date configuration
ReporteDateConfig.initDatePicker("#id_turncond_fecha_actual");

// Set default to today (0 days back)
ReporteDateConfig.setDefaultSingleDate("#id_turncond_fecha_actual", 0);

// Alternative: Set to yesterday
// ReporteDateConfig.setDefaultSingleDate("#id_turncond_fecha_actual", 1);
```

## Benefits

### User Experience
✅ **No manual date selection required** - Reports load with sensible defaults
✅ **Consistent behavior** - All reports use same 7-day default
✅ **Faster workflow** - Users can immediately view data without configuration

### Developer Experience
✅ **DRY principle** - Centralized configuration eliminates code duplication
✅ **Easy maintenance** - Change defaults in one place
✅ **Consistent patterns** - Standardized utility functions

## API Reference

### `initDatePicker(selector, options)`

Initialize a date picker with standardized configuration.

**Parameters:**
- `selector` (string): jQuery selector for the date input field
- `options` (object, optional): Override default configuration

**Returns:** jQuery object for chaining

**Example:**
```javascript
ReporteDateConfig.initDatePicker("#my_date_field");

// With custom options
ReporteDateConfig.initDatePicker("#my_date_field", {
  currentDate: new Date("2025-01-01")
});
```

### `setDefaultDateRange(startSelector, endSelector)`

Set default 7-day date range for start and end date fields.

**Parameters:**
- `startSelector` (string): Selector for start date field
- `endSelector` (string): Selector for end date field

**Example:**
```javascript
ReporteDateConfig.setDefaultDateRange("#fecha_inicio", "#fecha_fin");
// Sets: fecha_inicio = today - 7 days
//       fecha_fin = today
```

### `setDefaultSingleDate(selector, daysBack)`

Set default single date value.

**Parameters:**
- `selector` (string): Selector for date field
- `daysBack` (number, optional): Days to subtract from today (default: 0)

**Example:**
```javascript
// Set to today
ReporteDateConfig.setDefaultSingleDate("#fecha", 0);

// Set to yesterday
ReporteDateConfig.setDefaultSingleDate("#fecha", 1);

// Set to 7 days ago
ReporteDateConfig.setDefaultSingleDate("#fecha", 7);
```

### `getDefaultDateRange()`

Get the default 7-day date range as Date objects.

**Returns:** Object with `fechaInicio` and `fechaFin` Date objects

**Example:**
```javascript
const range = ReporteDateConfig.getDefaultDateRange();
console.log(range.fechaInicio); // Date object: 7 days ago
console.log(range.fechaFin);    // Date object: today
```

### `getMinDate()`, `getMaxDate()`

Get minimum (120 days ago) and maximum (today) allowed dates.

**Example:**
```javascript
const minDate = ReporteDateConfig.getMinDate();  // 120 days ago
const maxDate = ReporteDateConfig.getMaxDate();  // today
```

## Migration Guide

### Step 1: Include Script

Add to your template:
```html
<script src="{% static 'js/core_app_reporte/reporte_date_config.js' %}"></script>
```

### Step 2: Replace Manual Date Configuration

Find this pattern:
```javascript
const fechaDPActual = new Date();
const fechaDPMinima = new Date();
fechaDPMinima.setDate(fechaDPMinima.getDate() - 120);
$("#my_date").bootstrapMaterialDatePicker({...});
```

Replace with:
```javascript
ReporteDateConfig.initDatePicker("#my_date");
ReporteDateConfig.setDefaultSingleDate("#my_date", 0);  // or setDefaultDateRange
```

### Step 3: Test

1. Verify date pickers load with correct defaults
2. Confirm min/max date restrictions work
3. Test date range interactions (start/end date validation)

## Files to Update

All report JavaScript files should use this standardized configuration:

### Date Range Reports (7-day default):
- ✅ `reporte_driver_vigentes.js` (UPDATED)
- `reporte_driver_vigentes_print.js`
- `reporte_turno_conductor.js`
- `reporte_turno_conduct_r_simple.js`
- `reporte_turno_conduct_r_simple_print.js`
- `reporte_turno_conduct_r_celular.js`

### Single Date Reports (today default):
- `reporte_turno_operador_r_celular.js`
- `reporte_turno_operador_r_celular_print.js`
- `reporte_turno_operador_resumen_celular.js`
- `reporte_turno_operador_resumen_celular_print.js`

## Testing Checklist

- [ ] Date pickers initialize with correct defaults
- [ ] 7-day lookback works correctly (today - 7 to today)
- [ ] Min date restriction enforced (120 days max)
- [ ] Max date restriction enforced (today max)
- [ ] Start/end date cross-validation works
- [ ] Clear button resets to defaults
- [ ] Reports load data correctly with default dates

## Customization

To change the default lookback period globally, edit `reporte_date_config.js`:

```javascript
const ReporteDateConfig = {
  DEFAULT_LOOKBACK_DAYS: 14,  // Change to 14 days
  // ...
};
```

This change will affect all reports using the standardized configuration.
