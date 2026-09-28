from models.machine_readings_model import MachineReadings
from models.machine_model import Machine
from repositories.repository import Repository
from exceptions.exceptions import MachineNotFoundError


class MachineReadingsService:
    def get_readings(
        self,
        db,
        machine_id = None
    ):
        repository = Repository(db)
        
        if machine_id is not None:
            machine = repository.read(
                Machine,
                id = machine_id
            )
            
            if not machine:
                raise MachineNotFoundError
            
            

        machine_readings = repository.read(
            MachineReadings,
            machine_id = machine_id
        )
        
        return machine_readings
    
    
machine_readings_service = MachineReadingsService()