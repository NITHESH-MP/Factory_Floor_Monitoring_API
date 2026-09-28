from prometheus_client import Gauge, Counter

factory_machines_total = Gauge(
    "factory_machines_total",
    "Total number of machines in the factory"
)

factory_machine_status_total = Gauge(
    "factory_machine_status_total",
    "Number of machines grouped by status",
    ["status"]
)


factory_machine_health_total = Gauge(
    "factory_machine_health_total",
    "Number of machines grouped by health",
    ["health"]
)  

factory_maintenance_status_total = Gauge(
    "factory_maintenance_status_total",
    "Number of maintenance grouped by status",
    ["status"]
)
