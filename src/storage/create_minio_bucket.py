from minio import Minio
from config.config import (minio_endpoint,
                            minio_access_key,
                              minio_secret_key, 
                              minio_bucket_name)

class MinioBucketManager:
    """
    A class to manage MinIO bucket operations.
    """

    def __init__(self):
        """
        Initializes the Minio client with the provided configuration.
        """
        self.client = Minio(
            minio_endpoint,
            access_key=minio_access_key,
            secret_key=minio_secret_key,
            secure=False  # Set to True if using HTTPS
        )
        self.bucket_name = minio_bucket_name

    def create_bucket(self):
        """
        Creates a bucket in MinIO if it does not already exist.

        Returns:
            bool: True if the bucket was created or already exists, False otherwise.
        """
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                print(f"Bucket '{self.bucket_name}' created successfully.")
            else:
                print(f"Bucket '{self.bucket_name}' already exists.")
            return True
        except Exception as e:
            print(f"Error creating bucket '{self.bucket_name}': {e}")
            return False