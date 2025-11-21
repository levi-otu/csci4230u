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
 * Default HTTP client instance with auth token interceptor
 */
export const createDefaultHttpClient = (): HTTPClient => {
  const client = new HTTPClient({
    baseURL: config.baseApiUrl,
    timeout: config.requestTimeout,
    defaultHeaders: {
      'Content-Type': 'application/json',
    },
  });

  // Add authentication token request interceptor
  client.addRequestInterceptor((axiosConfig) => {
    const token = sessionStorage.getItem(config.tokenStorageKey);

    if (token && axiosConfig.headers) {
      axiosConfig.headers.Authorization = `Bearer ${token}`;
    }

    return axiosConfig;
  });

  // Add response error interceptor for standardized error handling
  client.addResponseInterceptor(
    (response) => response,
    async (error: AxiosError) => {
      // Convert to ApiError for consistency
      const apiError = ApiError.fromAxiosError(error);

      // Log error for debugging
      console.error('API Error:', {
        status: apiError.status,
        message: apiError.message,
        data: apiError.data,
      });

      // Handle 401 Unauthorized - clear session
      if (apiError.status === 401) {
        sessionStorage.removeItem(config.tokenStorageKey);
        // You can dispatch an event or call a logout function here
        window.dispatchEvent(new Event('unauthorized'));
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
