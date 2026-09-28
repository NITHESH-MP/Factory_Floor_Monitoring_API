def calculate_machine_health(temperature: float, vibration: float):
    if temperature <= 80 and vibration <= 5:
        return "Healthy"

    return "Warning"