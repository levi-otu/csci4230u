/**
 * Typed useDispatch hook
 * Use throughout the app instead of plain `useDispatch`
 */

import { useDispatch } from 'react-redux';
import type { AppDispatch } from '@/global/store';

/**
 * Pre-typed useDispatch hook
 */
export const useAppDispatch = useDispatch.withTypes<AppDispatch>();

export default useAppDispatch;
