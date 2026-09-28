class MachineNotFoundError(Exception):
    def __init__(self, machine_id: int):
        self.machine_id = machine_id
        super().__init__(f"Machine with id {machine_id} not found")


class DuplicateMachineError(Exception):
    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Machine with name '{name}' already exists")
        
class InvalidMachineStatusTransitionError(Exception):
    def __init__(
        self,
        machine_id : int,
        current_status : str,
        requested_status: str    
    ):
        self.machine_id = machine_id
        self.current_status = current_status
        self.requested_status = requested_status
        super().__init__(f"Machine {machine_id} restricted status transition "
                         f"from {current_status} to {requested_status}")

class MissingStatusForReadingError(Exception):
    def __init__(self):
        super().__init__(
            "Status must be specified when temperature or vibration readings are provided"
        )

class IncompleteMachineReadingError(Exception):
    def __init__(self):
        super().__init__(
            "Both temperature and vibration are required when submitting a machine reading"
        )

class DuplicateMaintenanceError(Exception):
    def __init__(
        self, 
        machine_id : int
    ):
        self.machine_id = machine_id
        super().__init__(
            f"Active Maintenance for Machine {machine_id} already exists"
        )
    
class MaintenanceNotFoundError(Exception):
    def __init__(
        self, 
        maintenance_id: int
    ):
        self.maintenance_id = maintenance_id
        super().__init__(
            f"Maintenance {maintenance_id} not found"
        )

class InvalidMaintenanceStatusTransitionError(Exception):

    def __init__(
        self,
        maintenance_id,
        current_status,
        requested_status
    ):
        super().__init__(
            f"Invalid maintenance status transition for maintenance "
            f"{maintenance_id}: {current_status} -> {requested_status}"
        )
        
class TechnicianAssignmentRequiredError(Exception):
    def __init__(
        self, 
        maintenance_id: int
    ):
        self.maintenance_id = maintenance_id
        super().__init__(
            f"Technician must be assigned before maintenance "
            f"{maintenance_id} can move to InProgress"
        )

class MachineDeletionRestrictedError(Exception):
    def __init__(self, machine_id: int):
        super().__init__(
            f"Machine {machine_id} cannot be deleted because it has "
            "readings or maintenance history"
        )
