import { createBrowserRouter } from 'react-router-dom';
import type { RouteObject } from 'react-router-dom';
import { AppLayout } from '@/global/components/AppLayout';
import { homeRoutes } from '@/modules/home/routes';
import { loginRoutes } from '@/modules/login/routes';
import { clubsRoutes } from '@/modules/clubs/routes';
import { libraryRoutes } from '@/modules/library/routes';
import { SidebarProvider } from '@/global/contexts/SidebarContext';

// Placeholder pages for navigation items
const PlaceholderPage = ({ title }: { title: string }) => (
  <div className="space-y-6">
    <div>
      <h1 className="text-3xl font-bold tracking-tight">{title}</h1>
      <p className="text-muted-foreground mt-2">This page is coming soon.</p>
    </div>
  </div>
);

const routes: RouteObject[] = [
  // Authentication routes (no layout)
  ...loginRoutes,
  // Protected routes with layout
  {
    element: (
      <SidebarProvider>
        <AppLayout />
      </SidebarProvider>
    ),
    children: [
      ...homeRoutes,
      ...clubsRoutes,
      ...libraryRoutes,
      {
        path: '/pages',
        element: <PlaceholderPage title="Pages" />,
      },
      {
        path: '/settings',
        element: <PlaceholderPage title="Settings" />,
      },
    ],
  },
];

export const router = createBrowserRouter(routes);
