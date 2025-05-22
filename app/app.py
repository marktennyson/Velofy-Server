from fastapi import FastAPI
from app.routes import auth, movies
from database import create_db_and_tables
from contextlib import asynccontextmanager
from app_config import BASE_DIR
from exceptions import VersionFileNotFoundException


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix="/auth")
app.include_router(movies.router, prefix="/media")

@app.get("/")
def read_root():
    return {"message": "Media Server API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"} 

@app.get("/version")
def version():
    try:
        with open(BASE_DIR / "VERSION", "r") as f:
            version = f.read().strip()
        return {"version": version}
    except FileNotFoundError:
        raise VersionFileNotFoundException