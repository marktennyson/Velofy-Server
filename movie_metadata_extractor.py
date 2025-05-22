import json
from pathlib import Path
from typing import Optional, TypedDict, List, Any, Dict, Tuple
from imdb import Cinemagoer  # type: ignore
import typer

app = typer.Typer()
ia: Any = Cinemagoer()

# ================= Configuration =================
ROOT_MEDIA_PATH: str = "/Users/aniketsarkar/Desktop/movies"  # ← Change this


# ================= Typed Models =================

class ParsedMovie(TypedDict):
    name: str
    year: int
    imdb_id: str
    resolution: str


class MovieMetadata(TypedDict):
    rating: float
    plot: str
    synopsis: str
    thumbnail: str
    category: str
    name: str
    year: int


class MovieRecord(TypedDict):
    name: str
    duration: float
    rating: float
    casts: "List[Cast]"
    category: str
    size: float
    published_year: int
    filename: str
    thumbnail: str
    plot: str
    synopsis: str
    subtitles: str
    location: str


class Cast(TypedDict):
    name: str
    role: str  # e.g., Actor, Director
    image_url: Optional[str]


# ================= Utility Functions =================

def extract_casts(movie_obj: Dict[str, Any]) -> List[Cast]:
    casts: List[Cast] = []
    for person in movie_obj.get('cast', []):
        personObj = ia.search_person(person.get("name"))
        casts.append({
            "name": person.get('name', 'Unknown'),
            "role": "Actor",
            "image_url": personObj[0].get('full-size headshot', None) if personObj else None,
        })
    for person in movie_obj.get('director', []):
        personObj = ia.search_person(person.get("name"))
        casts.append({
            "name": person.get('name', 'Unknown'),
            "role": "Director",
            "image_url": personObj[0].get('full-size headshot', None) if personObj else None,
        })
    return casts


def get_imdb_id_from_filename(filename: str) -> Optional[str]:
    return filename.split(".")[0] if filename.startswith("tt") else None


def get_movie_metadata(imdb_id: str) -> Tuple[MovieMetadata, List[Cast]]:
    try:
        movie = ia.get_movie(imdb_id[2:])  # remove "tt"
        metadata: MovieMetadata = {
            "rating": float(movie.get("rating", 0.0)),
            "plot": movie.get("plot", ""),
            "synopsis": movie.get("synopsis", ""),
            "thumbnail": movie.get("cover url", "N/A"),
            "category": movie.get("genres", ["Unknown"])[0],
            "name": movie.get("title", "Unknown"),
            "year": movie.get("year", 1970),
        }
        casts = extract_casts(movie)
        return metadata, casts
    except Exception as e:
        typer.echo(typer.style(f"[ERROR] Failed to fetch metadata for {imdb_id}: {e}", fg=typer.colors.RED))
        return {
            "rating": 0.0,
            "plot": "",
            "synopsis": "",
            "thumbnail": "N/A",
            "category": "Unknown",
            "name": "Unknown",
            "year": 1970,
        }, []


def get_file_size_in_gb(filepath: Path) -> float:
    try:
        return round(filepath.stat().st_size / (1024 ** 3), 2)
    except Exception:
        return 0.0


def download_subtitle_stub() -> str:
    return "Not Available"


# ================= Main Processor =================

def process_movies(directory: Path) -> List[MovieRecord]:
    movie_data: List[MovieRecord] = []
    for file in directory.iterdir():
        if file.is_file() and file.suffix.lower() in [".mp4", ".mkv", ".avi"]:
            try:
                imdb_id: Optional[str] = get_imdb_id_from_filename(file.name)
                if not imdb_id:
                    typer.echo(typer.style(f"[SKIP] Invalid filename format: {file.name}", fg=typer.colors.YELLOW))
                    continue

                metadata, casts = get_movie_metadata(imdb_id)

                movie_record: MovieRecord = {
                    "name": metadata["name"],
                    "duration": 2.0,  # Placeholder
                    "rating": metadata["rating"],
                    "casts": casts,
                    "category": metadata["category"],
                    "size": get_file_size_in_gb(file),
                    "published_year": metadata["year"],
                    "filename": file.name,
                    "thumbnail": metadata["thumbnail"],
                    "plot": metadata["plot"],
                    "synopsis": metadata["synopsis"],
                    "subtitles": download_subtitle_stub(),
                    "location": str(file.resolve())
                }

                movie_data.append(movie_record)
                typer.echo(typer.style(f"[DONE] Processed: {file.name}", fg=typer.colors.GREEN))
            except Exception as e:
                typer.echo(typer.style(f"[ERROR] Failed to process {file.name}: {e}", fg=typer.colors.RED))
    return movie_data


# ================= Entry Point =================

@app.command()
def main(media_path: str = ROOT_MEDIA_PATH):
    movies = process_movies(Path(media_path))
    with open("movie_metadata.json", "w", encoding="utf-8") as f:
        json.dump(movies, f, indent=2, ensure_ascii=False)
    typer.echo(typer.style("\n✅ Movie data exported to movie_metadata.json", fg=typer.colors.BRIGHT_GREEN))


if __name__ == "__main__":
    app()
