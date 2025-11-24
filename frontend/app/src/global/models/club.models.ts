/**
 * Club models matching backend API schemas
 */

/**
 * Club model representing a book club
 */
export interface Club {
  id: string;
  name: string;
  description: string | null;
  topic: string | null;
  created_by: string;
  is_active: boolean;
  max_members: number | null;
  created_at: string;
  updated_at: string;
}

/**
 * Request payload for creating a new club
 */
export interface CreateClubRequest {
  name: string;
  description?: string | null;
  topic?: string | null;
  max_members?: number | null;
}

/**
 * Request payload for updating a club
 */
export interface UpdateClubRequest {
  name?: string;
  description?: string | null;
  topic?: string | null;
  is_active?: boolean;
  max_members?: number | null;
}

/**
 * User-club membership model
 */
export interface UserClubMembership {
  user_id: string;
  club_id: string;
  join_date: string;
  role: 'member' | 'owner';
}

/**
 * Request payload for adding a user to a club
 */
export interface AddUserToClubRequest {
  user_id: string;
  role?: 'member' | 'owner';
}

/**
 * Club with additional metadata for UI
 */
export interface ClubWithMetadata extends Club {
  member_count?: number;
  is_member?: boolean;
  user_role?: 'member' | 'owner';
}
