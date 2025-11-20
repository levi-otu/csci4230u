import { Home, Users, FileText, BookOpen, Menu, X } from 'lucide-react';
import { Button } from '@/global/components/ui/button';
import { Sheet, SheetContent, SheetTrigger } from '@/global/components/ui/sheet';
import { Separator } from '@/global/components/ui/separator';
import { Link, useLocation } from 'react-router-dom';
import { cn } from '@/lib/utils';
import { useSidebar } from '@/global/contexts/SidebarContext';

interface NavItem {
  title: string;
  href: string;
  icon: React.ComponentType<{ className?: string }>;
}

const navItems: NavItem[] = [
  {
    title: 'Home',
    href: '/',
    icon: Home,
  },
  {
    title: 'Clubs',
    href: '/clubs',
    icon: Users,
  },
  {
    title: 'Pages',
    href: '/pages',
    icon: FileText,
  },
  {
    title: 'Library',
    href: '/library',
    icon: BookOpen,
  },
];

export function Navigation() {
  const { isOpen, toggle } = useSidebar();
  const location = useLocation();

  const NavContent = () => (
    <nav className="flex flex-col gap-2 p-4">
      {navItems.map((item) => {
        const Icon = item.icon;
        const isActive = location.pathname === item.href;

        return (
          <Link
            key={item.href}
            to={item.href}
            className={cn(
              'flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors',
              isActive
                ? 'bg-accent text-accent-foreground'
                : 'text-muted-foreground hover:bg-accent/50 hover:text-foreground'
            )}
          >
            <Icon className="h-5 w-5" />
            <span>{item.title}</span>
          </Link>
        );
      })}
    </nav>
  );

  return (
    <>
      {/* Mobile Navigation */}
      <Sheet>
        <SheetTrigger asChild className="lg:hidden">
          <Button variant="ghost" size="icon" className="fixed left-4 top-20 z-40">
            <Menu className="h-5 w-5" />
          </Button>
        </SheetTrigger>
        <SheetContent side="left" className="w-64 p-0">
          <div className="py-4">
            <h2 className="px-6 text-lg font-semibold">Navigation</h2>
            <Separator className="my-4" />
            <NavContent />
          </div>
        </SheetContent>
      </Sheet>

      {/* Desktop Navigation */}
      <aside
        className={cn(
          'hidden lg:block fixed left-0 top-16 h-[calc(100vh-4rem)] border-r border-border bg-card transition-all duration-300',
          isOpen ? 'w-64' : 'w-16'
        )}
      >
        <div className="flex h-full flex-col">
          {/* Toggle Button */}
          <div className={cn("flex items-center p-2", isOpen ? "justify-end" : "justify-center")}>
            <Button
              variant="ghost"
              size="icon"
              onClick={toggle}
              className="h-8 w-8"
            >
              {isOpen ? (
                <X className="h-4 w-4" />
              ) : (
                <Menu className="h-4 w-4" />
              )}
            </Button>
          </div>

          <Separator />

          {/* Navigation Items */}
          {isOpen ? (
            <NavContent />
          ) : (
            <nav className="flex flex-col gap-2 p-2">
              {navItems.map((item) => {
                const Icon = item.icon;
                const isActive = location.pathname === item.href;

                return (
                  <Link
                    key={item.href}
                    to={item.href}
                    className={cn(
                      'flex items-center justify-center rounded-lg p-2 transition-colors',
                      isActive
                        ? 'bg-accent text-accent-foreground'
                        : 'text-muted-foreground hover:bg-accent/50 hover:text-foreground'
                    )}
                    title={item.title}
                  >
                    <Icon className="h-5 w-5" />
                  </Link>
                );
              })}
            </nav>
          )}
        </div>
      </aside>
    </>
  );
}
