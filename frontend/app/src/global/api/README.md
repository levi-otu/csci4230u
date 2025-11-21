# HTTPClient API Documentation

## Overview

The HTTPClient is a flexible HTTP client built on top of Axios with interceptor support, inspired by Angular's HttpClient architecture. It provides a centralized way to handle API requests with built-in authentication, error handling, and session management.

## Quick Start

### Basic Usage

```typescript
import { httpClient, LoginService } from '@/global/api';
import type { LoginRequest } from '@/global/models';

// Login example
const credentials: LoginRequest = {
  email: 'user@example.com',
  password: 'password123'
};

try {
  const response = await LoginService.login(credentials);
  console.log('Login successful:', response);
} catch (error) {
  console.error('Login failed:', error);
}
```

### Making API Requests

```typescript
import { httpClient } from '@/global/api';

// GET request
const users = await httpClient.get('/api/users');

// POST request
const newUser = await httpClient.post('/api/users', {
  username: 'johndoe',
  email: 'john@example.com'
});

// PUT request
const updatedUser = await httpClient.put('/api/users/123', {
  full_name: 'John Doe'
});

// DELETE request
await httpClient.delete('/api/users/123');
```

## Configuration

### Environment Variables

Create a `.env` file in the root of your frontend app:

```env
VITE_API_BASE_URL=http://localhost:8000
```

### Config File

The configuration is centralized in `src/global/config.ts`:

```typescript
export const config = {
  baseApiUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  requestTimeout: 30000,
  tokenStorageKey: 'auth_token',
};
```

## Authentication

### Login

```typescript
import { LoginService } from '@/global/api';

const response = await LoginService.login({
  email: 'user@example.com',
  password: 'password123'
});

// Token is automatically stored in sessionStorage
// All subsequent requests will include the token in the Authorization header
```

### Register

```typescript
import { LoginService } from '@/global/api';

const response = await LoginService.register({
  username: 'johndoe',
  email: 'john@example.com',
  password: 'password123',
  full_name: 'John Doe'
});
```

### Logout

```typescript
import { LoginService } from '@/global/api';

LoginService.logout();
// Clears token from sessionStorage and dispatches logout event
```

### Check Authentication Status

```typescript
import { LoginService } from '@/global/api';

if (LoginService.isAuthenticated()) {
  console.log('User is authenticated');
}
```

## Session Management

### SessionManager

```typescript
import { SessionManager } from '@/global/api';

// Set token
SessionManager.setToken('your-jwt-token');

// Get token
const token = SessionManager.getToken();

// Clear token
SessionManager.clearToken();

// Check if session is valid
if (SessionManager.hasValidSession()) {
  console.log('Session is valid');
}
```

## Interceptors

### Request Interceptor

```typescript
import { httpClient } from '@/global/api';

httpClient.addRequestInterceptor((config) => {
  // Add custom headers
  if (config.headers) {
    config.headers['X-Custom-Header'] = 'value';
  }
  return config;
});
```

### Response Interceptor

```typescript
import { httpClient } from '@/global/api';

httpClient.addResponseInterceptor(
  (response) => {
    // Transform response
    console.log('Response received:', response);
    return response;
  },
  (error) => {
    // Handle errors
    console.error('Response error:', error);
    throw error;
  }
);
```

## Error Handling

```typescript
import { httpClient, ApiError } from '@/global/api';

try {
  const data = await httpClient.get('/api/users');
} catch (error) {
  if (error instanceof ApiError) {
    console.error('Status:', error.status);
    console.error('Message:', error.message);
    console.error('Data:', error.data);
  } else {
    console.error('Unexpected error:', error);
  }
}
```

## Events

The HTTPClient dispatches custom events that you can listen to:

### Login Event

```typescript
window.addEventListener('user-login', (event: CustomEvent) => {
  console.log('User logged in:', event.detail);
});
```

### Logout Event

```typescript
window.addEventListener('user-logout', () => {
  console.log('User logged out');
  // Redirect to login page, etc.
});
```

### Unauthorized Event

```typescript
window.addEventListener('unauthorized', () => {
  console.log('Unauthorized - redirecting to login');
  // Handle 401 errors globally
});
```

## Advanced Usage

### Creating Custom HTTP Client

```typescript
import { HTTPClient } from '@/global/api';

const customClient = new HTTPClient({
  baseURL: 'https://api.example.com',
  timeout: 10000,
  defaultHeaders: {
    'X-API-Key': 'your-api-key'
  }
});

// Add custom interceptors
customClient.addRequestInterceptor((config) => {
  // Custom logic
  return config;
});
```

### Direct Axios Access

```typescript
import { httpClient } from '@/global/api';

const axiosInstance = httpClient.getAxiosInstance();
// Use axios directly if needed
```

## TypeScript Support

All types are fully typed with TypeScript:

```typescript
import type {
  LoginRequest,
  TokenResponse,
  User
} from '@/global/models';

import type {
  HttpRequestOptions,
  HttpRequestInterceptor
} from '@/global/api';
```

## Security Best Practices

1. **Token Storage**: Tokens are stored in `sessionStorage` (not `localStorage`) for better security
2. **Automatic Token Injection**: Tokens are automatically added to request headers via interceptor
3. **401 Handling**: Unauthorized requests automatically clear the session
4. **HTTPS**: Always use HTTPS in production
5. **Token Expiry**: Tokens are validated before use to check expiry

## File Structure

```
src/global/
├── config.ts                           # Global configuration
├── api/
│   ├── http-client.ts                  # HTTPClient implementation
│   ├── index.ts                        # API exports
│   ├── actions/
│   │   └── auth/
│   │       └── api-login.service.ts    # Login/auth service
│   └── README.md                       # This file
└── models/
    ├── auth.models.ts                  # Auth-related models
    └── index.ts                        # Model exports
```
