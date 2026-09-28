import csv
import time
import requests
from pathlib import Path



# ============================================================
# CONFIGURATION
# ============================================================

BASE_URL = "http://localhost"

USERNAME = "testuser"
PASSWORD = "testpassword"

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "Dataset"

MACHINES_FILE = DATA_DIR / "machines.csv"
READINGS_FILE = DATA_DIR / "machine_readings.csv"

# ============================================================
# DASHBOARD DEMO STATES
# ============================================================

KEEP_RUNNING = {
    "M02", "M04", "M05", "M06",
    "M10", "M12", "M14", "M15"
}

KEEP_MAINTENANCE = {
    "M03", "M08", "M11", "M16", "M20"
}


# ============================================================
# LOGIN
# ============================================================

def login():

    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data={
            "username": USERNAME,
            "password": PASSWORD
        }
    )

    response.raise_for_status()

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


# ============================================================
# CREATE MACHINES
# ============================================================

def create_machines(headers):

    machine_ids = {}

    with open(MACHINES_FILE, newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            payload = {
                "name": row["name"],
                "machine_type": "CNC"
            }

            response = requests.post(
                f"{BASE_URL}/api/machines/",
                json=payload,
                headers=headers
            )

            response.raise_for_status()

            machine = response.json()

            csv_machine_name = row["name"].replace("Machine ", "")

            database_machine_id = machine["id"]

            machine_ids[csv_machine_name] = database_machine_id

            print(
                f"Created {csv_machine_name} "
                f"-> database id {database_machine_id}"
            )
            
            print("DEBUG INSIDE create_machines:")
            print(machine_ids)

    return machine_ids


def start_machine(
    headers,
    database_machine_id,
    temperature,
    vibration
):

    payload = {
        "status": "Running",
        "temperature": temperature,
        "vibration": vibration
    }

    response = requests.patch(
        f"{BASE_URL}/api/machines/{database_machine_id}",
        json=payload,
        headers=headers
    )

    response.raise_for_status()

    return response.json()



def stop_machine(headers, database_machine_id):

    payload = {
        "status": "Idle"
    }

    response = requests.patch(
        f"{BASE_URL}/api/machines/{database_machine_id}",
        json=payload,
        headers=headers
    )

    response.raise_for_status()

    return response.json()

def get_machine_maintenance(
    headers,
    database_machine_id
):

    response = requests.get(
        f"{BASE_URL}/api/maintenance/",
        params={
            "machine_id": database_machine_id
        },
        headers=headers
    )

    response.raise_for_status()

    maintenances = response.json()

    if not maintenances:
        return None

    # Return the latest maintenance
    return maintenances[-1]


def assign_technician(
    headers,
    maintenance_id
):

    payload = {
        "status": "InProgress",
        "assigned_to": "technician_01"
    }

    response = requests.patch(
        f"{BASE_URL}/api/maintenance/{maintenance_id}",
        json=payload,
        headers=headers
    )

    response.raise_for_status()

    return response.json()

def resolve_maintenance(headers, maintenance_id):

    payload = {
        "status": "Resolved"
    }

    response = requests.patch(
        f"{BASE_URL}/api/maintenance/{maintenance_id}",
        json=payload,
        headers=headers
    )

    response.raise_for_status()

    return response.json()

def process_readings(headers, machine_ids):

    readings_by_machine = {}

    with open(READINGS_FILE, newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            machine_name = row["machine_id"]

            readings_by_machine.setdefault(
                machine_name,
                []
            ).append(row)

    for machine_name, readings in readings_by_machine.items():

        database_machine_id = machine_ids[machine_name]

        print()
        print("=" * 50)
        print(f"Processing {machine_name}")
        print("=" * 50)

        for reading in readings:

            temperature = float(reading["temperature"])
            vibration = float(reading["vibration"])

            print()
            print(
                f"Starting {machine_name}: "
                f"T={temperature}, V={vibration}"
            )

            result = start_machine(
                headers,
                database_machine_id,
                temperature,
                vibration
            )

            print(
                f"API returned machine status: "
                f"{result['status']}"
            )

            # ------------------------------------------------
            # HEALTHY
            # ------------------------------------------------

            if result["status"] == "Running":

                print(
                    f"{machine_name}: Healthy → Running"
                )

                if machine_name not in KEEP_RUNNING:

                    time.sleep(0.2)

                    stop_machine(
                        headers,
                        database_machine_id
                    )

                    print(
                        f"{machine_name}: Running → Idle"
                    )

                else:

                    print(
                        f"{machine_name}: "
                        f"left in Running state for dashboard"
                    )
                    break

            # ------------------------------------------------
            # WARNING / MAINTENANCE
            # ------------------------------------------------

            elif result["status"] == "Maintenance":

                maintenance = get_machine_maintenance(
                    headers,
                    database_machine_id
                )

                if maintenance is None:

                    print(
                        "ERROR: API did not create "
                        "a maintenance record."
                    )

                    continue

                maintenance_id = maintenance["id"]

                print(
                    f"Maintenance created: "
                    f"{maintenance_id}"
                )

                if machine_name in KEEP_MAINTENANCE:

                    print(
                        f"{machine_name}: "
                        f"left in Maintenance state "
                        f"for dashboard"
                    )
                    
                    break

                else:

                    assign_technician(
                        headers,
                        maintenance_id
                    )

                    print(
                        "Technician assigned → InProgress"
                    )

                    resolve_maintenance(
                        headers,
                        maintenance_id
                    )

                    print(
                        "Maintenance resolved → Idle"
                    )

            time.sleep(0.2)

def main():

    print("Logging into Factory Floor Monitoring API...")

    headers = login()

    print("Login successful.")

    print()
    print("Creating demo machines...")

    machine_ids = create_machines(headers)

    print()
    print(
        f"Created {len(machine_ids)} machines."
    )
    print("DEBUG machine_ids:", machine_ids)

    print()
    print("Starting demo lifecycle...")

    process_readings(
        headers,
        machine_ids
    )

    print()
    print("=" * 50)
    print("DEMO COMPLETED")
    print("=" * 50)


if __name__ == "__main__":
    main()
    
    
