/**
 * Auth Redux Slice
 * Manages authentication state using Redux Toolkit with httpOnly cookies
 */

import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';
import LoginService from '@/global/api/actions/auth/api-login.service';
import RegisterService from '@/global/api/actions/auth/api-register.service';
import { httpClient } from '@/global/api/http-client';
import type {
  LoginRequest,
  RegisterRequest,
  User,
} from '@/global/models/auth.models';

/**
 * Auth state interface - NO TOKEN STORAGE
 */
export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

/**
 * Initial auth state
 */
const initialState: AuthState = {
  user: null,
  isAuthenticated: false,
  isLoading: false,
  error: null,
};

/**
 * Async thunk for user login
 */
export const loginAsync = createAsyncThunk<
  User,
  LoginRequest,
  { rejectValue: string }
>('auth/login', async (credentials, { rejectWithValue }) => {
  try {
    // Call login service (sets httpOnly cookie and returns access token)
    const tokenResponse = await LoginService.login(credentials);

    // Store access token in HTTP client (in-memory only, not persisted)
    httpClient.setAccessToken(tokenResponse.access_token);

    // Fetch user data
    const user = await httpClient.get<User>('/api/users/me');

    return user;
  } catch (error: any) {
    // Extract user-friendly error message from API response
    const errorMessage =
      error?.data?.detail || // FastAPI error format
      error?.response?.data?.detail || // Axios wrapped error
      error?.message ||
      'Login failed. Please check your credentials and try again.';

    return rejectWithValue(errorMessage);
  }
});

/**
 * Async thunk for user registration
 */
export const registerAsync = createAsyncThunk<
  User,
  RegisterRequest,
  { rejectValue: string }
>('auth/register', async (userData, { rejectWithValue }) => {
  try {
    // Call register service (sets httpOnly cookie and returns access token)
    const tokenResponse = await RegisterService.register(userData);

    // Store access token in HTTP client (in-memory only, not persisted)
    httpClient.setAccessToken(tokenResponse.access_token);

    // Fetch user data
    const user = await httpClient.get<User>('/api/users/me');

    return user;
  } catch (error: any) {
    // Extract user-friendly error message
    const errorMessage =
      error?.data?.detail ||
      error?.response?.data?.detail ||
      error?.message ||
      'Registration failed. Please try again.';

    return rejectWithValue(errorMessage);
  }
});

/**
 * Async thunk to fetch current user
 */
export const fetchCurrentUserAsync = createAsyncThunk<
  User,
  void,
  { rejectValue: string }
>('auth/fetchCurrentUser', async (_, { rejectWithValue }) => {
  try {
    const user = await httpClient.get<User>('/api/users/me');
    return user;
  } catch (error: any) {
    const errorMessage = error?.data?.detail || error?.message || 'Failed to fetch user';
    return rejectWithValue(errorMessage);
  }
});

/**
 * Async thunk for logout
 */
export const logoutAsync = createAsyncThunk<
  void,
  void,
  { rejectValue: string }
>('auth/logout', async (_, { rejectWithValue }) => {
  try {
    // Call logout endpoint (clears httpOnly cookie)
    await httpClient.post('/api/auth/logout', {});
  } catch (error: any) {
    // Even if logout fails, we clear local state
    console.error('Logout error:', error);
  } finally {
    // Always clear the access token from memory
    httpClient.setAccessToken(null);
  }
});

/**
 * Auth slice
 */
const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    /**
     * Clear authentication error
     */
    clearError(state) {
      state.error = null;
    },

    /**
     * Logout (synchronous)
     */
    logout(state) {
      state.user = null;
      state.isAuthenticated = false;
      state.error = null;
    },

    /**
     * Restore session from cookie (call this on app init)
     */
    restoreSession(state) {
      // Just mark as potentially authenticated
      // The AuthGuard will verify by calling /api/users/me
      state.isAuthenticated = false;
      state.user = null;
    },
  },
  extraReducers: (builder) => {
    // Login
    builder.addCase(loginAsync.pending, (state) => {
      state.isLoading = true;
      state.error = null;
    });
    builder.addCase(loginAsync.fulfilled, (state, action: PayloadAction<User>) => {
      state.isLoading = false;
      state.user = action.payload;
      state.isAuthenticated = true;
      state.error = null;
    });
    builder.addCase(loginAsync.rejected, (state, action) => {
      state.isLoading = false;
      state.error = action.payload || 'Login failed';
      state.isAuthenticated = false;
      state.user = null;
    });

    // Register
    builder.addCase(registerAsync.pending, (state) => {
      state.isLoading = true;
      state.error = null;
    });
    builder.addCase(registerAsync.fulfilled, (state, action: PayloadAction<User>) => {
      state.isLoading = false;
      state.user = action.payload;
      state.isAuthenticated = true;
      state.error = null;
    });
    builder.addCase(registerAsync.rejected, (state, action) => {
      state.isLoading = false;
      state.error = action.payload || 'Registration failed';
      state.isAuthenticated = false;
      state.user = null;
    });

    // Fetch current user
    builder.addCase(fetchCurrentUserAsync.pending, (state) => {
      state.isLoading = true;
    });
    builder.addCase(fetchCurrentUserAsync.fulfilled, (state, action: PayloadAction<User>) => {
      state.isLoading = false;
      state.user = action.payload;
      state.isAuthenticated = true;
      state.error = null;
    });
    builder.addCase(fetchCurrentUserAsync.rejected, (state) => {
      state.isLoading = false;
      state.isAuthenticated = false;
      state.user = null;
    });

    // Logout
    builder.addCase(logoutAsync.fulfilled, (state) => {
      state.user = null;
      state.isAuthenticated = false;
      state.error = null;
    });
  },
});

// Export actions
export const { clearError, logout, restoreSession } = authSlice.actions;

// Export reducer
export default authSlice.reducer;
