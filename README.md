# Velofy Server

Velofy is a robust, extensible backend server for media management and streaming, built with [FastAPI](https://fastapi.tiangolo.com/). It provides secure user authentication, efficient media handling, and a modern API for web and mobile clients. Velofy is designed for easy expansion, rapid development, and seamless integration with your home media setup.

---

## Features

- **User Authentication**: Secure JWT-based login, registration, and user management.
- **Media Management**: Endpoints for listing, searching, and streaming movies and media files.
- **Watch History**: Track and update user watch progress for each movie.
- **Metadata Extraction**: Automated movie metadata extraction from local files using IMDb.
- **Database Integration**: Uses SQLModel (built on SQLAlchemy and Pydantic) for ORM and data validation.
- **Custom Exception Handling**: Clear, consistent error messages for common issues and missing resources.
- **Health & Version Endpoints**: For monitoring, deployment checks, and CI/CD integration.
- **Development Ready**: Optimized for hot reloading, rapid iteration, and easy debugging.
- **Extensible Architecture**: Modular codebase for adding new features and endpoints.
- **CI/CD Friendly**: Includes linting workflows for code quality.

---

## Project Structure

```
Velofy-Server/
├── app/
│   ├── app.py                # FastAPI app initialization and router inclusion
│   └── routes/
│       ├── auth.py           # Authentication endpoints
│       └── movies.py         # Movie/media endpoints
├── jobs/
│   └── movie/
│       ├── interfaces.py     # TypedDicts for movie metadata
│       └── metadata_extractor.py # Script to extract movie metadata from files
├── schemas/                  # Pydantic schemas for API validation
│   ├── __init__.py
│   ├── auth.py
│   └── movies.py
├── models.py                 # SQLModel ORM models
├── database.py               # Database session and engine setup
├── exceptions.py             # Custom FastAPI exceptions
├── app_config.py             # App and environment configuration
├── init_db.py                # Script to initialize the database
├── server.py                 # Entrypoint for running the server with Uvicorn
├── movie_metadata.json       # Example output of metadata extraction
├── requirements.txt          # Python dependencies
├── VERSION                   # App version
├── LICENSE                   # Project license
└── .github/
    └── workflows/
        └── pylint.yml        # CI for linting
```

---

## Getting Started

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/Velofy-Server.git
cd Velofy-Server
```

### 2. Install Dependencies

It is recommended to use a virtual environment.

```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment

- Edit `app_config.py` or set environment variables as needed:
  - `MEDIA_DIR`: Path to your media directory (default: `<project>/media`)
  - `SECRET_KEY`: Secret key for JWT (default: `"default"`)
  - `MOVIE_MEDIA_DIR`: Path to your movies directory (default: `<MEDIA_DIR>/movies`)
- You can also create a `.env` file for environment variables.

### 4. Initialize the Database

```sh
python init_db.py
```

### 5. (Optional) Extract Movie Metadata

To scan your movie directory and generate `movie_metadata.json`:

```sh
python jobs/movie/metadata_extractor.py --media-path /path/to/your/movies
```

### 6. Run the Server

```sh
python server.py
```

The API will be available at [http://localhost:8000](http://localhost:8000).

---

## API Overview

### Authentication

- `POST /auth/login` — User login, returns JWT token.
- `POST /auth/register` — Register a new user.
- `GET /auth/me` — Get current user info (JWT required).
- `PUT /auth/me` — Update user info.
- `DELETE /auth/me` — Delete user account.

### Movies & Media

- `GET /media/movies/` — List all movies (with filtering, sorting, and pagination).
- `GET /media/movie/{movie_id}` — Get details for a specific movie.
- `GET /media/stream/{movie_id}` — Stream a movie file.
- `GET /media/subtitle/{movie_id}` — Download subtitles for a movie.
- `POST /media/watch/{movie_id}` — Log watch history.
- `PUT /media/watch/{movie_id}` — Update watch progress.
- `GET /media/watch/{movie_id}` — Get watch history for a movie.

### Health & Version

- `GET /health` — Health check endpoint.
- `GET /version` — Get server version.

---

## Database Models

- **User**: Stores user credentials and profile.
- **Movie**: Stores movie metadata and file info.
- **Cast**: Stores cast/crew info.
- **WatchHistory**: Tracks user watch progress.
- **MovieCastLink**: Many-to-many relationship between movies and cast.

See [`models.py`](models.py) for full details.

---

## Metadata Extraction

The script [`jobs/movie/metadata_extractor.py`](jobs/movie/metadata_extractor.py) scans your movie directory, fetches metadata from IMDb, and outputs a JSON file. It uses [`jobs/movie/interfaces.py`](jobs/movie/interfaces.py) for type definitions.

---

## Development

- **Hot Reload**: Enabled by default with Uvicorn (`reload=True` in `server.py`).
- **Linting**: Uses Pylint (see [`.github/workflows/pylint.yml`](.github/workflows/pylint.yml)).
- **Testing**: Add your own tests using [pytest](https://docs.pytest.org/) or [unittest](https://docs.python.org/3/library/unittest.html).
- **Configuration**: All configuration is centralized in [`app_config.py`](app_config.py).

---

## Deployment

- For production, run with Uvicorn or Gunicorn behind a reverse proxy (e.g., Nginx).
- Set `reload=False` and use a strong `SECRET_KEY`.
- Use a production-ready database (e.g., PostgreSQL).

---

## Contributing

Pull requests are welcome! Please lint your code and write clear commit messages. For major changes, open an issue first to discuss what you would like to change.

---

## License

MIT License

---

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [Cinemagoer (IMDbPY)](https://cinemagoer.github.io/)
- [Pydantic](https://docs.pydantic.dev/)
- [Uvicorn](https://www.uvicorn.org/)

---

## Contact

For questions or support, open an issue or contact the maintainer.

---

**Happy streaming!**