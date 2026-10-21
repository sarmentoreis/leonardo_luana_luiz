from sqlmodel import create_engine, Session
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_FILE = BASE_DIR / "database.db"

DATABASE_URL = f"sqlite:///{DATABASE_FILE.as_posix()}"

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session