/**
 * Library Routes
 * Routes for the library module
 */

import type { RouteObject } from 'react-router-dom';
import { Library } from './pages/Library';

export const libraryRoutes: RouteObject[] = [
  {
    path: '/library',
    element: <Library />,
  },
];

export default libraryRoutes;
