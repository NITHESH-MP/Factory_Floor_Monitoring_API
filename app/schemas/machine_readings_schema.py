from datetime import datetime
from pydantic import BaseModel, ConfigDict


class MachineReadingResponse(BaseModel):
    id: int
    machine_id: int
    temperature: float
    vibration: float
    recorded_at: datetime

    model_config = ConfigDict(from_attributes=True)