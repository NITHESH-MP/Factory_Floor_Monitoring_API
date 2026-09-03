from repositories.repository import Repository
from models.machine_model import Machine
import logging
from exceptions.exceptions import (
    MachineNotFoundError,
    DuplicateMachineError
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
            status = machine_data.status.value
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
        machine_data.model_dump(exclude_unset=True)

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
        if machine_data.name is not None:
            existing_with_name = repository.read(
                Machine,
                name=machine_data.name
            )
            
            for existing in existing_with_name:
                if existing.id != machine_id:
                    logger.warning(
                        "Machine update failed - duplicate name | id=%s | name=%s",
                        machine_id,
                        machine_data.name
                    )
                    raise DuplicateMachineError(machine_data.name)
            
            machine.name = machine_data.name
        
        # Update machine type
        if machine_data.machine_type is not None:
            machine.machine_type = machine_data.machine_type

        # update machine status
        if machine_data.status is not None:
            machine.status = machine_data.status.value

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
        machine_id
    ):
        repository = Repository(db)
        
        existing_machine = repository.read(
            Machine,
            id = machine_id
        )
 
        if not existing_machine:
            raise MachineNotFoundError(machine_id)

        repository.delete(existing_machine[0])

    
machine_service = MachineService()