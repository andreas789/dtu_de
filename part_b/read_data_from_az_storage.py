import os
import sys
from dotenv import load_dotenv
import pandas as pd
from azure.identity import DefaultAzureCredential
import adlfs


load_dotenv()


def download_blob_to_dataframe(storage_account_name, container_name, blob_path):
    # Set up Azure credentials
    credential = DefaultAzureCredential(
        exclude_visual_studio_code_credential=True,
        exclude_shared_token_cache_credential=True,
    )

    # Create the ADLFS fs object
    fs = adlfs.AzureBlobFileSystem(
        account_name=storage_account_name, credential=credential
    )

    full_blob_path = f"{container_name}/{blob_path}"

    # Open the blob and read it into a pandas DataFrame
    with fs.open(full_blob_path, mode="rb") as f:
        df = pd.read_csv(f)

    return df


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "Usage: python 2_read_data_from_az_storage.py <STORAGE_ACCOUNT_NAME> <CONTAINER_NAME> <BLOB_PATH>"
        )
        sys.exit(1)

    storage_account_name = sys.argv[1]
    container_name = sys.argv[2]
    blob_path = sys.argv[3]

    df = download_blob_to_dataframe(storage_account_name, container_name, blob_path)

    # Print the first few rows of the DataFrame
    print(df.head())
