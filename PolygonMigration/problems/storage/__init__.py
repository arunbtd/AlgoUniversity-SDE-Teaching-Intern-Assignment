from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .base import StorageBackend


def get_storage() -> StorageBackend:
    """Return the backend selected by STORAGE_PROVIDER in .env."""
    provider = settings.STORAGE_PROVIDER
    if provider == "azure":
        from .azure_backend import AzureBackend
        return AzureBackend()
    if provider == "s3":  # Backblaze B2, Cloudflare R2, MinIO, AWS S3
        from .s3_backend import S3Backend
        return S3Backend()
    raise ImproperlyConfigured(f"Unknown STORAGE_PROVIDER '{provider}'. Use 'azure' or 's3'.")