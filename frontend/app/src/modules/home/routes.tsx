import type { RouteObject } from 'react-router-dom';
import { HomePage } from './pages/HomePage';

export const homeRoutes: RouteObject[] = [
  {
    path: '/home',
    element: <HomePage />,
  },
];
