from django.conf import settings

from problems.AzureTestcase import AzureBlobManager
from .base import StorageBackend


class AzureBackend(StorageBackend):
    def __init__(self):
        manager = AzureBlobManager(
            account_url=settings.AZURE_STORAGE_ACCOUNT_URL,
            tenant_id=settings.AZURE_TENANT_ID,
            client_id=settings.AZURE_CLIENT_ID,
            username=settings.AZURE_USERNAME,
            password=settings.AZURE_PASSWORD,
        )
        self._client = manager.blob_service_client
        self._container = settings.AZURE_CONTAINER_NAME

    def upload_bytes(self, key, data):
        blob = self._client.get_blob_client(container=self._container, blob=key)
        blob.upload_blob(data, overwrite=True)

    def delete_prefix(self, prefix):
        container = self._client.get_container_client(self._container)
        names = [b.name for b in container.list_blobs(name_starts_with=prefix)]
        for name in names:
            container.delete_blob(name)
        return len(names)