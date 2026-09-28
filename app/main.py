from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from routes.metrics_route import metric_router
from routes.auth_route import auth_router
from routes.machines_route import machine_router
from routes.maintenance_route import maintenance_router
from routes.readings_route import readings_router
from exceptions.handlers import register_exception_handlers
from logging_config import setup_logging
from database.init_db import init_db
from utils.custom_openapi import custom_openapi


def create_app():
    setup_logging()
    init_db()
    
    #Calling FASTAPI
    app = FastAPI(
        title="Factory Floor Monitoring API",
        description= "API for monitoring and managing factor machines",
        version="1.0.0",
    )
    
    # Addition of instrumentation to fast-api
    Instrumentator().instrument(app)
    
    # Mapping Exception and it's handler
    register_exception_handlers(app)

    #including routers
    app.include_router(metric_router)
    app.include_router(auth_router)
    app.include_router(machine_router)
    app.include_router(maintenance_router)
    app.include_router(readings_router)
    
    custom_openapi(app)
        
    return app

app = create_app()