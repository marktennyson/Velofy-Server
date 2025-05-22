from pydantic import EmailStr, BaseModel
from typing import Optional, List, Any, TYPE_CHECKING
from datetime import datetime
from . import BaseRequestModel, BaseResponseModel

if TYPE_CHECKING:
    from .auth import UserResponseSchema

class MovieCreateSchema(BaseRequestModel):
    name: str
    duration: float  # in minutes or hours, based on usage
    rating: float  # should be between 0.0 and 10.0 (or based on your scale)
    casts: Optional[List[str]] = None
    category: str
    size: float  # in MB or GB
    added_date: datetime
    filename: str
    thumbnail: str
    description: str
    subtitles: Optional[str] = None
    location: Optional[str] = None
    # Add any other fields you need for creating a movie
class MovieReadSchema(BaseResponseModel):
    id: int
    name: str
    duration: float  # in minutes or hours, based on usage
    rating: float  # should be between 0.0 and 10.0 (or based on your scale)
    casts: Optional[List[str]] = None
    category: str
    size: float  # in MB or GB
    added_date: datetime
    filename: str
    thumbnail: str
    description: str
    subtitles: Optional[str] = None
    location: Optional[str] = None
    watch_history: Optional[List[Any]] = None  # This will be populated with related data
    # Add any other fields you need for reading a movie
class MovieUpdateSchema(BaseModel):
    name: Optional[str] = None
    duration: Optional[float] = None  # in minutes or hours, based on usage
    rating: Optional[float] = None  # should be between 0.0 and 10.0 (or based on your scale)
    casts: Optional[List[str]] = None
    category: Optional[str] = None
    size: Optional[float] = None  # in MB or GB
    added_date: Optional[datetime] = None
    filename: Optional[str] = None
    thumbnail: Optional[str] = None
    description: Optional[str] = None
    subtitles: Optional[str] = None
    location: Optional[str] = None
    # Add any other fields you need for updating a movie
class WatchHistorySchema(BaseModel):
    id: int
    user_id: int
    movie_id: int
    watched_at: datetime
    progress: float  # percentage (0.0 to 100.0)
    # Add any other fields you need for watch history
class WatchHistoryCreateSchema(BaseModel):
    user_id: int
    movie_id: int
    watched_at: datetime
    progress: float  # percentage (0.0 to 100.0)
    # Add any other fields you need for creating watch history
class WatchHistoryUpdateSchema(BaseModel):
    user_id: Optional[int] = None
    movie_id: Optional[int] = None
    watched_at: Optional[datetime] = None
    progress: Optional[float] = None  # percentage (0.0 to 100.0)
    # Add any other fields you need for updating watch history
class MovieFilterSchema(BaseModel):
    name: Optional[str] = None
    duration: Optional[float] = None  # in minutes or hours, based on usage
    rating: Optional[float] = None  # should be between 0.0 and 10.0 (or based on your scale)
    casts: Optional[List[str]] = None
    category: Optional[str] = None
    size: Optional[float] = None  # in MB or GB
    added_date: Optional[datetime] = None
    filename: Optional[str] = None
    thumbnail: Optional[str] = None
    description: Optional[str] = None
    subtitles: Optional[str] = None
    location: Optional[str] = None
    # Add any other fields you need for filtering movies
class MovieSortSchema(BaseModel):
    sort_by: Optional[str] = None  # e.g., "name", "rating", etc.
    sort_order: Optional[str] = "asc"  # "asc" or "desc"
    # Add any other fields you need for sorting movies
class MovieSearchSchema(BaseModel):
    query: str
    filter: Optional[MovieFilterSchema] = None
    sort: Optional[MovieSortSchema] = None
    # Add any other fields you need for searching movies
class MovieSearchResultSchema(BaseModel):
    movies: List[MovieReadSchema]
    total_count: int
    # Add any other fields you need for search results
class UserSearchSchema(BaseModel):
    query: str
    filter: Optional[UserResponseSchema] = None
    sort: Optional[MovieSortSchema] = None
    # Add any other fields you need for searching users
class UserSearchResultSchema(BaseModel):
    users: List[UserResponseSchema]
    total_count: int
    # Add any other fields you need for search results
class UserUpdateSchema(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None  # This will be hashed before storing in DB
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[datetime] = None