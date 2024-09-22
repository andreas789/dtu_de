#!/bin/bash

# Step 1: SSH into the VM
# Replace <VM_PUBLIC_IP> with your VM's public IP
ssh -i azuser1.pem azureuser@<VM_PUBLIC_IP> << 'EOF'

# Step 2: Install Azure CLI on the Azure VM
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Step 3: Log in via Azure CLI
az login

# Step 4: Download Files from Azure Blob Storage

# Download Country Average Rate File
az storage blob download \
    --account-name dataengineerv1 \
    --container-name your-name \
    --name Country-Avg-Rate-Your-Name.csv \
    --file /home/azureuser/Country-Avg-Rate-Your-Name.csv \
    --auth-mode login

# Download Top 3 Categories Per Country File
az storage blob download \
    --account-name dataengineerv1 \
    --container-name your-name \
    --name Top3-Categories-Per-Country-Your-Name.csv \
    --file /home/azureuser/Top3-Categories-Per-Country-Your-Name.csv \
    --auth-mode login

EOF
