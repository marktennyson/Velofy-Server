from pydantic import EmailStr
from typing import Optional, List, Any
from datetime import datetime
from . import BaseRequestModel, BaseResponseModel

# ======================= SCHEMAS =======================
class UserRequestSchema(BaseRequestModel):
    username: str
    password: str  # This will be hashed before storing in DB
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[datetime] = None


class UserResponseSchema(BaseResponseModel):
    id: int
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    created_at: datetime
    watch_history: Optional[List[Any]] = None  # This will be populated with related data
    
class TokenSchema(BaseResponseModel):
    access_token: str
    token_type: str

class UserLoginInputSchema(BaseRequestModel):
    username: str
    password: str

class UserLoginOutputSchema(TokenSchema, UserResponseSchema):
    """
    User login output schema that includes user details and token information.
    """
    
