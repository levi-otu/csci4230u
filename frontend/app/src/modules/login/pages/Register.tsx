/**
 * Register Page Component
 * Provides user registration interface with password strength validation
 */

import { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Eye, EyeOff } from 'lucide-react';
import { useAuth } from '@/global/hooks/useAuth';
import { Button } from '@/global/components/ui/button';
import { Input } from '@/global/components/ui/input';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
  FormDescription,
} from '@/global/components/ui/form';
import { validatePassword, getPasswordStrengthDisplay } from '@/global/utils/password-validator';
import libraryBg from '@/assets/library.jpg';
import logo from '@/assets/the_public_square_full.png';

/**
 * Register form validation schema
 */
const registerFormSchema = z.object({
  username: z
    .string()
    .min(3, 'Username must be at least 3 characters')
    .max(255, 'Username must be less than 255 characters'),
  email: z
    .string()
    .min(1, 'Email is required')
    .email('Please enter a valid email address'),
  fullName: z
    .string()
    .max(255, 'Full name must be less than 255 characters')
    .optional(),
  password: z
    .string()
    .min(8, 'Password must be at least 8 characters')
    .refine((password) => validatePassword(password).isValid, {
      message: 'Password does not meet strength requirements',
    }),
  confirmPassword: z.string().min(1, 'Please confirm your password'),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
});

type RegisterFormValues = z.infer<typeof registerFormSchema>;

/**
 * Register page with glassmorphic card design
 */
export function Register() {
  const navigate = useNavigate();
  const location = useLocation();
  const { register: registerUser, isLoading, error, isAuthenticated, clearError } = useAuth();
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [passwordStrength, setPasswordStrength] = useState({ label: '', color: '', percentage: 0 });

  // Get the location user tried to access before being redirected
  const from = (location.state as any)?.from?.pathname || '/home';

  // Initialize form
  const form = useForm<RegisterFormValues>({
    resolver: zodResolver(registerFormSchema),
    defaultValues: {
      username: '',
      email: '',
      fullName: '',
      password: '',
      confirmPassword: '',
    },
  });

  // Watch password field for strength indicator
  const password = form.watch('password');

  useEffect(() => {
    if (password) {
      setPasswordStrength(getPasswordStrengthDisplay(password));
    } else {
      setPasswordStrength({ label: '', color: '', percentage: 0 });
    }
  }, [password]);

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      navigate(from, { replace: true });
    }
  }, [isAuthenticated, navigate, from]);

  // Clear API errors when form values change
  useEffect(() => {
    if (error) {
      clearError();
    }
  }, [form.watch('email'), form.watch('password')]);

  /**
   * Handle registration form submission
   */
  const onSubmit = async (values: RegisterFormValues) => {
    try {
      const result = await registerUser({
        username: values.username.trim(),
        email: values.email.trim(),
        password: values.password,
        full_name: values.fullName?.trim() || undefined,
      });

      // Check if registration was successful
      if (result.type === 'auth/register/fulfilled') {
        // Navigation handled by useEffect when isAuthenticated changes
      }
    } catch (err) {
      // Error is handled by Redux state
      console.error('Registration error:', err);
    }
  };

  /**
   * Navigate to login page
   */
  const handleLogin = () => {
    navigate('/login');
  };

  return (
    <div className="relative min-h-screen w-full overflow-hidden bg-background">
      {/* Background Image with Gradient Overlay */}
      <div
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{ backgroundImage: `url(${libraryBg})` }}
      >
        <div className="absolute inset-0 bg-gradient-to-br from-background/80 via-background/70 to-accent/30" />
      </div>

      {/* Register Card Container */}
      <div className="relative z-10 flex min-h-screen items-center justify-center px-4 py-12">
        {/* Glassmorphic Register Card */}
        <div className="w-full max-w-md">
          <div className="rounded-3xl border border-border bg-card/80 p-8 shadow-2xl backdrop-blur-xl">
            {/* Logo */}
            <div className="mb-6 flex justify-center">
              <img
                src={logo}
                alt="The Public Square"
                className="h-24 w-auto object-contain"
              />
            </div>

            {/* Header */}
            <h1 className="mb-8 text-center text-3xl font-bold text-foreground">
              Create Account
            </h1>

            {/* Register Form */}
            <Form {...form}>
              <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-5">
                {/* Username Field */}
                <FormField
                  control={form.control}
                  name="username"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Username</FormLabel>
                      <FormControl>
                        <Input
                          type="text"
                          placeholder="Choose a username"
                          autoComplete="username"
                          disabled={isLoading}
                          className="bg-background/50"
                          {...field}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                {/* Email Field */}
                <FormField
                  control={form.control}
                  name="email"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Email</FormLabel>
                      <FormControl>
                        <Input
                          type="email"
                          placeholder="Enter your email"
                          autoComplete="email"
                          disabled={isLoading}
                          className="bg-background/50"
                          {...field}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                {/* Full Name Field (Optional) */}
                <FormField
                  control={form.control}
                  name="fullName"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>
                        Full Name <span className="text-muted-foreground text-xs">(optional)</span>
                      </FormLabel>
                      <FormControl>
                        <Input
                          type="text"
                          placeholder="Enter your full name"
                          autoComplete="name"
                          disabled={isLoading}
                          className="bg-background/50"
                          {...field}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                {/* Password Field */}
                <FormField
                  control={form.control}
                  name="password"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Password</FormLabel>
                      <FormControl>
                        <div className="relative">
                          <Input
                            type={showPassword ? 'text' : 'password'}
                            placeholder="Create a password"
                            autoComplete="new-password"
                            disabled={isLoading}
                            className="bg-background/50 pr-10"
                            {...field}
                          />
                          <button
                            type="button"
                            onClick={() => setShowPassword(!showPassword)}
                            className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                            tabIndex={-1}
                          >
                            {showPassword ? (
                              <EyeOff className="h-4 w-4" />
                            ) : (
                              <Eye className="h-4 w-4" />
                            )}
                          </button>
                        </div>
                      </FormControl>
                      <FormDescription className="text-xs">
                        Min 8 characters, one uppercase, one lowercase, one symbol
                      </FormDescription>
                      {password && (
                        <div className="mt-2">
                          <div className="flex items-center gap-2 mb-1">
                            <div className="flex-1 h-2 bg-background/50 rounded-full overflow-hidden">
                              <div
                                className="h-full transition-all duration-300"
                                style={{
                                  width: `${passwordStrength.percentage}%`,
                                  backgroundColor:
                                    passwordStrength.color === 'red'
                                      ? '#ef4444'
                                      : passwordStrength.color === 'orange'
                                      ? '#f97316'
                                      : '#22c55e',
                                }}
                              />
                            </div>
                            <span
                              className="text-xs font-medium"
                              style={{
                                color:
                                  passwordStrength.color === 'red'
                                    ? '#ef4444'
                                    : passwordStrength.color === 'orange'
                                    ? '#f97316'
                                    : '#22c55e',
                              }}
                            >
                              {passwordStrength.label}
                            </span>
                          </div>
                        </div>
                      )}
                      <FormMessage />
                    </FormItem>
                  )}
                />

                {/* Confirm Password Field */}
                <FormField
                  control={form.control}
                  name="confirmPassword"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Confirm Password</FormLabel>
                      <FormControl>
                        <div className="relative">
                          <Input
                            type={showConfirmPassword ? 'text' : 'password'}
                            placeholder="Confirm your password"
                            autoComplete="new-password"
                            disabled={isLoading}
                            className="bg-background/50 pr-10"
                            {...field}
                          />
                          <button
                            type="button"
                            onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                            className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                            tabIndex={-1}
                          >
                            {showConfirmPassword ? (
                              <EyeOff className="h-4 w-4" />
                            ) : (
                              <Eye className="h-4 w-4" />
                            )}
                          </button>
                        </div>
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                {/* API Error Message */}
                {error && (
                  <div className="rounded-lg bg-destructive/20 border border-destructive/30 px-4 py-3 text-sm text-destructive">
                    {error}
                  </div>
                )}

                {/* Register Button */}
                <Button
                  type="submit"
                  disabled={isLoading}
                  className="w-full rounded-full bg-[#F38B12] text-white py-3 font-semibold hover:bg-[#D87A0F] hover:scale-105 hover:shadow-xl shadow-lg h-auto transition-all duration-200 cursor-pointer"
                >
                  {isLoading ? 'Creating account...' : 'Create Account'}
                </Button>
              </form>
            </Form>

            {/* Login Link */}
            <div className="mt-6 text-center text-sm text-muted-foreground">
              Already have an account?{' '}
              <Button
                type="button"
                variant="link"
                onClick={handleLogin}
                disabled={isLoading}
                className="h-auto p-0 font-semibold cursor-pointer"
              >
                Login
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Register;
