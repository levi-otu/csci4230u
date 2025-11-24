/**
 * Get clubs service - fetches list of all clubs or user's clubs
 * State management is handled by Redux store
 */

import { httpClient } from '@/global/api/http-client';
import type { Club } from '@/global/models/club.models';

/**
 * Get clubs service for fetching clubs
 */
export class GetClubsService {
  private static readonly CLUBS_ENDPOINT = '/api/clubs';

  /**
   * Get all clubs with optional pagination
   * @param skip Number of records to skip (default: 0)
   * @param limit Maximum number of records to return (default: 100)
   * @returns Promise with array of clubs
   * @throws ApiError on failure
   */
  static async getAllClubs(skip = 0, limit = 100): Promise<Club[]> {
    const response = await httpClient.get<Club[]>(
      `${this.CLUBS_ENDPOINT}?skip=${skip}&limit=${limit}`
    );

    return response;
  }

  /**
   * Get clubs for a specific user
   * @param userId The user ID to fetch clubs for
   * @returns Promise with array of clubs
   * @throws ApiError on failure
   */
  static async getUserClubs(userId: string): Promise<Club[]> {
    const response = await httpClient.get<Club[]>(
      `${this.CLUBS_ENDPOINT}/user/${userId}`
    );

    return response;
  }

  /**
   * Get a single club by ID
   * @param clubId The club ID
   * @returns Promise with club data
   * @throws ApiError on failure
   */
  static async getClubById(clubId: string): Promise<Club> {
    const response = await httpClient.get<Club>(
      `${this.CLUBS_ENDPOINT}/${clubId}`
    );

    return response;
  }
}

/**
 * Export default get clubs service
 */
export default GetClubsService;
