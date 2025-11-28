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
   * Session storage key for JWT token (DEPRECATED - using httpOnly cookies now)
   * @deprecated This is kept for backward compatibility with SessionManager
   */
  tokenStorageKey: 'auth_token',
} as const;
