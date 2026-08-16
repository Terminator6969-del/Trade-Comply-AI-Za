"""
TradeComply API - Main FastAPI Application Entry Point
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.database import init_db, close_db

# Fully implemented routers
from app.routers import auth, organizations, shipments, documents, parties, classification

# Placeholder routers (Phase 4-5 — wired as proper modules)
from app.routers import compliance, duties, packets, tariffs


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI app.
    Handles startup and shutdown events.
    """
    # Startup
    await init_db()
    print("✅ Database initialized")
    
    yield
    
    # Shutdown
    await close_db()
    print("👋 Database connection closed")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered trade compliance automation for South Africa",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)


# ==================== Routes ====================

@app.get("/api/v1/health", tags=["health"])
async def health_check():
    """
    Health check endpoint.
    Returns 200 OK if API is running.
    """
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


# Register authentication router
app.include_router(auth.router)

# Register organization router
app.include_router(organizations.router)

# Register implemented domain routers
app.include_router(parties.router)
app.include_router(shipments.router)
app.include_router(documents.router)
app.include_router(classification.router)

# Register placeholder routers (Phase 4-5)
app.include_router(compliance.router)
app.include_router(duties.router)
app.include_router(packets.router)
app.include_router(tariffs.router)


# ==================== Error Handlers ====================

@app.exception_handler(ValueError)
async def value_error_handler(request, exc: ValueError):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """Handle general exceptions."""
    print(f"❌ Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


# ==================== OpenAPI ====================

@app.get("/", tags=["root"])
async def root():
    """API root endpoint."""
    return {
        "message": "TradeComply API - Trade Compliance Automation",
        "docs": "/docs",
        "openapi": "/openapi.json",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
