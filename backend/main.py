import time
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import httpx
original_httpx_init = httpx.Client.__init__
def patched_httpx_init(self, *args, **kwargs):
    kwargs['verify'] = False
    original_httpx_init(self, *args, **kwargs)
httpx.Client.__init__ = patched_httpx_init

original_httpx_async_init = httpx.AsyncClient.__init__
def patched_httpx_async_init(self, *args, **kwargs):
    kwargs['verify'] = False
    original_httpx_async_init(self, *args, **kwargs)
httpx.AsyncClient.__init__ = patched_httpx_async_init

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.api.router import api_router
from app.core.config import settings
from app.core.logging import logger

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Modern SaaS API for AI Resume Intelligence",
    version="2.0.0",
    openapi_tags=[
        {"name": "Analysis", "description": "Endpoints for CV and Job analysis"},
        {"name": "Interview", "description": "Endpoints for AI interview generation and evaluation"},
        {"name": "History", "description": "Endpoints to manage user analysis history"},
        {"name": "Export", "description": "Endpoints to export analysis reports"},
        {"name": "System", "description": "System health and version endpoints"}
    ]
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to actual frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handling Middleware
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Exception on {request.url}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "error": str(exc)}
    )

# Timing & Request Logging Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Incoming request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        logger.info(f"Request {request.method} {request.url} completed in {process_time:.4f} secs with status {response.status_code}")
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Request {request.method} {request.url} failed in {process_time:.4f} secs")
        raise e

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health", tags=["System"])
@limiter.limit("10/minute")
def health_check(request: Request):
    """
    Returns the health status of the API and its downstream dependencies.
    """
    status = {
        "status": "ok",
        "database": "unknown",
        "gemini": "unknown"
    }
    try:
        from app.core.database import get_db
        db = get_db()
        # Test supabase connection
        db.table("profiles").select("count", count="exact").limit(1).execute()
        status["database"] = "ok"
    except Exception as e:
        status["database"] = f"error: {str(e)}"
        status["status"] = "degraded"
        
    try:
        from app.agents.base import get_client
        client = get_client()
        # Minimal gemini API check - if client initializes, we assume ok for now
        # An actual generate_content call might cost tokens so we just check object existence
        if client:
            status["gemini"] = "ok"
    except Exception as e:
        status["gemini"] = f"error: {str(e)}"
        status["status"] = "degraded"

    return status

@app.get("/version", tags=["System"])
def get_version():
    """
    Returns the current API version and environment.
    """
    return {
        "version": "2.0.0",
        "environment": "development"
    }
