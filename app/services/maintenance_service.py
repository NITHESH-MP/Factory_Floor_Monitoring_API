from datetime import datetime, timezone 
import logging

from schemas.machine_schema import MachineStatus
from schemas.maintenance_schema import MaintenanceStatus
from models.machine_model import Machine
from models.maintenance_model import Maintenance
from repositories.repository import Repository

from exceptions.exceptions import (
    MachineNotFoundError,
    DuplicateMaintenanceError,
    MaintenanceNotFoundError,
    InvalidMaintenanceStatusTransitionError,
    TechnicianAssignmentRequiredError
)

logger = logging.getLogger(__name__)

class MaintenanceService:
    
    ###################
    # GET MAINTENANCE #
    ###################
    def get_maintenance(
        self,
        db,
        maintenance_id=None,
        machine_id=None,
        status=None
    ):
        repository = Repository(db)

        # Get one maintenance record using ID
        if maintenance_id is not None:
            result = repository.read(
                Maintenance,
                id=maintenance_id
            )

            if not result:
                raise MaintenanceNotFoundError(maintenance_id)

            return result[0]

        # Get maintenance records using filters
        result = repository.read(
            Maintenance,
            machine_id=machine_id,
            status=status
        )

        return result

    ######################
    # CREATE MAINTENANCE #
    ######################

    def create_maintenance(
        self,
        db,
        maintenance_data
    ):

        logger.info(
            "Creating maintenance for machine_id=%s",
            maintenance_data.machine_id
        )
        
        repository = Repository(db)

        # Check whether the machine exists
        machines = repository.read(
            Machine,
            id=maintenance_data.machine_id
        )

        if not machines:
            logger.warning(
                "Machine not found: machine_id=%s",
                maintenance_data.machine_id
            )
            raise MachineNotFoundError(
                maintenance_data.machine_id
            )

        machine = machines[0]
        
        # Check whether active maintenance already exists
        active_maintenance = repository.read(
            Maintenance,
            machine_id = maintenance_data.machine_id,
            status = MaintenanceStatus.OPEN.value
        )
        
        in_progress_maintenance = repository.read(
            Maintenance,
            machine_id = maintenance_data.machine_id,
            status = MaintenanceStatus.IN_PROGRESS.value
        )
        
        if active_maintenance or in_progress_maintenance:
            logger.warning(
                "Active maintenance already exists for machine_id = %s",
                maintenance_data.machine_id
            )
            
            raise DuplicateMaintenanceError(maintenance_data.machine_id)
        
        # Create Maintenance Record
        maintenance = Maintenance(
            machine_id = maintenance_data.machine_id,
            reason = maintenance_data.reason,
            status = MaintenanceStatus.OPEN.value
        )
        
        # Save Maintenance record
        created_maintenance = repository.create(maintenance)
        
        # Update machine status
        machine.status = "Maintenance"
        repository.update(machine)

        logger.info(
            "Maintenance created successfully: maintenance_id=%s, "
            "machine_id=%s",
            created_maintenance.id,
            created_maintenance.machine_id
        )

        return created_maintenance
    
    ######################
    # UPDATE MAINTENANCE #
    ######################
    def update_maintenance(
        self,
        db,
        maintenance_id,
        maintenance_data
    ):
        logger.info(
            "Updating maintenance for maintenance_id=%s",
            maintenance_id
        )

        # Convert only the fields supplied by the client
        maintenance_data = maintenance_data.model_dump(exclude_unset=True)

        repository = Repository(db)

        # Find existing maintenance record
        existing_maintenance = repository.read(
            Maintenance,
            id=maintenance_id
        )

        if not existing_maintenance:
            logger.warning(
                "Maintenance update failed - maintenance record not found | id=%s",
                maintenance_id
            )
            raise MaintenanceNotFoundError(maintenance_id)

        # Existing maintenance
        maintenance = existing_maintenance[0]

        current_status = maintenance.status
        requested_status = maintenance_data.get("status")

        if requested_status is not None:
            requested_status = requested_status.value

        # Prevent editing resolved maintenance records
        if current_status == MaintenanceStatus.RESOLVED.value:

            # Resolved -> not other transition is accepted
            if (
                requested_status is not None
                and requested_status != MaintenanceStatus.RESOLVED.value
            ):
                logger.warning(
                    "Maintenance update failed - Invalid transition for maintenance record | id=%s",
                    maintenance_id
                )
                
                raise InvalidMaintenanceStatusTransitionError( maintenance_id, current_status, requested_status)

            editable_fields = set(maintenance_data.keys()) - {"status"}

            if editable_fields:
                raise InvalidMaintenanceStatusTransitionError(
                    maintenance_id,
                    current_status,
                    current_status
                )

            return maintenance

        # Validate status transitions
        if requested_status is not None:

            # Open -> Open or InProgress
            if current_status == MaintenanceStatus.OPEN.value:
                
                if requested_status not in (
                    MaintenanceStatus.OPEN.value,
                    MaintenanceStatus.IN_PROGRESS.value
                ):
                    logger.warning(
                        "Maintenance update failed - Invalid transition for maintenance record | id=%s",
                        maintenance_id
                    )
                                    
                    raise InvalidMaintenanceStatusTransitionError( maintenance_id, current_status, requested_status)

                # Technician is required for InProgress
                if requested_status == MaintenanceStatus.IN_PROGRESS.value:
                    # Gets technician from current-data or requested-data
                    assigned_to = maintenance_data.get(
                        "assigned_to",
                        maintenance.assigned_to
                    )

                    if not assigned_to:
                        logger.warning(
                            "Maintenance update failed - Technicain is not assigned for transition to In_progress",
                            maintenance_id
                        )
                        
                        raise TechnicianAssignmentRequiredError(maintenance_id)

            # InProgress -> InProgress or Resolved
            elif current_status == MaintenanceStatus.IN_PROGRESS.value:

                if requested_status not in (
                    MaintenanceStatus.IN_PROGRESS.value,
                    MaintenanceStatus.RESOLVED.value
                ):
                    logger.warning(
                        "Maintenance update failed - Invalid transition for maintenance record | id=%s",
                        maintenance_id
                    )                                    
                    
                    raise InvalidMaintenanceStatusTransitionError( maintenance_id, current_status, requested_status)

            # Any other unexpected status
            else:
                logger.warning(
                    "Maintenance update failed - Invalid transition for maintenance record | id=%s",
                    maintenance_id
                )                                    
                    
                raise InvalidMaintenanceStatusTransitionError( maintenance_id, current_status, requested_status)
                

        # Apply other update fields

        if "reason" in maintenance_data:
            maintenance.reason = maintenance_data.get("reason")

        if "assigned_to" in maintenance_data:
            maintenance.assigned_to = maintenance_data.get("assigned_to")

        # Validate technician assignment for InProgress

        final_status = (
            requested_status
            if requested_status is not None
            else current_status
        )

        if final_status == MaintenanceStatus.IN_PROGRESS.value:

            if not maintenance.assigned_to:
                raise TechnicianAssignmentRequiredError(
                    maintenance_id
                )

        # Set resolved_at when resolving maintenance
      
        if (
            requested_status == MaintenanceStatus.RESOLVED.value
            and current_status != MaintenanceStatus.RESOLVED.value
        ):
            maintenance.resolved_at = datetime.now(timezone.utc).replace(tzinfo=None)

        if requested_status is not None:
            maintenance.status = requested_status
            
            # set machine status to idle
            machines = repository.read(
                Machine,
                id=maintenance.machine_id
            )

            if not machines:
                raise MachineNotFoundError(
                    maintenance.machine_id
                )

            machine = machines[0]
            machine.status = MachineStatus.IDLE.value

            repository.update(machine)

        updated_maintenance = repository.update(
            maintenance
        )

        logger.info(
            "Maintenance updated successfully: maintenance_id=%s",
            updated_maintenance.id
        )

        return updated_maintenance
        
    ######################
    # DELETE MAINTENANCE #
    ######################
    
    def delete_maintenance(
        self,
        db, 
        maintenance_id
    ):
        logger.info(
            "Deleting maintenance for maintenance_id=%s",
            maintenance_id
        )
        repository = Repository(db)
        
        existing_maintenance = repository.read(
            Maintenance,
            id = maintenance_id
        )
        
        if not existing_maintenance:
            logger.warning(
                "Maintenance Deletion failed - maintenance record not found | id=%s",
                maintenance_id
            )
            raise MaintenanceNotFoundError(maintenance_id)
        
        repository.delete(existing_maintenance[0])
    
    
        
maintenance_service = MaintenanceService()