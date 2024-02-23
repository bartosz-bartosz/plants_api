import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()
SQL_DB_URL = os.environ.get("SQL_DB_URL")

engine = create_engine(SQL_DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()
metadata_obj = MetaData(schema="public")


class Base(DeclarativeBase):
    metadata = metadata_obj


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
