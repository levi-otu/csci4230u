/**
 * API module exports
 * Central export point for all API-related functionality
 */

// HTTP Client
export { HTTPClient, httpClient, createDefaultHttpClient, ApiError } from './http-client';
export type {
  HttpClientConfig,
  HttpRequestOptions,
  HttpRequestInterceptor,
  HttpRequestErrorInterceptor,
  HttpResponseInterceptor,
  HttpResponseErrorInterceptor,
} from './http-client';

// Auth Services
export { LoginService } from './actions/auth/api-login.service';
export { default as loginService } from './actions/auth/api-login.service';
export { RegisterService } from './actions/auth/api-register.service';
export { default as registerService } from './actions/auth/api-register.service';
