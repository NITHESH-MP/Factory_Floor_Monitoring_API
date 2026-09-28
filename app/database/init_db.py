from database.database import engine
from core.Base import Base
from models.machine_model import Machine
from models.machine_readings_model import MachineReadings

def init_db():
    Base.metadata.create_all(bind=engine)


    