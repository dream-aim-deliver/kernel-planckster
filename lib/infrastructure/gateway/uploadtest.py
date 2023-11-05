from minio import Minio
from minio.error import S3Error


def main() -> None:
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio(
        "139.19.179.6:9000",
        access_key="minio_access_key",
        secret_key="minio_secret_key",
        secure=False
    )

    # Make 'asiatrip' bucket if not exist.
    found = client.bucket_exists("testbucket")
    if not found:
        client.make_bucket("testbucket")
    else:
        print("Bucket 'testbucket' already exists")

    # Upload '/home/user/Photos/asiaphotos.zip' as object name
    # 'asiaphotos-2015.zip' to bucket 'asiatrip'.
    client.fput_object(
        "testbucket",
        "testfile",
        "testfile",
    )
    print(
        "'/home/user/Photos/asiaphotos.zip' is successfully uploaded as "
        "object 'asiaphotos-2015.zip' to bucket 'asiatrip'."
    )


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)
