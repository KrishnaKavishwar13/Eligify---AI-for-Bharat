"""FastAPI application entry point"""

import logging
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.config.settings import settings
from src.handlers.auth_handler import router as auth_router
from src.handlers.profile_handler import router as profile_router
from src.handlers.skills_handler import router as skills_router
from src.handlers.internships_handler import router as internships_router
from src.handlers.projects_handler import router as projects_router
from src.handlers.intelligence_handler import router as intelligence_router
from src.handlers.chat_handler import router as chat_router
from src.utils.errors import AppError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import mangum only if available (for AWS Lambda deployment)
try:
    from mangum import Mangum
    MANGUM_AVAILABLE = True
except ImportError:
    MANGUM_AVAILABLE = False

# Create FastAPI app
app = FastAPI(
    title="Eligify API",
    description="AI-powered Employability Operating System",
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler for AppError
@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    """Handle custom application errors"""
    logger.error(
        f"AppError: {exc.code.value} - {exc.message}",
        extra={
            "path": request.url.path,
            "method": request.method,
            "status_code": exc.status_code,
            "details": exc.details
        }
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict()
    )


# Global exception handler for unhandled exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions"""
    logger.error(
        f"Unhandled exception: {type(exc).__name__} - {str(exc)}",
        exc_info=True,
        extra={
            "path": request.url.path,
            "method": request.method
        }
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred. Please try again later.",
                "details": {}
            }
        }
    )


# Include routers
app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(skills_router)
app.include_router(internships_router)
app.include_router(projects_router)
app.include_router(intelligence_router)
app.include_router(chat_router)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Eligify API is running",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy"}


# AWS Lambda handler (only if mangum is available)
if MANGUM_AVAILABLE:
    handler = Mangum(app, lifespan="off")
