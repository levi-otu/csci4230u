/**
 * AuthGuard Component
 * Protects routes by checking authentication status with cookie-based auth
 * Redirects to login if user is not authenticated
 */

import { useEffect, useState } from 'react';
import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '@/global/hooks/useAuth';

/**
 * AuthGuard wraps protected routes and ensures user is authenticated
 * Verifies authentication by fetching current user from backend
 * If not authenticated, redirects to /login
 */
export function AuthGuard() {
  const location = useLocation();
  const { isAuthenticated, fetchCurrentUser } = useAuth();
  const [isChecking, setIsChecking] = useState(true);

  useEffect(() => {
    // On mount, verify authentication by fetching current user
    // If refresh token cookie is valid, this will succeed
    const checkAuth = async () => {
      if (!isAuthenticated) {
        try {
          await fetchCurrentUser();
        } catch (error) {
          // Not authenticated - will redirect below
          console.log('Auth check failed:', error);
        }
      }
      setIsChecking(false);
    };

    checkAuth();
  }, []);

  // Show loading state while checking authentication
  if (isChecking) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="text-center">
          <div className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent"></div>
          <p className="mt-2 text-sm text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  // If not authenticated after check, redirect to login
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Render protected routes
  return <Outlet />;
}

export default AuthGuard;
