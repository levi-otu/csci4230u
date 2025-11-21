/**
 * Authentication models matching backend API schemas
 */

/**
 * User login request payload
 */
export interface LoginRequest {
  email: string;
  password: string;
}

/**
 * User registration request payload
 */
export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  full_name?: string | null;
}

/**
 * Token response from login/register endpoints
 */
export interface TokenResponse {
  access_token: string;
  token_type: string;
}

/**
 * User model representing authenticated user data
 */
export interface User {
  id: string;
  username: string;
  email: string;
  full_name?: string | null;
  is_active: boolean;
}

/**
 * Decoded JWT token data
 */
export interface TokenData {
  user_id?: string | null;
  exp?: number;
  iat?: number;
}
