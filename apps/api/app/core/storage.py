"""
MinIO storage client for file upload/download.
Provides S3-compatible object storage operations.
"""

import uuid
from typing import BinaryIO

from minio import Minio
from minio.error import S3Error

from app.core.config import settings


class StorageClient:
    """
    MinIO/S3 storage client for document management.
    
    Handles file upload, download, and deletion with proper
    organization-scoped key prefixes for multi-tenancy.
    """

    def __init__(self):
        """Initialize MinIO client."""
        self.client = Minio(
            settings.S3_ENDPOINT.replace("http://", "").replace("https://", ""),
            access_key=settings.S3_ACCESS_KEY,
            secret_key=settings.S3_SECRET_KEY,
            secure=settings.S3_USE_SSL,
        )
        self.bucket = settings.S3_BUCKET

    async def ensure_bucket_exists(self) -> None:
        """Ensure the storage bucket exists, create if not."""
        try:
            if not self.client.bucket_exists(self.bucket):
                self.client.make_bucket(self.bucket)
        except S3Error as e:
            raise RuntimeError(f"Failed to create bucket: {e}")

    async def upload_file(
        self,
        file_data: BinaryIO,
        file_name: str,
        content_type: str,
        file_size: int,
        org_id: str,
        shipment_id: str,
    ) -> str:
        """
        Upload a file to MinIO storage.
        
        Args:
            file_data: File-like object to upload
            file_name: Original filename
            content_type: MIME type
            file_size: File size in bytes
            org_id: Organization ID (for key prefix)
            shipment_id: Shipment ID (for key prefix)
            
        Returns:
            MinIO object key for the uploaded file
        """
        # Generate unique key with org/shipment prefix
        file_ext = file_name.rsplit(".", 1)[-1] if "." in file_name else "bin"
        object_key = f"{org_id}/{shipment_id}/{uuid.uuid4()}.{file_ext}"

        try:
            self.client.put_object(
                bucket_name=self.bucket,
                object_name=object_key,
                data=file_data,
                length=file_size,
                content_type=content_type,
            )
        except S3Error as e:
            raise RuntimeError(f"Failed to upload file: {e}")

        return object_key

    async def download_file(self, file_key: str) -> bytes:
        """
        Download a file from MinIO storage.
        
        Args:
            file_key: MinIO object key
            
        Returns:
            File contents as bytes
        """
        try:
            response = self.client.get_object(self.bucket, file_key)
            return response.read()
        except S3Error as e:
            raise FileNotFoundError(f"File not found: {file_key}")

    async def delete_file(self, file_key: str) -> bool:
        """
        Delete a file from MinIO storage.
        
        Args:
            file_key: MinIO object key
            
        Returns:
            True if deleted, False if not found
        """
        try:
            self.client.remove_object(self.bucket, file_key)
            return True
        except S3Error:
            return False

    async def get_presigned_url(self, file_key: str, expires_minutes: int = 60) -> str:
        """
        Generate a presigned URL for file access.
        
        Args:
            file_key: MinIO object key
            expires_minutes: URL expiration time in minutes
            
        Returns:
            Presigned URL string
        """
        from datetime import timedelta

        try:
            url = self.client.presigned_get_object(
                bucket_name=self.bucket,
                object_name=file_key,
                expires=timedelta(minutes=expires_minutes),
            )
            return url
        except S3Error as e:
            raise RuntimeError(f"Failed to generate presigned URL: {e}")


# Global storage client instance
storage_client = StorageClient()
