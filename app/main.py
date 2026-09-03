from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from routes.auth_route import auth_router
from routes.machines_route import machine_router
from exceptions.handlers import register_exception_handlers
from logging_config import setup_logging
from database.init_db import init_db


def create_app():
    setup_logging()
    init_db()
    
    #Calling FASTAPI
    app = FastAPI(
        title="Factory Floor Monitoring API",
        description= "API for monitoring and managing factor machines",
        version="1.0.0"
    )
    
    # Addition of instrumentation to fast-api
    Instrumentator().instrument(app).expose(app)

    # Mapping Exception and it's handler
    register_exception_handlers(app)

    #including routers
    app.include_router(auth_router)
    app.include_router(machine_router)
        
    return app

app = create_app()