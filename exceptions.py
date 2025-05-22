from fastapi.exceptions import HTTPException
from fastapi import status

class MediaNotFoundException(HTTPException):
    def __init__(self, media_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Media with ID {media_id} not found.",
            headers={"X-Error": "MediaNotFound"},
        )
class UserNotFoundException(HTTPException): 
    def __init__(self, username: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username '{username}' not found.",
            headers={"X-Error": "UserNotFound"},
        )
class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
class UserAlreadyExistsException(HTTPException):
    def __init__(self, username: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with username '{username}' already exists.",
            headers={"X-Error": "UserAlreadyExists"},
        )
class InvalidTokenException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
class TokenExpiredException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
class TokenMissingException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing",
            headers={"WWW-Authenticate": "Bearer"},
        )

class VersionFileNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Version file not found",
            headers={"X-Error": "VersionFileNotFound"},
        )

class MovieNotFoundException(HTTPException):
    def __init__(self, movie_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie with ID {movie_id} not found.",
            headers={"X-Error": "MovieNotFound"},
        )
class InvalidFileLocationException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Invalid file location",
            headers={"X-Error": "InvalidFileLocation"},
        )

class FileNotFoundException(HTTPException):
    def __init__(self, filepath: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"File not found: {filepath}",
            headers={"X-Error": "FileNotFound"},
        )

class InvalidSortingFieldException(HTTPException):
    def __init__(self, field: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid sorting field: {field}",
            headers={"X-Error": "InvalidSortingField"},
        )

class SubtitleNotFoundException(HTTPException):
    def __init__(self, movie_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subtitle for movie ID {movie_id} not found.",
            headers={"X-Error": "SubtitleNotFound"},
        )