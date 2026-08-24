import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

#session factory
sessionLocal = sessionmaker(
    autocommit= False,
    autoflush= False,
    bind= engine
)

# Base Model -> With DB
Base = declarative_base()

#Session Allocation
def get_db():
    db = sessionLocal()

    try:
        yield db
    finally:
        db.close()
