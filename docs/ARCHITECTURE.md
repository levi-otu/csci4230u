# Architecture Documentation

## System Architecture Overview

The Public Square follows a **three-tier monolithic architecture** with clear separation of concerns between the presentation layer (frontend), application logic layer (backend), and data layer (database). The system is containerized using Docker and deployed on Google Cloud Platform.

## High-Level Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        Browser[Web Browser]
    end

    subgraph "Google Cloud Platform"
        subgraph "Cloud Run - Frontend"
            Frontend[React + TypeScript<br/>Vite + Tailwind CSS]
        end

        subgraph "Cloud Run - Backend"
            API[FastAPI Backend]

            subgraph "API Layer"
                AuthAPI[Auth Routes]
                ClubsAPI[Clubs Routes]
                LibraryAPI[Library Routes]
                BooksAPI[Books Routes]
                UsersAPI[Users Routes]
                PagesAPI[Pages Routes]
                MeetingsAPI[Meetings Routes]
            end

            subgraph "Business Logic Layer"
                AuthHandler[Auth Handler]
                ClubsHandler[Clubs Handler]
                LibraryHandler[Library Handler]
                BooksHandler[Books Handler]
                UsersHandler[Users Handler]
            end

            subgraph "Data Access Layer"
                UserStorage[User Storage]
                ClubStorage[Club Storage]
                BookStorage[Book Storage]
                LibraryStorage[Library Storage]
                TokenStorage[Token Storage]
            end
        end

        subgraph "Cloud SQL"
            PostgreSQL[(PostgreSQL<br/>Database)]
        end

        subgraph "Supporting Services"
            ArtifactRegistry[Artifact Registry<br/>Docker Images]
            CloudLogging[Cloud Logging]
            CloudMonitoring[Cloud Monitoring]
        end
    end

    subgraph "External Services"
        OpenLibrary[Open Library API<br/>ISBN Lookup]
    end

    subgraph "CI/CD Pipeline"
        GitHub[GitHub Repository]
        GitHubActions[GitHub Actions]
        CodeQL[CodeQL SAST]
        Pytest[Pytest]
    end

    Browser --> Frontend
    Frontend --> API
    AuthAPI --> AuthHandler
    ClubsAPI --> ClubsHandler
    LibraryAPI --> LibraryHandler
    BooksAPI --> BooksHandler
    UsersAPI --> UsersHandler

    AuthHandler --> UserStorage
    AuthHandler --> TokenStorage
    ClubsHandler --> ClubStorage
    LibraryHandler --> BookStorage
    LibraryHandler --> LibraryStorage
    BooksHandler --> BookStorage
    UsersHandler --> UserStorage

    UserStorage --> PostgreSQL
    ClubStorage --> PostgreSQL
    BookStorage --> PostgreSQL
    LibraryStorage --> PostgreSQL
    TokenStorage --> PostgreSQL

    LibraryHandler -.ISBN Lookup.-> OpenLibrary

    API --> CloudLogging
    API --> CloudMonitoring

    GitHub --> GitHubActions
    GitHubActions --> CodeQL
    GitHubActions --> Pytest
    GitHubActions --> ArtifactRegistry
    ArtifactRegistry --> Frontend
    ArtifactRegistry --> API
```

## Package Structure Diagram

```mermaid
graph TB
    subgraph "Frontend Application"
        FrontendRoot[app/]

        subgraph "Global Resources"
            GlobalAPI[global/api/]
            GlobalComponents[global/components/]
            GlobalModels[global/models/]
            GlobalStore[global/store/]
            GlobalHooks[global/hooks/]
            GlobalUtils[global/utils/]
        end

        subgraph "Feature Modules"
            AuthModule[modules/login/]
            ClubsModule[modules/clubs/]
            LibraryModule[modules/library/]
            HomeModule[modules/home/]
            PagesModule[modules/pages/]
        end

        FrontendRoot --> GlobalAPI
        FrontendRoot --> GlobalComponents
        FrontendRoot --> GlobalModels
        FrontendRoot --> GlobalStore
        FrontendRoot --> GlobalHooks
        FrontendRoot --> GlobalUtils

        FrontendRoot --> AuthModule
        FrontendRoot --> ClubsModule
        FrontendRoot --> LibraryModule
        FrontendRoot --> HomeModule
        FrontendRoot --> PagesModule
    end

    subgraph "Backend Application"
        BackendRoot[src/]

        subgraph "API Layer"
            APIRoutes[api/]
            APIDeps[api/deps.py]
        end

        subgraph "Business Logic"
            Handlers[handlers/]
        end

        subgraph "Data Access"
            Storage[storage/data/sql/]
        end

        subgraph "Core"
            Models[models/]
            Database[database.py]
            Security[security.py]
            Config[config.py]
        end

        BackendRoot --> APIRoutes
        BackendRoot --> APIDeps
        BackendRoot --> Handlers
        BackendRoot --> Storage
        BackendRoot --> Models
        BackendRoot --> Database
        BackendRoot --> Security
        BackendRoot --> Config

        APIRoutes --> Handlers
        Handlers --> Storage
        Storage --> Models
        Storage --> Database
        APIRoutes --> Security
    end

    subgraph "Database Layer"
        Alembic[alembic/]
        Migrations[migrations/versions/]

        Alembic --> Migrations
    end

    GlobalAPI -.HTTP Requests.-> APIRoutes
    BackendRoot -.Manages.-> Alembic
```

## Data Model Class Diagram

```mermaid
classDiagram
    class UserORM {
        +UUID id
        +String username
        +String email
        +String full_name
        +Boolean is_active
        +DateTime created_at
        +DateTime updated_at
    }

    class UserSecurityORM {
        +UUID user_id
        +String email
        +String password
        +String old_password
        +DateTime password_changed_at
        +DateTime created_at
        +DateTime updated_at
    }

    class RefreshTokenModel {
        +UUID id
        +UUID user_id
        +String token_hash
        +DateTime expires_at
        +DateTime created_at
        +Boolean revoked
        +UUID replaced_by_token_id
        +String device_info
        +String ip_address
        +is_expired() bool
        +is_valid() bool
    }

    class ClubORM {
        +UUID id
        +String name
        +String description
        +String topic
        +UUID created_by
        +Boolean is_active
        +Integer max_members
        +DateTime created_at
        +DateTime updated_at
    }

    class ClubMeetingORM {
        +UUID id
        +UUID club_id
        +UUID meeting_id
        +DateTime start_date
        +DateTime end_date
        +String frequency
        +String recurrence_rule
        +DateTime created_at
        +DateTime updated_at
    }

    class MeetingORM {
        +UUID id
        +String name
        +String description
        +String status
        +DateTime scheduled_start
        +DateTime scheduled_end
        +DateTime actual_start
        +DateTime actual_end
        +Integer duration
        +UUID created_by
        +UUID club_id
        +DateTime created_at
        +DateTime updated_at
    }

    class BookORM {
        +UUID id
        +String title
        +String author
        +Date date_of_first_publish
        +String genre
        +String description
        +String cover_image_url
        +String series_title
        +Integer volume_number
        +String volume_title
        +DateTime created_at
        +DateTime updated_at
    }

    class BookVersionORM {
        +UUID id
        +UUID book_id
        +UUID publisher_id
        +String isbn
        +Date publish_date
        +String edition
        +String editors
        +String editor_info
        +DateTime created_at
        +DateTime updated_at
    }

    class PublisherORM {
        +UUID id
        +String name
        +String country
        +String website
        +DateTime created_at
        +DateTime updated_at
    }

    class UserBookORM {
        +UUID id
        +UUID user_id
        +UUID book_id
        +UUID book_version_id
        +DateTime added_date
        +Boolean is_read
        +DateTime read_date
        +String reading_status
        +Float rating
        +String review
        +String notes
        +Boolean is_favorite
        +DateTime created_at
        +DateTime updated_at
    }

    class ReadingListORM {
        +UUID id
        +UUID user_id
        +String name
        +String description
        +DateTime created_date
        +Boolean is_default
        +DateTime created_at
        +DateTime updated_at
    }

    class ReadingListItemORM {
        +UUID id
        +UUID reading_list_id
        +UUID user_book_id
        +Integer order_index
        +DateTime added_date
        +DateTime created_at
        +DateTime updated_at
    }

    class PageORM {
        +UUID id
        +String name
        +String description
        +String topic
        +UUID created_by
        +Boolean is_active
        +DateTime created_at
        +DateTime updated_at
    }

    class Role {
        +UUID id
        +String name
        +String description
        +DateTime created_at
        +DateTime updated_at
    }

    class Group {
        +UUID id
        +String name
        +String description
        +UUID created_by
        +DateTime created_at
        +DateTime updated_at
    }

    %% Relationships
    UserORM "1" -- "1" UserSecurityORM : has
    UserORM "1" -- "*" RefreshTokenModel : has
    UserORM "1" -- "*" ClubORM : creates
    UserORM "*" -- "*" ClubORM : member of
    UserORM "1" -- "*" MeetingORM : creates
    UserORM "*" -- "*" PageORM : follows
    UserORM "1" -- "*" PageORM : creates
    UserORM "*" -- "*" Role : has
    UserORM "*" -- "*" Group : member of

    ClubORM "1" -- "*" ClubMeetingORM : schedules
    MeetingORM "1" -- "*" ClubMeetingORM : scheduled in

    BookORM "1" -- "*" BookVersionORM : has versions
    PublisherORM "1" -- "*" BookVersionORM : publishes

    UserORM "1" -- "*" UserBookORM : owns
    BookORM "1" -- "*" UserBookORM : tracked by
    BookVersionORM "1" -- "*" UserBookORM : specific edition

    UserORM "1" -- "*" ReadingListORM : creates
    ReadingListORM "1" -- "*" ReadingListItemORM : contains
    UserBookORM "1" -- "*" ReadingListItemORM : included in
```

## Backend Layer Architecture

```mermaid
graph LR
    subgraph "API Layer (FastAPI Routers)"
        A1[auth.py]
        A2[clubs.py]
        A3[library.py]
        A4[books.py]
        A5[users.py]
        A6[pages.py]
        A7[meetings.py]
    end

    subgraph "Business Logic Layer (Handlers)"
        B1[AuthHandler]
        B2[ClubHandler]
        B3[LibraryHandler]
        B4[BookHandler]
        B5[UserHandler]
    end

    subgraph "Data Access Layer (Storage/Repositories)"
        C1[UserStorage]
        C2[ClubStorage]
        C3[BookStorage]
        C4[UserBookStorage]
        C5[ReadingListStorage]
        C6[RefreshTokenStorage]
    end

    subgraph "Data Layer"
        D1[(PostgreSQL)]
    end

    A1 --> B1
    A2 --> B2
    A3 --> B3
    A4 --> B4
    A5 --> B5

    B1 --> C1
    B1 --> C6
    B2 --> C2
    B3 --> C3
    B3 --> C4
    B3 --> C5
    B4 --> C3
    B5 --> C1

    C1 --> D1
    C2 --> D1
    C3 --> D1
    C4 --> D1
    C5 --> D1
    C6 --> D1
```

## Request Flow Diagram

```mermaid
sequenceDiagram
    actor User
    participant Frontend
    participant API as FastAPI Router
    participant Handler as Business Logic
    participant Storage as Data Access
    participant DB as PostgreSQL
    participant ExtAPI as External API

    User->>Frontend: Interact with UI
    Frontend->>API: HTTP Request (JSON)

    API->>API: Validate JWT Token
    API->>API: Validate Request Schema

    API->>Handler: Call handler method
    Handler->>Handler: Business logic validation

    alt External API needed
        Handler->>ExtAPI: ISBN Lookup Request
        ExtAPI-->>Handler: Book Metadata
    end

    Handler->>Storage: Data operation
    Storage->>DB: SQL Query (via SQLAlchemy)
    DB-->>Storage: Query Results
    Storage-->>Handler: Domain Models

    Handler->>Handler: Transform data
    Handler-->>API: Response Model

    API-->>Frontend: HTTP Response (JSON)
    Frontend-->>User: Update UI
```

## Authentication Flow

```mermaid
sequenceDiagram
    actor User
    participant Frontend
    participant AuthAPI
    participant AuthHandler
    participant UserStorage
    participant TokenStorage
    participant DB

    User->>Frontend: Login (username, password)
    Frontend->>AuthAPI: POST /api/auth/login

    AuthAPI->>AuthHandler: login(credentials)
    AuthHandler->>UserStorage: get_user_by_username()
    UserStorage->>DB: SELECT user
    DB-->>UserStorage: User record
    UserStorage-->>AuthHandler: UserORM

    AuthHandler->>UserStorage: get_user_security()
    UserStorage->>DB: SELECT user_security
    DB-->>UserStorage: Security record
    UserStorage-->>AuthHandler: UserSecurityORM

    AuthHandler->>AuthHandler: Verify password (bcrypt)

    AuthHandler->>AuthHandler: Generate access token (JWT)
    AuthHandler->>AuthHandler: Generate refresh token

    AuthHandler->>TokenStorage: create_refresh_token()
    TokenStorage->>DB: INSERT refresh_token
    DB-->>TokenStorage: Token saved

    AuthHandler-->>AuthAPI: TokenResponse
    AuthAPI->>AuthAPI: Set HTTP-only cookie
    AuthAPI-->>Frontend: Access token + Cookie

    Frontend->>Frontend: Store access token
    Frontend-->>User: Redirect to dashboard
```

## Deployment Architecture

```mermaid
graph TB
    subgraph "Development"
        Dev[Developer]
        Git[Git Repository]
    end

    subgraph "CI/CD Pipeline - GitHub Actions"
        Trigger[Push to main]
        Tests[Run Tests<br/>Pytest]
        SAST[Security Scan<br/>CodeQL]
        Lint[Code Quality<br/>Flake8]
        BuildBE[Build Backend<br/>Docker Image]
        BuildFE[Build Frontend<br/>Docker Image]
    end

    subgraph "Google Cloud - Artifact Registry"
        Registry[Docker Images]
    end

    subgraph "Google Cloud - Cloud Run"
        BackendService[Backend Service<br/>FastAPI Container]
        FrontendService[Frontend Service<br/>Nginx + React]
        Migration[Migration Job<br/>Alembic]
    end

    subgraph "Google Cloud - Cloud SQL"
        Database[(PostgreSQL)]
    end

    subgraph "Google Cloud - Monitoring"
        Logging[Cloud Logging]
        Monitoring[Cloud Monitoring]
    end

    Dev --> Git
    Git --> Trigger
    Trigger --> Tests
    Tests --> SAST
    SAST --> Lint
    Lint --> BuildBE
    Lint --> BuildFE

    BuildBE --> Registry
    BuildFE --> Registry

    Registry --> BackendService
    Registry --> FrontendService
    Registry --> Migration

    Migration --> Database
    BackendService --> Database

    BackendService --> Logging
    BackendService --> Monitoring
    FrontendService --> Logging
```

## Key Architectural Decisions

### 1. Monolithic Architecture
**Decision**: Use a monolithic backend with FastAPI rather than microservices.

**Rationale**:
- Simpler deployment and development for a university project
- Reduced operational complexity
- Faster development cycle
- Sufficient for expected user load
- Can be refactored to microservices later if needed

### 2. Three-Layer Architecture
**Decision**: Strict separation into API, Business Logic, and Data Access layers.

**Rationale**:
- Clear separation of concerns
- Easier testing and mocking
- Independent layer modification
- Business logic reusability
- Database technology independence

### 3. Repository Pattern
**Decision**: Implement repository pattern for data access.

**Rationale**:
- Abstraction over database operations
- Easier unit testing with mocks
- Centralized query logic
- Database migration flexibility

### 4. JWT with Refresh Tokens
**Decision**: Use short-lived JWT access tokens with long-lived HTTP-only refresh tokens.

**Rationale**:
- Enhanced security with token rotation
- XSS attack mitigation (HTTP-only cookies)
- Session management across devices
- Token revocation capability

### 5. Frontend State Management
**Decision**: Use Redux Toolkit for global state management.

**Rationale**:
- Centralized application state
- Predictable state updates
- DevTools support for debugging
- Integration with React best practices

### 6. Containerization
**Decision**: Deploy using Docker containers on Google Cloud Run.

**Rationale**:
- Environment consistency
- Easy scaling
- Platform independence
- CI/CD integration
- Serverless cost model

### 7. Automated Migrations
**Decision**: Use Alembic for database schema migrations.

**Rationale**:
- Version-controlled schema changes
- Rollback capability
- Team collaboration support
- Automated deployment integration

## Technology Stack Justification

### Frontend
- **React + TypeScript**: Type safety, component reusability, large ecosystem
- **Vite**: Fast build times, modern tooling, HMR support
- **Redux Toolkit**: Simplified Redux setup, built-in best practices
- **Tailwind CSS**: Utility-first styling, rapid development, consistency
- **Shadcn/Radix**: Accessible components, full customization

### Backend
- **FastAPI**: Async support, automatic API docs, Pydantic validation
- **SQLAlchemy**: Powerful ORM, migration support, async capabilities
- **PostgreSQL**: ACID compliance, JSON support, reliability
- **Pydantic**: Data validation, settings management, type safety
- **Alembic**: Database migration management

### DevOps
- **Docker**: Containerization, reproducible environments
- **GitHub Actions**: CI/CD automation, integrated with repository
- **Google Cloud Run**: Serverless containers, auto-scaling, cost-effective
- **Pytest**: Comprehensive testing framework, fixtures, async support

## Security Architecture

### Authentication & Authorization
1. **Password Security**: bcrypt hashing with salt
2. **Token Management**: JWT access tokens (15 min) + refresh tokens (7 days)
3. **Session Tracking**: Device and IP logging
4. **Token Rotation**: Refresh token rotation on renewal
5. **CORS**: Configured cross-origin resource sharing
6. **Dependency Injection**: Secure route protection with FastAPI dependencies

### Data Protection
1. **HTTP-Only Cookies**: Prevent XSS attacks on refresh tokens
2. **Environment Variables**: Sensitive config in .env files
3. **SQL Injection Prevention**: SQLAlchemy parameterized queries
4. **Input Validation**: Pydantic schema validation

## Performance Considerations

1. **Async Operations**: FastAPI async/await for I/O operations
2. **Database Indexing**: Indexed columns for frequent queries
3. **Connection Pooling**: SQLAlchemy connection management
4. **Caching**: Frontend state caching with Redux
5. **Lazy Loading**: Component and route code splitting
6. **CDN**: Static asset delivery via Cloud Run

## Scalability Strategy

1. **Horizontal Scaling**: Cloud Run automatic instance scaling
2. **Database Scaling**: Cloud SQL read replicas (future)
3. **Stateless Backend**: JWT-based authentication enables scaling
4. **Containerization**: Easy deployment of multiple instances
5. **Load Balancing**: Cloud Run built-in load balancing
