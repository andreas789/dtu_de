import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.mgmt.monitor import MonitorManagementClient

from datetime import timedelta, datetime
import json

load_dotenv()

SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID")
RESOURCE_GROUP = os.getenv("RESOURCE_GROUP")
RESOURCE_NAME = "VM-Andreas"
RESOURCE_ID = f"/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{RESOURCE_GROUP}/providers/Microsoft.Compute/virtualMachines/{RESOURCE_NAME}"


try:
    credential = DefaultAzureCredential()
    monitor_client = MonitorManagementClient(credential, SUBSCRIPTION_ID)

except Exception as e:
    raise RuntimeError(f"Failed to authenticate or create MonitorManagementClient: {e}")


# Define time range and create filter for logs
end_time = datetime.utcnow()
start_time = end_time - timedelta(days=5)


odata_filter = f""" ResourceId eq '{RESOURCE_ID}' 
    and eventTimestamp ge '{start_time.isoformat()}' 
    and eventTimestamp le '{end_time.isoformat()}' 
"""

try:

    logs = monitor_client.activity_logs.list(
        filter=odata_filter,
        select="eventTimestamp,operationName,status,caller,claims",
    )

    log_list = []
    log_count = 0

    # Iterate over logs and print/save details
    for log in logs:
        log_count += 1

        log_entry = {
            "Time": log.event_timestamp,
            "Operation": log.operation_name.value if log.operation_name else "N/A",
            "Status": log.status.value if log.status else "N/A",
            "Caller": log.caller,
            "IP": log.claims.get("ipaddr", "N/A") if log.claims else "N/A",
        }

        log_list.append(log_entry)

        print(f"Time: {log_entry['Time']}")
        print(f"Operation: {log_entry['Operation']}")
        print(f"Status: {log_entry['Status']}")
        print(f"Caller: {log_entry['Caller']}")
        print(f"IP: {log_entry['IP']}")
        print("---")

    if log_count == 0:
        print("No logs were returned for the specified time range and resource.")
    else:
        print(f"Total logs fetched: {log_count}")

    # Save logs to a JSON file only when logs were returned
    if log_list:
        with open(f"azure_logs_{str(end_time)}.json", "w") as f:
            json.dump(log_list, f, default=str, indent=4)

        print("Logs have been saved to azure_logs.json")
    else:
        print("No logs to save.")


except Exception as e:
    print(f"Failed to fetch or process logs: {e}")
