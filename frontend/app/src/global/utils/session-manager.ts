/**
 * SessionManager - Utility for managing authentication tokens
 * Handles secure storage and retrieval of JWT tokens
 */

import { config } from '@/global/config';

/**
 * Decoded JWT token payload
 */
export interface TokenPayload {
  user_id?: string;
  exp?: number;
  iat?: number;
}

/**
 * Session manager for handling authentication tokens
 */
export class SessionManager {
  private static readonly TOKEN_KEY = config.tokenStorageKey;

  /**
   * Store authentication token securely in sessionStorage
   * @param token JWT token to store
   */
  static setToken(token: string): void {
    sessionStorage.setItem(this.TOKEN_KEY, token);
  }

  /**
   * Get stored authentication token
   * @returns JWT token or null if not found
   */
  static getToken(): string | null {
    return sessionStorage.getItem(this.TOKEN_KEY);
  }

  /**
   * Remove authentication token (logout)
   */
  static clearToken(): void {
    sessionStorage.removeItem(this.TOKEN_KEY);
  }

  /**
   * Check if user has a valid session
   * @returns true if token exists and is not expired
   */
  static hasValidSession(): boolean {
    const token = this.getToken();
    if (!token) return false;

    try {
      const payload = this.decodeToken(token);
      if (payload.exp) {
        const expiryTime = payload.exp * 1000; // Convert to milliseconds
        return Date.now() < expiryTime;
      }
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Decode JWT token to extract payload
   * @param token JWT token to decode
   * @returns Decoded token payload
   */
  static decodeToken(token: string): TokenPayload {
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );
      return JSON.parse(jsonPayload);
    } catch (error) {
      console.error('Failed to decode token:', error);
      return {};
    }
  }

  /**
   * Get user ID from stored token
   * @returns User ID or null
   */
  static getUserId(): string | null {
    const token = this.getToken();
    if (!token) return null;

    try {
      const payload = this.decodeToken(token);
      return payload.user_id || null;
    } catch {
      return null;
    }
  }

  /**
   * Get token expiry time
   * @returns Expiry timestamp in milliseconds or null
   */
  static getTokenExpiry(): number | null {
    const token = this.getToken();
    if (!token) return null;

    try {
      const payload = this.decodeToken(token);
      return payload.exp ? payload.exp * 1000 : null;
    } catch {
      return null;
    }
  }
}

export default SessionManager;
