from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core import security
from app.db.session import SessionLocal
from app.models.user import User
from app.models.institute import Institute
from app.schemas.auth import TokenPayload

# Allow both OAuth2 form and manual header for Flexibility
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    auto_error=False
)

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user_payload(
    token: str = Depends(reusable_oauth2)
) -> TokenPayload:
    if not token:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Authorization token missing",
                "code": "TOKEN_MISSING"
            }
        )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Invalid or expired token",
                "code": "TOKEN_INVALID"
            }
        )
    return token_data

def get_current_user(
    db: Session = Depends(get_db), 
    payload: TokenPayload = Depends(get_current_user_payload)
) -> User:
    user = db.query(User).filter(User.id == int(payload.sub)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_institute_id(
    payload: TokenPayload = Depends(get_current_user_payload)
) -> int:
    if not payload.institute_id:
        raise HTTPException(status_code=400, detail="Token missing institute context")
    return payload.institute_id

def check_role(roles: list[str]):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted for your role"
            )
        return current_user
    return role_checker
