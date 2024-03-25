from datetime import timedelta
import logging
from typing import Tuple
from minio import Minio

from lib.core.entity.models import ProtocolEnum
from lib.infrastructure.repository.minio.models import MinIOObject, MinIOPFN


class MinIOObjectStore:
    """
    A util class to interact with the MinIO S3 Object Store and the MinIO client.

    @ivar access_key: The access key for the MinIO S3 Object Store.
    @type access_key: str
    @ivar secret_key: The secret key for the MinIO S3 Object Store.
    @type secret_key: str
    @ivar host: The host of the MinIO S3 Object Store.
    @type host: str
    @ivar port: The port of the MinIO S3 Object Store.
    @type port: str
    @ivar signed_url_expiry: The expiry time for signed URLs in minutes.
    @type signed_url_expiry: int
    """

    def __init__(
        self,
        host: str,
        port: str,
        access_key: str,
        secret_key: str,
        signed_url_expiry: int = 60,
    ) -> None:
        self._access_key = access_key
        self._secret_key = secret_key
        self._host = host
        self._port = port
        self._signed_url_expiry = signed_url_expiry
        self._client = self._get_client()
        self.logger = logging.getLogger(self.__class__.__name__)

    @property
    def url(self) -> str:
        return f"{self.host}:{self.port}"

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> str:
        return self._port

    @property
    def signed_url_expiry(self) -> int:
        return self._signed_url_expiry

    @property
    def client(self) -> Minio:
        return self._client

    def _get_client(self) -> Minio:
        client = Minio(
            self.url,
            access_key=self._access_key,
            secret_key=self._secret_key,
            secure=False,  # TODO: make this configurable
        )
        return client

    def list_buckets(self) -> list[str]:
        buckets = self.client.list_buckets()
        return [bucket.name for bucket in buckets]

    def ping(self) -> bool:
        """
        Ping the MinIO S3 Object Store to check if it is reachable.
        """
        try:
            self.client.list_buckets()
            return True

        except Exception as e:
            self.logger.exception(f"Failed to ping MinIO with error: {e}")
            return False

    def process_bucket_name(self, bucket_name_raw: str) -> str:
        """
        Process the bucket name by converting it to lowercase, stripping whitespaces, and truncating it to 62 characters, as per MinIO's bucket naming conventions.
        """
        bucket_name = MinIOPFN.process_bucket_name(bucket_name_raw)
        return bucket_name

    def bucket_exists(self, bucket_name_raw: str) -> bool:
        bucket_name = self.process_bucket_name(bucket_name_raw)
        found = self.client.bucket_exists(bucket_name)
        assert isinstance(found, bool)
        return found

    def create_bucket_if_not_exists(self, bucket_name_raw: str) -> None:
        """
        Create a bucket in the MinIO S3 Object Store if it does not exist. The bucket name is converted to lowercase, stripped of whitespaces, and truncated to 62 characters.

        :param bucket_name_raw: The name of the bucket.
        :type bucket_name_raw: str
        """
        bucket_name = self.process_bucket_name(bucket_name_raw)
        if self.bucket_exists(bucket_name):
            self.logger.info(f"MinIO Repository: Bucket '{bucket_name}' already exists.")
            return

        self.client.make_bucket(bucket_name)
        self.logger.info(f"MinIO Repository: Created bucket '{bucket_name}'.")

    def initialize_store(self, bucket_name: str) -> None:
        """
        Initialize the MinIO S3 Repository with a bucket.
        """
        self.create_bucket_if_not_exists(bucket_name)

    def list_objects(self, bucket_name_raw: str) -> list[MinIOObject]:
        bucket_name = self.process_bucket_name(bucket_name_raw)
        objects = self.client.list_objects(bucket_name, recursive=True)
        objects = list(objects)

        minio_objects = [MinIOObject(bucket_name=bucket_name, object_name=obj.object_name) for obj in objects]

        return minio_objects

    def protocol_and_relative_path_to_pfn(
        self, protocol: ProtocolEnum, relative_path: str, bucket_name: str
    ) -> MinIOPFN:
        """
        Generate a PFN for MinIO S3 Repository from a SourceData object.
        **NOTE**: Underscores are not allowed anywhere in the relative path of the Sourc.

        :param protocol: The protocol of the SourceData.
        :type protocol: ProtocolEnum
        :param relative_path: The relative path of the SourceData.
        :type relative_path: str
        :param bucket_name: The name of the bucket.
        :type bucket_name: str
        :raises ValueError: If the protocol is not S3.
        :return: The PFN.
        """

        if protocol == ProtocolEnum.S3:
            return MinIOPFN(
                protocol=protocol,
                host=self.host,
                port=self.port,
                relative_path=relative_path,
                bucket_name=bucket_name,
            )

        raise ValueError(
            f"Protocol {protocol} is not supported by MinIO Repository. Cannot create a PFN for path '{relative_path}'."
        )

    def pfn_to_source_data_composite_index(self, pfn: MinIOPFN) -> Tuple[ProtocolEnum, str]:
        """
        Generate a composite index from a PFN that uniquely identifies a SourceData object.

        :raises ValueError: If the PFN protocol is not S3.
        :return: The composite index. It is a tuple of the protocol and the relative path.
        """
        if pfn.protocol != ProtocolEnum.S3:
            raise ValueError(
                f"Path '{pfn}' is not supported by this MinIO Repository at {self.url}. Cannot create a SourceData for PFN {pfn}."
            )

        return pfn.protocol, pfn.relative_path

    def pfn_to_object_name(self, pfn: MinIOPFN) -> MinIOObject:
        """
        Generate an object from a PFN for MinIO S3 Repository.
        """
        return MinIOObject(
            bucket_name=pfn.bucket_name,
            object_name=pfn.relative_path,
        )

    def object_to_pfn(self, minio_object: MinIOObject) -> MinIOPFN:
        """
        Generate a PFN from an object for MinIO S3 Repository.
        """
        return MinIOPFN(
            protocol=ProtocolEnum.S3,
            host=self.host,
            port=self.port,
            relative_path=minio_object.object_name,
            bucket_name=minio_object.bucket_name,
        )

    def get_signed_url_for_file_upload(self, minio_object: MinIOObject) -> str:
        """
        Get a signed URL to upload a file to a bucket in MinIO S3 Repository.
        """

        self.create_bucket_if_not_exists(minio_object.bucket_name)

        url = self.client.presigned_put_object(
            bucket_name=minio_object.bucket_name,
            object_name=minio_object.object_name,
            expires=timedelta(minutes=self.signed_url_expiry),
        )
        assert isinstance(url, str)

        return url

    def object_exists(self, minio_object: MinIOObject) -> bool:
        """
        Check if an object exists in a bucket in MinIO S3 Repository.
        """
        object_list = self.list_objects(minio_object.bucket_name)
        existence = minio_object in object_list
        return existence

    def get_signed_url_for_file_download(self, minio_object: MinIOObject) -> str:
        """
        Get a signed URL to download a file from a bucket in MinIO S3 Repository.

        :raises ValueError: If the object does not exist in MinIO.
        """

        existence = self.object_exists(minio_object)

        if not existence or existence == False:
            self.logger.error(f"Object '{minio_object}' does not exist in MinIO")
            errorMessage = f"Object '{minio_object}' does not exist in MinIO"
            raise ValueError(errorMessage)

        url = self.client.presigned_get_object(
            bucket_name=minio_object.bucket_name,
            object_name=minio_object.object_name,
            expires=timedelta(minutes=self.signed_url_expiry),
        )
        assert isinstance(url, str)

        return url
