# Velofy Server

Velofy is a FastAPI-based backend server for media management and streaming, designed for easy expansion and modern web integration.

## Features

- **User Authentication**: Secure JWT-based login and registration.
- **Media Management**: Endpoints for listing, searching, and streaming movies.
- **Health Check**: Simple endpoint for monitoring server status.
- **Database**: Uses SQLModel for ORM and Pydantic for data validation.
- **Custom Exception Handling**: Clear error messages for common issues.
- **Development Ready**: Optimized for hot reloading and rapid iteration.

## Project Structure

```
Velofy-Server/
├── app/
│   ├── app.py                # FastAPI app and routers
│   └── routes/               # API endpoints (auth, movies, etc.)
├── jobs/
│   └── movie/
│       ├── interfaces.py
│       └── metadata_extractor.py
├── schemas/                  # Pydantic schemas
├── models.py                 # SQLModel ORM models
├── database.py               # Database setup
├── exceptions.py             # Custom exceptions
├── app_config.py             # App configuration
├── init_db.py                # DB initialization script
├── server.py                 # Uvicorn entrypoint (main script)
├── requirements.txt          # Dependencies
└── README.md                 # Project documentation
```

## Getting Started

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/Velofy-Server.git
cd Velofy-Server
```

### 2. Install Dependencies

```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Environment

- Edit `app_config.py` or set environment variables as needed (e.g., `MEDIA_DIR`, `SECRET_KEY`).

### 4. Initialize the Database

```sh
python init_db.py
```

### 5. Run the Server

```sh
python server.py
```

The API will be available at [http://localhost:8000](http://localhost:8000).

## API Overview

- `POST /auth/login` — User login (JWT)
- `POST /auth/register` — Register new user
- `GET /media/movies/` — List all movies
- `GET /media/movie/{movie_id}` — Movie details
- `GET /media/stream/{movie_id}` — Stream a movie
- `GET /health` — Health check

## Development

- **Hot Reload**: Enabled by default in `server.py` with `reload=True`.
- **Linting**: Use Pylint for code quality.

## License

MIT License

---

**Happy streaming!**