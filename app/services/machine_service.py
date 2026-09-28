import logging

from schemas.machine_schema import MachineStatus
from schemas.maintenance_schema import MaintenanceCreate
from services.maintenance_service import maintenance_service
from repositories.repository import Repository
from models.machine_model import Machine
from models.machine_readings_model import MachineReadings
from models.maintenance_model import Maintenance
from utils.health_check import calculate_machine_health
from exceptions.exceptions import (
    MachineNotFoundError,
    DuplicateMachineError, 
    InvalidMachineStatusTransitionError,
    MissingStatusForReadingError,
    IncompleteMachineReadingError,
    MachineDeletionRestrictedError
)

logger = logging.getLogger(__name__)

class MachineService:
  
    ###############
    # GET MACHINE #
    ###############
    
    def get_machine(
        self,
        db,
        machine_id=None,
        name=None,
        status=None,
        machine_type=None
    ):
    
        repository = Repository(db)
        
        # get using machine id
        if machine_id is not None:
            result = repository.read(
                Machine,
                id=machine_id
            )

            if not result:
                raise MachineNotFoundError(machine_id)

            return result[0]
        
        result = repository.read(
            Machine, 
            name = name,
            status = status,
            machine_type = machine_type
        )

        #get using filters
        return result
        
    
    
    ###################
    #  CREATE MACHINE #
    ###################
    
    def create_machine(
        self,
        db, 
        machine_data
    ):
        logger.info(
            "Creating machine | name=%s | type=%s",
            machine_data.name,
            machine_data.machine_type
        )
        
        repository = Repository(db)
        
        # Checks for existing machine
        existing_machine = repository.read(
            Machine, 
            name = machine_data.name
        )
        
        if existing_machine:
            logger.warning(
                "Duplicate machine | name=%s",
                machine_data.name
            )
            
            raise DuplicateMachineError(machine_data.name)

        # Conversion from py obj -> SQLAlchemy obj
        machine_obj = Machine(
            name = machine_data.name,
            machine_type = machine_data.machine_type,
            status = MachineStatus.IDLE.value
        )
        
        result = repository.create(machine_obj)
    
        
        logger.info(
            "Machine created | id=%s | name=%s",
            result.id,
            result.name
        )
                
        return result
    
    ##################
    # UPDATE MACHINE #
    ##################
    
    def update_machine(
        self,
        db, 
        machine_id, 
        machine_data
    ):
        logger.info(
            "Updating machine | id=%s",
            machine_id
        )
        
        # Excluding the non - given values
        machine_data = machine_data.model_dump(exclude_unset=True)
              
        repository = Repository(db)
        
        # Find the existing machine
        existing_machine = repository.read(
            Machine,
            id = machine_id,
        )
        
        if not existing_machine:
            logger.warning(
                "Machine update failed - machine not found | id=%s",
                machine_id
            )
            raise MachineNotFoundError(machine_id)
        
        machine = existing_machine[0]

        #  name update
        if machine_data.get("name") is not None:
            existing_with_name = repository.read(
                Machine,
                name=machine_data.get("name")
            )
            
            for existing in existing_with_name:
                if existing.id != machine_id:
                    logger.warning(
                        "Machine update failed - duplicate name | id=%s | name=%s",
                        machine_id,
                        machine_data.get("name")
                    )
                    raise DuplicateMachineError(machine_data.get("name"))
            
            machine.name = machine_data.get("name")
        
        # Update machine type
        if machine_data.get("machine_type") is not None:
            machine.machine_type = machine_data.get("machine_type")

        # update machine status
        
        temperature = machine_data.get("temperature")
        vibration = machine_data.get("vibration")
        requested_status = machine_data.get("status")
        
        if requested_status is not None:
            requested_status = requested_status.value

        # Validate incomplete readings
        if (temperature is None) != (vibration is None):
            logger.warning(
                "Machine update failed - incomplete reading | id=%s",
                machine_id
            )
            raise IncompleteMachineReadingError()

        # Validate status requirement for readings
        if (temperature is not None and vibration is not None and requested_status is None):
            logger.warning(
                "Machine update failed - status missing for reading | id=%s",
                machine_id
            )
            raise MissingStatusForReadingError()
        
        # Validate status transition
        current_status = machine.status

        if (
            current_status == MachineStatus.MAINTENANCE.value
            and requested_status is not None
            and requested_status != MachineStatus.MAINTENANCE.value
        ):
            logger.warning(
                "Machine update failed - invalid status transition | "
                "id=%s | current_status=%s | requested_status=%s",
                machine_id,
                current_status,
                requested_status
            )

            raise InvalidMachineStatusTransitionError(
                machine_id=machine_id,
                current_status=current_status,
                requested_status=requested_status
            )


        # If staus to be changed into running
        if requested_status == MachineStatus.RUNNING.value:
            if temperature is None or vibration is None:
                raise IncompleteMachineReadingError()
            # Health Check
            health_status = calculate_machine_health(
                temperature= temperature,
                vibration= vibration
            )
            
            logger.info(
                "Machine health calculated | id=%s | health=%s",
                machine_id,
                health_status
            )
            
            reading = MachineReadings(
                machine_id= machine_id,
                temperature = temperature,
                vibration= vibration
            )
            
            repository.create(reading)
            
            logger.info(
                "Machine reading saved | machine_id=%s | reading_id=%s",
                machine_id,
                reading.id
            )
            
            if health_status == "Warning":
                
                maintenance = MaintenanceCreate(
                    machine_id= machine_id,
                    reason=(
                        f"Unhealthy machine reading: "
                        f"temperature={machine_data['temperature']}, "
                        f"vibration={machine_data['vibration']}"
                    )
                )
                
                maintenance_service.create_maintenance(
                    db,
                    maintenance
                )
                
                logger.warning(
                    "Machine moved to Maintenance due to unsafe reading | id=%s | temperature=%s | vibration=%s",
                    machine_id,
                    temperature,
                    vibration
                )
                
            else:
                machine.status = MachineStatus.RUNNING.value

            
        # To update to status-only updates
        elif machine_data.get("status") is not None and current_status != MachineStatus.MAINTENANCE.value:
            machine.status = machine_data.get("status").value
        

        result = repository.update(machine)
        
        logger.info(
            "Machine updated | id=%s",
            machine.id
        )
        
        return result
    
    
    ##################
    # DELETE MACHINE #
    ##################
    
    def delete_machine(
        self, 
        db,
        machine_id: int
    ):
        repository = Repository(db)
        machine = repository.read(
            Machine,
            id=machine_id
        )

        if not machine:
            raise MachineNotFoundError(machine_id)

        readings = repository.read(
            MachineReadings,
            machine_id=machine_id
        )

        maintenances = repository.read(
            Maintenance,
            machine_id=machine_id
        )

        if readings or maintenances:
            raise MachineDeletionRestrictedError(machine_id)

        repository.delete(machine[0])

    
machine_service = MachineService()