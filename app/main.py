from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.core.config import settings
from app.middleware.response_wrapper import ResponseWrapperMiddleware
from app.api.routers import auth, onboarding, knowledge_base, leads, communication, bookings, settings as settings_router, dev
from app.db.session import engine, Base

# Create tables on startup (In production use Almebic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

from fastapi.exceptions import RequestValidationError

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
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Something went wrong",
            "data": None
        }
    )

# Always add CORS middleware to allow requests from the Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom response wrapper middleware
app.add_middleware(ResponseWrapperMiddleware)

# Create and mount static uploads directory
os.makedirs("uploads/knowledge", exist_ok=True)
app.mount("/static", StaticFiles(directory="uploads"), name="static")

# Include Routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(onboarding.router, prefix=f"{settings.API_V1_STR}/onboarding", tags=["onboarding"])
app.include_router(knowledge_base.router, prefix=f"{settings.API_V1_STR}/knowledge-base", tags=["knowledge-base"])
app.include_router(leads.router, prefix=f"{settings.API_V1_STR}/leads", tags=["leads"])
app.include_router(communication.router, prefix=f"{settings.API_V1_STR}/communication", tags=["communication"])
app.include_router(bookings.router, prefix=f"{settings.API_V1_STR}/bookings", tags=["bookings"])
app.include_router(settings_router.router, prefix=f"{settings.API_V1_STR}/settings", tags=["settings"])
app.include_router(dev.router, prefix=f"{settings.API_V1_STR}/dev", tags=["dev"])

@app.get("/")
def root():
    return {"message": "Admission AI API is running", "success": True}
