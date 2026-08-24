from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from exceptions.exceptions import(
    MachineNotFoundError,
    DuplicateMachineError
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
        SQLAlchemyError,
        database_error_handler
    )
    
    app.add_exception_handler(
        Exception,
        general_exception_handler
    )