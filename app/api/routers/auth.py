from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.core import security
from app.models.user import User
from app.models.institute import Institute
from app.models.bookings_settings import Settings
from app.schemas.auth import LoginRequest, RegisterRequest

router = APIRouter()

@router.post("/login", summary="Login with email & password")
def login(
    db: Session = Depends(deps.get_db), 
    login_data: LoginRequest = None
) -> Any:
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
    if not security.verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid credentials"
        )
    
    access_token = security.create_access_token(user.id, user.institute_id)
    refresh_token = security.create_refresh_token(user.id, user.institute_id)
    
    return {
        "success": True,
        "message": "Login successful",
        "data": {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user.id,
                "role": user.role
            }
        }
    }

@router.post("/register", status_code=status.HTTP_201_CREATED, summary="Register a new user")
def register(
    db: Session = Depends(deps.get_db),
    reg_data: RegisterRequest = None
) -> Any:
    # Check if user already exists
    if db.query(User).filter(User.email == reg_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Email already registered"
        )
    
    # Create Institute
    new_institute = Institute(
        name=reg_data.instituteName or f"{reg_data.fullName}'s Institute",
        email=reg_data.email,
        onboarding_status=False
    )
    db.add(new_institute)
    db.flush()
    
    # Create User
    new_user = User(
        institute_id=new_institute.id,
        full_name=reg_data.fullName,
        email=reg_data.email,
        password_hash=security.get_password_hash(reg_data.password),
        role="admin"
    )
    db.add(new_user)
    
    # Create default settings with JSONB config
    new_settings = Settings(
        institute_id=new_institute.id,
        config={
            "whatsappEnabled": True,
            "callEnabled": True
        }
    )
    db.add(new_settings)
    
    db.commit()
    db.refresh(new_user)
    
    return {
        "success": True,
        "message": "User have been created",
        "data": {
            "userId": new_user.id,
            "email": new_user.email
        }
    }

@router.post("/logout", summary="Logout current user")
def logout(
    current_user: User = Depends(deps.get_current_user)
) -> Any:
    return {
        "success": True,
        "message": "Logout successful",
        "data": {}
    }
