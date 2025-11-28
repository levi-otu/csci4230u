/**
 * Password validation utilities
 * Validates password strength requirements
 */

export interface PasswordValidationResult {
  isValid: boolean;
  errors: string[];
  strength: 'weak' | 'medium' | 'strong';
}

/**
 * Validate password strength
 * Requirements:
 * - Minimum 8 characters
 * - At least one uppercase letter
 * - At least one lowercase letter
 * - At least one symbol
 */
export function validatePassword(password: string): PasswordValidationResult {
  const errors: string[] = [];

  // Check minimum length
  if (password.length < 8) {
    errors.push('Password must be at least 8 characters long');
  }

  // Check for uppercase letter
  if (!/[A-Z]/.test(password)) {
    errors.push('Password must contain at least one uppercase letter');
  }

  // Check for lowercase letter
  if (!/[a-z]/.test(password)) {
    errors.push('Password must contain at least one lowercase letter');
  }

  // Check for symbol/special character
  if (!/[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/~`]/.test(password)) {
    errors.push('Password must contain at least one symbol (!@#$%^&*(),.?":{}|<>_-+=[]\\\/~`)');
  }

  const isValid = errors.length === 0;

  // Calculate strength
  let strength: 'weak' | 'medium' | 'strong' = 'weak';
  if (isValid) {
    if (password.length >= 12) {
      strength = 'strong';
    } else if (password.length >= 10) {
      strength = 'medium';
    } else {
      strength = 'medium';
    }
  }

  return {
    isValid,
    errors,
    strength,
  };
}

/**
 * Get password strength score (0-100)
 */
export function getPasswordStrength(password: string): number {
  let score = 0;

  // Length score (max 40 points)
  score += Math.min(password.length * 2, 40);

  // Variety score (max 60 points)
  if (/[a-z]/.test(password)) score += 10;
  if (/[A-Z]/.test(password)) score += 10;
  if (/[0-9]/.test(password)) score += 10;
  if (/[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/~`]/.test(password)) score += 15;

  // Bonus for mixing character types (max 15 points)
  const hasLower = /[a-z]/.test(password);
  const hasUpper = /[A-Z]/.test(password);
  const hasNumber = /[0-9]/.test(password);
  const hasSymbol = /[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/~`]/.test(password);
  const varietyCount = [hasLower, hasUpper, hasNumber, hasSymbol].filter(Boolean).length;
  score += varietyCount * 3.75;

  return Math.min(score, 100);
}

/**
 * Get password strength label and color
 */
export function getPasswordStrengthDisplay(password: string): {
  label: string;
  color: string;
  percentage: number;
} {
  const strength = getPasswordStrength(password);

  if (strength < 40) {
    return { label: 'Weak', color: 'red', percentage: strength };
  } else if (strength < 70) {
    return { label: 'Medium', color: 'orange', percentage: strength };
  } else {
    return { label: 'Strong', color: 'green', percentage: strength };
  }
}

export default validatePassword;
