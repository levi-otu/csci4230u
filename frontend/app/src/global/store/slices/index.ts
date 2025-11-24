/**
 * Slices exports
 * Central export point for all Redux slices
 */

export {
  loginAsync,
  registerAsync,
  fetchCurrentUserAsync,
  logout,
  clearError,
  setToken,
  restoreSession,
} from './authSlice';

export type { AuthState } from './authSlice';

export { default as authReducer } from './authSlice';

export {
  fetchAllClubsAsync,
  fetchUserClubsAsync,
  fetchClubByIdAsync,
  createClubAsync,
  joinClubAsync,
  leaveClubAsync,
  clearError as clearClubsError,
  setSelectedClub,
  clearSelectedClub,
  resetClubsState,
} from './clubsSlice';

export type { ClubsState } from './clubsSlice';

export { default as clubsReducer } from './clubsSlice';
