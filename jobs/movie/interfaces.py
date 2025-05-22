from typing import Optional, TypedDict, List


class MovieMetadata(TypedDict):
    rating: float
    plot: str
    synopsis: str
    thumbnail: str
    category: str
    name: str
    year: int

class Cast(TypedDict):
    name: str
    role: str  # e.g., Actor, Director
    image_url: Optional[str]
        
class MovieRecord(TypedDict):
    imdb_id: str
    name: str
    duration: float
    rating: float
    casts: List[Cast]
    category: str
    size: float
    published_year: int
    filename: str
    thumbnail: str
    plot: str
    synopsis: str
    subtitles: str
    location: str