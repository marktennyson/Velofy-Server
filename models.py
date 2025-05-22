from typing import Optional, List
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship

class Cast(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    role: str  # e.g., Actor, Director
    image_url: Optional[str] = None
    movies: List["MovieCastLink"] = Relationship(back_populates="cast")

class MovieCastLink(SQLModel, table=True):
    movie_id: Optional[int] = Field(default=None, foreign_key="movie.id", primary_key=True)
    cast_id: Optional[int] = Field(default=None, foreign_key="cast.id", primary_key=True)
    order: Optional[int] = Field(default=0)  # To maintain appearance order if needed

    movie: Optional["Movie"] = Relationship(back_populates="cast_links")
    cast: Optional["Cast"] = Relationship(back_populates="movies")

class Movie(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    imdb_id: str = Field(index=True, unique=True)
    name: str = Field(index=True)
    duration: float  # in minutes
    rating: float  # should be between 0.0 and 10.0 (or based on your scale)
    category: str = Field(index=True)
    size: float  # in MB
    published_year: int
    filename: str
    thumbnail: str
    plot: str
    synopsis: str
    subtitles: str
    location: str
    watch_history: list["WatchHistory"] = Relationship(back_populates="movie")
    cast_links: List["MovieCastLink"] = Relationship(back_populates="movie")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password_hash: str = Field(repr=False)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    watch_history: list["WatchHistory"] = Relationship(back_populates="user")


class WatchHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    movie_id: int = Field(foreign_key="movie.id")
    watched_at: datetime
    progress: float  # percentage (0.0 to 100.0)

    user: Optional[User] = Relationship(back_populates="watch_history")
    movie: Optional[Movie] = Relationship(back_populates="watch_history")
