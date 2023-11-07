"""
>Spawn docker container

mkdir -p ~/minio/data
docker run \
   -p 9000:9000 \
   -p 9090:9090 \
   --name minio \
   -v ~/minio/data:/data \
   -e "MINIO_ACCESS_KEY=minio_access_key" \
   -e "MINIO_SECRET_KEY=minio_secret_key" \
   -e "MINIO_ROOT_USER=ROOTNAME" \
   -e "MINIO_ROOT_PASSWORD=CHANGEME123" \
   quay.io/minio/minio server /data --console-address ":9090"


> to fix/investigate:
> For some reazon command do not add keypairs of MINIO_ACCESS_KEY & MINIO_SECRET_KEY and it was added manualy from root panel on web UI 

"""


from minio import Minio
from minio.error import S3Error


def main() -> None:
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio(
        "139.19.179.6:9000", #brain12 ip address
        access_key="minio_access_key",
        secret_key="minio_secret_key",
        secure=False
    )

    # Make 'test' bucket if not exist.
    found = client.bucket_exists("testbucket")
    if not found:
        client.make_bucket("testbucket")
    else:
        print("Bucket 'testbucket' already exists")

    # Upload path/testfile' as object name
    # 'testfile' to bucket 'testbucket'.
    client.fput_object(
        "testbucket",
        "testfile",
        "testfile",
    )
    print(
        "'path/testfile' is successfully uploaded as "
        "object 'testfile' to bucket 'testbucket'."
    )


if __name__ == "__main__":
    try:
        main()
    except S3Error as exc:
        print("error occurred.", exc)
