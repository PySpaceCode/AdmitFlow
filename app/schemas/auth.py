from typing import Optional
from .base import BaseSchema

class Token(BaseSchema):
    access_token: str
    user: Optional["UserInnerResponse"] = None

class UserInnerResponse(BaseSchema):
    id: int
    role: str

class TokenPayload(BaseSchema):
    sub: Optional[str] = None
    institute_id: Optional[int] = None
    exp: Optional[int] = None
    
    model_config = {"extra": "allow"}

class LoginRequest(BaseSchema):
    email: str
    password: str

class RegisterRequest(BaseSchema):
    fullName: str
    email: str
    password: str
    instituteName: Optional[str] = None

class UserResponse(BaseSchema):
    id: int
    full_name: str
    email: str
    role: str
    institute_id: int
