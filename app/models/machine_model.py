from sqlalchemy import Column, Integer, String
from database.database import Base

class Machine(Base):
    __tablename__ = "machines"
    
    id = Column(Integer, primary_key= True)
    name = Column(String, nullable=False)
    machine_type = Column(String, nullable=False)
    status = Column(String, nullable=False)