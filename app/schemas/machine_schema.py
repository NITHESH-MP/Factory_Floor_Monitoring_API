from pydantic import BaseModel, ConfigDict
from enum import Enum

# Machine status representation
class MachineStatus(str, Enum):
    IDLE = "Idle"
    RUNNING = "Running"

# Create Schema
class MachineCreate(BaseModel):
    name : str
    machine_type : str
    status : MachineStatus
    
# Put Schema
class MachinePut(BaseModel):
    name: str
    machine_type: str
    status: MachineStatus

# Patch Schema
class MachinePatch(BaseModel):
    name: str | None = None
    machine_type: str | None = None
    status: MachineStatus | None = None

# Response Schema
class MachineResponse(BaseModel):
    id : int
    name : str
    machine_type : str
    status : MachineStatus
    
    model_config = ConfigDict(from_attributes=True)
    
    

