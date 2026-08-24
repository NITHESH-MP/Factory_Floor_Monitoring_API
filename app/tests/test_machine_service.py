import pytest
from unittest.mock import Mock, patch

from services.machine_service import MachineService
from exceptions.exceptions import DuplicateMachineError
from models.machine_model import Machine
from schemas.machine_schema import MachineCreate, MachineStatus

def test_create_machine_duplicate_name():
    
    #Arrange
    db = Mock()
    
    existing_machine = Machine(
        id=1,
        name="CNC001",
        machine_type="CNC",
        status="Idle"
    )
    
    with patch(
        "services.machine_service.Repository"
    ) as repository_mock:
        repository_mock.return_value.read.return_value = [existing_machine]
    
    service = MachineService()
    
    machine_data = MachineCreate(
        name = "CNC001",
        machine_type="CNC",
        status = MachineStatus.IDLE
    )
    
    with pytest.raises(DuplicateMachineError):
        service.create_machine(
            db,
            machine_data
        )
    