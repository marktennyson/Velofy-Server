import os
from pathlib import Path

APP_NAME:str = "Velofy - The Home Server"
BASE_DIR:Path = Path(os.path.dirname(os.path.abspath(__file__)))
# MEDIA_DIR:Path = Path(os.getenv("MEDIA_DIR") or "") or BASE_DIR / "media"
MEDIA_DIR:Path = Path(os.getenv("MEDIA_DIR") or BASE_DIR / "media")

SECRET_KEY:str = os.getenv("SECRET_KEY") or "default"
ALGORITHM:str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES:int = 7*24*60  # 7 days

MOVIE_MEDIA_DIR:Path = Path(os.getenv("MOVIE_MEDIA_DIR") or MEDIA_DIR / "movies")