import json
from pathlib import Path
from sqlmodel import Session, SQLModel, create_engine

# 🔁 Adjust these to your actual project structure
from models import Movie  # ← Update this import to match your project

# 🔧 Path to your results.json file
DATA_FILE = Path("results.json")
DATABASE_URL = "sqlite:///database.db"  # ← Adjust this to your DB config

# 🔌 Create engine and session
engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)  # Ensure tables are created

def load_movies_from_json():
    with DATA_FILE.open("r") as f:
        movie_data = json.load(f)

    with Session(engine) as session:
        for item in movie_data:
            movie = Movie(**item)
            session.add(movie)

        session.commit()
        print(f"✅ Loaded {len(movie_data)} movies into the database.")

if __name__ == "__main__":
    load_movies_from_json()
