/**
 * Clubs Redux Slice
 * Manages clubs state using Redux Toolkit
 */

import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';
import GetClubsService from '@/global/api/actions/clubs/api-get-clubs.service';
import CreateClubService from '@/global/api/actions/clubs/api-create-club.service';
import JoinClubService from '@/global/api/actions/clubs/api-join-club.service';
import type {
  Club,
  CreateClubRequest,
  AddUserToClubRequest,
  UserClubMembership,
} from '@/global/models/club.models';

/**
 * Clubs state interface
 */
export interface ClubsState {
  allClubs: Club[];
  userClubs: Club[];
  selectedClub: Club | null;
  isLoading: boolean;
  isCreating: boolean;
  isJoining: boolean;
  error: string | null;
}

/**
 * Initial clubs state
 */
const initialState: ClubsState = {
  allClubs: [],
  userClubs: [],
  selectedClub: null,
  isLoading: false,
  isCreating: false,
  isJoining: false,
  error: null,
};

/**
 * Async thunk for fetching all clubs
 */
export const fetchAllClubsAsync = createAsyncThunk<
  Club[],
  { skip?: number; limit?: number },
  { rejectValue: string }
>(
  'clubs/fetchAllClubs',
  async ({ skip = 0, limit = 100 }, { rejectWithValue }) => {
    try {
      const clubs = await GetClubsService.getAllClubs(skip, limit);
      return clubs;
    } catch (error: any) {
      const errorMessage =
        error?.data?.detail ||
        error?.response?.data?.detail ||
        error?.message ||
        'Failed to fetch clubs. Please try again.';

      return rejectWithValue(errorMessage);
    }
  }
);

/**
 * Async thunk for fetching user's clubs
 */
export const fetchUserClubsAsync = createAsyncThunk<
  Club[],
  string,
  { rejectValue: string }
>('clubs/fetchUserClubs', async (userId, { rejectWithValue }) => {
  try {
    const clubs = await GetClubsService.getUserClubs(userId);
    return clubs;
  } catch (error: any) {
    const errorMessage =
      error?.data?.detail ||
      error?.response?.data?.detail ||
      error?.message ||
      'Failed to fetch your clubs. Please try again.';

    return rejectWithValue(errorMessage);
  }
});

/**
 * Async thunk for fetching a single club
 */
export const fetchClubByIdAsync = createAsyncThunk<
  Club,
  string,
  { rejectValue: string }
>('clubs/fetchClubById', async (clubId, { rejectWithValue }) => {
  try {
    const club = await GetClubsService.getClubById(clubId);
    return club;
  } catch (error: any) {
    const errorMessage =
      error?.data?.detail ||
      error?.response?.data?.detail ||
      error?.message ||
      'Failed to fetch club details. Please try again.';

    return rejectWithValue(errorMessage);
  }
});

/**
 * Async thunk for creating a new club
 */
export const createClubAsync = createAsyncThunk<
  Club,
  CreateClubRequest,
  { rejectValue: string }
>('clubs/createClub', async (clubData, { rejectWithValue }) => {
  try {
    const club = await CreateClubService.createClub(clubData);
    return club;
  } catch (error: any) {
    const errorMessage =
      error?.data?.detail ||
      error?.response?.data?.detail ||
      error?.message ||
      'Failed to create club. Please try again.';

    return rejectWithValue(errorMessage);
  }
});

/**
 * Async thunk for joining a club
 */
export const joinClubAsync = createAsyncThunk<
  { membership: UserClubMembership; clubId: string },
  { clubId: string; membershipData: AddUserToClubRequest },
  { rejectValue: string }
>(
  'clubs/joinClub',
  async ({ clubId, membershipData }, { rejectWithValue }) => {
    try {
      const membership = await JoinClubService.joinClub(
        clubId,
        membershipData
      );
      return { membership, clubId };
    } catch (error: any) {
      const errorMessage =
        error?.data?.detail ||
        error?.response?.data?.detail ||
        error?.message ||
        'Failed to join club. Please try again.';

      return rejectWithValue(errorMessage);
    }
  }
);

/**
 * Async thunk for leaving a club
 */
export const leaveClubAsync = createAsyncThunk<
  { clubId: string; userId: string },
  { clubId: string; userId: string },
  { rejectValue: string }
>(
  'clubs/leaveClub',
  async ({ clubId, userId }, { rejectWithValue }) => {
    try {
      await JoinClubService.leaveClub(clubId, userId);
      return { clubId, userId };
    } catch (error: any) {
      const errorMessage =
        error?.data?.detail ||
        error?.response?.data?.detail ||
        error?.message ||
        'Failed to leave club. Please try again.';

      return rejectWithValue(errorMessage);
    }
  }
);

/**
 * Clubs slice
 */
const clubsSlice = createSlice({
  name: 'clubs',
  initialState,
  reducers: {
    /**
     * Clear error action
     */
    clearError: (state) => {
      state.error = null;
    },

    /**
     * Set selected club
     */
    setSelectedClub: (state, action: PayloadAction<Club | null>) => {
      state.selectedClub = action.payload;
    },

    /**
     * Clear selected club
     */
    clearSelectedClub: (state) => {
      state.selectedClub = null;
    },

    /**
     * Reset clubs state
     */
    resetClubsState: (state) => {
      state.allClubs = [];
      state.userClubs = [];
      state.selectedClub = null;
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    // Fetch all clubs
    builder
      .addCase(fetchAllClubsAsync.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchAllClubsAsync.fulfilled, (state, action) => {
        state.isLoading = false;
        state.allClubs = action.payload;
        state.error = null;
      })
      .addCase(fetchAllClubsAsync.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload || 'Failed to fetch clubs';
      });

    // Fetch user clubs
    builder
      .addCase(fetchUserClubsAsync.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchUserClubsAsync.fulfilled, (state, action) => {
        state.isLoading = false;
        state.userClubs = action.payload;
        state.error = null;
      })
      .addCase(fetchUserClubsAsync.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload || 'Failed to fetch your clubs';
      });

    // Fetch club by ID
    builder
      .addCase(fetchClubByIdAsync.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchClubByIdAsync.fulfilled, (state, action) => {
        state.isLoading = false;
        state.selectedClub = action.payload;
        state.error = null;
      })
      .addCase(fetchClubByIdAsync.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload || 'Failed to fetch club';
      });

    // Create club
    builder
      .addCase(createClubAsync.pending, (state) => {
        state.isCreating = true;
        state.error = null;
      })
      .addCase(createClubAsync.fulfilled, (state, action) => {
        state.isCreating = false;
        state.allClubs.unshift(action.payload); // Add to beginning of list
        state.userClubs.unshift(action.payload); // Add to user's clubs
        state.error = null;
      })
      .addCase(createClubAsync.rejected, (state, action) => {
        state.isCreating = false;
        state.error = action.payload || 'Failed to create club';
      });

    // Join club
    builder
      .addCase(joinClubAsync.pending, (state) => {
        state.isJoining = true;
        state.error = null;
      })
      .addCase(joinClubAsync.fulfilled, (state, action) => {
        state.isJoining = false;
        // Find the club and add it to user's clubs
        const club = state.allClubs.find(
          (c) => c.id === action.payload.clubId
        );
        if (club && !state.userClubs.find((c) => c.id === club.id)) {
          state.userClubs.push(club);
        }
        state.error = null;
      })
      .addCase(joinClubAsync.rejected, (state, action) => {
        state.isJoining = false;
        state.error = action.payload || 'Failed to join club';
      });

    // Leave club
    builder
      .addCase(leaveClubAsync.pending, (state) => {
        state.isJoining = true; // Reuse isJoining for leaving
        state.error = null;
      })
      .addCase(leaveClubAsync.fulfilled, (state, action) => {
        state.isJoining = false;
        // Remove the club from user's clubs
        state.userClubs = state.userClubs.filter(
          (c) => c.id !== action.payload.clubId
        );
        state.error = null;
      })
      .addCase(leaveClubAsync.rejected, (state, action) => {
        state.isJoining = false;
        state.error = action.payload || 'Failed to leave club';
      });
  },
});

/**
 * Export actions
 */
export const {
  clearError,
  setSelectedClub,
  clearSelectedClub,
  resetClubsState,
} = clubsSlice.actions;

/**
 * Export reducer
 */
export default clubsSlice.reducer;
