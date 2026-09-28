from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from services.readings_service import machine_readings_service
from core.security import get_current_user
from database.database import get_db
from schemas.machine_readings_schema import MachineReadingResponse



readings_router = APIRouter(
    prefix="/api/readings",
    tags=["Machine_Readings"],
    dependencies= [Depends(get_current_user)]
)

@readings_router.get(
    "/",
    response_model= list[MachineReadingResponse],
    status_code= 200
)
def get_readings(
    machine_id : int | None = None,
    db: Session = Depends(get_db)
):
    return machine_readings_service.get_readings(
        db,
        machine_id,
    )

