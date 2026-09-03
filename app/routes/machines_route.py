from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.security import get_current_user

from schemas.machine_schema import (
    MachineCreate, 
    MachinePut,
    MachinePatch, 
    MachineResponse
)
from services.machine_service import machine_service
from database.database import get_db

# ROUTER CREATION
machine_router = APIRouter(
        prefix = "/api/machines",
        tags= ["Machines"],
        dependencies=[Depends(get_current_user)]
    )


#GET MACHINE -> WITH FILTERS
@machine_router.get(
    "/",
    response_model = list[MachineResponse],
    status_code=200
)
def get_machines(
    name : str | None = None,
    status: str | None = None,
    machine_type : str | None = None,
    
    db : Session = Depends(get_db)
):
    return machine_service.get_machine(
        db, 
        name = name,
        status = status,
        machine_type = machine_type,
    )


# GET MACHINE -> WITH ID
@machine_router.get(
    "/{machine_id}",
    response_model = MachineResponse,
    status_code= 200    
)
def get_machine(
    machine_id: int,
    
    db : Session = Depends(get_db)
):
    return machine_service.get_machine(
        db,
        machine_id
    )
    
    
# CREATE MACHINE
@machine_router.post(
    "/",
    response_model=MachineResponse,
    status_code=201
)
def create_machines(
    machine_data: MachineCreate,
    
    db : Session = Depends(get_db)
):
    return machine_service.create_machine(
        db,
        machine_data
    )


# UPDATE MACHINE
@machine_router.put(
    "/{machine_id}",
    response_model= MachineResponse,
    status_code=200    
)
def update_machines(
    machine_id: int, 
    machine_data: MachinePut,
    
    db : Session = Depends(get_db)
):
    return machine_service.update_machine(
        db,
        machine_id, 
        machine_data
    )


# PATCH MACHINE
@machine_router.patch(
    "/{machine_id}",
    response_model= MachineResponse,
    status_code=200    
)
def patch_machines(
    machine_id: int,
    machine_data: MachinePatch,
    
    db : Session = Depends(get_db)
):
    
    return machine_service.update_machine(
        db,
        machine_id, 
        machine_data
    )
    
    
#DELETE MACHINE  
@machine_router.delete(
    "/{machine_id}",
    status_code=204    
)
def delete_machines(
    machine_id: int,
    
    db : Session = Depends(get_db)
):
    machine_service.delete_machine(
        db,
        machine_id
    )


