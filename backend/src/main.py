"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import auth, books, clubs, meetings, pages, users
from src.config import settings

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    description="FastAPI backend for The Public Square book club application",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(clubs.router)
app.include_router(meetings.router)
app.include_router(pages.router)
app.include_router(books.router)
app.include_router(users.router)


@app.get("/")
async def root() -> dict[str, str]:
    """
    Root endpoint.

    Returns:
        dict: Welcome message.
    """
    return {
        "message": "Welcome to The Public Square API",
        "version": "0.1.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check() -> dict[str, str]:
    """
    Health check endpoint.

    Returns:
        dict: Health status.
    """
    return {"status": "healthy"}
