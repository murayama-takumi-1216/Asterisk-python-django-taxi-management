/**
 * Standardized Date Range Configuration for Reports
 *
 * This module provides consistent date range defaults and utilities
 * across all report types to avoid inconsistent behavior.
 */

const ReporteDateConfig = {
  /**
   * Default date range lookback in days
   * All reports will default to showing data from the last 7 days
   */
  DEFAULT_LOOKBACK_DAYS: 7,

  /**
   * Maximum allowed lookback in days
   * Users can query up to 120 days in the past
   */
  MAX_LOOKBACK_DAYS: 120,

  /**
   * Get standardized default date range
   * @returns {Object} Object with fechaInicio and fechaFin as Date objects
   */
  getDefaultDateRange: function() {
    const today = new Date();
    const startDate = new Date();
    startDate.setDate(today.getDate() - this.DEFAULT_LOOKBACK_DAYS);

    return {
      fechaInicio: startDate,
      fechaFin: today
    };
  },

  /**
   * Get minimum allowed date
   * @returns {Date} Date object representing earliest queryable date
   */
  getMinDate: function() {
    const minDate = new Date();
    minDate.setDate(minDate.getDate() - this.MAX_LOOKBACK_DAYS);
    return minDate;
  },

  /**
   * Get maximum allowed date (today)
   * @returns {Date} Today's date
   */
  getMaxDate: function() {
    return new Date();
  },

  /**
   * Initialize date picker with standardized config
   * @param {string} selector - jQuery selector for date picker
   * @param {Object} options - Additional options to override defaults
   */
  initDatePicker: function(selector, options = {}) {
    const defaults = {
      format: "YYYY-MM-DD",
      time: false,
      date: true,
      lang: "es-us",
      clearButton: true,
      shortTime: false,
      clearText: "Limpiar",
      cancelText: "Cancelar",
      currentDate: this.getMaxDate(),
      minDate: this.getMinDate(),
      maxDate: this.getMaxDate()
    };

    const config = { ...defaults, ...options };
    return $(selector).bootstrapMaterialDatePicker(config);
  },

  /**
   * Set default values for a date range (start and end date fields)
   * @param {string} startSelector - Selector for start date field
   * @param {string} endSelector - Selector for end date field
   */
  setDefaultDateRange: function(startSelector, endSelector) {
    const range = this.getDefaultDateRange();
    const formatDate = (date) => moment(date).format("YYYY-MM-DD");

    $(startSelector).val(formatDate(range.fechaInicio));
    $(endSelector).val(formatDate(range.fechaFin));
  },

  /**
   * Set default single date (for operator reports)
   * @param {string} selector - Selector for date field
   * @param {number} daysBack - Days to go back from today (default: 0 = today)
   */
  setDefaultSingleDate: function(selector, daysBack = 0) {
    const date = new Date();
    date.setDate(date.getDate() - daysBack);
    $(selector).val(moment(date).format("YYYY-MM-DD"));
  }
};

// Make available globally
window.ReporteDateConfig = ReporteDateConfig;
