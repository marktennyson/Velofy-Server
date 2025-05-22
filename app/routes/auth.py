from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from typing import Optional, Dict, Any

from sqlmodel import select
from database import SessionDep
from models import User
from schemas.auth import (
    UserRequestSchema, UserResponseSchema, 
    UserLoginInputSchema, UserLoginOutputSchema
)
from app_config import (
    SECRET_KEY, ALGORITHM, 
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from exceptions import (
    InvalidCredentialsException,
    TokenMissingException, InvalidTokenException,
    TokenExpiredException, UserAlreadyExistsException,
)

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ======================= UTILITY FUNCTIONS =======================

def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user_by_username(username: str, db: SessionDep) -> Optional[User]:
    return db.exec(select(User).where(User.username == username)).first()

def authenticate_user(username: str, password: str, db: SessionDep) -> Optional[User]:
    user = get_user_by_username(username, db)
    if user and verify_password(password, user.password_hash):
        return user
    return None

# ======================= ROUTES =======================

@router.post("/login", response_model=UserLoginOutputSchema)
def login(user: UserLoginInputSchema, db: SessionDep) -> UserLoginOutputSchema:
    authenticated_user: "Optional[User]" = authenticate_user(user.username, user.password, db)
    if not authenticated_user:
        raise InvalidCredentialsException
    access_token = create_access_token(
        data={"username": authenticated_user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return UserLoginOutputSchema(
        **authenticated_user.model_dump(),
        access_token=access_token, token_type="bearer",
    )

@router.post("/register", response_model=UserResponseSchema)
def register(user: UserRequestSchema, db: SessionDep) -> UserResponseSchema:
    existing_user = get_user_by_username(user.username, db)
    if existing_user:
        raise UserAlreadyExistsException(user.username)
    
    db_user = User(
        username=user.username,
        password_hash=get_password_hash(user.password),
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        address=user.address,
        phone=user.phone,
        date_of_birth=user.date_of_birth,
        created_at=datetime.now(timezone.utc)
    )
    db.add_user(db_user)
    return UserResponseSchema.model_validate(db_user)

# ======================= AUTH DEPENDENCY =======================

def get_current_user(db: SessionDep, token: str = Depends(oauth2_scheme)) -> UserResponseSchema:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("username")
        if not username:
            raise TokenMissingException
    except JWTError:
        raise InvalidTokenException
    exp = payload.get("exp")
    if exp is None or not isinstance(exp, (int, float)):
        raise InvalidTokenException
    if datetime.now(timezone.utc) > datetime.fromtimestamp(exp, tz=timezone.utc):
        raise TokenExpiredException

    user = get_user_by_username(username, db)
    if not user:
        raise InvalidCredentialsException
    return UserResponseSchema.model_validate(user)

@router.get("/me", response_model=UserResponseSchema)
def read_users_me(current_user: UserResponseSchema = Depends(get_current_user)) -> UserResponseSchema:
    return current_user


@router.put("/me", response_model=UserResponseSchema)
def update_user(
    db: SessionDep,
    user: UserRequestSchema, 
    current_user: UserResponseSchema = Depends(get_current_user), 
) -> UserResponseSchema:
    """Update user details."""
    db_user = db.get(User, current_user.id)
    if not db_user:
        raise InvalidCredentialsException
    db_user.username = user.username
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.email = user.email
    db_user.phone = user.phone
    db_user.address = user.address
    db_user.date_of_birth = user.date_of_birth
    db.commit()
    return UserResponseSchema.model_validate(db_user)


@router.delete("/me", response_model=UserResponseSchema)
def delete_user(
    db: SessionDep,
    current_user: UserResponseSchema = Depends(get_current_user), 
) -> UserResponseSchema:
    db_user = db.get(User, current_user.id)
    if not db_user:
        raise InvalidCredentialsException
    db.delete(db_user)
    db.commit()
    return UserResponseSchema.model_validate(db_user)