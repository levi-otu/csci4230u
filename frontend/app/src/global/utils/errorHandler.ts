/**
 * Error handling utilities for API responses
 */

/**
 * Extract a user-friendly error message from various error formats
 */
export function extractErrorMessage(error: any, fallbackMessage = 'An error occurred'): string {
  // If error is already a string, return it
  if (typeof error === 'string') {
    return error;
  }

  // Check for axios/fetch error structure
  const detail = error?.data?.detail || error?.detail || error?.response?.data?.detail;

  // If detail is a string, return it
  if (typeof detail === 'string') {
    return detail;
  }

  // If detail is an array of validation errors (FastAPI format)
  if (Array.isArray(detail) && detail.length > 0) {
    // Extract messages from validation errors
    const messages = detail
      .map((err) => {
        if (typeof err === 'string') return err;
        if (err.msg) return err.msg;
        if (err.message) return err.message;
        return null;
      })
      .filter(Boolean);

    if (messages.length > 0) {
      return messages.join(', ');
    }
  }

  // Try error.message
  if (error?.message) {
    return error.message;
  }

  // Try error?.data?.message
  if (error?.data?.message) {
    return error.data.message;
  }

  // Return fallback
  return fallbackMessage;
}
