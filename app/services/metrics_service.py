from sqlalchemy import func
from sqlalchemy.orm import Session

from core.metrics import (
    factory_machines_total,
    factory_machine_status_total,
    factory_machine_health_total,
    factory_maintenance_status_total
)
from utils.health_check import calculate_machine_health

from models.machine_model import Machine
from models.maintenance_model import Maintenance
from models.machine_readings_model import MachineReadings


MACHINE_STATUSES = [
    "Idle",
    "Running",
    "Maintenance"
]

MAINTENANCE_STATUSES = [
    "Open",
    "InProgress",
    "Resolved"
]

MACHINE_HEALTH_STATUSES = [
    "Healthy",
    "Warning"
]


def update_machine_metrics(db: Session):
    # Total machines
    total_machines = (
        db.query(func.count(Machine.id))
        .scalar()
    )

    factory_machines_total.set(total_machines or 0)

    # Machines grouped by status
    machine_status_counts = dict(
        db.query(
            Machine.status,
            func.count(Machine.id)
        )
        .group_by(Machine.status)
        .all()
    )

    for status in MACHINE_STATUSES:
        count = machine_status_counts.get(status, 0)

        factory_machine_status_total.labels(
            status=status
        ).set(count)
        
    
    # Latest readings for every machine
    latest_readings = {}

    readings = (
        db.query(MachineReadings)
        .order_by(MachineReadings.recorded_at.desc())
        .all()
    )

    for reading in readings:
        if reading.machine_id not in latest_readings:
            latest_readings[reading.machine_id] = reading
    
   
    # Count machines by health
    health_counts = {
        "Healthy": 0,
        "Warning": 0
    }

    for reading in latest_readings.values():
        health = calculate_machine_health(
            temperature=reading.temperature,
            vibration=reading.vibration
        )

        health_counts[health] += 1

    for health in MACHINE_HEALTH_STATUSES:
        factory_machine_health_total.labels(
            health=health
        ).set(health_counts[health])
        
    
    # Maintenance Grouped by status
    maintenance_status_counts = dict(
        db.query(
            Maintenance.status,
            func.count(Maintenance.id)
        )
        .group_by(Maintenance.status)
        .all()
    )
    
    for status in MAINTENANCE_STATUSES:
        count = maintenance_status_counts.get(status, 0)
        
        factory_maintenance_status_total.labels(
            status = status
        ).set(count)
   