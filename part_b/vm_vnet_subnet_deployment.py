import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient

load_dotenv()

# Constants
# ---------
# Modify the following constants from .env file to customize your deployment.


# AZ Configuration
SUBSCRIPTION_ID = os.getenv("SUBSCRIPTION_ID")
RESOURCE_GROUP = os.getenv("RESOURCE_GROUP")
AZ_REGION = os.getenv("AZ_REGION")

# Names for resource naming configuration
FULL_NAME = os.getenv("FULL_NAME")
FIRST_NAME = os.getenv("FIRST_NAME")

# Network naming configuration
VNET_NAME = f"VNet-{FULL_NAME}"
SUBNET_NAME = f"Subnet-{FIRST_NAME}"
NIC_NAME = f"NIC-{FIRST_NAME}"
NSG_NAME = f"NSG_Andreas"
IP_CONFIG_NAME = f"IPConfig-{FIRST_NAME}"
# Add a new constant for the public IP name
PUBLIC_IP_NAME = f"PublicIP-{FIRST_NAME}"


# VM configuration
VM_NAME = f"VM-{FIRST_NAME}"
VM_TYPE = "Standard_DS1_v2"
VM_PROFILE = {
    "publisher": "Canonical",
    "offer": "UbuntuServer",
    "sku": "18.04-LTS",
    "version": "latest",
}

VM_USER = os.getenv("VM_USER")
VM_PASSWORD = os.getenv("VM_PASSWORD")

# ---------


# Initialize credentials & AZ clients.
credential = DefaultAzureCredential()
network_client = NetworkManagementClient(credential, SUBSCRIPTION_ID)
compute_client = ComputeManagementClient(credential, SUBSCRIPTION_ID)
resource_client = ResourceManagementClient(credential, SUBSCRIPTION_ID)


resource_client.resource_groups.create_or_update(
    resource_group_name=RESOURCE_GROUP, 
    parameters={"location": AZ_REGION}
)

# Create VNet

vnet_params = {
    "location": AZ_REGION,
    "address_space": {
        "address_prefixes": ["10.0.0.0/16"]
    },
}

network_client.virtual_networks.begin_create_or_update(
    resource_group_name=RESOURCE_GROUP,
    virtual_network_name=VNET_NAME,
    parameters=vnet_params,
).result()

print(f"Vnet {VNET_NAME} just got created!")

# Create Network Security Group
nsg_params = {
    "location": AZ_REGION
}

nsg = network_client.network_security_groups.begin_create_or_update(
    RESOURCE_GROUP,
    NSG_NAME,
    nsg_params
).result()

# Create Subnet
subnet_params = {
    "address_prefix": "10.0.0.0/24",
    "network_security_group": {
        "id": nsg.id
    }
}

network_client.subnets.begin_create_or_update(
    resource_group_name=RESOURCE_GROUP,
    virtual_network_name=VNET_NAME,
    subnet_name=SUBNET_NAME,
    subnet_parameters=subnet_params,
).result()

print(f"Vnet {SUBNET_NAME} just got created!")

# Create Public IP Address
public_ip_params = {
    "location": AZ_REGION,
    "public_ip_allocation_method": "Dynamic"
}
public_ip = network_client.public_ip_addresses.begin_create_or_update(
    resource_group_name=RESOURCE_GROUP,
    public_ip_address_name=PUBLIC_IP_NAME,
    parameters=public_ip_params
).result()

print(f"Public IP {PUBLIC_IP_NAME} created!")

# Create NIC
nic_params = {
    "location": AZ_REGION,
    "ip_configurations": [
        {
            "name": IP_CONFIG_NAME,
            "subnet": {
                "id": f"/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{RESOURCE_GROUP}/providers/Microsoft.Network/virtualNetworks/{VNET_NAME}/subnets/{SUBNET_NAME}"
            },
            "public_ip_address": {"id": public_ip.id}
        }
    ],
    "network_security_group": {
        "id": f"/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{RESOURCE_GROUP}/providers/Microsoft.Network/networkSecurityGroups/{NSG_NAME}"
    }
}

nic = network_client.network_interfaces.begin_create_or_update(
    resource_group_name=RESOURCE_GROUP,
    network_interface_name=NIC_NAME,
    parameters=nic_params
).result()

print(f"NIC {NIC_NAME} just got created!")

# Create VM
vm_params = {
    "location": AZ_REGION,
    "os_profile": {
        "computer_name": VM_NAME,
        "admin_username": VM_USER,
        "admin_password": VM_PASSWORD,
    },
    "hardware_profile": {
        "vm_size": VM_TYPE
    },
    "storage_profile": {
        "image_reference": VM_PROFILE
    },
    "network_profile": {
        "network_interfaces": [{"id": nic.id}]
        },
}

compute_client.virtual_machines.begin_create_or_update(
    resource_group_name=RESOURCE_GROUP, 
    vm_name=VM_NAME, 
    parameters=vm_params
).result()

print(f"VM '{VM_NAME}' has been successfully deployed in the VNet {VNET_NAME}. VM is type of {VM_TYPE}.")