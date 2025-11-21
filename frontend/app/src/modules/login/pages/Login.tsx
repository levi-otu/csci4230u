/**
 * Login Page Component
 * Provides user authentication interface with glassmorphic design
 */

import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useAuth } from '@/global/hooks/useAuth';
import { Button } from '@/global/components/ui/button';
import { Input } from '@/global/components/ui/input';
import { Checkbox } from '@/global/components/ui/checkbox';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/global/components/ui/form';
import libraryBg from '@/assets/library.jpg';
import logo from '@/assets/the_public_square_full.png';

/**
 * Login form validation schema
 */
const loginFormSchema = z.object({
  email: z
    .string()
    .min(1, 'Email is required')
    .email('Please enter a valid email address'),
  password: z
    .string()
    .min(1, 'Password is required')
    .min(6, 'Password must be at least 6 characters'),
  rememberMe: z.boolean(),
});

type LoginFormValues = z.infer<typeof loginFormSchema>;

/**
 * Login page with glassmorphic card design
 * Uses global dark theme with amber accent colors
 */
export function Login() {
  const navigate = useNavigate();
  const { login, isLoading, error, isAuthenticated, clearError } = useAuth();

  // Initialize form with React Hook Form and Zod validation
  const form = useForm<LoginFormValues>({
    resolver: zodResolver(loginFormSchema),
    defaultValues: {
      email: '',
      password: '',
      rememberMe: false,
    },
  });

  // Redirect if already authenticated
  useEffect(() => {
    if (isAuthenticated) {
      navigate('/home');
    }
  }, [isAuthenticated, navigate]);

  // Clear API errors when form values change
  useEffect(() => {
    if (error) {
      clearError();
    }
  }, [form.watch('email'), form.watch('password')]);

  /**
   * Handle login form submission
   */
  const onSubmit = async (values: LoginFormValues) => {
    try {
      const result = await login({
        email: values.email.trim(),
        password: values.password,
      });

      // Check if login was successful
      if (result.type === 'auth/login/fulfilled') {
        // Navigation handled by useEffect when isAuthenticated changes
      }
    } catch (err) {
      // Error is handled by Redux state
      console.error('Login error:', err);
    }
  };

  /**
   * Navigate to forgot password page
   */
  const handleForgotPassword = () => {
    navigate('/forgot-password');
  };

  /**
   * Navigate to register page
   */
  const handleRegister = () => {
    navigate('/register');
  };

  return (
    <div className="relative min-h-screen w-full overflow-hidden bg-background">
      {/* Background Image with Gradient Overlay */}
      <div
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{ backgroundImage: `url(${libraryBg})` }}
      >
        {/* Gradient overlay using theme colors - lighter to show more background */}
        <div className="absolute inset-0 bg-gradient-to-br from-background/80 via-background/70 to-accent/30" />
      </div>

      {/* Login Card Container */}
      <div className="relative z-10 flex min-h-screen items-center justify-center px-4 py-12">
        {/* Glassmorphic Login Card */}
        <div className="w-full max-w-md">
          <div className="rounded-3xl border border-border bg-card/80 p-8 shadow-2xl backdrop-blur-xl">
            {/* Logo */}
            <div className="mb-6 flex justify-center">
              <img
                src={logo}
                alt="The Public Square"
                className="h-32 w-auto object-contain"
              />
            </div>

            {/* Header */}
            <h1 className="mb-8 text-center text-3xl font-bold text-foreground">
              Login
            </h1>

            {/* Login Form */}
            <Form {...form}>
              <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
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

                {/* Password Field */}
                <FormField
                  control={form.control}
                  name="password"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Password</FormLabel>
                      <FormControl>
                        <Input
                          type="password"
                          placeholder="Enter your password"
                          autoComplete="current-password"
                          disabled={isLoading}
                          className="bg-background/50"
                          {...field}
                        />
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

                {/* Remember Me & Forgot Password */}
                <div className="flex items-center justify-between text-sm">
                  <FormField
                    control={form.control}
                    name="rememberMe"
                    render={({ field }) => (
                      <FormItem className="flex items-center gap-2 space-y-0">
                        <FormControl>
                          <Checkbox
                            checked={field.value}
                            onCheckedChange={field.onChange}
                            disabled={isLoading}
                          />
                        </FormControl>
                        <FormLabel className="cursor-pointer font-normal">
                          Remember Me
                        </FormLabel>
                      </FormItem>
                    )}
                  />
                  <Button
                    type="button"
                    variant="link"
                    onClick={handleForgotPassword}
                    disabled={isLoading}
                    className="h-auto p-0 cursor-pointer"
                  >
                    Forgot Password?
                  </Button>
                </div>

                {/* Login Button */}
                <Button
                  type="submit"
                  disabled={isLoading}
                  className="w-full rounded-full bg-[#F38B12] text-white py-3 font-semibold hover:bg-[#D87A0F] hover:scale-105 hover:shadow-xl shadow-lg h-auto transition-all duration-200 cursor-pointer"
                >
                  {isLoading ? 'Logging in...' : 'Log in'}
                </Button>
              </form>
            </Form>

            {/* Register Link */}
            <div className="mt-6 text-center text-sm text-muted-foreground">
              Don't have an account?{' '}
              <Button
                type="button"
                variant="link"
                onClick={handleRegister}
                disabled={isLoading}
                className="h-auto p-0 font-semibold cursor-pointer"
              >
                Register
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
