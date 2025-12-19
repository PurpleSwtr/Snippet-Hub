from typing import Generator
from src.core.db import session

def get_db() -> Generator:
    db = session()
    try:
        yield db
    finally:
        db.close()