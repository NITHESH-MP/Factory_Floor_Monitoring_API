from database.database import Base, engine

from models.machine_model import Machine
from models.user_model import User

def init_db():
    Base.metadata.create_all(bind=engine)
    
    