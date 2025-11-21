/**
 * Auth Redux Slice
 * Manages authentication state using Redux Toolkit
 */

import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import type { PayloadAction } from '@reduxjs/toolkit';
import LoginService from '@/global/api/actions/auth/api-login.service';
import RegisterService from '@/global/api/actions/auth/api-register.service';
import SessionManager from '@/global/utils/session-manager';
import { httpClient } from '@/global/api/http-client';
import type {
  LoginRequest,
  RegisterRequest,
  TokenResponse,
  User,
} from '@/global/models/auth.models';

/**
 * Auth state interface
 */
export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

/**
 * Initial auth state
 */
const initialState: AuthState = {
  user: null,
  token: SessionManager.getToken(),
  isAuthenticated: SessionManager.hasValidSession(),
  isLoading: false,
  error: null,
};

/**
 * Async thunk for user login
 */
export const loginAsync = createAsyncThunk<
  { token: TokenResponse; user: User },
  LoginRequest,
  { rejectValue: string }
>('auth/login', async (credentials, { rejectWithValue }) => {
  try {
    // Call login service
    const tokenResponse = await LoginService.login(credentials);

    // Store token
    SessionManager.setToken(tokenResponse.access_token);

    // Fetch user data
    const user = await httpClient.get<User>('/api/users/me');

    return { token: tokenResponse, user };
  } catch (error: any) {
    // Clear token on error
    SessionManager.clearToken();

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
  { token: TokenResponse; user: User },
  RegisterRequest,
  { rejectValue: string }
>('auth/register', async (userData, { rejectWithValue }) => {
  try {
    // Call register service
    const tokenResponse = await RegisterService.register(userData);

    // Store token
    SessionManager.setToken(tokenResponse.access_token);

    // Fetch user data
    const user = await httpClient.get<User>('/api/users/me');

    return { token: tokenResponse, user };
  } catch (error: any) {
    // Clear token on error
    SessionManager.clearToken();

    // Extract user-friendly error message from API response
    const errorMessage =
      error?.data?.detail || // FastAPI error format
      error?.response?.data?.detail || // Axios wrapped error
      error?.message ||
      'Registration failed. Please try again.';

    return rejectWithValue(errorMessage);
  }
});

/**
 * Async thunk for fetching current user
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
    SessionManager.clearToken();

    // Extract user-friendly error message from API response
    const errorMessage =
      error?.data?.detail || // FastAPI error format
      error?.response?.data?.detail || // Axios wrapped error
      error?.message ||
      'Failed to fetch user data. Please try logging in again.';

    return rejectWithValue(errorMessage);
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
     * Logout action - clears auth state and session
     */
    logout: (state) => {
      SessionManager.clearToken();
      state.user = null;
      state.token = null;
      state.isAuthenticated = false;
      state.error = null;
    },

    /**
     * Clear error action
     */
    clearError: (state) => {
      state.error = null;
    },

    /**
     * Set token action (for manual token setting)
     */
    setToken: (state, action: PayloadAction<string>) => {
      state.token = action.payload;
      SessionManager.setToken(action.payload);
      state.isAuthenticated = true;
    },

    /**
     * Restore session from storage (on app init)
     */
    restoreSession: (state) => {
      const token = SessionManager.getToken();
      const isValid = SessionManager.hasValidSession();

      if (token && isValid) {
        state.token = token;
        state.isAuthenticated = true;
      } else {
        SessionManager.clearToken();
        state.token = null;
        state.isAuthenticated = false;
      }
    },
  },
  extraReducers: (builder) => {
    // Login
    builder
      .addCase(loginAsync.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(loginAsync.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isAuthenticated = true;
        state.token = action.payload.token.access_token;
        state.user = action.payload.user;
        state.error = null;
      })
      .addCase(loginAsync.rejected, (state, action) => {
        state.isLoading = false;
        state.isAuthenticated = false;
        state.token = null;
        state.user = null;
        state.error = action.payload || 'Login failed';
      });

    // Register
    builder
      .addCase(registerAsync.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(registerAsync.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isAuthenticated = true;
        state.token = action.payload.token.access_token;
        state.user = action.payload.user;
        state.error = null;
      })
      .addCase(registerAsync.rejected, (state, action) => {
        state.isLoading = false;
        state.isAuthenticated = false;
        state.token = null;
        state.user = null;
        state.error = action.payload || 'Registration failed';
      });

    // Fetch current user
    builder
      .addCase(fetchCurrentUserAsync.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(fetchCurrentUserAsync.fulfilled, (state, action) => {
        state.isLoading = false;
        state.user = action.payload;
        state.isAuthenticated = true;
      })
      .addCase(fetchCurrentUserAsync.rejected, (state, action) => {
        state.isLoading = false;
        state.isAuthenticated = false;
        state.token = null;
        state.user = null;
        state.error = action.payload || 'Failed to fetch user';
      });
  },
});

/**
 * Export actions
 */
export const { logout, clearError, setToken, restoreSession } = authSlice.actions;

/**
 * Export reducer
 */
export default authSlice.reducer;
