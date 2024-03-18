from datetime import timedelta
import logging
from minio import Minio

from lib.core.entity.models import LFN, KnowledgeSourceEnum, ProtocolEnum


class MinIOObjectStore:
    """
    A util class to interact with the MinIO S3 Object Store and the MinIO client.

    @ivar access_key: The access key for the MinIO S3 Object Store.
    @type access_key: str
    @ivar secret_key: The secret key for the MinIO S3 Object Store.
    @type secret_key: str
    @ivar bucket: The name of the bucket for the MinIO S3 Object Store.
    @type bucket: str
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
        bucket: str = "default",
        signed_url_expiry: int = 60,
    ) -> None:
        self._access_key = access_key
        self._secret_key = secret_key
        self._bucket = bucket
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
    def bucket(self) -> str:
        return self._bucket

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

    def create_bucket_if_not_exists(self, bucket_name: str) -> None:
        if bucket_name in self.list_buckets():
            self.logger.info(f"MinIO Repository: Bucket {bucket_name} already exists.")

            return
        self.client.make_bucket(bucket_name)
        self.logger.info(f'MinIO Repository: Created bucket "{bucket_name}".')

    def ping(self) -> bool:
        try:
            self.create_bucket_if_not_exists(self.bucket)
            bucket_exists = self.client.bucket_exists(self.bucket)

            if not bucket_exists:
                self.logger.error(f'MinIO: ping successful, but bucket "{self.bucket}" does not exist.')
                return False

            return True

        except Exception as e:
            self.logger.exception(f"Failed to ping MinIO with error: {e}")
            return False

    def list_buckets(self) -> list[str]:
        buckets = self.client.list_buckets()
        return [bucket.name for bucket in buckets]

    def bucket_exists(self, bucket_name: str) -> bool:
        found = self.client.bucket_exists(bucket_name)
        assert isinstance(found, bool)
        return found

    def list_objects(self, bucket_name: str) -> list[str]:
        objects = self.client.list_objects(bucket_name, recursive=True)
        objects = list(objects)
        return [obj.object_name for obj in objects]

    def lfn_to_pfn(self, lfn: LFN) -> str:
        """
        Generate a PFN for MinIO S3 Repository from a LFN.
        **NOTE**: Underscores are not allowed anywhere in the relative path of the LFN.

        :param lfn: The LFN to generate a PFN for.
        :type lfn: LFN
        :raises ValueError: If the LFN protocol is S3.
        :return: The PFN.
        """
        if lfn.protocol == ProtocolEnum.S3:
            return f"s3://{self.host}:{self.port}/{self.bucket}/{lfn.tracer_id}/{lfn.source.value}/{lfn.job_id}/{lfn.relative_path}"
        raise ValueError(
            f"Protocol {lfn.protocol} is not supported by MinIO Repository. Cannot create a PFN for LFN {lfn}."
        )

    def pfn_to_lfn(self, pfn: str) -> LFN:
        """
        Generate a LFN from a PFN for MinIO S3 Repository.

        :param pfn: The PFN to generate a LFN for.
        :type pfn: str
        :raises ValueError: If the PFN protocol is S3.
        :return: The LFN.
        """
        if pfn.startswith(f"s3://{self.host}:{self.port}/{self.bucket}"):
            without_protocol = pfn.split("://")[1]
            path_components = without_protocol.split("/")[1:]
            bucket = path_components[0]
            if bucket != self.bucket:
                raise ValueError(
                    f"Bucket {bucket} does not match the bucket of this MinIO Repository at {self.url}. Cannot create a LFN for PFN {pfn}."
                )
            tracer_id = path_components[1]
            source = KnowledgeSourceEnum(path_components[2])
            job_id = int(path_components[3])
            relative_path = "/".join(path_components[4:])
            lfn: LFN = LFN(
                protocol=ProtocolEnum.S3,
                tracer_id=tracer_id,
                source=source,
                job_id=job_id,
                relative_path=relative_path,
            )
            return lfn
        raise ValueError(
            f"Path {pfn} is not supported by this MinIO Repository at {self.url}. Cannot create a LFN for PFN {pfn}."
        )

    def pfn_to_object_name(self, pfn: str) -> str:
        """
        Generate an object name from a PFN for MinIO S3 Repository.
        """
        return "/".join(pfn.split("://")[1].split("/")[2:])

    def object_name_to_pfn(self, object_name: str) -> str:
        """
        Generate a PFN from an object name for MinIO S3 Repository.
        """
        return f"s3://{self.host}:{self.port}/{self.bucket}/{object_name}"

    def initialize_store(self) -> None:
        """
        Initialize the MinIO S3 Repository.
        """
        self.create_bucket_if_not_exists(self.bucket)

    def get_signed_url_for_file_upload(self, bucket_name: str, object_name: str) -> str:
        """
        Get a signed URL to upload a file to a bucket in MinIO S3 Repository.

        :param bucket_name: The name of the bucket.
        :param object_name: The name of the object.
        :param file_path: The path to the file to upload.
        """

        url = self.client.presigned_put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            expires=timedelta(minutes=self.signed_url_expiry),
        )
        assert isinstance(url, str)

        return url
