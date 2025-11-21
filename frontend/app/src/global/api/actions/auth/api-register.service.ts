/**
 * Register service - handles user registration via register endpoint
 * State management is handled by Redux store
 */

import { httpClient } from '@/global/api/http-client';
import type { RegisterRequest, TokenResponse } from '@/global/models/auth.models';

/**
 * Register service for user registration
 */
export class RegisterService {
  private static readonly REGISTER_ENDPOINT = '/api/auth/register';

  /**
   * Register a new user account
   * @param userData User registration data (username, email, password, full_name)
   * @returns Promise with token response
   * @throws ApiError on registration failure
   */
  static async register(userData: RegisterRequest): Promise<TokenResponse> {
    const response = await httpClient.post<TokenResponse>(
      this.REGISTER_ENDPOINT,
      userData
    );

    return response;
  }
}

/**
 * Export default register service
 */
export default RegisterService;
