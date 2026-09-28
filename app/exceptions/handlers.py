from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from exceptions.exceptions import(
    MachineNotFoundError,
    DuplicateMachineError,
    InvalidMachineStatusTransitionError,
    MissingStatusForReadingError,
    IncompleteMachineReadingError,
    DuplicateMaintenanceError,
    MaintenanceNotFoundError,
    InvalidMaintenanceStatusTransitionError,
    TechnicianAssignmentRequiredError,
    MachineDeletionRestrictedError
)


def machine_not_found_handler(
    request: Request,
    exc: MachineNotFoundError
):
    return JSONResponse(
        status_code= 404,
        content = {
            "message" : str(exc)
        }
    )
    

def duplicate_machine_handler(
    request: Request,
    exc: DuplicateMachineError
):
    return JSONResponse(
        status_code= 409,
        content={
            "detail": str(exc)
        }
    )

def invalid_machine_status_transition_handler(
    request: Request,
    exc: InvalidMachineStatusTransitionError
):
    return JSONResponse(
        status_code= 409,
        content={
            "detail" : str(exc)
        }
    )

def missing_status_for_reading_handler(
    request: Request,
    exc: MissingStatusForReadingError
):
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)}
    )

def incomplete_machine_reading_handler(
    request: Request,
    exc: IncompleteMachineReadingError
):
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)}
    )

def duplicate_maintenance_error(
    request: Request,
    exc: DuplicateMaintenanceError
):
    return JSONResponse(
        status_code= 409,
        content={"detail" : str(exc)}
    )
    
def maintenance_not_found(
    reques: Request,
    exc: MaintenanceNotFoundError
):
    return JSONResponse(
        status_code= 409,
        content={"detail": str(exc)}
    )

def invalid_maintenance_status_transition_error(
    request: Request,
    exc: InvalidMaintenanceStatusTransitionError
):
    return JSONResponse(
        status_code= 409,
        content={"details" : str(exc)}
    )

def technician_assignment_required_error(
    request: Request,
    exc: TechnicianAssignmentRequiredError
):
    return JSONResponse(
        status_code= 409,
        content={"details" : str(exc)}
    )

def machine_deletion_restricted_Error(
    request: Request,
    exc: MachineDeletionRestrictedError
):
    return JSONResponse(
        status_code= 409,
        content={"details" : str(exc)}
    )

def database_error_handler(
    request: Request,
    exc: SQLAlchemyError
):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Database error occurred"
        }
    )


def general_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error"
        }
    )
    
def register_exception_handlers(app : FastAPI):
    app.add_exception_handler(
        MachineNotFoundError,
        machine_not_found_handler
    )
    
    app.add_exception_handler(
        DuplicateMachineError,
        duplicate_machine_handler
    )
    
    app.add_exception_handler(
        InvalidMachineStatusTransitionError,
        invalid_machine_status_transition_handler
    )
    
    app.add_exception_handler(
        MissingStatusForReadingError,
        missing_status_for_reading_handler
    )

    app.add_exception_handler(
        IncompleteMachineReadingError,
        incomplete_machine_reading_handler
    )
    
    app.add_exception_handler(
        DuplicateMaintenanceError,
        duplicate_maintenance_error
    )
    
    app.add_exception_handler(
        InvalidMaintenanceStatusTransitionError,
        invalid_maintenance_status_transition_error
    )
    
    app.add_exception_handler(
        TechnicianAssignmentRequiredError,
        technician_assignment_required_error
    )
    
    app.add_exception_handler(
        MachineDeletionRestrictedError,
        machine_deletion_restricted_Error
    )
    
    app.add_exception_handler(
        SQLAlchemyError,
        database_error_handler
    )
    
    app.add_exception_handler(
        Exception,
        general_exception_handler
    )
    