/**
 * Redux Provider Component
 * Wraps the application with Redux Provider
 */

import { Provider } from 'react-redux';
import { store } from '@/global/store';
import type { ReactNode } from 'react';

interface ReduxProviderProps {
  children: ReactNode;
}

/**
 * Redux Provider wrapper component
 * Use this to wrap your app in main.tsx or App.tsx
 */
export function ReduxProvider({ children }: ReduxProviderProps) {
  return <Provider store={store}>{children}</Provider>;
}

export default ReduxProvider;
