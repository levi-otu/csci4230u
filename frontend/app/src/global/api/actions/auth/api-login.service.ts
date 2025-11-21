/**
 * Login service - handles user authentication via login endpoint
 * State management is handled by Redux store
 */

import { httpClient } from '@/global/api/http-client';
import type { LoginRequest, TokenResponse } from '@/global/models/auth.models';

/**
 * Login service for user authentication
 */
export class LoginService {
  private static readonly LOGIN_ENDPOINT = '/api/auth/login';

  /**
   * Authenticate user with email and password
   * @param credentials User login credentials (email and password)
   * @returns Promise with token response
   * @throws ApiError on authentication failure
   */
  static async login(credentials: LoginRequest): Promise<TokenResponse> {
    const response = await httpClient.post<TokenResponse>(
      this.LOGIN_ENDPOINT,
      credentials
    );

    return response;
  }
}

/**
 * Export default login service
 */
export default LoginService;
