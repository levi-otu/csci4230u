# Redux Architecture - Authentication System

## Overview

This document describes the Redux-based authentication architecture implemented for the HTTPClient system.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         React Components                         │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐       │
│  │ LoginPage     │  │ UserProfile   │  │ ProtectedRoute│       │
│  └───────┬───────┘  └───────┬───────┘  └───────┬───────┘       │
│          │                  │                  │                 │
│          └──────────────────┴──────────────────┘                 │
│                             │                                    │
│                    ┌────────▼────────┐                          │
│                    │   useAuth Hook   │                          │
│                    └────────┬────────┘                          │
└─────────────────────────────┼───────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                        Redux Layer                               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    Redux Store                            │   │
│  │  ┌──────────────────────────────────────────────────┐    │   │
│  │  │              Auth Slice                          │    │   │
│  │  │  ┌────────────────┐  ┌────────────────────────┐ │    │   │
│  │  │  │     State      │  │   Async Thunks        │ │    │   │
│  │  │  │  - user        │  │  - loginAsync         │ │    │   │
│  │  │  │  - token       │  │  - registerAsync      │ │    │   │
│  │  │  │  - isAuth      │  │  - fetchCurrentUser   │ │    │   │
│  │  │  │  - isLoading   │  └──────────┬────────────┘ │    │   │
│  │  │  │  - error       │             │              │    │   │
│  │  │  └────────────────┘             │              │    │   │
│  │  └───────────────────────────────────┼──────────────┘    │   │
│  └────────────────────────────────────────┼──────────────────┘   │
└─────────────────────────────────────────────┼──────────────────┘
                                              │
┌─────────────────────────────────────────────▼──────────────────┐
│                       Services Layer                            │
│  ┌──────────────────┐  ┌──────────────────┐                    │
│  │  LoginService    │  │ RegisterService  │                    │
│  │  .login()        │  │ .register()      │                    │
│  └────────┬─────────┘  └────────┬─────────┘                    │
│           │                     │                               │
│           └──────────┬──────────┘                               │
│                      │                                          │
│           ┌──────────▼──────────┐                              │
│           │    HTTPClient       │                              │
│           │  (Axios-based)      │                              │
│           └──────────┬──────────┘                              │
└──────────────────────┼─────────────────────────────────────────┘
                       │
┌──────────────────────▼─────────────────────────────────────────┐
│                    Utilities Layer                              │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              SessionManager                            │    │
│  │  - setToken()      - getToken()                        │    │
│  │  - clearToken()    - hasValidSession()                 │    │
│  │  - decodeToken()   - getUserId()                       │    │
│  └────────────────────────────────────────────────────────┘    │
│                             │                                   │
│                    ┌────────▼────────┐                         │
│                    │  sessionStorage  │                         │
│                    └──────────────────┘                         │
└─────────────────────────────────────────────────────────────────┘
```

## Layer Responsibilities

### 1. Components Layer
**Responsibility**: UI rendering and user interaction

- Uses `useAuth` hook to access state and actions
- Dispatches actions via hook methods
- Renders based on auth state (isAuthenticated, isLoading, error)
- Does NOT directly call services or manage tokens

**Example**:
```tsx
const { login, isLoading, error } = useAuth();
await login({ email, password });
```

### 2. Hooks Layer
**Responsibility**: Bridge between components and Redux

- `useAuth`: Main hook providing auth state and actions
- `useAppDispatch`: Typed Redux dispatch hook
- `useAppSelector`: Typed Redux selector hook

**Key Point**: Components should ONLY use hooks, never Redux directly.

### 3. Redux Layer
**Responsibility**: State management and orchestration

#### State (authSlice.ts)
```typescript
{
  user: User | null,
  token: string | null,
  isAuthenticated: boolean,
  isLoading: boolean,
  error: string | null
}
```

#### Async Thunks
- `loginAsync`: Orchestrates login flow
  1. Calls LoginService
  2. Stores token via SessionManager
  3. Fetches user data
  4. Updates state

- `registerAsync`: Orchestrates registration flow
  1. Calls RegisterService
  2. Stores token via SessionManager
  3. Fetches user data
  4. Updates state

- `fetchCurrentUserAsync`: Gets current user data
  1. Calls HTTPClient to fetch user
  2. Updates user in state
  3. Clears session on failure

#### Synchronous Actions
- `logout`: Clears state and session
- `clearError`: Removes error message
- `setToken`: Manually sets token
- `restoreSession`: Restores from sessionStorage

### 4. Services Layer
**Responsibility**: HTTP requests ONLY

- `LoginService.login()`: POST to /api/auth/login
- `RegisterService.register()`: POST to /api/auth/register

**Key Point**: Services do NOT:
- Manage state
- Store tokens
- Handle errors (beyond throwing)

### 5. HTTPClient Layer
**Responsibility**: HTTP transport and interceptors

- Axios-based HTTP client
- Request interceptor: Adds Bearer token from SessionManager
- Response interceptor: Handles 401 errors
- Error interceptor: Logs and transforms errors

### 6. Utilities Layer
**Responsibility**: Token storage and validation

- `SessionManager`: Manages sessionStorage
- Decodes JWT tokens
- Validates token expiry
- No direct state management

## Data Flow Examples

### Login Flow

```
User submits form
    │
    ▼
Component calls login({ email, password })
    │
    ▼
useAuth dispatches loginAsync thunk
    │
    ▼
Thunk calls LoginService.login()
    │
    ▼
LoginService calls httpClient.post('/api/auth/login', credentials)
    │
    ▼
HTTPClient adds interceptors and makes request
    │
    ▼
Backend responds with { access_token, token_type }
    │
    ▼
Thunk calls SessionManager.setToken(token)
    │
    ▼
SessionManager stores to sessionStorage
    │
    ▼
Thunk calls httpClient.get('/api/users/me')
    │
    ▼
HTTPClient interceptor adds Bearer token
    │
    ▼
Backend responds with user data
    │
    ▼
Thunk updates Redux state with user and token
    │
    ▼
Component re-renders with new state
```

### Making Authenticated Request

```
Component calls httpClient.get('/api/users')
    │
    ▼
HTTPClient request interceptor runs
    │
    ▼
Interceptor calls SessionManager.getToken()
    │
    ▼
SessionManager retrieves from sessionStorage
    │
    ▼
Interceptor adds Authorization: Bearer {token}
    │
    ▼
Request sent to backend
    │
    ▼
Backend validates token and responds
    │
    ▼
HTTPClient returns data to component
```

### 401 Error Handling

```
Backend returns 401 Unauthorized
    │
    ▼
HTTPClient response interceptor catches error
    │
    ▼
Interceptor calls SessionManager.clearToken()
    │
    ▼
Interceptor dispatches 'unauthorized' event
    │
    ▼
App can listen to event and redirect to login
```

## File Organization

```
src/global/
├── api/
│   ├── http-client.ts              # Layer 5: HTTP transport
│   ├── actions/auth/
│   │   ├── api-login.service.ts    # Layer 4: Login endpoint
│   │   └── api-register.service.ts # Layer 4: Register endpoint
│   └── index.ts                    # Exports
│
├── store/
│   ├── index.ts                    # Redux store setup
│   └── slices/
│       ├── authSlice.ts            # Layer 3: Auth state
│       └── index.ts                # Exports
│
├── hooks/
│   ├── useAuth.ts                  # Layer 2: Main auth hook
│   ├── useAppDispatch.ts           # Layer 2: Typed dispatch
│   ├── useAppSelector.ts           # Layer 2: Typed selector
│   └── index.ts                    # Exports
│
├── utils/
│   ├── session-manager.ts          # Layer 6: Token management
│   └── index.ts                    # Exports
│
├── providers/
│   ├── AppProvider.tsx             # App setup
│   ├── ReduxProvider.tsx           # Redux provider
│   └── index.ts                    # Exports
│
└── models/
    └── auth.models.ts              # TypeScript interfaces
```

## Key Principles

### 1. Separation of Concerns
- Each layer has a single responsibility
- No layer should skip layers (e.g., components calling services directly)
- State management is centralized in Redux

### 2. Single Source of Truth
- Auth state lives ONLY in Redux
- Token storage managed by SessionManager
- No duplicated state in components

### 3. Unidirectional Data Flow
- Actions → Thunks → Services → HTTPClient → Backend
- State updates flow back through Redux to components

### 4. Type Safety
- All layers fully typed with TypeScript
- Type-safe hooks (useAppDispatch, useAppSelector)
- Type-safe async thunks

### 5. Testability
- Services can be tested independently
- Redux logic can be tested with mock store
- Components can be tested with test store

## Testing Strategy

### Unit Tests

**Services**:
```typescript
test('LoginService.login calls correct endpoint', async () => {
  const mockPost = jest.fn().mockResolvedValue({ access_token: 'token' });
  httpClient.post = mockPost;

  await LoginService.login({ email: 'test@test.com', password: 'pass' });

  expect(mockPost).toHaveBeenCalledWith('/api/auth/login', {
    email: 'test@test.com',
    password: 'pass'
  });
});
```

**SessionManager**:
```typescript
test('SessionManager stores token', () => {
  SessionManager.setToken('test-token');
  expect(sessionStorage.getItem('auth_token')).toBe('test-token');
});
```

**Redux Slice**:
```typescript
test('loginAsync updates state on success', async () => {
  const store = createTestStore();
  await store.dispatch(loginAsync({ email: 'test@test.com', password: 'pass' }));

  const state = store.getState().auth;
  expect(state.isAuthenticated).toBe(true);
  expect(state.user).toBeDefined();
});
```

### Integration Tests

**Component with Redux**:
```typescript
test('LoginPage logs in user', async () => {
  const store = createTestStore();
  const { getByLabelText, getByText } = render(
    <Provider store={store}>
      <LoginPage />
    </Provider>
  );

  fireEvent.change(getByLabelText('Email'), { target: { value: 'test@test.com' }});
  fireEvent.change(getByLabelText('Password'), { target: { value: 'password' }});
  fireEvent.click(getByText('Login'));

  await waitFor(() => {
    expect(store.getState().auth.isAuthenticated).toBe(true);
  });
});
```

## Common Patterns

### Protected Route
```tsx
function ProtectedRoute({ children }) {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) return <Loading />;
  if (!isAuthenticated) return <Navigate to="/login" />;

  return children;
}
```

### Automatic Session Restore
```tsx
function App() {
  const { restoreSession, isAuthenticated, fetchCurrentUser } = useAuth();

  useEffect(() => {
    restoreSession();
    if (isAuthenticated) {
      fetchCurrentUser();
    }
  }, []);

  return <Routes>...</Routes>;
}
```

### Error Handling
```tsx
function LoginPage() {
  const { login, error, clearError } = useAuth();

  useEffect(() => {
    return () => clearError(); // Clear on unmount
  }, [clearError]);

  const handleLogin = async (credentials) => {
    const result = await login(credentials);

    if (result.meta.requestStatus === 'fulfilled') {
      navigate('/dashboard');
    }
    // Error automatically set in Redux state
  };

  return (
    <form onSubmit={handleLogin}>
      {error && <ErrorMessage message={error} onDismiss={clearError} />}
      {/* ... */}
    </form>
  );
}
```

## Benefits of This Architecture

1. **Scalable**: Easy to add new features (refresh tokens, MFA, etc.)
2. **Maintainable**: Clear separation of concerns
3. **Testable**: Each layer can be tested independently
4. **Type-safe**: Full TypeScript support
5. **Predictable**: Redux DevTools for debugging
6. **Reusable**: Hooks abstract Redux complexity
7. **Consistent**: Single pattern for all auth operations

## Migration Path

If you have existing components using direct service calls:

**Before**:
```tsx
const handleLogin = async () => {
  const response = await LoginService.login(credentials);
  SessionManager.setToken(response.access_token);
  setIsAuthenticated(true);
};
```

**After**:
```tsx
const { login } = useAuth();

const handleLogin = async () => {
  await login(credentials);
  // State automatically updated
};
```

## Future Enhancements

1. **Refresh Token Support**: Add refresh token logic to auth slice
2. **Role-Based Access**: Add user roles to state and permissions checking
3. **Multi-Factor Auth**: Add MFA flow to auth slice
4. **Session Persistence**: Optional localStorage for "remember me"
5. **Token Refresh**: Automatic token refresh before expiry
6. **Optimistic Updates**: Update UI before server confirms
