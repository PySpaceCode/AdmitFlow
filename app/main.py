from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
import logging
import os

from app.core.config import settings
from app.middleware.response_wrapper import ResponseWrapperMiddleware
from app.api.all_routes import router as all_router
from app.db.session import engine, Base
import app.models  # Ensure all tables are registered

# -----------------------------
# Logging Setup
# -----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------
# Create Tables (OK for now)
# -----------------------------
Base.metadata.create_all(bind=engine)

# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# -----------------------------
# CORS (VERY IMPORTANT)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # local frontend
        "http://127.0.0.1:3000",
        "https://admiflow-frontend-rv2z.vercel.app",  # deployed frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Custom Middleware
# -----------------------------
app.add_middleware(ResponseWrapperMiddleware)

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

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Invalid input data",
            "data": None
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

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(onboarding.router, prefix=f"{settings.API_V1_STR}/onboarding", tags=["onboarding"])
app.include_router(leads.router, prefix=f"{settings.API_V1_STR}/leads", tags=["leads"])
app.include_router(knowledge_base.router, prefix=f"{settings.API_V1_STR}/knowledge_base", tags=["knowledge_base"])
app.include_router(dev.router, prefix=f"{settings.API_V1_STR}/dev", tags=["dev"])

app.include_router(all_router, prefix=f"{settings.API_V1_STR}", tags=["all_routes"])

# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
def root():
    return {
        "message": "Admission AI API is running",
        "success": True
    }
