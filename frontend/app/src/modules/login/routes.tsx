/**
 * Login module routes
 * Defines authentication-related routes
 */

import type { RouteObject } from 'react-router-dom';
import { Login } from './pages/Login';

/**
 * Login routes configuration
 * These routes are outside the main app layout (no sidebar)
 */
export const loginRoutes: RouteObject[] = [
  {
    path: '/',
    element: <Login />,
  },
  {
    path: '/login',
    element: <Login />,
  },
  // Register route placeholder - to be implemented
  {
    path: '/register',
    element: (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold">Register</h1>
          <p className="text-muted-foreground">Coming soon...</p>
        </div>
      </div>
    ),
  },
  // Forgot password route placeholder
  {
    path: '/forgot-password',
    element: (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold">Forgot Password</h1>
          <p className="text-muted-foreground">Coming soon...</p>
        </div>
      </div>
    ),
  },
];

export default loginRoutes;
