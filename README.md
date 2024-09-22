# DTU Data Engineering Tasks

This repository contains various tasks and projects related to data engineering, 
primarily focusing on working with the Azure cloud platform  and data analysis using Python and Jupyter notebooks.

## Repository Structure

The repository is divided into the following parts:

- **part_a**: Contains Jupyter notebooks and scripts related to the first set of data engineering tasks.
- **part_b**: Contains Jupyter notebooks and scripts for the second set of tasks.
- **requirements.txt**: Specifies the Python dependencies required to run the project.
- **azure_vm_setup.sh**: A bash script to set up an Azure VM, install Azure CLI, login, and download files from Azure Blob Storage.

----

## Main Technologies/Libraries Used

- **Python**
- **Jupyter Notebooks**
- **Azure Cloud Services**: Networking, Identity, and Compute.
- **Pandas**: Data manipulation and analysis.

## Getting Started

### Prerequisites

- Python 3.x
- Install dependencies from `requirements.txt`:

### Running the Python scripts

**Make sure you have set up your .env file in the root directory.**

1. Clone the repository:
  ```bash
    git clone https://github.com/andreas789/dtu_de.git
  ```
2. Navigate into the cloned repository:
  ```bash
    pip install -r requirements.txt
  ```
3. Install the required dependencies:
  ```
    pip install -r requirements.txt
  ```
4. Run any script/notebook you like. 

----

### About the sh script

This script performs the following actions:

1. SSH into the Azure VM.
2. Install the Azure CLI.
3. Log into Azure using the CLI.
4. Download files from an Azure Blob Storage container to the VM.

----
### Topics Covered
- **Cloud-based data engineering**
- **Data manipulation with Pandas**
- **Azure services for data solutions**
