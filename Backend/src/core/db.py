from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine(url="postgresql+psycopg2://app_user:example@localhost:5432/app_db")
session = sessionmaker(engine)

class Base(DeclarativeBase):
    pass