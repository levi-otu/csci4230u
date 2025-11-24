/**
 * Join club service - handles adding users to clubs
 * State management is handled by Redux store
 */

import { httpClient } from '@/global/api/http-client';
import type {
  UserClubMembership,
  AddUserToClubRequest,
} from '@/global/models/club.models';

/**
 * Join club service
 */
export class JoinClubService {
  private static readonly CLUBS_ENDPOINT = '/api/clubs';

  /**
   * Add a user to a club (join club)
   * @param clubId The club ID to join
   * @param membershipData Membership data (user_id and optional role)
   * @returns Promise with membership data
   * @throws ApiError on failure
   */
  static async joinClub(
    clubId: string,
    membershipData: AddUserToClubRequest
  ): Promise<UserClubMembership> {
    const response = await httpClient.post<UserClubMembership>(
      `${this.CLUBS_ENDPOINT}/${clubId}/members`,
      membershipData
    );

    return response;
  }

  /**
   * Get all members of a club
   * @param clubId The club ID
   * @returns Promise with array of memberships
   * @throws ApiError on failure
   */
  static async getClubMembers(clubId: string): Promise<UserClubMembership[]> {
    const response = await httpClient.get<UserClubMembership[]>(
      `${this.CLUBS_ENDPOINT}/${clubId}/members`
    );

    return response;
  }

  /**
   * Remove a user from a club (leave club)
   * @param clubId The club ID
   * @param userId The user ID to remove
   * @returns Promise that resolves when user is removed
   * @throws ApiError on failure
   */
  static async leaveClub(clubId: string, userId: string): Promise<void> {
    await httpClient.delete(
      `${this.CLUBS_ENDPOINT}/${clubId}/members/${userId}`
    );
  }
}

/**
 * Export default join club service
 */
export default JoinClubService;
