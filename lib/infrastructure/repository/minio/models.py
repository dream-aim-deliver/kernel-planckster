import re
from pydantic import BaseModel, field_validator

from lib.core.entity.models import ProtocolEnum


class MinIOPFN(BaseModel):
    """
    MinIO PFN (Physical File Name) model.

    @param protocol: The protocol of the file to be uploaded. Has to be one of the supported protocols.
    @param host: The host of the MinIO server.
    @param port: The port of the MinIO server.
    @param relative_path: The relative path of the file to be uploaded.
    @param bucket_name: The name of the bucket in which the file is stored.
    """

    protocol: ProtocolEnum = ProtocolEnum.S3
    host: str
    port: int
    relative_path: str
    bucket_name: str

    def __str__(cls) -> str:
        return f"{cls.protocol.value}://{cls.host}:{cls.port}/{cls.bucket_name}/{cls.relative_path}"

    @classmethod
    def process_bucket_name(cls, bucket_name_raw: str) -> str:
        """
        Process the bucket name to ensure it is correctly formatted, following the MinIO bucket naming conventions. For safety:
        - Only alphanumeric characters are allowed
        - The bucket name must be at least 3 characters long.
        """
        bucket_name_preproc = re.sub(r"[^a-zA-Z0-9]", "", bucket_name_raw)
        bucket_name = "".join(f"{bucket_name_preproc}".lower().split())[:62]
        if len(bucket_name) < 3:
            bucket_name = f"{bucket_name}{'-bucket' * (3 - len(bucket_name))}"
        return bucket_name

    @field_validator("bucket_name", mode="before")
    def format_bucket_name(cls, v: str) -> str:
        bucket_name = cls.process_bucket_name(v)
        return bucket_name


class MinIOObject(BaseModel):
    """
    MinIO Object model, to represent an object in a MinIO bucket.

    @param bucket_name: The name of the bucket in which the object is stored.
    @param object_name: The object name in the bucket. It will be the relative path of the file passed to the PFN.
    """

    bucket_name: str
    object_name: str

    def __str__(cls) -> str:
        return f"{cls.bucket_name}/{cls.object_name}"

    @field_validator("bucket_name", mode="before")
    def format_bucket_name(cls, v: str) -> str:
        bucket_name = MinIOPFN.process_bucket_name(v)
        return bucket_name
