import type { RouteObject } from 'react-router-dom';
import { Clubs } from './pages/Clubs';
import { Club } from './pages/pages/club/Club';

export const clubsRoutes: RouteObject[] = [
  {
    path: '/clubs',
    element: <Clubs />,
  },
  {
    path: '/clubs/:clubId',
    element: <Club />,
  },
];
