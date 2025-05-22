from typing import Annotated, TYPE_CHECKING
from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session as SessionBase

if TYPE_CHECKING:
    from models import User

# Database configuration
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

class Session(SessionBase):
    def add_user(self, user: "User") -> "User":
        self.add(user)
        self.commit()
        self.refresh(user)
        return user

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    print("Database and tables created successfully.")