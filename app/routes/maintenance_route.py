from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.security import get_current_user
from database.database import get_db
from services.maintenance_service import maintenance_service
from schemas.maintenance_schema import(
    MaintenanceStatus,
    MaintenanceCreate,
    MaintenanceUpdate,
    MaintenanceResponse
)

# Router Creation 
maintenance_router = APIRouter(
    prefix="/api/maintenance",
    tags=["Maintenance"],
    dependencies=[Depends(get_current_user)]
)

# GET MAINTENANCE List
@maintenance_router.get(
    "/",
    response_model= list[MaintenanceResponse],
    status_code=200
)
def get_maintenances(
    machine_id : int | None = None,
    maintenance_status: MaintenanceStatus | None = None,
    
    db : Session = Depends(get_db)
):
    return maintenance_service.get_maintenance(
        db,
        machine_id = machine_id,
        status = maintenance_status
    )

# GET MAINTENANCE BY ID
@maintenance_router.get(
    "/{maintenance_id}",
    response_model= MaintenanceResponse,
    status_code=200
)
def get_maintenance(
    maintenance_id : int,
    db : Session = Depends(get_db)
):
    return maintenance_service.get_maintenance(
        db,
        maintenance_id
    )
    
# CREATE MAINTENANCE
@maintenance_router.post(
    "/",
    response_model= MaintenanceResponse,
    status_code= 201
)
def create_maintenance(
    maintenance_data: MaintenanceCreate,
    db : Session = Depends(get_db)
):
    return maintenance_service.create_maintenance(
        db,
        maintenance_data
    )
    
# UPDATE MAINTENANCE
@maintenance_router.patch(
    "/{maintenance_id}",
    response_model= MaintenanceResponse,
    status_code=200
)
def update_maintenance(
    maintenance_id : int,
    maintenance_data : MaintenanceUpdate,
    db : Session = Depends(get_db)
):
    return maintenance_service.update_maintenance(
        db,
        maintenance_id,
        maintenance_data
    )

# DELETE MAINTENANCE
@maintenance_router.delete(
    "/{maintenance_id}",
    status_code=204
)
def delete_maintenance(
    maintenance_id: int,
    db: Session = Depends(get_db)
):
    maintenance_service.delete_maintenance(
        db,
        maintenance_id
    )

    return None
