class MachineNotFoundError(Exception):
    def __init__(self, machine_id: int):
        self.machine_id = machine_id
        super().__init__(f"Machine with id {machine_id} not found")


class DuplicateMachineError(Exception):
    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Machine with name '{name}' already exists")