from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime, timezone
from core.Base import Base

class Maintenance(Base):
    __tablename__ = "maintenances"
    
    id = Column(Integer, primary_key= True)
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable= False)
    reason = Column(String, nullable= False)
    status = Column(String, nullable= False, default= "Open")
    assigned_to = Column(String, nullable=True)
    created_at = Column(DateTime,default= lambda : datetime.now(timezone.utc).replace(tzinfo=None), nullable= False)
    resolved_at = Column(DateTime, nullable= True)
    