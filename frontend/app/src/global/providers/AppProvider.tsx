/**
 * App Provider Component
 * Combines all providers for the application
 */

import { ReduxProvider } from './ReduxProvider';
import type { ReactNode } from 'react';

interface AppProviderProps {
  children: ReactNode;
}

/**
 * Main app provider that wraps all context providers
 * Use this in your main.tsx or App.tsx:
 *
 * ```tsx
 * import { AppProvider } from '@/global/providers/AppProvider';
 *
 * <AppProvider>
 *   <App />
 * </AppProvider>
 * ```
 */
export function AppProvider({ children }: AppProviderProps) {
  return (
    <ReduxProvider>
      {/* Add other providers here as needed */}
      {children}
    </ReduxProvider>
  );
}

export default AppProvider;
