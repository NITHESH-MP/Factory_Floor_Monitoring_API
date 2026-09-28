from enum import Enum
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class MaintenanceStatus(str, Enum):
    OPEN = "Open"
    IN_PROGRESS = "InProgress"
    RESOLVED = "Resolved"
    
class MaintenanceCreate(BaseModel):
    machine_id: int
    reason: str
    
class MaintenanceUpdate(BaseModel):
    status: MaintenanceStatus | None = None
    assigned_to: str | None = None
    reason: str | None = None
    
class MaintenanceResponse(BaseModel):
    id : int 
    machine_id: int
    reason: str
    status: MaintenanceStatus
    assigned_to: str | None = None
    created_at: datetime
    resolved_at: datetime | None = None
    
    model_config = ConfigDict(from_attributes=True)
    