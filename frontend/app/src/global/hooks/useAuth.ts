/**
 * useAuth Hook
 * Custom hook for accessing auth state and actions
 */

import { useCallback } from 'react';
import { useAppDispatch } from './useAppDispatch';
import { useAppSelector } from './useAppSelector';
import {
  loginAsync,
  registerAsync,
  logoutAsync,
  logout,
  clearError,
  fetchCurrentUserAsync,
  restoreSession,
} from '@/global/store/slices/authSlice';
import type { LoginRequest, RegisterRequest } from '@/global/models/auth.models';

/**
 * Custom hook for authentication
 * Provides auth state and actions to components
 */
export function useAuth() {
  const dispatch = useAppDispatch();

  // Select auth state from Redux store (NO TOKEN!)
  const { user, isAuthenticated, isLoading, error } = useAppSelector(
    (state) => state.auth
  );

  /**
   * Login user
   */
  const login = useCallback(
    async (credentials: LoginRequest) => {
      const result = await dispatch(loginAsync(credentials));
      return result;
    },
    [dispatch]
  );

  /**
   * Register new user
   */
  const register = useCallback(
    async (userData: RegisterRequest) => {
      const result = await dispatch(registerAsync(userData));
      return result;
    },
    [dispatch]
  );

  /**
   * Logout user (async - calls API)
   */
  const handleLogout = useCallback(async () => {
    await dispatch(logoutAsync());
  }, [dispatch]);

  /**
   * Clear error message
   */
  const handleClearError = useCallback(() => {
    dispatch(clearError());
  }, [dispatch]);

  /**
   * Fetch current user data
   */
  const fetchCurrentUser = useCallback(async () => {
    const result = await dispatch(fetchCurrentUserAsync());
    return result;
  }, [dispatch]);

  /**
   * Restore session from storage
   */
  const handleRestoreSession = useCallback(() => {
    dispatch(restoreSession());
  }, [dispatch]);

  return {
    // State
    user,
    isAuthenticated,
    isLoading,
    error,

    // Actions
    login,
    register,
    logout: handleLogout,
    clearError: handleClearError,
    fetchCurrentUser,
    restoreSession: handleRestoreSession,
  };
}

export default useAuth;
