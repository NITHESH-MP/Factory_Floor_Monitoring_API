from sqlalchemy import Column, Integer, String
from core.Base import Base

class Machine(Base):
    __tablename__ = "machines"
    
    id = Column(Integer, primary_key= True)
    name = Column(String, nullable=False)
    machine_type = Column(String, nullable=False)
    status = Column(String, nullable=False)