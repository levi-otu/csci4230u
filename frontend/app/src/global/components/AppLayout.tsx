import { Outlet } from 'react-router-dom';
import { Header } from './Header';
import { Navigation } from './Navigation';
import { useSidebar } from '@/global/contexts/SidebarContext';
import { cn } from '@/lib/utils';

export function AppLayout() {
  const { isOpen } = useSidebar();

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <Navigation />
      <main
        className={cn(
          "pt-16 min-h-screen transition-all duration-300",
          isOpen ? "lg:pl-64" : "lg:pl-16"
        )}
      >
        <div className="p-6 max-w-[1600px] mx-auto">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
