from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from database.database import get_db
from services.metrics_service import (
    update_machine_metrics,
    # update_latest_reading_metrics
)

metric_router = APIRouter(
    tags=["Monitoring"]
)

@metric_router.get(
    "/metrics",
    status_code= 200
)
def metrics(
    db : Session = Depends(get_db)
):
    update_machine_metrics(db)
    # update_latest_reading_metrics(db)
    
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

    