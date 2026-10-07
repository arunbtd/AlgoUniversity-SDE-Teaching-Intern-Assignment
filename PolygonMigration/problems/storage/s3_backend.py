import boto3
from botocore.config import Config
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .base import StorageBackend


class S3Backend(StorageBackend):
    """Any S3-compatible storage. The provider is chosen by AWS_S3_ENDPOINT_URL."""

    def __init__(self):
        required = {
            "AWS_ACCESS_KEY_ID": settings.AWS_ACCESS_KEY_ID,
            "AWS_SECRET_ACCESS_KEY": settings.AWS_SECRET_ACCESS_KEY,
            "AWS_REGION": settings.AWS_REGION,
            "AWS_S3_BUCKET_NAME": settings.AWS_S3_BUCKET_NAME,
        }
        missing = [name for name, value in required.items() if not value]
        if missing:
            raise ImproperlyConfigured(f"Missing storage settings in .env: {', '.join(missing)}")

        self._bucket = settings.AWS_S3_BUCKET_NAME
        self._client = boto3.client(
            "s3",
            endpoint_url=settings.AWS_S3_ENDPOINT_URL or None,
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=Config(
                signature_version="s3v4",
                s3={"addressing_style": "path"},
                # newer boto3 adds checksum headers that some S3-compatible services reject
                request_checksum_calculation="when_required",
                response_checksum_validation="when_required",
            ),
        )

    def upload_bytes(self, key, data):
        self._client.put_object(Bucket=self._bucket, Key=key, Body=data)

    def delete_prefix(self, prefix):
        deleted = 0
        paginator = self._client.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=self._bucket, Prefix=prefix):
            for obj in page.get("Contents", []):
                self._client.delete_object(Bucket=self._bucket, Key=obj["Key"])
                deleted += 1
        return deleted
    