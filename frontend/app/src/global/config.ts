/**
 * Global application configuration
 */

export const config = {
  /**
   * Base API URL for all backend requests
   * Default: http://localhost:8000
   * Can be overridden by VITE_API_BASE_URL environment variable
   */
  baseApiUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',

  /**
   * Default request timeout in milliseconds
   */
  requestTimeout: 30000,

  /**
   * Token storage key in sessionStorage
   */
  tokenStorageKey: 'auth_token',
} as const;
