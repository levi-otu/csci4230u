/**
 * Redux Store Configuration
 * Central store setup using Redux Toolkit
 */

import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';

/**
 * Configure and create the Redux store
 */
export const store = configureStore({
  reducer: {
    auth: authReducer,
    // Add other reducers here as your app grows
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        // Ignore these action types
        ignoredActions: ['auth/login/pending', 'auth/register/pending'],
      },
    }),
});

/**
 * Infer the `RootState` and `AppDispatch` types from the store itself
 */
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

export default store;
