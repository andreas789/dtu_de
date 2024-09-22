import os
from dotenv import load_dotenv
import sys
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

load_dotenv()

# Az configs
CREDENTIAL = DefaultAzureCredential()
STORAGE_ACCOUNT = os.getenv("STORAGE_ACCOUNT")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")
ACCOUNT_URL = f"https://{STORAGE_ACCOUNT}.blob.core.windows.net"


def upload_blob_file(
    blob_service_client: BlobServiceClient,
    container_name: str,
    file_path: str,
    blob_name: str,
) -> None:

    try:

        container_client = blob_service_client.get_container_client(container_name)

        if not container_client.exists():
            container_client.create_container()
            print(f"Container '{container_name}' just got created.")

        print(
            f"Uploading file {blob_name} to storage account: {STORAGE_ACCOUNT}, container name: {CONTAINER_NAME}."
        )

        with open(file_path, mode="rb") as data:
            blob_client = container_client.upload_blob(
                name=blob_name, data=data, overwrite=True
            )

        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=blob_name
        )

        if blob_client.exists():
            print("File uploaded to blob.")

    except Exception as err:
        print(f"Unexpected error: {err}")
        sys.exit(1)


if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("Usage: python upload_blob.py <container_name> <file_path> <blob_name>")
        sys.exit(1)

    container_name = sys.argv[1]
    file_path = sys.argv[2]
    blob_name = sys.argv[3]

    # Check if file exists before proceeding
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        sys.exit(1)

    blob_service_client = BlobServiceClient(
        account_url=ACCOUNT_URL, credential=CREDENTIAL
    )

    upload_blob_file(blob_service_client, container_name, file_path, blob_name)
