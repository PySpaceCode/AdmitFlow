from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
import logging
import os

from app.core.config import settings
from app.middleware.response_wrapper import ResponseWrapperMiddleware
# all_routes.py is kept on disk but no longer mounted (routes moved to individual routers below)
from app.db.session import engine, Base
import app.models  # Ensure all tables are registered

# -----------------------------
# Logging Setup
# -----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AdmitFlow Backend API - All endpoints are listed below",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.PROJECT_NAME}...")
    logger.info(f"DATABASE_URL is set: {'Yes' if settings.DATABASE_URL else 'No'}")
    logger.info(f"SECRET_KEY is set: {'Yes' if settings.SECRET_KEY else 'No'}")
    
    # Run table creation in a threadpool to avoid blocking the event loop
    import asyncio
    try:
        logger.info("Connecting to database and creating tables...")
        await asyncio.to_thread(Base.metadata.create_all, bind=engine)
        logger.info("Database tables checked/created successfully")
    except Exception as e:
        logger.error(f"Error during database initialization: {e}")
        # We don't raise here so the app can still bind to the port and respond to health checks

# -----------------------------
# Custom Middleware
# -----------------------------
app.add_middleware(ResponseWrapperMiddleware)

# -----------------------------
# CORS (added LAST = executes FIRST, so it always runs before
# ResponseWrapperMiddleware and handles OPTIONS preflight correctly)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",   # local dev
        "http://127.0.0.1:3000",
    ],
    # Allow ALL Vercel preview + production URLs permanently
    allow_origin_regex=r"https?://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# -----------------------------
# Exception Handlers
# -----------------------------
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    message = str(exc.detail)

    if isinstance(exc.detail, dict):
        message = exc.detail.get("message", str(exc.detail))

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": message,
            "data": None
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation Error: {exc}")
    
    # Extract readable error messages
    details = []
    for error in exc.errors():
        loc = ".".join(str(l) for l in error.get("loc", []))
        msg = error.get("msg", "Unknown error")
        details.append(f"{loc}: {msg}")
    
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation failed",
            "data": None,
            "details": details
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled Error: {exc}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Something went wrong",
            "data": None
        }
    )

# -----------------------------
# Static Files
# -----------------------------
os.makedirs("uploads/knowledge", exist_ok=True)
app.mount("/static", StaticFiles(directory="uploads"), name="static")

# -----------------------------
# Routers
# -----------------------------
from app.api.routers import auth, onboarding, leads, knowledge_base, dev

# -----------------------------
# Clean & Simple Route Prefixes
# (No /api prefix — easy to test on Render, easy to call from Vercel)
# -----------------------------
# Auth:         POST /register | POST /login | POST /logout
# Onboarding:   GET /onboarding/status | POST /onboarding/setup
# Leads:        GET /leads | POST /leads/upload | POST /leads/calling-config
# Knowledge:    GET /knowledge/documents | POST /knowledge/upload | POST /knowledge/persona | POST /knowledge/script
# Dev (seed):   POST /dev/seed
app.include_router(auth.router,           prefix="",             tags=["🔐 Auth"])
app.include_router(onboarding.router,     prefix="/onboarding",  tags=["🏫 Onboarding"])
app.include_router(leads.router,          prefix="/leads",       tags=["👥 Leads"])
app.include_router(knowledge_base.router, prefix="/knowledge",   tags=["📚 Knowledge Base"])
app.include_router(dev.router,            prefix="/dev",         tags=["🛠 Dev / Seeding"])

# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
def root():
    return {
        "message": "Admission AI API is running",
        "success": True
    }
