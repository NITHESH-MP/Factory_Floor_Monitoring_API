from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey

from core.Base import Base

class MachineReadings(Base):
    __tablename__ = "machine_readings"
    
    id = Column(Integer, primary_key=True)
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable=False)
    temperature = Column(Float, nullable=False)
    vibration = Column(Float, nullable=False)
    recorded_at = Column(DateTime,default= lambda: datetime.now(timezone.utc).replace(tzinfo=None), nullable=False)
    