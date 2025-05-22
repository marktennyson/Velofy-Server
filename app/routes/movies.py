from fastapi import APIRouter, Query
from fastapi.responses import FileResponse
from sqlmodel import select, desc, asc
from typing import Dict, Optional, Any
import os
from app_config import MEDIA_DIR
from database import SessionDep
from datetime import datetime, timezone
from models import WatchHistory, Movie
# from sqlalchemy import String
from exceptions import (
    FileNotFoundException,
    MovieNotFoundException, 
    InvalidFileLocationException,
    InvalidSortingFieldException,
    SubtitleNotFoundException
)

router = APIRouter()

@router.get("/movies/")
def list_movies(
    db: SessionDep,
    category: Optional[str] = None,
    sort_by: Optional[str] = Query("name", enum=["name", "size", "added_date", "rating"]),
    sort_order: Optional[str] = Query("asc", enum=["asc", "desc"]),
    search: Optional[str] = None
):
    query = select(Movie)

    if category:
        query = query.where(Movie.category == category)
    
    # if search:
    #     query = query.where(Movie.name.cast(String).ilike(f"%{search}%"))
    if sort_by:
        if sort_by not in ["name", "size", "added_date", "rating"]:
            raise InvalidSortingFieldException(sort_by)
        sort_column = getattr(Movie, sort_by)
        if sort_order == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))

    result = db.exec(query).all()
    return [movie_to_dict(movie) for movie in result]

def movie_to_dict(movie: Movie) -> Dict[str, Any]:
    return {
        "id": movie.id,
        "name": movie.name,
        "duration": movie.duration,
        "rating": movie.rating,
        "category": movie.category,
        "size": movie.size,
        "published_year": movie.published_year,
        "filename": movie.filename,
        "casts": [
            {
                "name": link.cast.name,
                "role": link.cast.role,
                "image_url": link.cast.image_url,
            } for link in movie.cast_links if link.cast is not None
        ]
    }

@router.get("/stream/{movie_id}")
def stream_file(movie_id: int, db: SessionDep):
    movie = db.get(Movie, movie_id)
    if not movie:
        raise MovieNotFoundException(movie_id)

    location = getattr(movie, "location", None)
    if not location or not isinstance(location, str):
        raise InvalidFileLocationException
    filepath = location
    if not os.path.isfile(filepath):
        filepath = os.path.join(MEDIA_DIR, location)
    if not os.path.isfile(filepath):
        raise FileNotFoundException(filepath)
    if os.path.isfile(filepath):
        return FileResponse(filepath, media_type="video/mp4")
    raise FileNotFoundException(filepath)

@router.get("/movie/{movie_id}")
def get_movie_details(movie_id: int, db: SessionDep):
    movie = db.get(Movie, movie_id)
    if not movie:
        raise MovieNotFoundException(movie_id)
    
    return movie_to_dict(movie)

@router.post("/watch/{movie_id}")
def log_watch(movie_id: int, user_id: int, progress: float, db: SessionDep):
    """Log watch history for a movie."""
    history = WatchHistory(
        user_id=user_id,
        movie_id=movie_id,
        watched_at=datetime.now(timezone.utc),
        progress=progress
    )
    db.add(history)
    db.commit()
    return {"status": "logged"}

@router.put("/watch/{movie_id}")
def update_watch(movie_id: int, user_id: int, progress: float, db: SessionDep):
    """Update watch history for a movie."""
    history = db.exec(select(WatchHistory).where(WatchHistory.movie_id == movie_id, WatchHistory.user_id == user_id)).first()
    if not history:
        raise MovieNotFoundException(movie_id)
    
    history.progress = progress
    db.commit()
    return {"status": "updated"}

@router.get("/watch/{movie_id}")
def get_watch_history(movie_id: int, user_id: int, db: SessionDep) -> Dict[str, Any]:
    """Get watch history for a movie."""
    history = db.exec(select(WatchHistory).where(WatchHistory.movie_id == movie_id, WatchHistory.user_id == user_id)).first()
    if not history:
        raise MovieNotFoundException(movie_id)
    
    return {
        "movie_id": history.movie_id,
        "user_id": history.user_id,
        "watched_at": history.watched_at,
        "progress": history.progress
    }

@router.get("/subtitle/{movie_id}")
def get_subtitle(movie_id: int, db: SessionDep):
    movie = db.get(Movie, movie_id)
    if movie is not None and getattr(movie, "subtitles", None) is not None:
        subtitle_path = os.path.join(MEDIA_DIR, movie.subtitles)
        if os.path.isfile(subtitle_path):
            return FileResponse(subtitle_path, media_type="text/plain")
    raise SubtitleNotFoundException(movie_id)