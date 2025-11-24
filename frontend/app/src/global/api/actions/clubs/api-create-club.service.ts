/**
 * Create club service - handles club creation
 * State management is handled by Redux store
 */

import { httpClient } from '@/global/api/http-client';
import type { Club, CreateClubRequest } from '@/global/models/club.models';

/**
 * Create club service
 */
export class CreateClubService {
  private static readonly CLUBS_ENDPOINT = '/api/clubs';

  /**
   * Create a new club
   * @param clubData Club creation data
   * @returns Promise with created club
   * @throws ApiError on failure
   */
  static async createClub(clubData: CreateClubRequest): Promise<Club> {
    const response = await httpClient.post<Club>(
      this.CLUBS_ENDPOINT,
      clubData
    );

    return response;
  }
}

/**
 * Export default create club service
 */
export default CreateClubService;
