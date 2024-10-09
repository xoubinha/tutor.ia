from pydantic.dataclasses import dataclass
from azure.storage.blob import BlobServiceClient

import logging
import os
import json
import tempfile

from typing import List, Dict
from features.parsers import File

logger = logging.getLogger("ingester")


@dataclass(config=dict(arbitrary_types_allowed=True))
class AzureStorageAccount:
    """
    Concrete strategy for listing files that are located in an Azure Storage Account
    """

    storage_account_name: str
    storage_container_name: str
    connection_string: str

    def get_service_client(self):
        return BlobServiceClient.from_connection_string(self.connection_string)

    def get_container_client(self):
        service_client = self.get_service_client()
        return service_client.get_container_client(self.storage_container_name)

    def list_blobs(self) -> List[str]:
        container_client = self.get_container_client()
        return [blob.name for blob in container_client.list_blobs()]

    def download_files(self) -> List[File]:
        container_client = self.get_container_client()
        files = []
        for blob_name in self.list_blobs():
            if blob_name.split(".")[-1] not in ["pdf", "docx", "pptx"]:
                continue
            temp_file_path = os.path.join(
                tempfile.gettempdir(), os.path.basename(blob_name)
            )
            try:
                blob_client = container_client.get_blob_client(blob_name)
                with open(temp_file_path, "wb") as temp_file:
                    downloader = blob_client.download_blob()
                    downloader.readinto(temp_file)
                files.append(
                    File(content=open(temp_file_path, "rb"), url=blob_client.url)
                )
            except Exception as storage_exception:
                logger.error(
                    f"\tGot an error while reading {blob_name} -> {storage_exception} --> skipping file"
                )
                try:
                    os.remove(temp_file_path)
                except Exception as file_delete_exception:
                    logger.error(
                        f"\tGot an error while deleting {temp_file_path} -> {file_delete_exception}"
                    )
        return files

    def upload_blob(self, data: List[Dict], blob_name: str) -> None:
        """
        Uploads a list of dictionaries as a JSON blob to the Azure Blob Storage container.

        Args:
            data (List[Dict]): The list of dictionaries to be uploaded.
            blob_name (str): The name of the blob in the container.
        """
        container_client = self.get_container_client()
        try:
            blob_client = container_client.get_blob_client(blob_name)
            json_data = json.dumps(data, indent=4)
            blob_client.upload_blob(json_data, overwrite=True)
            logger.info(f"Successfully uploaded data as {blob_name}")
        except Exception as e:
            logger.error(f"Failed to upload data as {blob_name} -> {e}")
