/**
 * HTTPClient - A flexible HTTP client with interceptor support using Axios
 * Inspired by Angular's HttpClient architecture
 */

import axios, { AxiosError } from 'axios';
import type {
  AxiosInstance,
  AxiosRequestConfig,
  AxiosResponse,
  InternalAxiosRequestConfig,
} from 'axios';
import { config } from '@/global/config';

/**
 * HTTP request interceptor function type
 */
export type HttpRequestInterceptor = (
  config: InternalAxiosRequestConfig
) => InternalAxiosRequestConfig | Promise<InternalAxiosRequestConfig>;

/**
 * HTTP request error interceptor function type
 */
export type HttpRequestErrorInterceptor = (error: AxiosError) => Promise<never>;

/**
 * HTTP response interceptor function type
 */
export type HttpResponseInterceptor = (
  response: AxiosResponse
) => AxiosResponse | Promise<AxiosResponse>;

/**
 * HTTP response error interceptor function type
 */
export type HttpResponseErrorInterceptor = (error: AxiosError) => Promise<never>;

/**
 * HTTP Client configuration options
 */
export interface HttpClientConfig {
  baseURL?: string;
  timeout?: number;
  defaultHeaders?: Record<string, string>;
}

/**
 * HTTP request options
 */
export interface HttpRequestOptions extends Omit<AxiosRequestConfig, 'data'> {
  skipInterceptors?: boolean;
}

/**
 * API Error class for standardized error handling
 */
export class ApiError extends Error {
  status: number;
  statusText: string;
  data?: unknown;

  constructor(
    message: string,
    status: number,
    statusText: string,
    data?: unknown
  ) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.statusText = statusText;
    this.data = data;
  }

  static fromAxiosError(error: AxiosError): ApiError {
    const status = error.response?.status || 0;
    const statusText = error.response?.statusText || 'Unknown Error';
    const data = error.response?.data;
    const message = error.message || `HTTP Error ${status}: ${statusText}`;

    return new ApiError(message, status, statusText, data);
  }
}

/**
 * HTTPClient - Main HTTP client class with interceptor support using Axios
 */
export class HTTPClient {
  private axiosInstance: AxiosInstance;
  private accessToken: string | null = null;

  constructor(config: HttpClientConfig = {}) {
    // Create axios instance with configuration
    this.axiosInstance = axios.create({
      baseURL: config.baseURL || '',
      timeout: config.timeout || 30000,
      headers: config.defaultHeaders || {
        'Content-Type': 'application/json',
      },
    });
  }

  /**
   * Set the access token for authenticated requests
   */
  setAccessToken(token: string | null): void {
    this.accessToken = token;
    if (token) {
      this.axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
      delete this.axiosInstance.defaults.headers.common['Authorization'];
    }
  }

  /**
   * Get the current access token
   */
  getAccessToken(): string | null {
    return this.accessToken;
  }

  /**
   * Get the underlying Axios instance for advanced usage
   */
  getAxiosInstance(): AxiosInstance {
    return this.axiosInstance;
  }

  /**
   * Add a request interceptor
   */
  addRequestInterceptor(
    onFulfilled?: HttpRequestInterceptor,
    onRejected?: HttpRequestErrorInterceptor
  ): number {
    return this.axiosInstance.interceptors.request.use(onFulfilled, onRejected);
  }

  /**
   * Add a response interceptor
   */
  addResponseInterceptor(
    onFulfilled?: HttpResponseInterceptor,
    onRejected?: HttpResponseErrorInterceptor
  ): number {
    return this.axiosInstance.interceptors.response.use(onFulfilled, onRejected);
  }

  /**
   * Remove a request interceptor
   */
  removeRequestInterceptor(interceptorId: number): void {
    this.axiosInstance.interceptors.request.eject(interceptorId);
  }

  /**
   * Remove a response interceptor
   */
  removeResponseInterceptor(interceptorId: number): void {
    this.axiosInstance.interceptors.response.eject(interceptorId);
  }

  /**
   * GET request
   */
  async get<T>(url: string, options?: HttpRequestOptions): Promise<T> {
    const response = await this.axiosInstance.get<T>(url, options);
    return response.data;
  }

  /**
   * POST request
   */
  async post<T>(
    url: string,
    data?: unknown,
    options?: HttpRequestOptions
  ): Promise<T> {
    const response = await this.axiosInstance.post<T>(url, data, options);
    return response.data;
  }

  /**
   * PUT request
   */
  async put<T>(
    url: string,
    data?: unknown,
    options?: HttpRequestOptions
  ): Promise<T> {
    const response = await this.axiosInstance.put<T>(url, data, options);
    return response.data;
  }

  /**
   * PATCH request
   */
  async patch<T>(
    url: string,
    data?: unknown,
    options?: HttpRequestOptions
  ): Promise<T> {
    const response = await this.axiosInstance.patch<T>(url, data, options);
    return response.data;
  }

  /**
   * DELETE request
   */
  async delete<T>(url: string, options?: HttpRequestOptions): Promise<T> {
    const response = await this.axiosInstance.delete<T>(url, options);
    return response.data;
  }

  /**
   * Generic request method for full control
   */
  async request<T>(config: AxiosRequestConfig): Promise<T> {
    const response = await this.axiosInstance.request<T>(config);
    return response.data;
  }
}

/**
 * Default HTTP client instance with cookie-based auth and auto-refresh
 */
export const createDefaultHttpClient = (): HTTPClient => {
  const client = new HTTPClient({
    baseURL: config.baseApiUrl,
    timeout: config.requestTimeout,
    defaultHeaders: {
      'Content-Type': 'application/json',
    },
  });

  // Enable credentials to send cookies automatically
  client.getAxiosInstance().defaults.withCredentials = true;

  // Track if we're currently refreshing to avoid refresh loops
  let isRefreshing = false;
  let refreshPromise: Promise<string> | null = null;

  // Add response error interceptor for auto-refresh and error handling
  client.addResponseInterceptor(
    (response) => response,
    async (error: AxiosError) => {
      const originalRequest = error.config;

      // Convert to ApiError for consistency
      const apiError = ApiError.fromAxiosError(error);

      // Log error for debugging
      console.error('API Error:', {
        status: apiError.status,
        message: apiError.message,
        data: apiError.data,
        url: originalRequest?.url,
      });

      // Handle 401 Unauthorized - try to refresh token
      if (apiError.status === 401 && originalRequest && !originalRequest.url?.includes('/auth/refresh')) {
        // Avoid refresh loop
        if (isRefreshing) {
          // Wait for the current refresh to complete
          try {
            await refreshPromise;
            // Retry original request
            return client.getAxiosInstance().request(originalRequest);
          } catch (refreshError) {
            // Refresh failed, redirect to login
            window.dispatchEvent(new Event('session-expired'));
            window.location.href = '/login';
            throw apiError;
          }
        }

        isRefreshing = true;

        try {
          // Try to refresh the access token
          refreshPromise = client.post<{ access_token: string }>('/api/auth/refresh', {})
            .then(response => {
              // Store the new access token
              client.setAccessToken(response.access_token);
              return response.access_token;
            });

          await refreshPromise;

          isRefreshing = false;
          refreshPromise = null;

          // Retry the original request with new token
          return client.getAxiosInstance().request(originalRequest);
        } catch (refreshError) {
          // Refresh failed - session expired
          isRefreshing = false;
          refreshPromise = null;

          // Clear access token
          client.setAccessToken(null);

          // Dispatch event and redirect to login
          window.dispatchEvent(new Event('session-expired'));
          window.location.href = '/login';
          throw apiError;
        }
      }

      throw apiError;
    }
  );

  return client;
};

/**
 * Singleton instance of the HTTP client
 */
export const httpClient = createDefaultHttpClient();
