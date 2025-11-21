When writing TypeScript code in this project:

- Always use strict mode
- Prefer interfaces over types for object shapes
- Use explicit return types for functions
- Follow our error handling pattern: Invoke global error handling component to inform the user of an error in the application.
- Never use `any` - use `unknown` instead
- All api connections will be under global/api/actions/{domain}/{function}/api-{function}.service.ts. These endpoints should follow the single responsibility principle such that only one endpoint is accessed from a single typescript file.
    - For example, global/api/actions/auth/login/api-login.service.ts
- All endpoints should have API models, such as APIGetUserRequest, which will return an APIGetUserResponse. We will then need a function tranformAPIUserToUser() function that will transform the returned backend User to the frontend User model.