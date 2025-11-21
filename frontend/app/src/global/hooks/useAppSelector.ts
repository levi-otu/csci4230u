/**
 * Typed useSelector hook
 * Use throughout the app instead of plain `useSelector`
 */

import { useSelector } from 'react-redux';
import type { RootState } from '@/global/store';

/**
 * Pre-typed useSelector hook
 */
export const useAppSelector = useSelector.withTypes<RootState>();

export default useAppSelector;
