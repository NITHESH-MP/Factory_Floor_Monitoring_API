from database.database import engine
from core.Base import Base

def init_db():
    Base.metadata.create_all(bind=engine)

    